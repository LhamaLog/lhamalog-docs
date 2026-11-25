# Core (Rotas Públicas e Internas) e Notificação — Referência LLT-145

**Repositório do Core:** [`lhamalog-core`](https://github.com/LhamaLog/lhamalog-core) (branch `LLT-145-consulta-metricas-dashboard`, HEAD `82e7725`).
**Módulo Notificação:** ainda sem repositório em `org:LhamaLog` (`ADR_146` / `ADR_165`).

## 1. Resumo para a equipe

Pela `ADR_141`, o **Core é a única porta HTTP para o Web e Mobile**. Além dos dois endpoints de dashboard já implementados (`82e7725`) e dos endpoints de uso (`UsageFactsController` / `UsageReservationsController`), o Core precisa de:
- um receptor interno chamado pelo **Finder** (`POST /internal/v1/alerts/finder`, autenticado com `Authorization: Bearer <JWT>` — **D1**/**D2**);
- um receptor chamado pelo **Módulo Ocorrência** (`POST /internal/v1/occurrences/notifications`, com `X-LhamaLog-Service-Token` — **D8**/**D9**);
- um cliente Core → Ocorrência (`GET /internal/v1/occurrences/metrics` com `X-LhamaLog-Service-Token`) para o `SSID_011` somar `SeriesPoint.occurrences` (**D3**/**D4**).

## 2. Endpoints no Core e stream do módulo Notificação

| Método e Rota | Autenticação | Situação | Finalidade | Quem consome |
|---|---|---|---|---|
| `GET /api/dashboard/products/{productId}/metrics` | Clerk JWT (`Bearer`) | Implementado (`DashboardMetricsController.java:29-37`) | Métricas de produto (`LLT-222`) + eco `X-Correlation-Id` | Web (`fetchProductMetrics.ts`) / Mobile (`LLT-159`) |
| `GET /api/dashboard/company/metrics` | Clerk JWT (`Bearer`) | Implementado (`DashboardMetricsController.java:39-47`) | Métricas consolidadas da empresa (`LLT-223`) | Web (`fetchCompanyMetrics.ts`) / Mobile (`LLT-159`) |
| `POST /internal/usage-facts`, `GET /internal/usage-facts`, `GET /internal/usage-facts/current-cycle` | `X-LhamaLog-Service-Token` | Implementado (`UsageFactsController.java:20-48`, `UsageFactsSecurityConfiguration.java:26-108`) | Registrar e consultar fatos de uso (`volumeUsedBytes`, `traces`), inclusive do upload manual (**D7**) | Collector (`POST`) / uso interno |
| `POST /internal/usage-reservations/**`, `GET /internal/usage-reservations/balance` | `X-LhamaLog-Service-Token` | Implementado (`UsageReservationsController.java:23-71`) | Reservar/confirmar/liberar/estornar cota de ingestão | Collector |
| `POST /internal/v1/alerts/finder` | `Authorization: Bearer <JWT>` (**D1**, exceção decidida) | **A implementar no Core** (rota atual no Finder ainda é `/internal/v1/alertas/finder`, a atualizar — **D2**) | Receber aviso do Finder após 3 falhas ao ler OpenObserve (`DN-008-3`) | Finder (`aviso.go:31`) |
| `POST /internal/v1/occurrences/notifications` | `X-LhamaLog-Service-Token` | Decidido (Michel, 25/11/2026) (**D8**/**D9**); a implementar | Receber ocorrência `ERROR`/`WARNING` do Módulo Ocorrência (`SSID_009.1`) e publicar na stream de notificação. `INFO` não gera ocorrência nem notificação. | Módulo Ocorrência |
| *(Redis Stream Notificação)* | Rede interna / Redis ACL | A implementar (`ADR_165`) | Consumir eventos publicados pelo Core e entregar por e-mail e WebSocket | Notificação consome |

## 3. Contratos de request e response (JSON)

### 3.1 `GET /api/dashboard/products/{productId}/metrics` (Web → Core, implementado em `82e7725`)

**Headers:** `Authorization: Bearer <clerk_jwt>`, `X-Correlation-Id: <uuid>`.
**Query params:** `from` (ISO-8601 UTC), `to` (ISO-8601 UTC), `severities` (opcional CSV `ERROR,WARNING,INFO`).

**Response `200 OK` (`DashboardMetricsResponses.java:14-43`):**
```json
{
  "productId": "prod_checkout_01",
  "from": "2026-11-24T17:00:00Z",
  "to": "2026-11-25T17:00:00Z",
  "dadosConsolidadosAte": "2026-11-25T17:00:00Z",
  "retentionDays": 30,
  "volumeIngestaoBytes": 107374182400,
  "totals": {
    "logs": 1200,
    "error": 14,
    "warning": 8,
    "info": 1178,
    "traces": 450,
    "volumeUsedBytes": 184320
  },
  "series": {
    "bucket": "hour",
    "points": [
      {
        "start": "2026-11-25T16:00:00Z",
        "end": "2026-11-25T17:00:00Z",
        "error": 14,
        "warning": 8
      }
    ]
  },
  "serviceRanking": [
    {
      "serviceName": "payment-service",
      "error": 14
    }
  ]
}
```
*(Nota: quando o Módulo Ocorrência estiver integrado pós-`LLT-104`, cada item de `series.points` ganhará `"occurrences": <long>`, somado pelo `SSID_011` a partir de `GET /internal/v1/occurrences/metrics` — **D3**/**D4**.)*

### 3.2 `GET /api/dashboard/company/metrics` (Web → Core, implementado em `82e7725`)

**Query params:** `from`, `to`, `productIds` (opcional CSV), `severities` (opcional CSV).

**Response `200 OK` (`DashboardMetricsResponses.java:46-63`):**
```json
{
  "from": "2026-11-24T17:00:00Z",
  "to": "2026-11-25T17:00:00Z",
  "dadosConsolidadosAte": "2026-11-25T17:00:00Z",
  "retentionDays": 30,
  "totals": {
    "logs": 1200,
    "error": 14,
    "warning": 8,
    "productsMonitored": 1
  },
  "seriesByProduct": [
    {
      "productId": "prod_checkout_01",
      "productName": "Checkout API",
      "bucket": "hour",
      "points": [
        {
          "start": "2026-11-25T16:00:00Z",
          "end": "2026-11-25T17:00:00Z",
          "error": 14,
          "warning": 8
        }
      ]
    }
  ],
  "products": [
    {
      "productId": "prod_checkout_01",
      "productName": "Checkout API",
      "logs": 1200,
      "error": 14,
      "warning": 8
    }
  ]
}
```

### 3.3 `POST /internal/v1/occurrences/notifications` (**D8**/**D9**, Decidido (Michel, 25/11/2026), `SSID_009.1`)

**Headers:** `X-LhamaLog-Service-Token: <token>`, `X-Correlation-Id: <uuid>`.

**Request (Ocorrência → Core):**
```json
{
  "occurrenceId": "occ_01JXYZ",
  "tenantId": "org_2nABC123",
  "productId": "prod_checkout_01",
  "type": "ERROR",
  "severity": "CRITICAL",
  "recurrent": true,
  "suggestionId": null,
  "occurredAt": "2026-11-25T16:45:10Z"
}
```
- `type` aceito: `ERROR` ou `WARNING`. `INFO` não gera ocorrência nem notificação (**D9**): o Core deve recusar (`400`/`422`) ou ignorar um payload com `type=INFO`.

**Response `202 Accepted`:**
```json
{
  "accepted": true,
  "occurrenceId": "occ_01JXYZ"
}
```

### 3.4 `POST /internal/v1/alerts/finder` (**D1**/**D2**, Decidido (Michel, 25/11/2026))

Ver contrato em [endpoints-finder.md](endpoints-finder.md) (§ 3.2). Autenticação: `Authorization: Bearer <JWT>` (exceção decidida; **não** reutilizar o filtro de `UsageFactsSecurityConfiguration` que rejeita `Authorization`).

## 4. Códigos de erro

- **Bordas `/api/dashboard/**`:** `400` (`invalid_filter` quando `from >= to`, severidade inválida ou período > `min(30, retentionDays)`), `401` (Clerk JWT inválido/ausente), `403` (sem tenant ativo — revoga sessão Clerk, `SecurityConfig.java:51-52`), `404` (produto inexistente, de outro tenant ou `MEMBRO` sem `AcessoProduto` — `LLT-158`/`LLT-171`), `5xx` (falha OpenObserve sem corromper agregados Mongo).
- **Internos com Service Token** (`/internal/usage-facts/**`, `/internal/usage-reservations/**`, `/internal/v1/occurrences/notifications`): `400` (payload inválido, inclusive `type=INFO` em notifications — **D9**), `401` (`X-LhamaLog-Service-Token` inválido/ausente ou presença de `Authorization`), `409` (conflito de idempotência).
- **Interno chamado pelo Finder** (`/internal/v1/alerts/finder`): `401` se o JWT estiver ausente/inválido (**D1**); não rejeitar só pela presença de `Authorization`.

## 5. Origem dos dados no Core

1. **MongoDB:** `DashboardLogHourlyAggregateDocument`, `DashboardAggregationWatermarkDocument` (job `SSID_011` `DashboardAggregationJob.java` com cron `lhamalog.dashboard.aggregation.cron:0 0 * * * *`), `UsageFactDocument` (incluindo upload manual — **D7**), `PlanSubscription`, `Product`, `AcessoProduto`.
2. **OpenObserve (`org: lhamalog`):** `OpenObserveLogQueryAdapter.java` consulta `POST /api/{org}/_search` no stream do tenant (`OpenObserveStreamNames`) com SQL agrupado por `histogram(_timestamp, '1 hour')`, `severitynumber`, `severitytext` e `servicename`.
3. **Módulo Ocorrência (pós-LLT-104):** `GET /internal/v1/occurrences/metrics` e `GET /internal/v1/occurrences` com `X-LhamaLog-Service-Token`. O `SSID_011` agrega logs no Core e soma as ocorrências pela rota `metrics` (**D3**/**D4**).

## 6. Padrão de logs

Já implementado no Core (`application.properties:35-37`, `CorrelationIdFilter.java:11-26`):
- Lê `X-Correlation-Id` (ou gera UUID), grava no MDC `correlationId` e devolve na resposta HTTP.
- Formato com timestamp `America/Sao_Paulo`, nível, `[cid=%X{correlationId:-none}]`, `%logger{40}.%M` e mensagem `event=...`.

## 7. Decisões aplicadas e portão restante

- **D1/D2**, Decidido (Michel, 25/11/2026): implementar `POST /internal/v1/alerts/finder` no Core com `Authorization: Bearer <JWT>` (exceção em relação a `/internal/usage-facts`).
- **D3/D4**, Decidido (Michel, 25/11/2026): o Core consulta `GET /internal/v1/occurrences/metrics` com `X-LhamaLog-Service-Token`; o `SSID_011` agrega logs e soma as ocorrências por essa rota.
- **D7**, Decidido (Michel, 25/11/2026): o upload manual grava `UsageFact` (documentado; código do Collector permanece parado).
- **D8/D9**, Decidido (Michel, 25/11/2026): `POST /internal/v1/occurrences/notifications` no Core, com `X-LhamaLog-Service-Token`; `INFO` não gera ocorrência nem notificação.
- Ainda em aberto: o portão humano **T029** do Core (revisão do Felipe sobre Clerk/papéis/`AcessoProduto` na spec 011).
