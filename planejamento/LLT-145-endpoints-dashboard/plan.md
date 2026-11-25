# Plano Arquitetural: Endpoints dos módulos para o Dashboard (LLT-145)

**Branch**: `LLT-145-endpoints-dashboard` | **Data**: 2026-11-25 (America/Sao_Paulo) | **Spec**: [spec.md](spec.md)

Atualizado com as decisões D1–D9 do Michel (25/11/2026 15:14, America/Sao_Paulo).

## Resumo da arquitetura

Pela `ADR_141`, o **Web** (e futuramente o Mobile, `LLT-159`) comunica-se **exclusivamente** com o **Core**. Todos os demais módulos (`Collector`, `Varredura`, `Finder`, `Módulo Ocorrência`, `Notificação`) operam em rede interna e interagem via **HTTP interno** ou **Redis Streams**, nunca expostos diretamente ao navegador.

```text
[Web SPA (9adb018)]
   │  HTTPS + Clerk JWT (Authorization: Bearer) + X-Correlation-Id
   ▼
[Core (82e7725)] ──(SQL _search)──────────────► [OpenObserve (org: lhamalog)]
   │  ▲                                                 ▲
   │  ├──(leitura/agregados SSID_011)──► [MongoDB]      │ (grava logs/traces)
   │  │                                                 │
   │  ├──(POST /internal/manual/upload, LLT-292)──► [Collector (5fb3160 + LLT-292)]
   │  │                                                 │
   │  ◄──(POST /internal/usage-facts + reservations)────┘  (inclui upload manual, D7)
   │                                                    │ (log.ingested / trace.ingested)
   │                                                    ▼
   │                                            [Redis Streams: lhamalog:stream:logs|traces]
   │                                                    │
   │  (pós-LLT-104)                                     ├──► [Varredura] ──(log.checked c/ execId, D4)──┐
   │  ├──(GET /internal/v1/occurrences/metrics)──┐      │                                               │
   │  ├──(GET /internal/v1/occurrences)──────────┤      └──► [Finder (Go worker, 693be4f)] ◄─────────────┘
   │  │                                          ▼                  │
   │  │                                 [Módulo Ocorrência] ◄───────┼── POST /internal/v1/occurrences/lookup
   │  │                                          │                  ├── POST /internal/v1/analysis-summaries
   │  ◄──(POST /internal/v1/occurrences/notifications)              ├── POST /internal/v1/scans/completions ──► [Varredura]
   │  ◄──(POST /internal/v1/alerts/finder)──────────────────────────┘
   │
   └──(Redis Stream de notificações, ADR_146/165)──► [Notificação]
```

## Decisões transversais de contrato

### 1. Autenticação e autorização

| Fronteira | Mecanismo | Regra | Fonte / Referência |
|---|---|---|---|
| **Web / Mobile → Core** (`/api/**`) | Clerk JWT (`Authorization: Bearer`) | Validação RS256 via JWKS, `exp`, `nbf`, `iss`, `azp`, sessão ativa (`SecurityConfig.java:83-94`). Acesso a produto validado por `tenantId` do token e `AcessoProduto` (`LLT-171`). Produto não autorizado ou de outro tenant retorna **404** no endpoint de produto. | `SecurityConfig.java:53-94`, `DashboardMetricsService.java`, `ADR_123`, `ADR_141` |
| **Cliente externo → Collector** (`/v1/logs`, `/v1/traces`) | Token de ingestão do produto (`Authorization: Bearer <productToken>`) | Collector calcula SHA-256 hex do token e consulta `product_tokens` → `products` no MongoDB para resolver `productId` e `tenantId`. Valores de tenant/produto do payload OTLP são ignorados. | `lhamalog-collector/specs/001-otlp-receiver/data-model.md:7-76` |
| **Rotas de saúde** (`/health`, `/actuator/health`, `/actuator/prometheus`) | Sem autenticação (rede interna / loopback para Prometheus) | `200 OK` ou `503 Service Unavailable`; nunca expõe dados de tenant. | `ADR_118`, `ActuatorSecurityConfiguration.java:21-36`, `health.go:7-14` |
| **Rotas que o Finder chama** (`POST /internal/v1/occurrences/lookup`, `POST /internal/v1/analysis-summaries`, `POST /internal/v1/scans/completions`, `POST /internal/v1/alerts/finder`) | `Authorization: Bearer <JWT>` | **Exceção decidida (D1, Michel, 25/11/2026):** o Finder **mantém** `Authorization: Bearer <JWT>` e **não** troca para `X-LhamaLog-Service-Token`. Os servidores (Ocorrência, Varredura e o alerta no Core) devem aceitar esse JWT nessas rotas. O código atual do Finder já envia `Authorization: Bearer` (`cliente.go:184`, `confirmacao/http.go:53`, `ADR_028`). | Decidido (Michel, 25/11/2026); `lhamalog-finder/.../cliente.go:184`, `confirmacao/http.go:53` |
| **Demais rotas módulo ↔ módulo** (`/internal/usage-facts/**`, `/internal/usage-reservations/**`, `/internal/manual/upload`, e as rotas novas entre Core e Ocorrência: `GET /internal/v1/occurrences/metrics`, `GET /internal/v1/occurrences`, `GET /internal/v1/occurrences/{occurrenceId}`, `POST /internal/v1/occurrences/notifications`) | `X-LhamaLog-Service-Token` | Padrão atual (Core `UsageFactsSecurityConfiguration.java:26-108` e `ADR_172`): cabeçalho `X-LhamaLog-Service-Token` comparado em tempo constante (`MessageDigest.isEqual` em Java / `crypto/subtle.ConstantTimeCompare` em Go) e **rejeição explícita (401)** se o cabeçalho `Authorization` estiver presente. | `UsageFactsSecurityConfiguration.java:26-108`, `ADR_172`; Decidido (Michel, 25/11/2026) (**D1**) |

### 2. Padrão de rotas e contratos JSON

- **Rotas públicas / borda do Core**: prefixo `/api/...` em inglês (ex.: `/api/dashboard/products/{productId}/metrics`, `/api/dashboard/company/metrics`).
- **Rotas internas entre serviços**: prefixo `/internal/...` (ou `/internal/v1/...`) em inglês, seguindo `/internal/usage-facts`, `/internal/usage-reservations` e `/internal/manual/upload`.
  - **Rotas do Finder (D2, Decidido (Michel, 25/11/2026))**: `/internal/v1/occurrences/lookup`, `/internal/v1/analysis-summaries`, `/internal/v1/scans/completions` e `/internal/v1/alerts/finder`. O código atual do Finder (`proposta-dn-009-2.openapi.yaml`, `cliente.go:21-22`, `finalizar.go:36`, `aviso.go:31`) ainda usa as rotas em português (`/internal/v1/ocorrencias/consultas`, `/internal/v1/resumos-analise`, `/internal/v1/execucoes/conclusoes`, `/internal/v1/alertas/finder`) e deve ser atualizado.
- **Timestamps em JSON**: sempre UTC ISO-8601 (`2026-11-25T17:41:00Z`) ou microssegundos inteiros (`_timestamp` no OpenObserve), conforme padrão do Core (`DashboardMetricsResponses.java:16-18`) e do Collector (`UsageFactRequest.java:21,36-38`). A conversão para o fuso do usuário ocorre na exibição (Web/Mobile).
- **Volumes e planos**: sempre em **bytes** inteiros (`volumeUsedBytes`, `volumeIngestaoBytes` = `allowanceGigabytes * 2^30`), com conversão visual para GiB apenas no Web (`ADR_131`, `spec 011`).

### 3. Padrão obrigatório de logs e correlação

Todos os serviços (Java e Go) devem seguir o padrão já implementado no Core (`application.properties:35-37`, `CorrelationIdFilter.java:11-26`) e no Collector (`application.properties:12-14`, `CorrelationId.java`). No Finder, isso é decisão fechada (**D5/D6**, Decidido (Michel, 25/11/2026)): o Finder propaga `X-Correlation-Id` e loga no fuso `America/Sao_Paulo` com referência à função.

1. **Cabeçalho HTTP**: `X-Correlation-Id`. Se ausente ou inválido na entrada, o serviço de borda gera um UUID v4; nas chamadas HTTP internas entre módulos, o chamador **deve** repassar o mesmo `X-Correlation-Id` (e em Redis Streams, carregar em `metadata.correlationId`); toda resposta HTTP devolve `X-Correlation-Id` ecoado.
2. **Formato de log em Java (Spring Boot)**:
   ```text
   %d{yyyy-MM-dd'T'HH:mm:ss.SSSXXX,${lhamalog.logging.time-zone:America/Sao_Paulo}} %5p [${spring.application.name:-}] [cid=%X{correlationId:-none}] [%t] %logger{40}.%M - %m%n%wEx
   ```
   Exemplo real:
   ```text
   2026-11-25T14:40:12.345-03:00  INFO [lhamalog-ocorrencia] [cid=6b9f1d2e-9a8b-4c7d-8e6f-1234567890ab] [http-nio-8082-exec-1] b.c.l.o.api.OccurrenceController.metrics - event=occurrences.metrics.completed | tenantId=org_2x... productId=prod_1 count=42
   ```
3. **Formato de log em Go (`lhamalog-finder` e eventuais workers Go)** — **D5/D6**, Decidido (Michel, 25/11/2026):
   - Usar `log/slog` com `AddSource: true` (referência à função/arquivo), `ReplaceAttr` formatando `slog.TimeKey` em `America/Sao_Paulo` (`time.LoadLocation("America/Sao_Paulo")`, layout `2006-01-02T15:04:05.000-03:00`), atributo fixo `"correlationId"` (extraído de `metadata.correlationId` do Redis ou `X-Correlation-Id`) e atributo `"event"` / `"msg"`.
   - *Estado atual do código (`693be4f`):* `cmd/finder/main.go:24` instancia `slog.NewJSONHandler(os.Stdout, nil)` sem `AddSource`, sem fuso `America/Sao_Paulo` e sem envio de `X-Correlation-Id` nos clientes HTTP. Essa lacuna vira tarefa de implementação (não mais decisão em aberto).
4. **Sigilo em logs**: nunca registrar tokens (`X-LhamaLog-Service-Token`, `Authorization`, `productToken`), senhas do OpenObserve/Mongo/Redis nem corpo bruto de log do cliente em logs de erro/debug.

### 4. Origem dos dados por componente do Dashboard

| Indicador do Dashboard (Web/Core) | Origem primária no MVP | Origem após `LLT-104` / pipeline completo |
|---|---|---|
| Totais de logs (`logs`, `error`, `warning`, `info`) e séries por hora/dia | **Core** (`DashboardLogHourlyAggregate` no Mongo via job `SSID_011` + consulta SQL OpenObserve no intervalo aberto) | Mantém logs no OpenObserve/agregados; o `SSID_011` no Core continua agregando logs e **soma as ocorrências** via `GET /internal/v1/occurrences/metrics` (**D4**, Decidido (Michel, 25/11/2026)) |
| Ranking de serviços (`serviceRanking`, top 5 por `ERROR`) | **Core** (mesmos buckets OpenObserve + agregados Mongo, coluna `servicename`) | Idem |
| Volume ingerido (`volumeUsedBytes`) e `traces` | **MongoDB `UsageFact`** gravado pelo **Collector** via `POST /internal/usage-facts`, inclusive no upload manual (**D7**, Decidido (Michel, 25/11/2026)) | Idem |
| Limite de plano e retenção (`volumeIngestaoBytes`, `retentionDays`) | **MongoDB `PlanSubscription`** no **Core** (`TenantRetentionResolver` + `ADR_131`) | Idem |
| Ocorrências (`SeriesPoint.occurrences` e drill-down `LLT-222`) | **Omitido** no Core (`DashboardMetricsResponses.java:39`); Web exibe *"não implementado ainda"* | **Módulo Ocorrência** via `GET /internal/v1/occurrences/metrics` + `GET /internal/v1/occurrences` (**D3**, Decidido (Michel, 25/11/2026)); apenas `ERROR` e `WARNING` viram `Ocorrencia` (**D9**) |
| Status de varredura / dados sensíveis mascarados (`ADR_102`) | Fora do contrato LLT-145 MVP | **Varredura fica fora do dashboard no MVP** (**D4**, Decidido (Michel, 25/11/2026)). `log.checked` / `trace.checked` levam `execId` para o pipeline, não para o gráfico do dashboard |
