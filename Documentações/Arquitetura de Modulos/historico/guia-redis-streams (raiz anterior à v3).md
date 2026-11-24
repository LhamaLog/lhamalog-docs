# Guia padrão — Redis Streams no LhamaLog

**Versão 2 (14/10/2026, Michel Bocchi Junior).** Agendador definido na ADR_147 (versão 1 em `v1/`). Padrão obrigatório para criar streams, produtores e consumidores em todos os
serviços (ADR_143 a ADR_146). Como não existe biblioteca comum (ADR_145), as classes base da seção 9 são **copiadas** em cada
repositório, no pacote `br.com.lhamalog.MODULO.adaptador.fila.base`, e só mudam por decisão registrada.
Marcações: `[PENDENTE]` sem decisão; `[INFERIDO]` derivado das ADRs.

## 1. Onde usamos streams

| Stream (papel) | Produtor | Consumidor (grupo) | ADRs |
|---|---|---|---|
| FilaDesordenada do Produto | Coletor (OTLP) | Varredura (`varredura`) | 007, 057 |
| FilaOrdenada do Produto | Varredura; Coletor (upload manual, fim da fila) | Finder (`finder`) | 041, 059, 065 |
| DLQ da FilaOrdenada | consumidor do Finder após 3 tentativas | Core/Varredura para alerta (`dlq-alerta`) | 046, 059, 073 |
| Sugestão manual | Ocorrência (após 202) | Ocorrência/Sugestão (`sugestao`) | 083, 094, 096 |
| Execuções de Varredura | tick @Scheduled+ShedLock e gatilho de 500 arquivos (ADR_147) | Varredura (`varredura`) | 057, 147 |
| Eventos de notificação | Core | Notificação (`notificacao`) | 060, 130, 141 |

## 2. Nomes de streams

Formato: `lhamalog:AMBIENTE:PAPEL:{TENANT:PRODUTO}` — prefixo fixo, ambiente (`local`, `dev`, `prod`), papel em kebab-case e,
quando a fila é por Produto, a **hash tag** `{tenantId:produtoId}` (mantém as chaves do mesmo Produto no mesmo slot do Redis Cluster).

| Papel | Chave |
|---|---|
| FilaDesordenada | `lhamalog:prod:fila-desordenada:{TENANT:PRODUTO}` |
| FilaOrdenada | `lhamalog:prod:fila-ordenada:{TENANT:PRODUTO}` |
| DLQ | `lhamalog:prod:fila-ordenada-dlq:{TENANT:PRODUTO}` |
| Sugestão manual | `lhamalog:prod:sugestao-manual` (global; tenantId no envelope) `[INFERIDO]` |
| Notificação | `lhamalog:prod:notificacao-eventos` (global) `[INFERIDO]` |
| Registro de streams ativas | SET `lhamalog:prod:registro:fila-ordenada` com as chaves por Produto |

- Uma FilaDesordenada por Produto (ADR_057). A FilaOrdenada também é por Produto, e **qualquer worker** consome qualquer Produto (ADR_065, ADR_068) — por isso o registro de streams ativas `[INFERIDO]`.
- Nunca colocar nome de arquivo ou dado pessoal na chave.

## 3. Grupos e consumidores

- **Grupo = nome do serviço consumidor** (`varredura`, `finder`, `sugestao`, `notificacao`, `dlq-alerta`). Um grupo por serviço por stream.
- Criação idempotente: `XGROUP CREATE CHAVE GRUPO $ MKSTREAM`; ignorar o erro `BUSYGROUP`.
- **Nome do consumidor**: `SERVICO-HOSTNAME-INDICE` (ex.: `finder-pod-7f9c-3`) — HOSTNAME do pod + índice do worker (10 workers por pod, ADR_065).
- Consumidores mortos: remover com `XGROUP DELCONSUMER` depois que não tiverem pendentes (rotina de limpeza `[PENDENTE — frequência]`).

## 4. Comandos padrão

| Operação | Comando | Regra |
|---|---|---|
| Publicar | `XADD CHAVE MAXLEN ~ LIMITE * campo valor...` | sempre com o envelope (seção 5) e trim aproximado |
| Consumir | `XREADGROUP GROUP GRUPO CONSUMIDOR COUNT 10 BLOCK 2000 STREAMS CHAVE...  >` | `COUNT` e `BLOCK` vêm das propriedades |
| Confirmar | `XACK CHAVE GRUPO ID` | **só depois** de processar e gravar o resultado |
| Pendentes | `XPENDING CHAVE GRUPO - + 100` | monitoramento |
| Reivindicar | `XAUTOCLAIM CHAVE GRUPO CONSUMIDOR MIN-IDLE 0-0 COUNT 10` | mensagens paradas acima do tempo mínimo (seção 6) |

## 5. Envelope da mensagem

Toda mensagem é um hash de campos string; o campo `payload` carrega JSON.

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `eventId` | UUID | sim | id único do evento (idempotência e rastreio) |
| `type` | string | sim | ex.: `arquivo.enfileirado`, `arquivo.ordenado`, `sugestao.solicitada`, `alerta.emitido` |
| `version` | inteiro | sim | versão do contrato do `payload` (começa em 1) |
| `timestamp` | ISO-8601 UTC | sim | momento da emissão |
| `tenantId` | string | sim | isolamento (ADR_121) |
| `produtoId` | string | quando houver | filas por Produto |
| `execId` | string | filas da Varredura/Finder | `V` ou `M` + UUID (ADR_069/075) |
| `tentativa` | inteiro | sim | começa em 1; sobe a cada reenvio (seção 7) |
| `traceparent` | string | não | contexto W3C do OpenTelemetry `[INFERIDO]` |
| `payload` | JSON | sim | dados do tipo (ex.: `arquivoId`, `loteId`) |

Mensagem sem `tenantId`, `eventId`, `type` ou `version` vai direto para a DLQ como `envelope_invalido`, sem novas tentativas.

## 6. Pendentes (mensagens não confirmadas)

- Cada consumidor roda, a cada `reclaim-interval` (padrão 30 s `[INFERIDO]`), um `XAUTOCLAIM` com `min-idle` igual ao **TTL do lock** do arquivo (estimativa + 10%, ADR_072) — assim só reivindica mensagens de worker que caiu.
- Para filas sem lock (Sugestão, Notificação), `min-idle` = timeout do processamento + margem (Sugestão: 30 s + 2%, ADR_077/078).
- Reivindicada a mensagem, o processamento é o mesmo; a idempotência (seção 8) impede trabalho duplicado.

## 7. Tentativas e DLQ

- **FilaOrdenada (Finder):** até **3 tentativas** no total (ADR_046/059). Em falha de processamento (instabilidade), o consumidor
  publica uma cópia com `tentativa + 1` no **fim da mesma FilaOrdenada** e faz `XACK` da original (ADR_059). Na 3ª falha:
  publica na DLQ e o alerta segue o fluxo da ADR_073 (usuário só pode reenviar novo arquivo).
- **Erro crítico** (leitura/parse inválido, malware, prompt injection): **sem retry, sem DLQ de reprocessamento** — cancela o arquivo e
  registra o erro (ADR_049); a mensagem é confirmada.
- **Sugestão manual:** 3 novas tentativas com espera de 5 s, 15 s e 45 s (4 execuções; ADR_094). Redis Streams não tem atraso nativo:
  reenvio atrasado por ZSET `lhamalog:prod:atrasadas:sugestao-manual` (score = horário) movido para a stream por um agendador `[INFERIDO]`; cada tentativa troca a reserva atomicamente (ADR_098).
- **DLQ:** mesma estrutura de envelope + campos `motivoFalha`, `ultimoErro`, `streamOrigem`. A DLQ não é reprocessada automaticamente.

## 8. Idempotência

- Chave por fila: FilaOrdenada/Finder = `arquivoId + execId` (ADR_070); demais = `eventId`.
- Antes de processar: `SET lhamalog:prod:idem:GRUPO:CHAVE 1 NX EX TTL` — se já existe, só faz `XACK`.
- TTL da chave de idempotência = retenção da stream `[INFERIDO]`.
- O lock de arquivo continua na coleção MongoDB (ADR_058/069); a chave Redis só evita reprocessar a mesma mensagem.

## 9. Código base (copiar em cada repositório)

### 9.1 Propriedades

```yaml
lhamalog:
  streams:
    ambiente: prod
    consumidor:
      grupo: finder
      workers: 10
      count: 10
      block: 2s
      reclaim-interval: 30s
      min-idle: 120s
    tentativas-maximas: 3
    maxlen: 100000
spring:
  data:
    redis:
      host: ${REDIS_HOST}
      port: 6379
      password: ${REDIS_PASSWORD}
      ssl:
        enabled: true
```

### 9.2 Envelope

```java
public record EnvelopeEvento(
        String eventId, String type, int version, Instant timestamp,
        String tenantId, String produtoId, String execId, int tentativa,
        String traceparent, String payload) {

    public Map<String, String> paraCampos() {
        Map<String, String> m = new LinkedHashMap<>();
        m.put("eventId", eventId); m.put("type", type);
        m.put("version", Integer.toString(version));
        m.put("timestamp", timestamp.toString());
        m.put("tenantId", tenantId);
        if (produtoId != null) m.put("produtoId", produtoId);
        if (execId != null) m.put("execId", execId);
        m.put("tentativa", Integer.toString(tentativa));
        if (traceparent != null) m.put("traceparent", traceparent);
        m.put("payload", payload);
        return m;
    }

    public static EnvelopeEvento deCampos(Map<String, String> c) {
        if (c.get("eventId") == null || c.get("tenantId") == null
                || c.get("type") == null || c.get("version") == null) {
            throw new EnvelopeInvalidoException(c);
        }
        return new EnvelopeEvento(c.get("eventId"), c.get("type"),
                Integer.parseInt(c.get("version")), Instant.parse(c.get("timestamp")),
                c.get("tenantId"), c.get("produtoId"), c.get("execId"),
                Integer.parseInt(c.getOrDefault("tentativa", "1")),
                c.get("traceparent"), c.get("payload"));
    }

    public EnvelopeEvento proximaTentativa() {
        return new EnvelopeEvento(eventId, type, version, Instant.now(), tenantId,
                produtoId, execId, tentativa + 1, traceparent, payload);
    }
}
```

### 9.3 Nomes de chaves

```java
public final class ChavesStream {
    private final String ambiente;
    public ChavesStream(String ambiente) { this.ambiente = ambiente; }

    public String filaDesordenada(String tenantId, String produtoId) {
        return "lhamalog:" + ambiente + ":fila-desordenada:{" + tenantId + ":" + produtoId + "}";
    }
    public String filaOrdenada(String tenantId, String produtoId) {
        return "lhamalog:" + ambiente + ":fila-ordenada:{" + tenantId + ":" + produtoId + "}";
    }
    public String dlq(String tenantId, String produtoId) {
        return "lhamalog:" + ambiente + ":fila-ordenada-dlq:{" + tenantId + ":" + produtoId + "}";
    }
    public String idempotencia(String grupo, String chave) {
        return "lhamalog:" + ambiente + ":idem:" + grupo + ":" + chave;
    }
}
```

### 9.4 Produtor

```java
@Component
public class PublicadorStream {
    private final StringRedisTemplate redis;
    private final long maxlen;

    public PublicadorStream(StringRedisTemplate redis,
                            @Value("${lhamalog.streams.maxlen}") long maxlen) {
        this.redis = redis; this.maxlen = maxlen;
    }

    public RecordId publicar(String chave, EnvelopeEvento e) {
        MapRecord<String, String, String> rec =
                StreamRecords.newRecord().in(chave).ofMap(e.paraCampos());
        return redis.opsForStream().add(rec,
                RedisStreamCommands.XAddOptions.maxlen(maxlen).approximateTrimming(true));
    }
}
```

### 9.5 Consumidor base

```java
public abstract class ConsumidorStreamBase
        implements StreamListener<String, MapRecord<String, String, String>> {

    protected final StringRedisTemplate redis;
    protected final PublicadorStream publicador;
    protected final MeterRegistry metricas;
    protected final String grupo;
    protected final int tentativasMaximas;

    protected ConsumidorStreamBase(StringRedisTemplate redis, PublicadorStream publicador,
                                   MeterRegistry metricas, String grupo, int tentativasMaximas) {
        this.redis = redis; this.publicador = publicador; this.metricas = metricas;
        this.grupo = grupo; this.tentativasMaximas = tentativasMaximas;
    }

    /** Regra de negocio do modulo. Lancar ErroCriticoException para falha sem retry. */
    protected abstract void processar(EnvelopeEvento evento);
    protected abstract String chaveIdempotencia(EnvelopeEvento evento);
    protected abstract String chaveDlq(EnvelopeEvento evento);
    protected abstract Duration ttlIdempotencia();

    @Override
    public final void onMessage(MapRecord<String, String, String> msg) {
        String stream = msg.getStream();
        Timer.Sample amostra = Timer.start(metricas);
        EnvelopeEvento evento;
        try {
            evento = EnvelopeEvento.deCampos(msg.getValue());
        } catch (EnvelopeInvalidoException ex) {
            redis.opsForStream().add(StreamRecords.newRecord().in(stream + "-dlq")
                    .ofMap(Map.of("motivoFalha", "envelope_invalido", "streamOrigem", stream)));
            ack(stream, msg.getId());
            metricas.counter("lhamalog.stream.envelope_invalido", "grupo", grupo).increment();
            return;
        }
        String idem = chaveIdempotencia(evento);
        Boolean novo = redis.opsForValue().setIfAbsent(idem, "1", ttlIdempotencia());
        if (Boolean.FALSE.equals(novo)) {
            ack(stream, msg.getId());
            metricas.counter("lhamalog.stream.duplicada", "grupo", grupo).increment();
            return;
        }
        try {
            processar(evento);
            ack(stream, msg.getId());
            metricas.counter("lhamalog.stream.sucesso", "grupo", grupo, "type", evento.type()).increment();
        } catch (ErroCriticoException ex) {
            ack(stream, msg.getId());
            metricas.counter("lhamalog.stream.erro_critico", "grupo", grupo).increment();
        } catch (RuntimeException ex) {
            redis.delete(idem);
            if (evento.tentativa() < tentativasMaximas) {
                publicador.publicar(stream, evento.proximaTentativa());
                metricas.counter("lhamalog.stream.retry", "grupo", grupo).increment();
            } else {
                Map<String, String> campos = new LinkedHashMap<>(evento.paraCampos());
                campos.put("motivoFalha", "tentativas_esgotadas");
                campos.put("ultimoErro", String.valueOf(ex.getMessage()));
                campos.put("streamOrigem", stream);
                redis.opsForStream().add(StreamRecords.newRecord().in(chaveDlq(evento)).ofMap(campos));
                metricas.counter("lhamalog.stream.dlq", "grupo", grupo).increment();
            }
            ack(stream, msg.getId());
        } finally {
            amostra.stop(metricas.timer("lhamalog.stream.processamento", "grupo", grupo));
        }
    }

    private void ack(String stream, RecordId id) {
        redis.opsForStream().acknowledge(stream, grupo, id);
    }
}
```

### 9.6 Container e grupos

```java
@Configuration
public class StreamConfig {

    @Bean(initMethod = "start", destroyMethod = "stop")
    public StreamMessageListenerContainer<String, MapRecord<String, String, String>> container(
            RedisConnectionFactory cf, StreamProperties props) {
        var opcoes = StreamMessageListenerContainer.StreamMessageListenerContainerOptions
                .builder()
                .batchSize(props.count())
                .pollTimeout(props.block())
                .errorHandler(t -> LoggerFactory.getLogger("stream").error("erro no container", t))
                .build();
        return StreamMessageListenerContainer.create(cf, opcoes);
    }

    /** Cria o grupo se nao existir (BUSYGROUP e ignorado). */
    public static void garantirGrupo(StringRedisTemplate redis, String chave, String grupo) {
        try {
            redis.opsForStream().createGroup(chave, ReadOffset.latest(), grupo);
        } catch (RedisSystemException ex) {
            if (ex.getCause() == null || !String.valueOf(ex.getCause().getMessage()).contains("BUSYGROUP")) {
                throw ex;
            }
        }
    }

    /** Registra um worker para uma stream. Nome do consumidor: SERVICO-HOSTNAME-INDICE. */
    public static Subscription registrar(
            StreamMessageListenerContainer<String, MapRecord<String, String, String>> container,
            String chave, String grupo, String servico, int indice, ConsumidorStreamBase consumidor) {
        String nome = servico + "-" + System.getenv().getOrDefault("HOSTNAME", "local") + "-" + indice;
        return container.receive(Consumer.from(grupo, nome),
                StreamOffset.create(chave, ReadOffset.lastConsumed()), consumidor);
    }
}
```

- `receive` (sem auto-ack) — o `XACK` é feito pela classe base.
- Streams por Produto: ao surgir uma chave nova no SET de registro, o serviço chama `garantirGrupo` + `registrar` para ela `[INFERIDO]`.

### 9.7 Reivindicação de pendentes

```java
@Component
public class ReivindicadorPendentes {
    private final StringRedisTemplate redis;
    public ReivindicadorPendentes(StringRedisTemplate redis) { this.redis = redis; }

    /** Chamado a cada reclaim-interval (@Scheduled + ShedLock, ADR_147). */
    public void reivindicar(String chave, String grupo, String consumidor, Duration minIdle,
                            ConsumidorStreamBase destino) {
        PendingMessages pendentes = redis.opsForStream()
                .pending(chave, grupo, Range.unbounded(), 10);
        RecordId[] parados = pendentes.stream()
                .filter(p -> p.getElapsedTimeSinceLastDelivery().compareTo(minIdle) >= 0)
                .map(PendingMessage::getId)
                .toArray(RecordId[]::new);
        if (parados.length == 0) return;
        List<MapRecord<String, Object, Object>> recs = redis.opsForStream()
                .claim(chave, grupo, consumidor, minIdle, parados);
        for (MapRecord<String, Object, Object> r : recs) {
            Map<String, String> campos = new LinkedHashMap<>();
            r.getValue().forEach((k, v) -> campos.put(k.toString(), v.toString()));
            destino.onMessage(StreamRecords.newRecord().in(chave).withId(r.getId()).ofMap(campos));
        }
    }
}
```

- Usa `XPENDING` + `XCLAIM` (expostos em `StreamOperations`). `XAUTOCLAIM` faz o mesmo em um comando; adotar se a API da versão do Spring Data Redis gerenciada pelo Boot 4.1.1 o expuser `[PENDENTE — verificar]`.

## 10. MAXLEN e retenção

- Toda publicação usa `MAXLEN ~` (trim aproximado). Proposta: 100 000 entradas por stream `[INFERIDO]`.
- O trim só remove entradas antigas; mensagens pendentes não confirmadas podem ser perdidas se a fila crescer além do limite — por isso o alerta de tamanho (seção 11).
- DLQ: `MAXLEN ~ 10000` e retenção de 3 meses, alinhada ao histórico (ADR_071) `[INFERIDO]`.
- Persistência do Redis: AOF ligado (`appendonly yes`, `everysec`) `[INFERIDO]`.

## 11. Observabilidade

| Métrica | Origem |
|---|---|
| `lhamalog.stream.processamento` (timer) | classe base |
| `lhamalog.stream.sucesso` / `retry` / `dlq` / `erro_critico` / `duplicada` / `envelope_invalido` | classe base |
| tamanho da stream (`XLEN`) e pendentes (`XPENDING`) por grupo | job de coleta `[INFERIDO]` → Prometheus |
| tempo na fila (agora − `timestamp`) | classe base `[INFERIDO]` — métrica usada pela DevOps para escalar pods do Finder (ADR_065) |

- Propagar `traceparent` do envelope para o span do processamento (OpenTelemetry).
- Logs com `tenantId`, `produtoId`, `eventId`, `execId` no MDC.

## 12. Tratamento de erros (resumo)

| Situação | Ação |
|---|---|
| Envelope inválido | DLQ `envelope_invalido`, `XACK`, sem retry |
| Erro crítico de negócio | registra, `XACK`, sem retry, sem DLQ |
| Falha transitória | nova tentativa no fim da stream (até 3); depois DLQ + alerta |
| Worker caiu | `XAUTOCLAIM` após `min-idle` |
| Redis indisponível | container reconecta; health do actuator fica DOWN |

## 13. Testes

- Testcontainers com a imagem oficial `redis` `[PENDENTE — versão do Redis]` e `@ServiceConnection`.
- Casos mínimos por consumidor: sucesso com `XACK`; duplicada (idempotência); falha transitória gera nova tentativa com `tentativa + 1`; 3ª falha vai para a DLQ; erro crítico sem retry; envelope inválido; reivindicação de pendente após `min-idle`.

```java
@SpringBootTest
@Testcontainers
class ConsumidorFinderTest {
    @Container @ServiceConnection(name = "redis")
    static GenericContainer<?> redis = new GenericContainer<>("redis:7-alpine").withExposedPorts(6379);
    // publicar envelope, aguardar processamento e verificar XPENDING vazio e DLQ conforme o caso
}
```

## 14. Pontos em aberto

- **Resolvido (ADR_147)** agendador: @Scheduled + ShedLock (Mongo) `[INFERIDO — uso também para reivindicação e reenvios]`.
- `[PENDENTE]` versão do Redis e topologia (standalone, Sentinel ou Cluster).
- `[PENDENTE]` usar XAUTOCLAIM no lugar de XPENDING + XCLAIM se a API do Spring Data Redis do Boot 4.1.1 expuser.
- `[PENDENTE]` frequência da limpeza de consumidores mortos.
- `[INFERIDO]` MAXLEN 100 000, retenção de 3 meses na DLQ, registro de streams por Produto, ZSET para atrasos.
