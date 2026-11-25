# Módulo Varredura — Endpoints, Streams e Papel no Dashboard (LLT-145)

**Repositório:** ainda não criado em `org:LhamaLog` (estado em 25/11/2026).
**Fontes de referência:** `ADR_057`, `ADR_061`, `ADR_146 v2`, `ADR_173`, `SSID_005.1`, `SSID_006.1`, `lhamalog-collector/specs/002-tenant-product-logs/contracts/log-ingested-stream.md:71-75`, `lhamalog-finder/internal/adapter/out/finalizacao/finalizar.go:16-75`, `Modelo de Classes LhamaLog.xlsx` (`Varredura`, `Arquivo Varredura`).

## 1. Resumo para a equipe

**D4**, Decidido (Michel, 25/11/2026): no **MVP do Dashboard LLT-145** (`spec 011` do Core e `spec 007` do Web), **nenhuma métrica do dashboard consulta a Varredura por HTTP**. A Varredura fica **fora do dashboard no MVP**. O papel principal da Varredura na arquitetura é **assíncrono via Redis Streams**:
1. Consumir `log.ingested` / `trace.ingested` publicados pelo Collector (`lhamalog:stream:logs` / `lhamalog:stream:traces`);
2. Organizar e priorizar lotes por Produto (`ADR_057`, gatilho agendado `SSID_006.1` ou contínuo por tamanho padrão 500 `SSID_005.1`);
3. Realizar varredura de dados sensíveis e validação de prompt-injection (`Collector` `spec 002` `research.md:104-105`);
4. Publicar `log.checked` / `trace.checked` **com `execId`** (**D4**) para o **Finder** consumir;
5. Receber do Finder a confirmação de conclusão de cada arquivo vinculado a um `execId` (`ADR_061`, `POST /internal/v1/scans/completions` — **D2**, autenticado com `Authorization: Bearer <JWT>` — **D1**) e fechar a execução (`COMPLETED` / `COMPLETED_WITH_ERROR`), avisando o Core.

## 2. Endpoints necessários e contratos de stream

| Interface | Método / Canal | Autenticação | Situação | Finalidade | Quem consome / chama |
|---|---|---|---|---|---|
| HTTP | `GET /health` | Nenhuma (`ADR_118`) | A implementar | Saúde do serviço | Orquestração / infra |
| HTTP | `POST /internal/v1/scans/completions` | `Authorization: Bearer <JWT>` (**D1**, exceção decidida) | A implementar (cliente pronto em `finalizar.go:36`; rota atual no código ainda é `/internal/v1/execucoes/conclusoes`, a atualizar — **D2**) | Receber conclusão de arquivo/lote pelo Finder e fechar `Varredura` (`ADR_061`) | Finder (`finalizar.go:36-57`) |
| HTTP | `GET /internal/v1/scans/summary` | — | **Fora do dashboard no MVP** (**D4**, Decidido (Michel, 25/11/2026)) | Não entra nesta entrega | — |
| Redis Stream (entrada) | `lhamalog:stream:logs` (`log.ingested`) e `lhamalog:stream:traces` (`trace.ingested`) | Rede interna / Redis ACL | Já publicado pelo Collector (`5fb3160`) | Receber referências de lotes no OpenObserve | Varredura consome |
| Redis Stream (saída) | `log.checked` / `trace.checked` **com `execId`** (**D4**) | Rede interna / Redis ACL | Decidido (Michel, 25/11/2026) (**D4**); contrato a implementar no módulo | Entregar lote verificado com `execId` para o Finder | Finder consome |

## 3. Contratos de request, response e mensagem (JSON)

### 3.1 `POST /internal/v1/scans/completions` (Finder → Varredura, payload real em `finalizar.go:16-57`)

**Headers:** `Authorization: Bearer <JWT>` (**D1**), `X-Correlation-Id: <uuid>` (**D5/D6**), `Content-Type: application/json`.

**Request:**
```json
{
  "tenantId": "org_2nABC123",
  "productId": "prod_checkout_01",
  "batchId": "b9f8e7d6-5c4b-3a2f-1e0d-9876543210fe",
  "execId": "V-44112233"
}
```

**Response `200 OK` ou `201 Created` (`finalizar.go:22-26,49-55`):**
```json
{
  "aceito": true,
  "tenantId": "org_2nABC123",
  "productId": "prod_checkout_01",
  "batchId": "b9f8e7d6-5c4b-3a2f-1e0d-9876543210fe",
  "execId": "V-44112233",
  "execucaoFinalizada": false
}
```
- `execucaoFinalizada: false` confirma que o arquivo/lote foi concluído, mas ainda restam outros itens em processamento na execução `execId` (`finalizar.go:52`).
- `execucaoFinalizada: true` indica que todos os itens terminaram e a Varredura fechou a execução (`COMPLETED` / `COMPLETED_WITH_ERROR`, `SSID_005.1`).

### 3.2 Contrato do evento Redis `log.checked` (**D4**, Decidido (Michel, 25/11/2026): leva `execId`)

Espelhando `TelemetryIngestedBody` (`lhamalog-collector/.../TelemetryIngestedBody.java:12-19`) e `ADR_146 v2`, com `execId` exigido pelo Finder (`spec 006` `DN-006-1b B`, `finalizar.go:69`):

```json
{
  "event": "log.checked",
  "origin": "varredura",
  "schemaVersion": "1",
  "publishedAt": "2026-11-25T17:11:05Z",
  "idempotencyId": "b9f8e7d6-5c4b-3a2f-1e0d-9876543210fe:V-44112233",
  "metadata": {
    "tenantId": "org_2nABC123",
    "productId": "prod_checkout_01",
    "correlationId": "6b9f1d2e-9a8b-4c7d-8e6f-1234567890ab",
    "execId": "V-44112233"
  },
  "body": {
    "signal": "LOGS",
    "productId": "prod_checkout_01",
    "execId": "V-44112233",
    "openobserve": {
      "organization": "lhamalog",
      "stream": "logs_org_2nabc123_a1b2c3d4",
      "batchId": "b9f8e7d6-5c4b-3a2f-1e0d-9876543210fe",
      "recordId": null,
      "minTimestampMicros": 1764090000000000,
      "maxTimestampMicros": 1764090600000000
    },
    "serviceNames": ["payment-service"],
    "priority": "HIGH",
    "criticality": "ERROR",
    "maxSeverityNumber": 17,
    "severityCounts": {"ERROR": 14, "WARNING": 8, "INFO": 1178},
    "recordCount": 1200,
    "bytes": 184320,
    "receivedAt": "2026-11-25T17:10:00Z",
    "sensitiveDataCheck": "PASSED",
    "promptInjectionCheck": "PASSED"
  }
}
```
*(Atenção: conforme `ADR_173`, uploads manuais da `LLT-292` no MVP vão direto para `lhamalog:stream:logs` e OpenObserve sem passar por `FilaOrdenada`.)*

## 4. Códigos de erro

| Código HTTP | Significado | Observação |
|---|---|---|
| `400 Bad Request` | Campos obrigatórios ausentes (`tenantId`, `productId`, `batchId`, `execId`) | — |
| `401 Unauthorized` | JWT ausente/inválido na rota que o Finder chama (**D1**) | — |
| `404 Not Found` | `execId` ou `batchId` não pertence ao `tenantId`/`productId` informado | Isolamento `LLT-158` |
| `409 Conflict` | Execução já encerrada em estado incompatível | — |
| `503 Service Unavailable` | MongoDB ou Redis indisponível | Finder trata como `ErrConclusao` |

## 5. Origem dos dados

- **Redis Streams:** lê `log.ingested` / `trace.ingested` (`lhamalog:stream:logs` e `lhamalog:stream:traces`); publica `log.checked` / `trace.checked` **com `execId`** após análise de segurança (**D4**).
- **MongoDB:** persiste `Varredura` (`id`, `company_id`, `product_id`, `status`, contadores, timestamps), `ArquivoVarredura` (`status`, `order`, `attempts`, `error`) e lock distribuído ShedLock (`SSID_006.1`).
- **OpenObserve:** consultado apenas se a checagem de dados sensíveis/prompt-injection precisar inspecionar o corpo do lote por `lhamalog_batch_id` (a referência já vem em `body.openobserve`).

## 6. Como Core e Front consomem

- **Front (Web):** **nunca** chama a Varredura (`ADR_141`). No dashboard LLT-145 atual (`9adb018`), não há card ou filtro de execução de Varredura. **D4**, Decidido (Michel, 25/11/2026): a Varredura permanece fora do dashboard no MVP.
- **Core:** não consulta a Varredura para montar os dois endpoints do dashboard (`/api/dashboard/products/{id}/metrics` e `/api/dashboard/company/metrics`). Quando a Varredura fechar uma execução (`ADR_061`), emite evento para o Core notificar o usuário (via WebSocket/Notificação).

## 7. Padrão de logs

Mesmo padrão dos demais serviços Spring Boot:
- Ler/propagar `X-Correlation-Id` em HTTP e `metadata.correlationId` nos eventos Redis Streams (`log.ingested` → `log.checked`).
- Logar com `[cid=%X{correlationId:-none}]`, referência à função (`%logger{40}.%M`), mensagem estruturada e timestamp em `America/Sao_Paulo`.

## 8. Decisões aplicadas

- **D4**, Decidido (Michel, 25/11/2026): o Dashboard LLT-145 continua sem exibir status/progresso de Varredura no MVP; o evento `log.checked` / `trace.checked` leva `execId`.
- **D1/D2**, Decidido (Michel, 25/11/2026): `POST /internal/v1/scans/completions` (inglês) é autenticado com `Authorization: Bearer <JWT>` (exceção decidida para a rota que o Finder chama).
