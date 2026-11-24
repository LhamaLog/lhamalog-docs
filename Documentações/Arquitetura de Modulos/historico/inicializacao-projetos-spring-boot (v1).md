# Inicialização dos projetos Spring Boot — proposta para revisão (LhamaLog)

**Versão 1 (12/10/2026, Michel Bocchi Junior).** Documento de **revisão**: nenhum projeto foi criado. Versões são **propostas**
(não viram ADR até decisão). Base: `arquitetura-modulos.md` e ADR_028, 054, 057–075, 096, 105–142.
Marcações: `[PENDENTE]` sem decisão; `[INFERIDO]` derivado das decisões existentes.

## 1. Versões propostas (pesquisa de 12/10/2026)

| Item | Proposta | Motivo | Fonte |
|---|---|---|---|
| Java | **25 (LTS)** | LTS de setembro/2025, suporte premier até 09/2030; Oracle JDK 25 sob licença gratuita; JDK 21 sai da licença permissiva em out/2026 | https://www.oracle.com/java/technologies/java-se-support-roadmap.html |
| Spring Boot | **4.1.1** (estável, 20/08/2026) | 4.1 é a linha estável atual (suporte OSS até ~07/2027); 4.2 ainda em milestone (4.2.0-M2); Boot 4.1 aceita Java 17–26 | https://spring.io/blog/2026/08/20/spring-boot-4-1-1-available-now · https://docs.spring.io/spring-boot/system-requirements.html |
| Spring Framework | 7.x (gerenciado pelo Boot) | base do Boot 4 | https://spring.io/blog/2025/11/20/spring-boot-4-0-0-available-now |
| Spring AI (cliente LLM) | **2.0.0** | GA em 12/06/2026, compatível com Boot 4.0/4.1 | https://spring.io/blog/2026/06/12/spring-ai-2-0-0-GA-available-now |
| Build | **Maven** (3.9+) `[INFERIDO]` | equipe Java tradicional, BOM do Boot, parent POM simples; Gradle 8.14+/9 também é suportado | https://docs.spring.io/spring-boot/system-requirements.html |

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
| `lhamalog-commons` (opcional, seção 5) | `commons` | `br.com.lhamalog.commons` |

- groupId sugerido: **`br.com.lhamalog`** `[PENDENTE — confirmar domínio; alternativa io.lhamalog]`.
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

**Comuns a todos** (via parent/commons):
- `spring-boot-starter-web` (exceto onde indicado), `spring-boot-starter-validation`
- `spring-boot-starter-actuator` — `/actuator/health` interno e métricas
- `spring-boot-starter-data-mongodb` — MongoDB compartilhado (ADR_029/116)
- `spring-boot-starter-security` + `spring-boot-starter-oauth2-resource-server` — validação do **JWT interno** (ADR_028)
- `spring-boot-starter-opentelemetry` / Micrometer Tracing + exportador OTLP — observabilidade dos próprios serviços `[INFERIDO]`
- `spring-boot-starter-test`, Testcontainers (MongoDB, Elasticsearch, broker)
- Lombok `[PENDENTE — preferência da equipe]`
- Starter do broker: `spring-boot-starter-amqp` (RabbitMQ) **ou** `spring-boot-starter-data-redis` (Redis Streams) — `[PENDENTE]` (ADR_096; planilha sugere benchmark)

| Módulo | Dependências específicas | Observações |
|---|---|---|
| **Core** | `oauth2-resource-server` com JWKS da **Clerk** (session token) + emissor do JWT interno; `spring-boot-starter-websocket` (WebSocket do front, ADR_051/141); SDK/webhooks da Clerk (verificação Svix `[PENDENTE]`); cliente HTTP (`RestClient` / HTTP Service Clients) para os outros módulos; SDK do gateway de pagamento `[PENDENTE — LLT-88/89/90]` | único com API pública do front; filtro `tenantId` centralizado (ADR_121); rotas `/papeis` (ADR_139) |
| **Coletor** | **receptor OTLP**: `io.opentelemetry.proto:opentelemetry-proto` + `grpc-netty-shaded`/`grpc-protobuf`/`grpc-services` (OTLP gRPC 4317 e `grpc.health.v1`) e endpoint HTTP 4318 `/v1/logs`, `/v1/traces` aceitando protobuf e JSON; `spring-boot-starter-data-elasticsearch` (logs, ADR_116); cliente de object storage (S3-compatível `[INFERIDO]`); criptografia AES-256-GCM via JCA (`javax.crypto`) + KMS/secret manager `[PENDENTE — provedor]`; Caffeine/Redis para cache hash do token `[INFERIDO]` | não há starter Spring para receber OTLP: o receptor é implementado com os protos oficiais `[INFERIDO]`; responder 401, 429/503 + `Retry-After: 120` (ADR_118/120) |
| **Varredura** | broker; MongoDB (locks chave-valor com TTL, ADR_058/069/072); `spring-boot-starter-quartz` ou `@Scheduled` para o cron `[PENDENTE]` | API rápida de fim de execução (ADR_070); IDs `V`/`M` + UUID |
| **Finder** | broker (consumo paralelo, idempotência arquivoId + execId); `spring-boot-starter-data-elasticsearch`; **Spring AI 2.0** (`GatewayLLMFinder`, provedor do LhamaLog, sem BYOK); BancoVetorial por Produto (Spring AI Vector Store — MongoDB Atlas Vector Search ou Elasticsearch `[PENDENTE]`) | mascaramento por regex (ADR_064, lista `[PENDENTE]`) |
| **Ocorrência + Sugestão** | **Spring AI 2.0** (`GatewayLLMSugestao`; OpenAI/Anthropic/DeepSeek `[PENDENTE]`) com cliente por tenant para **BYOK** (`ChaveLLMTenant`, AES-256-GCM); broker (fila da Sugestão manual, retries 5/15/45 s); MongoDB | timeouts de 30 s; reserva de Créditos (ADR_078/096) |
| **Notificação** | `spring-boot-starter-mail` (e-mail) e SDK de push (FCM/APNs `[PENDENTE]`); broker ou chamada interna do Core; **sem** web pública — só egress (ADR_141) | o WebSocket fica no Core (proposta da ADR_141); Notificação devolve ao Core o que vai por WebSocket `[PENDENTE confirmação]` |

**Nota sobre WebSocket:** o pedido cita WebSocket na Notificação, mas a ADR_141 deixa a Notificação só de saída e propõe o
WebSocket no **Core**. Por isso `spring-boot-starter-websocket` está no Core. Se Michel decidir o contrário, mover a dependência.

## 5. Biblioteca comum (`lhamalog-commons`) — opção

| Opção | Prós | Contras |
|---|---|---|
| **A. commons publicado como artefato Maven** (repositório próprio, versionado, publicado em GitHub Packages `[INFERIDO]`) | uma só implementação do JWT interno, filtro `tenantId`, AES-256-GCM, DTOs de eventos de fila, erros padrão | acoplamento de versão entre serviços; exige pipeline de publicação |
| **B. sem commons — cada serviço copia o mínimo** | serviços totalmente independentes | duplicação de segurança e criptografia (risco de divergência) |

Recomendação: **A, enxuto** — só segurança interna (JWT), criptografia, contexto de tenant e contratos de evento; nada de regra de negócio. `[PENDENTE — decisão do Michel]`

## 6. Configuração inicial sugerida (por serviço)

- `application.yml` + perfis `local`, `dev`, `prod`; segredos por variável de ambiente / secret manager.
- Porta interna HTTP por serviço `[PENDENTE]`; Coletor também 4318 e 4317 públicas (via gateway).
- `management.endpoints.web.exposure.include=health,info,prometheus` só na rede interna.
- Dockerfile ou buildpacks (`spring-boot:build-image`); deploy Kubernetes `[INFERIDO]`.
- Spring Initializr com: Java 25, Boot 4.1.1, Maven, Jar, groupId `br.com.lhamalog`.

## 7. Pontos em aberto

- `[PENDENTE]` broker das filas (RabbitMQ × Redis Streams) — define o starter em Coletor, Varredura, Finder, Ocorrência e Notificação.
- `[PENDENTE]` Maven × Gradle (proposta: Maven) e groupId.
- `[PENDENTE]` adotar o `lhamalog-commons`.
- `[PENDENTE]` provedor LLM padrão; tecnologia do BancoVetorial.
- `[PENDENTE]` KMS/secret manager, object storage, provedor de e-mail/push, gateway de pagamento.
- `[PENDENTE]` WebSocket no Core (proposta) × na Notificação.
- `[PENDENTE]` agendador da Varredura (Quartz × `@Scheduled`).
- `[INFERIDO]` receptor OTLP implementado com os protos oficiais; verificar versões de `opentelemetry-proto` e `grpc-java` compatíveis no momento da criação.
