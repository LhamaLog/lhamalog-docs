# Módulo Ocorrência — Endpoints para o Dashboard (LLT-145 + LLT-104)

**Repositório:** ainda não criado em `org:LhamaLog` (estado em 25/11/2026).
**Fontes de referência:** `ADR_062`, `ADR_101`, `ADR_162`, `ADR_170`, `SSID_009.1`, `SSID_011`, Jira (`LLT-104`, `LLT-145`, `LLT-222`, `LLT-223`, `LLT-158`, `LLT-171`), `lhamalog-finder/specs/009-publicar-evento-ocorrencia/contracts/proposta-dn-009-2.openapi.yaml` e `lhamalog-core/specs/011-consulta-metricas-dashboard/`.

## 1. Resumo para a equipe

O **Módulo Ocorrência** é o módulo que hoje **bloqueia** a entrega completa do gráfico e dos contadores de **Ocorrências** no Dashboard (`ProductDashboardPage.tsx:336-342` exibe *"não implementado ainda"*). Ele tem duas responsabilidades HTTP claras:
1. **Ingerir achados do Finder (`DN-009-2`):** consultar estado de achado único e receber `ResumoAnalise` para criar/atualizar entidades `Ocorrencia` no MongoDB, calculando gravidade (`ADR_062`) e notificando o Core (`SSID_009.1`). Essas rotas usam `Authorization: Bearer <JWT>` (**D1**, exceção decidida) e os caminhos em inglês (**D2**).
2. **Servir consultas e agregações para o Core (`ADR_101`, `ADR_162`, `LLT-104`, `LLT-222`):** `GET /internal/v1/occurrences/metrics`, `GET /internal/v1/occurrences` e `GET /internal/v1/occurrences/{occurrenceId}` (**D3**, Decidido (Michel, 25/11/2026)), autenticadas com `X-LhamaLog-Service-Token`. O Core (`SSID_011`) agrega logs e soma as ocorrências pela rota `metrics` (**D4**). `INFO` entra só nos contadores, sem gerar `Ocorrencia` nem notificação (**D9**).

## 2. Endpoints necessários

| Método e Rota | Autenticação | Situação | Finalidade | Quem consome |
|---|---|---|---|---|
| `GET /health` | Nenhuma (`ADR_118`) | A implementar | Saúde do serviço | Orquestração / infra |
| `POST /internal/v1/occurrences/lookup` | `Authorization: Bearer <JWT>` (**D1**, exceção decidida para rotas que o Finder chama) | A implementar (contrato `DN-009-2` pronto no Finder; rota atual no código Go ainda é `/internal/v1/ocorrencias/consultas`, a atualizar — **D2**) | Consultar estado acumulado de um achado antes do `ResumoAnalise` | Finder (`cliente.go:21,70-105`) |
| `POST /internal/v1/analysis-summaries` | `Authorization: Bearer <JWT>` (**D1**, exceção decidida) | A implementar (contrato `DN-009-2` pronto no Finder; rota atual no código Go ainda é `/internal/v1/resumos-analise`, a atualizar — **D2**) | Persistir `ResumoAnalise` e criar/atualizar `Ocorrencia` (com idempotência por `batchId`/`execId`) apenas para `ERROR`/`WARNING` (**D9**) | Finder (`cliente.go:22,131-169`) |
| `GET /internal/v1/occurrences/metrics` | `X-LhamaLog-Service-Token` | Decidido (Michel, 25/11/2026) (**D3**/**D4**); a implementar após a LLT-104 | Retornar contagens de ocorrências agrupadas por `hour`/`day`, `productId`, `severity` e `serviceName` para `SeriesPoint.occurrences`; o `SSID_011` no Core soma por esta rota | Core (`DashboardMetricsService` / job `SSID_011`) |
| `GET /internal/v1/occurrences` | `X-LhamaLog-Service-Token` | Decidido (Michel, 25/11/2026) (**D3**); a implementar após a LLT-104 | Consulta paginada nos 3 níveis (`ADR_101`: produto, lote, arquivo) e filtros empresariais (`ADR_162`: `productIds`, período, tipo, status, busca) | Core (`LLT-104` / `LLT-222`) → Web |
| `GET /internal/v1/occurrences/{occurrenceId}` | `X-LhamaLog-Service-Token` | Decidido (Michel, 25/11/2026) (**D3**); a implementar após a LLT-104 | Detalhe completo de uma `Ocorrencia` (achados, linhas, `traceId`, `recorrente`, revisão) | Core (`LLT-104`) → Web |

### Endpoint que o Módulo Ocorrência **consome** no Core

| Método e Rota (no Core) | Autenticação | Situação | Finalidade |
|---|---|---|---|
| `POST /internal/v1/occurrences/notifications` | `X-LhamaLog-Service-Token` | Decidido (Michel, 25/11/2026) (**D8**/**D9**); a implementar | Enviar ocorrência `ERROR`/`WARNING` (e `suggestionId` quando houver) para o Core publicar na stream de notificação (`SSID_009.1`). `INFO` não é enviado. |

## 3. Contratos de request e response (JSON)

### 3.1 `POST /internal/v1/occurrences/lookup` (Finder → Ocorrência, payload real em `cliente.go:70-129`)

**Headers:** `Authorization: Bearer <JWT>` (**D1**), `X-Correlation-Id: <uuid>` (**D5/D6**), `Content-Type: application/json`.

**Request:**
```json
{
  "tenantId": "org_2nABC123",
  "productId": "prod_checkout_01",
  "tipo": "ERROR",
  "assinatura": "ERROR|connection refused to payment-gateway|payment-service|pod-7f8b"
}
```
*(Valores válidos de `tipo` conforme `ADR_170` e `domain/classificacao.go`: `"ERROR"`, `"WARNING"`, `"INFO"`.)*

**Response `200 OK` (achado existente):**
```json
{
  "estado": {
    "contagemAcumulada": 14,
    "primeiraOcorrencia": "2026-11-20T12:15:00Z",
    "ultimaOcorrencia": "2026-11-25T16:45:10Z",
    "status": "ABERTA",
    "revisao": "rev_019"
  }
}
```
- `status` aceito pelo Finder (`cliente.go:118-120`): `"ABERTA"`, `"EM_ANALISE"`, `"FECHADA"`.
- `primeiraOcorrencia` e `ultimaOcorrencia` **devem** terminar em `"Z"` (`cliente.go:125`).
- Quando não existe ocorrência prévia, retornar:
```json
{
  "estado": null
}
```

### 3.2 `POST /internal/v1/analysis-summaries` (Finder → Ocorrência, payload real em `serializar_resumo.go:11-49` e `cliente.go:145-169`)

**Headers:** `Authorization: Bearer <JWT>` (**D1**), `X-Correlation-Id: <uuid>` (**D5/D6**).

**Request:**
```json
{
  "batchId": "b9f8e7d6-5c4b-3a2f-1e0d-9876543210fe",
  "execId": "V-44112233",
  "tenantId": "org_2nABC123",
  "productId": "prod_checkout_01",
  "versaoRegras": "rules-v1.4.0+cat-2026.11",
  "versaoCatalogo": "cat-2026.11",
  "contadores": {
    "linhasProcessadas": 1200,
    "erros": 14,
    "warnings": 8,
    "informacao": 1178,
    "dadosSensiveisMascarados": 3
  },
  "achados": [
    {
      "tipo": "ERROR",
      "assinatura": "ERROR|connection refused to payment-gateway|payment-service|pod-7f8b",
      "hostName": "pod-7f8b",
      "contagem": 14,
      "primeiraOcorrencia": "2026-11-25T16:40:00Z",
      "ultimaOcorrencia": "2026-11-25T16:45:10Z",
      "recorrente": true,
      "linhas": [
        "2026-11-25T16:45:10Z ERROR connection refused to payment-gateway"
      ],
      "revisaoConsultada": "rev_019",
      "titulo": "Falha de conexão com gateway de pagamento",
      "resumo": "14 erros de conexão recusada no serviço payment-service.",
      "numeroLinha": 412,
      "camposExtraido": {
        "service.name": "payment-service"
      },
      "dadosSensiveis": true,
      "traceId": "4bf92f3577b34da6a3ce929d0e0e4736",
      "correlationId": "6b9f1d2e-9a8b-4c7d-8e6f-1234567890ab",
      "moduloId": "payment-service"
    }
  ]
}
```
*(Nota: `execId` é omitido pelo Finder enquanto consome `log.ingested` v1; nesse caso, `recibo.execId` na resposta deve ser `null` ou omitido conforme `cliente.go:158-161`. Achados `INFO` entram só em `contadores.informacao` e **não** geram `Ocorrencia` nem notificação — **D9**.)*

**Response `201 Created` (novo) ou `200 OK` (reenvio idempotente, `repeticao: true`):**
```json
{
  "aceito": true,
  "reciboId": "rcp_991188",
  "tenantId": "org_2nABC123",
  "productId": "prod_checkout_01",
  "batchId": "b9f8e7d6-5c4b-3a2f-1e0d-9876543210fe",
  "execId": "V-44112233",
  "repeticao": false
}
```
*(Regra estrita do Finder em `cliente.go:155`: `*recibo.Repeticao == (resp.StatusCode == 200)`.)*

### 3.3 `GET /internal/v1/occurrences/metrics` (**D3**/**D4**, Decidido (Michel, 25/11/2026))

Endpoint consumido pelo Core para preencher `SeriesPoint.occurrences` e para o `SSID_011` somar as ocorrências, mantendo paridade `LLT-222`.

**Headers:** `X-LhamaLog-Service-Token: <token>`, `X-Correlation-Id: <uuid>`.

**Query params:**
`tenantId` (obrigatório), `productIds` (CSV obrigatório), `from` (ISO-8601 UTC), `to` (ISO-8601 UTC), `bucket` (`hour` | `day`, padrão seguindo Core: `hour` se ≤ 48h senão `day`), `severities` (opcional CSV `ERROR,WARNING`).

**Response `200 OK`:**
```json
{
  "tenantId": "org_2nABC123",
  "from": "2026-11-24T17:00:00Z",
  "to": "2026-11-25T17:00:00Z",
  "bucket": "hour",
  "totals": {
    "occurrences": 22,
    "error": 14,
    "warning": 8
  },
  "byProduct": [
    {
      "productId": "prod_checkout_01",
      "occurrences": 22,
      "error": 14,
      "warning": 8,
      "points": [
        {
          "start": "2026-11-25T16:00:00Z",
          "end": "2026-11-25T17:00:00Z",
          "occurrences": 22,
          "error": 14,
          "warning": 8
        }
      ]
    }
  ]
}
```

### 3.4 `GET /internal/v1/occurrences` (**D3**, Decidido (Michel, 25/11/2026), `ADR_101`, `ADR_162`)

**Headers:** `X-LhamaLog-Service-Token: <token>`, `X-Correlation-Id: <uuid>`.

**Query params:** `tenantId` (obrigatório), `productIds` (CSV), `batchId` (nível lote `ADR_101`), `fileId` (nível arquivo `ADR_101`), `from`, `to`, `severities` (`ERROR,WARNING`), `status` (`OPEN,IN_ANALYSIS,CLOSED`), `search` (`termoBusca` `ADR_162`), `limit` (1..100), `cursor`.

**Response `200 OK`:**
```json
{
  "items": [
    {
      "occurrenceId": "occ_01JXYZ",
      "tenantId": "org_2nABC123",
      "productId": "prod_checkout_01",
      "batchId": "b9f8e7d6-5c4b-3a2f-1e0d-9876543210fe",
      "type": "ERROR",
      "severity": "CRITICAL",
      "status": "OPEN",
      "recurrent": true,
      "count": 14,
      "title": "Falha de conexão com gateway de pagamento",
      "serviceName": "payment-service",
      "firstSeenAt": "2026-11-25T16:40:00Z",
      "lastSeenAt": "2026-11-25T16:45:10Z"
    }
  ],
  "totalMatching": 22,
  "nextCursor": null
}
```

## 4. Códigos de erro

| Código HTTP | Significado | Observação |
|---|---|---|
| `400 Bad Request` | Parâmetros inválidos (`from >= to`, `severities` fora de `ERROR\|WARNING\|INFO`, JSON inválido) | Retornar código estruturado (ex.: `invalid_filter`) |
| `401 Unauthorized` | Nas rotas do Finder: JWT ausente/inválido. Nas rotas do Core: `X-LhamaLog-Service-Token` ausente/inválido ou cabeçalho `Authorization` presente | **D1**: as duas cadeias convivem no mesmo serviço |
| `404 Not Found` | `occurrenceId` inexistente ou pertencente a outro `tenantId` | Isolamento `LLT-158` |
| `409 Conflict` | Conflito de revisão (`{"codigo": "REVISAO_DESATUALIZADA"}`) ou entrega simultânea (`{"codigo": "ENTREGA_EM_ANDAMENTO"}` + `Retry-After`) no `POST /internal/v1/analysis-summaries` | Exigido por `cliente.go:207-220` |
| `422 Unprocessable Entity` | Payload semanticamente inválido (ex.: `contadores` negativos, `ultimaOcorrencia < primeiraOcorrencia`) | `cliente.go:222-223` |
| `429` / `503` + `Retry-After` | Sobrecarga ou MongoDB indisponível | Finder agenda backoff com base no `Retry-After` (`cliente.go:221-240`) |

## 5. Origem dos dados

- **Entrada:** `ResumoAnalise` e `AchadoAnalise` enviados via HTTP pelo Finder (que por sua vez leu `lhamalog:stream:logs` e OpenObserve org `lhamalog`).
- **Armazenamento próprio:** coleção MongoDB `occurrences` (e recibos de idempotência por `batchId` / `execId`), isolados por `tenantId` e `productId`. Somente `ERROR` e `WARNING` viram documentos de `Ocorrencia` (**D9**).
- **Metadados de criticidade:** lê criticidade do módulo/produto (`ADR_062`, `products`) para calcular a gravidade (`critico`, `alto`, etc.).

## 6. Como Core e Front consomem

- **Front (Web):** **nunca** chama o Módulo Ocorrência diretamente (`ADR_141`). No dashboard LLT-145, o Web já lê `SeriesPoint.occurrences` opcionalmente (`parseDashboardMetrics.ts:57-69`); enquanto não houver dados do Módulo Ocorrência, exibe *"não implementado ainda"* (`ProductDashboardPage.tsx:336-342`).
- **Core:** após `LLT-104`, o Core (`DashboardMetricsService` e o job `SSID_011`) chama `GET /internal/v1/occurrences/metrics` com `X-LhamaLog-Service-Token`, filtrando estritamente pelos `productIds` já autorizados via `AcessoProduto` (`LLT-171`) e `tenantId` do Clerk JWT (`LLT-158`). O `SSID_011` agrega logs no Core e **soma as ocorrências por essa rota** (**D4**), garantindo que o total exibido no gráfico bata com a futura listagem `/api/occurrences` (servida pelo Core a partir de `GET /internal/v1/occurrences`).

## 7. Padrão de logs

Mesmo padrão Spring Boot / Go do projeto:
- Exigir e propagar `X-Correlation-Id` (e logar `[cid=<id>]`), registrar referência à função (`%logger{40}.%M`), mensagem estruturada (`event=occurrences.* | ...`) e timestamp em `America/Sao_Paulo` (`yyyy-MM-dd'T'HH:mm:ss.SSSXXX`).
- Nunca logar tokens ou conteúdo completo de `linhas` com dados não mascarados.

## 8. Decisões aplicadas

- **D1/D2**, Decidido (Michel, 25/11/2026): as rotas que o Finder chama ficam em inglês (`/internal/v1/occurrences/lookup`, `/internal/v1/analysis-summaries`) e autenticadas com `Authorization: Bearer <JWT>`. As rotas novas entre Core e Ocorrência usam `X-LhamaLog-Service-Token`.
- **D3**, Decidido (Michel, 25/11/2026): aprovadas `GET /internal/v1/occurrences/metrics`, `GET /internal/v1/occurrences` e `GET /internal/v1/occurrences/{occurrenceId}`.
- **D4**, Decidido (Michel, 25/11/2026): o `SSID_011` no Core continua agregando logs e soma as ocorrências via `/internal/v1/occurrences/metrics`.
- **D9**, Decidido (Michel, 25/11/2026): achados `INFO` não geram `Ocorrencia` nem notificação (`SSID_009.1`); entram apenas nos contadores de `ResumoAnalise` e nos gráficos de logs do dashboard.
