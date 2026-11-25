# Módulo Collector — Endpoints e Papel no Dashboard (LLT-145)

**Repositório:** [`lhamalog-collector`](https://github.com/LhamaLog/lhamalog-collector)
**Branches inspecionadas:** `Development` (`5fb3160`), `feature/LLT-290-file-hash-dedup` (`44d36b4`, sem PR) e planejamento da `LLT-292` (`origin/LLT-290-292-planejamento` em `c2aa1fc`).

## 1. Resumo para a equipe

O **Collector não precisa implementar nenhum endpoint de consulta de métricas para o Dashboard LLT-145**. No MVP atual, o **Core** lê as contagens de logs diretamente no **OpenObserve** (`OpenObserveLogQueryAdapter.java`) e o volume/traces ingeridos diretamente do MongoDB (`UsageMetricsAdapter.java` sobre `UsageFact`), alimentado de forma assíncrona/em tempo de ingestão pelo próprio Collector (`POST /internal/usage-facts`).

**D7** (= I3 da LLT-292), Decidido (Michel, 25/11/2026): o upload manual (`POST /internal/manual/upload`) **grava `UsageFact`** no Core, para que o volume ingerido no dashboard (`volumeUsedBytes`) reflita também os uploads manuais. Esta decisão está registrada nesta documentação; **o código do Collector não foi alterado e permanece parado**.

## 2. Endpoints necessários e existentes no Collector

| Método e Rota | Autenticação | Situação | Finalidade | Quem consome |
|---|---|---|---|---|
| `POST /v1/logs` e `POST /v1/traces` (HTTP `4318` / gRPC `4317`) | `Authorization: Bearer <productToken>` | Implementado (`5fb3160`) | Receber lotes OTLP, gravar no OpenObserve, publicar `log.ingested`/`trace.ingested` no Redis e gravar `UsageFact` no Core | SDKs e agentes do cliente |
| `POST /internal/manual/upload` | `X-LhamaLog-Service-Token` (comparação em tempo constante, rejeita `Authorization`) | Implementado no worktree `LLT-292` (sem commit; código permanece parado) | Receber arquivos manuais (`.txt`, `.json`, `.csv`, `.log`), gravar no OpenObserve (`fileSource=upload`), publicar `log.ingested` e gravar `UsageFact` (**D7**) | Core (`PR #15` `POST /api/manual/upload`) ← Web |
| `GET /health` (+ gRPC `grpc.health.v1.Health`) | Nenhuma (`ADR_118`) | Implementado na `LLT-290` (`44d36b4`) | Verificação de saúde Liveness/Readiness | Orquestração / infra |
| `GET /actuator/prometheus` (porta `9464`) | Nenhuma (loopback por padrão) | Implementado (`5fb3160`, `ActuatorSecurityConfiguration.java:21-36`) | Scrape de métricas operacionais (`lhamalog_ingestion_*`, `lhamalog_queue_size`, `lhamalog_dlq_size`) | Prometheus / Grafana |

### Endpoints que o Collector **consome** no Core (alimentando o Dashboard)

| Método e Rota (no Core) | Autenticação | Situação | Finalidade para o LLT-145 |
|---|---|---|---|
| `POST /internal/usage-facts` | `X-LhamaLog-Service-Token` | Implementado (`5fb3160` ↔ Core `82e7725`); também usado no upload manual (**D7**, Decidido (Michel, 25/11/2026)) | Grava `acceptedRecordCount` e `acceptedBytes` (`LOGS`/`TRACES`), usados por `UsageMetricsAdapter` em `volumeUsedBytes` e `traces` do dashboard |
| `POST /internal/usage-reservations/**` | `X-LhamaLog-Service-Token` | Implementado (`5fb3160` ↔ Core `82e7725`) | Reserva/confirma/libera cota de ingestão |

## 3. Contratos de request e response (JSON)

### 3.1 `POST /internal/usage-facts` (Collector → Core)

Contrato em `lhamalog-core/src/main/java/br/com/lhamalog/core/usage/api/UsageFactRequest.java:12-38` e `UsageFactsController.java:28-35`. Vale tanto para ingestão OTLP quanto para o upload manual (**D7**).

**Request (`X-LhamaLog-Service-Token: <token>`, `X-Correlation-Id: <uuid>`):**
```json
{
  "usageFactId": "8f3c2a1b-4d5e-4f6a-9b0c-1234567890ab",
  "batchId": "b9f8e7d6-5c4b-3a2f-1e0d-9876543210fe",
  "tenantId": "org_2nABC123",
  "productId": "prod_checkout_01",
  "domain": "LOGS",
  "acceptedRecordIds": [
    "rec_001",
    "rec_002"
  ],
  "acceptedRecordCount": 2,
  "acceptedBytes": 1024,
  "acceptedAt": "2026-11-25T17:30:00Z",
  "schemaVersion": 1
}
```
- `domain`: `"LOGS"` ou `"TRACES"` (`UsageDomain.java:3-5`).
- `acceptedAt`: **obrigatório em UTC** (`hasUtcAcceptedAt()`, offset `0`).
- `acceptedRecordIds`: sem duplicatas, tamanho igual a `acceptedRecordCount` (`hasValidRecords()`).

**Responses:**
- `201 Created` (corpo vazio): fato registrado pela primeira vez.
- `200 OK` (corpo vazio): reenvio idempotente idêntico (`DUPLICATE`).
- `409 Conflict` (corpo vazio): mesmo `usageFactId` com conteúdo divergente (`CONFLICT`).

### 3.2 `POST /internal/manual/upload` (Core → Collector, `LLT-292`)

Conforme planejamento da `LLT-292` (`origin/LLT-290-292-planejamento` em `c2aa1fc`):
- **Content-Type:** `multipart/form-data` (máx. 100 MB de conteúdo / 101 MB no contêiner, 60 partes; cabeçalhos `X-LhamaLog-Service-Token`, `X-Correlation-Id`, campos `tenantId`, `productId`, `files`).
- **UsageFact:** após a confirmação no OpenObserve, o Collector grava `UsageFact` (`domain=LOGS`, `batchId`) em `POST /internal/usage-facts` (**D7**, Decidido (Michel, 25/11/2026)). O código do Collector permanece parado; esta pasta apenas documenta a decisão.
- **Response `202 Accepted` (ou `207`/parcial via status por arquivo no array `files[]`):**
```json
{
  "batchId": "b9f8e7d6-5c4b-3a2f-1e0d-9876543210fe",
  "files": [
    {
      "filename": "app-2026-11-25.log",
      "status": "ACCEPTED",
      "recordCount": 145,
      "bytes": 48210
    },
    {
      "filename": "duplicado.log",
      "status": "REJECTED",
      "reason": "duplicate_file"
    }
  ]
}
```
*(Demais status por arquivo previstos na `LLT-292`: `IN_FLIGHT`, `QUOTA_EXCEEDED`, `RATE_LIMITED`, `UNAVAILABLE`, `REJECTED`.)*

### 3.3 `GET /health` (`LLT-290` / `ADR_118`)

**Response `200 OK` (ou `503 Service Unavailable`):**
```json
{
  "status": "UP"
}
```

## 4. Códigos de erro

| Código HTTP | Onde ocorre | Significado |
|---|---|---|
| `400 Bad Request` | `/v1/logs`, `/v1/traces`, `/internal/manual/upload`, `/internal/usage-facts` | Payload malformado, extensão não permitida, `acceptedAt` fora de UTC, todos os registros inválidos (`InvalidPayload`) |
| `401 Unauthorized` | `/v1/*` e `/internal/**` | `productToken` ausente/revogado/expirado ou `X-LhamaLog-Service-Token` ausente/inválido ou presença indevida de `Authorization` em `/internal/**` (`UsageFactsSecurityConfiguration.java:87-106`) |
| `409 Conflict` | `/v1/*`, `/internal/manual/upload`, `/internal/usage-facts` | Arquivo já processado (`done` no dedup MD5 `LLT-290`) ou conflito de `usageFactId` |
| `413 Payload Too Large` | `/v1/*`, `/internal/manual/upload` | Lote ou arquivo acima do teto (`100 MB`, `ADR_171`) |
| `429 Too Many Requests` | `/v1/*`, `/internal/manual/upload` | Rate limit ou cota esgotada (`Retry-After` quando aplicável) |
| `503 Service Unavailable` | `/v1/*`, `/internal/manual/upload`, `/health` | OpenObserve ou Redis indisponível, dedup `IN_FLIGHT` (`Retry-After: 5`, `ADR_118`/LLT-290) ou sem plano ativo |

## 5. Origem e destino dos dados

1. **OpenObserve (`org: lhamalog`):** `OpenObserveLogsSink` envia JSON para `POST /api/lhamalog/{stream}/_json` (`lhamalog-collector/specs/001-otlp-receiver/data-model.md:122-190`), com stream por tenant (`OpenObserveStreamNames`). Campos gravados em camelCase (`tenantId`, `productId`, `severityNumber`, `severityText`, `serviceName`, `_timestamp`, `receivedAt`, `lhamalog_batch_id`, `lhamalog_record_id`) que o OpenObserve indexa em **minúsculas** (`tenantid`, `productid`, etc.). No upload manual (`LLT-292` / `ADR_173`), grava 1 documento por arquivo + `fileSource=upload`.
2. **Redis Streams (`lhamalog:stream:logs` e `lhamalog:stream:traces` + DLQs):** `PublishingLogsSink.java:88-126` e `LogIngestedPublisher.java:16-58` gravam primeiro no OpenObserve e só depois publicam referência leve `log.ingested` / `trace.ingested` (`TelemetryIngestedBody.java:12-19`), com `idempotencyId = batchId` e `metadata.correlationId`.
3. **MongoDB (somente leitura pelo Collector):** coleções `product_tokens` e `products` para autenticar token e resolver `tenantId` (`data-model.md:7-76`).
4. **Usage Facts (`Core`):** `CoreUsageFactsClient` envia `POST /internal/usage-facts` com retry via outbox durável (`PublishingLogsSink.java:97-113`), inclusive no upload manual (**D7**), garantindo consistência de `volumeUsedBytes` e `traces` no dashboard.

## 6. Como Core e Front consomem

- **Front (Web):** **nunca** chama o Collector (`ADR_141`). Quando o usuário faz upload manual (`LLT-292`), o Web chama o Core (`POST /api/manual/upload`) com Clerk JWT, e o Core encaminha para `POST /internal/manual/upload` no Collector com `X-LhamaLog-Service-Token`. No dashboard (`LLT-145`), o Web chama apenas `GET /api/dashboard/products/{id}/metrics` e `GET /api/dashboard/company/metrics` no Core.
- **Core:** consome os efeitos do Collector indiretamente lendo **OpenObserve** (`OpenObserveLogQueryAdapter`) e **MongoDB `UsageFact`** (`UsageMetricsAdapter`), além de chamar `POST /internal/manual/upload` na `LLT-292`.

## 7. Padrão de logs

Já alinhado em `lhamalog-collector/src/main/resources/application.properties:12-14` e `TelemetryIngestedPublisher.java:33-36, 91-94`:
- `X-Correlation-Id` (HTTP) / `x-correlation-id` (gRPC) lido no filtro `CorrelationId`, salvo no MDC `correlationId` e copiado para `metadata.correlationId` nas entradas do Redis Streams.
- Timestamp no fuso `America/Sao_Paulo`, nível, nome da aplicação, `[cid=%X{correlationId:-none}]`, thread, `%logger{40}.%M` (referência à função) e mensagem.

## 8. Decisões aplicadas

- **D7** (= I3 da LLT-292), Decidido (Michel, 25/11/2026): o upload manual grava `UsageFact` (`domain=LOGS`) em `POST /internal/usage-facts` após a confirmação no OpenObserve, para que o volume apareça em `volumeUsedBytes` do Dashboard LLT-145. **O código do Collector não foi alterado nesta entrega e permanece parado.**
- As métricas operacionais de fila do Collector (`lhamalog_queue_size`, `lhamalog_dlq_size` de `specs/008-collector-metrics/metricas.md:17-18`) permanecem no Grafana/Prometheus operacional (`LLT-187`) e **não** entram no dashboard do cliente no MVP (fora do escopo da LLT-145; não houve pedido de exposição nessas decisões).
