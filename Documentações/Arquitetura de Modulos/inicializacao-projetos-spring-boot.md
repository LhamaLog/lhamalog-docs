# Inicialização dos projetos Spring Boot — proposta para revisão (LhamaLog)

**Versão 4 (30/10/2026, Pedro Alvaro).** Aplica a ADR_165 (WebSocket no Core decidido; a Notificação devolve ao Core as notificações web pela fila de entregas web; push em espera, ADR_025) e a ADR_167 (o Finder não usa LLM: sai o Spring AI do Finder). Versão 3 em `v3/`.

**Versão 3 (14/10/2026, Michel Bocchi Junior).** Aplica a ADR_147 (agendador da Varredura: @Scheduled + ShedLock). Versão 2 em `v2/`.

Aplica as ADR_143 a ADR_146: **Redis Streams**, **Maven** com groupId `br.com.lhamalog`, **sem biblioteca comum** e padrão de streams (`guia-redis-streams.md`). Versão 1 em `v1/`.

Documento de **revisão**: nenhum projeto foi criado. Versões são **propostas**
(não viram ADR até decisão). Base: `arquitetura-modulos.md` e ADR_028, 054, 057–075, 096, 105–142.
Marcações: `[PENDENTE]` sem decisão; `[INFERIDO]` derivado das decisões existentes.

## 1. Versões propostas (pesquisa de 12/10/2026)

| Item | Proposta | Motivo | Fonte |
|---|---|---|---|
| Java | **25 (LTS)** | LTS de setembro/2025, suporte premier até 09/2030; Oracle JDK 25 sob licença gratuita; JDK 21 sai da licença permissiva em out/2026 | https://www.oracle.com/java/technologies/java-se-support-roadmap.html |
| Spring Boot | **4.1.1** (estável, 20/08/2026) | 4.1 é a linha estável atual (suporte OSS até ~07/2027); 4.2 ainda em milestone (4.2.0-M2); Boot 4.1 aceita Java 17–26 | https://spring.io/blog/2026/08/20/spring-boot-4-1-1-available-now · https://docs.spring.io/spring-boot/system-requirements.html |
| Spring Framework | 7.x (gerenciado pelo Boot) | base do Boot 4 | https://spring.io/blog/2025/11/20/spring-boot-4-0-0-available-now |
| Spring AI (cliente LLM) | **2.0.0** | GA em 12/06/2026, compatível com Boot 4.0/4.1 | https://spring.io/blog/2026/06/12/spring-ai-2-0-0-GA-available-now |
| Build | **Maven** (3.9+) — **decidido (ADR_144)** | parent POM do Boot | https://docs.spring.io/spring-boot/system-requirements.html |

Observações:
- Spring Boot não tem LTS; cada minor tem 12 meses de suporte OSS — planejar subir para 4.2 quando sair estável.
- Começar em 4.1.1 e não em 4.2 milestone, por estabilidade.

## 2. Repositórios (5+1, ADR_054 + ADR_141)

| Repositório | artifactId | Pacote base |
|---|---|---|
| `lhamalog-core` | `core` | `br.com.lhamalog.core` |
| `lhamalog-coletor` | `coletor` | `br.com.lhamalog.coletor` |
| `lhamalog-varredura` | `varredura` | `br.com.lhamalog.varredura` |
| `lhamalog-finder` | `finder` | `br.com.lhamalog.finder` |
| `lhamalog-ocorrencia` | `ocorrencia` (inclui Sugestão IA) | `br.com.lhamalog.ocorrencia` |
| `lhamalog-notificacao` | `notificacao` | `br.com.lhamalog.notificacao` |

- groupId: **`br.com.lhamalog`** — decidido (ADR_144).
- Um repositório por serviço; todos com o mesmo parent (`spring-boot-starter-parent` 4.1.1) e as mesmas convenções.

## 3. Estrutura de pacotes

Proposta: **hexagonal leve (ports and adapters)** em todos os serviços — o domínio não conhece MongoDB, fila nem HTTP, o que
facilita trocar o broker (ainda `[PENDENTE]`) e o provedor de LLM (BYOK). Para serviços pequenos (Notificação, Varredura)
pode-se usar camadas simples `[INFERIDO]`.

```
br.com.lhamalog.MODULO
  dominio/            entidades, regras, enums (sem Spring)
  aplicacao/          casos de uso (services) e portas
    porta/entrada/    interfaces chamadas pelos adaptadores de entrada
    porta/saida/      interfaces para banco, fila, LLM, outros servicos
  adaptador/
    entrada/rest/     controllers (API publica ou interna)
    entrada/fila/     consumidores de fila
    saida/mongo/      repositorios Spring Data MongoDB
    saida/fila/       publicadores
    saida/http/       clientes para outros servicos (JWT interno)
  config/             seguranca, beans, propriedades
```

## 4. Dependências por módulo

**Comuns a todos** (via parent POM; sem biblioteca comum, ADR_145):
- `spring-boot-starter-web` (exceto onde indicado), `spring-boot-starter-validation`
- `spring-boot-starter-actuator` — `/actuator/health` interno e métricas
- `spring-boot-starter-data-mongodb` — MongoDB compartilhado (ADR_029/116)
- `spring-boot-starter-security` + `spring-boot-starter-oauth2-resource-server` — validação do **JWT interno** (ADR_028)
- `spring-boot-starter-opentelemetry` / Micrometer Tracing + exportador OTLP — observabilidade dos próprios serviços `[INFERIDO]`
- `spring-boot-starter-test`, Testcontainers (MongoDB, Elasticsearch, broker)
- Lombok `[PENDENTE — preferência da equipe]`
- Broker: **`spring-boot-starter-data-redis`** (Redis Streams, ADR_143) em Coletor, Varredura, Finder, Ocorrência, Notificação e Core (eventos de notificação e entregas web, ADR_165); padrão no `guia-redis-streams.md` (ADR_146)

| Módulo | Dependências específicas | Observações |
|---|---|---|
| **Core** | `oauth2-resource-server` com JWKS da **Clerk** (session token) + emissor do JWT interno; `spring-boot-starter-websocket` (WebSocket do front, ADR_051/141); SDK/webhooks da Clerk (verificação Svix `[PENDENTE]`); cliente HTTP (`RestClient` / HTTP Service Clients) para os outros módulos; SDK do gateway de pagamento `[PENDENTE — LLT-88/89/90]` | único com API pública do front; filtro `tenantId` centralizado (ADR_121); rotas `/papeis` (ADR_139) |
| **Coletor** | **receptor OTLP**: `io.opentelemetry.proto:opentelemetry-proto` + `grpc-netty-shaded`/`grpc-protobuf`/`grpc-services` (OTLP gRPC 4317 e `grpc.health.v1`) e endpoint HTTP 4318 `/v1/logs`, `/v1/traces` aceitando protobuf e JSON; `spring-boot-starter-data-elasticsearch` (logs, ADR_116); cliente de object storage (S3-compatível `[INFERIDO]`); criptografia AES-256-GCM via JCA (`javax.crypto`) + KMS/secret manager `[PENDENTE — provedor]`; Caffeine/Redis para cache hash do token `[INFERIDO]` | não há starter Spring para receber OTLP: o receptor é implementado com os protos oficiais `[INFERIDO]`; responder 401, 429/503 + `Retry-After: 120` (ADR_118/120) |
| **Varredura** | Redis Streams; MongoDB (locks chave-valor com TTL, ADR_058/069/072); agendador **@Scheduled + ShedLock** (`net.javacrumbs.shedlock:shedlock-spring` e `shedlock-provider-mongo`, ADR_147): um tick global lê `varredura_schedules` e publica as execuções vencidas no Redis Streams; o gatilho de 500 arquivos publica na mesma stream; histórico com TTL de ~90 dias | API rápida de fim de execução (ADR_070); IDs `V`/`M` + UUID |
| **Finder** | broker (consumo paralelo, idempotência arquivoId + execId); `spring-boot-starter-data-elasticsearch`; **sem LLM** (IA própria: classificação por regras e padrões, ADR_167); BancoVetorial no Elasticsearch (ADR_152) | mascaramento por regex (ADR_064, lista `[PENDENTE]`); o Finder passou a ser em Go (ADR_152/153) e a stack dele está no plano de inicialização do Finder |
| **Ocorrência + Sugestão** | **Spring AI 2.0** (`GatewayLLMSugestao`; OpenAI/Anthropic/DeepSeek `[PENDENTE]`) com cliente por tenant para **BYOK** (`ChaveLLMTenant`, AES-256-GCM); broker (fila da Sugestão manual, retries 5/15/45 s); MongoDB | timeouts de 30 s; reserva de Créditos (ADR_078/096) |
| **Notificação** | `spring-boot-starter-mail` (e-mail); SDK de push (FCM/APNs `[PENDENTE]`) em espera enquanto o app móvel estiver em STANDBY (ADR_025/165); Redis Streams (consome os eventos de notificação e publica as entregas web, ADR_165); **sem** web pública — só egress (ADR_141) | o WebSocket fica no Core (decidido, ADR_165); a Notificação devolve ao Core as notificações web pela fila de entregas web |

**Nota sobre WebSocket:** o pedido cita WebSocket na Notificação, mas a ADR_141 deixa a Notificação só de saída, e a ADR_165
decidiu o WebSocket no **Core**. Por isso `spring-boot-starter-websocket` está no Core.

## 5. Sem biblioteca comum (ADR_145)

Não há `lhamalog-commons`. Cada repositório copia as classes padrão no próprio código:
- base de streams (`EnvelopeEvento`, `ChavesStream`, `PublicadorStream`, `ConsumidorStreamBase`, `StreamConfig`, `ReivindicadorPendentes`) — `guia-redis-streams.md`;
- validação/emissão do JWT interno e AES-256-GCM `[INFERIDO — mesmo padrão de cópia]`.
Mudanças nessas classes são aplicadas em todos os repositórios a partir dos guias.

## 6. Configuração inicial sugerida (por serviço)

- `application.yml` + perfis `local`, `dev`, `prod`; segredos por variável de ambiente / secret manager.
- Porta interna HTTP por serviço `[PENDENTE]`; Coletor também 4318 e 4317 públicas (via gateway).
- `management.endpoints.web.exposure.include=health,info,prometheus` só na rede interna.
- Dockerfile ou buildpacks (`spring-boot:build-image`); deploy Kubernetes `[INFERIDO]`.
- Spring Initializr com: Java 25, Boot 4.1.1, Maven, Jar, groupId `br.com.lhamalog`, dependência Spring Data Redis.

## 7. Pontos em aberto

- **Resolvido (ADR_143)** broker: Redis Streams.
- **Resolvido (ADR_144)** Maven e groupId `br.com.lhamalog`.
- **Resolvido (ADR_145)** sem biblioteca comum.
- **Resolvido (ADR_147)** agendador: @Scheduled + ShedLock (Mongo).
- `[INFERIDO]` intervalo do tick e `lockAtMostFor` a definir.
- `[PENDENTE]` versão e topologia do Redis.
- `[PENDENTE]` provedor LLM padrão da Sugestão; o Finder não usa LLM (ADR_167).
- **Resolvido (ADR_152)** BancoVetorial no Elasticsearch.
- `[PENDENTE]` KMS/secret manager, object storage, provedor de e-mail/push, gateway de pagamento.
- **Resolvido (ADR_165)** WebSocket no Core; a Notificação devolve as notificações web pela fila de entregas web.
- `[INFERIDO]` receptor OTLP implementado com os protos oficiais; verificar versões de `opentelemetry-proto` e `grpc-java` compatíveis no momento da criação.
