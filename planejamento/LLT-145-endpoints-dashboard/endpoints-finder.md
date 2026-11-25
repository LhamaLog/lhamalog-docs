# Módulo Finder — Endpoints e Papel no Dashboard (LLT-145)

**Repositório:** [`lhamalog-finder`](https://github.com/LhamaLog/lhamalog-finder)
**Branch inspecionada:** `Development` (`693be4f`)

## 1. Resumo para a equipe

O **Finder é um worker em Go**, sem API HTTP de consulta para Core ou Web (`specs/008-agrupar-logs-ocorrencia`, `specs/009-publicar-evento-ocorrencia`). Ele:
1. Consome referências de lote na stream Redis `lhamalog:stream:logs` (`log.ingested` v1) — e futuramente `log.checked` da Varredura, com `execId` (**D4**);
2. Busca os logs no **OpenObserve** (`POST /api/{organization}/_search` por `lhamalog_batch_id` + faixa `_timestamp` + deduplicação por `lhamalog_record_id`, `LLT-270`);
3. Classifica e mascara os registros (`ERROR`, `WARNING`, `INFO` conforme `ADR_170`);
4. Envia **achados e resumos** (`AchadoAnalise` e `ResumoAnalise`, `ADR_062`) para o **Módulo Ocorrência** via HTTP;
5. Emite alerta ao **Core** após 3 falhas no OpenObserve (`DN-008-3`, **sem DLQ** no `log.ingested`) e finaliza execução na **Varredura** quando houver `execId` (`ADR_061`).

**O Finder não deve implementar endpoints HTTP de consulta para o Dashboard.** O trabalho necessário no Finder é alinhar as chamadas HTTP **de saída** às decisões D1, D2 e D5/D6 (Decidido (Michel, 25/11/2026)):
- **D1:** o Finder **mantém** `Authorization: Bearer <JWT>` (não troca para `X-LhamaLog-Service-Token`).
- **D2:** as rotas passam para inglês (o código `693be4f` ainda usa português e precisa ser atualizado).
- **D5/D6:** o Finder propaga `X-Correlation-Id` e loga no fuso `America/Sao_Paulo` com referência à função.

## 2. Endpoints no Finder (entrada e saída)

### 2.1 Entrada HTTP (exposta pelo Finder)

| Método e Rota | Autenticação | Situação | Finalidade | Quem consome |
|---|---|---|---|---|
| `GET /health` | Nenhuma (`ADR_118`) | Implementado (`internal/adapter/in/http/health.go:7-14`) | Liveness/Readiness do worker Go | Orquestração / infra |

### 2.2 Saída HTTP (clientes já implementados no Finder; rotas alvo em inglês — D2)

| Destino | Método e Rota alvo (D2) | Autenticação (D1) | Situação |
|---|---|---|---|
| **Módulo Ocorrência** | `POST /internal/v1/occurrences/lookup` | `Authorization: Bearer <JWT>` (**D1**, exceção decidida) | Servidor não existe ainda. No código atual (`cliente.go:21`) a rota ainda é `/internal/v1/ocorrencias/consultas` — atualizar para inglês (**D2**). |
| **Módulo Ocorrência** | `POST /internal/v1/analysis-summaries` | `Authorization: Bearer <JWT>` (**D1**, exceção decidida) | Servidor não existe ainda. No código atual (`cliente.go:22`) a rota ainda é `/internal/v1/resumos-analise` — atualizar para inglês (**D2**). |
| **Varredura** | `POST /internal/v1/scans/completions` | `Authorization: Bearer <JWT>` (**D1**, exceção decidida) | Servidor não existe ainda; hoje o Finder pula essa chamada porque `log.ingested` v1 não tem `execId` (`finalizar.go:69-75`). No código atual (`finalizar.go:36`) a rota ainda é `/internal/v1/execucoes/conclusoes` — atualizar para inglês (**D2**). Passa a ser usada quando `log.checked` trouxer `execId` (**D4**). |
| **Core** | `POST /internal/v1/alerts/finder` | `Authorization: Bearer <JWT>` (**D1**, exceção decidida) | Endpoint não existe no Core (`82e7725`). No código atual (`aviso.go:31`) a rota ainda é `/internal/v1/alertas/finder` — atualizar para inglês (**D2**). |

## 3. Contratos de request e response (JSON)

### 3.1 `GET /health` (Inbound no Finder)

Fonte: `internal/adapter/in/http/health.go:7-14`:
```json
{
  "status": "UP"
}
```

### 3.2 `POST /internal/v1/alerts/finder` (Finder → Core)

Fonte do payload: `internal/adapter/out/core/aviso.go:12-50`. Rota alvo em inglês (**D2**). Autenticação: `Authorization: Bearer <JWT>` + `X-Correlation-Id` (**D1**, **D5/D6**).

**Request:**
```json
{
  "tenantId": "org_2nABC123",
  "productId": "prod_checkout_01",
  "batchId": "b9f8e7d6-5c4b-3a2f-1e0d-9876543210fe",
  "motivo": "consulta_openobserve_indisponivel"
}
```
*(No código atual, `motivo` é fixo em `"consulta_openobserve_indisponivel"`, `aviso.go:35`.)*

**Response esperada (`200 OK` ou `201 Created`, máx. 64 KB):**
```json
{
  "aceito": true,
  "tenantId": "org_2nABC123",
  "productId": "prod_checkout_01",
  "batchId": "b9f8e7d6-5c4b-3a2f-1e0d-9876543210fe",
  "motivo": "consulta_openobserve_indisponivel"
}
```
*(Os contratos de `occurrences/lookup`, `analysis-summaries` e `scans/completions` estão detalhados em [endpoints-ocorrencia.md](endpoints-ocorrencia.md) e [endpoints-varredura.md](endpoints-varredura.md).)*

## 4. Códigos de erro tratados pelo Finder

Conforme `internal/adapter/out/modocorrencia/cliente.go:205-229` e `internal/adapter/out/confirmacao/http.go:62-64`:
- `200 OK` / `201 Created`: sucesso (com validação estrita de campos obrigatórios no JSON).
- `409 Conflict`:
  - `{"codigo": "REVISAO_DESATUALIZADA"}` → força reconsulta do achado (`ErrRevisaoDesatualizada`);
  - `{"codigo": "ENTREGA_EM_ANDAMENTO"}` → tratado como temporário (`ErrModuloTemporario`) respeitando `Retry-After`.
- `429`, `500`, `502`, `503`, `504`: erro temporário (`ErrModuloTemporario`), respeitando cabeçalho `Retry-After` em segundos ou HTTP-date.
- `400`, `401`, `403`, `422`: erro de requisição/contrato (`ErrModuloRequisicao`, sem retry automático cego).
- Em `confirmacao/http.go` (Varredura e Core), qualquer status diferente de `200`/`201` retorna `ErrConfirmacao`.

## 5. Origem e destino dos dados

- **Entrada (Redis Streams):** consome `lhamalog:stream:logs` (`event = "log.ingested"`, `schemaVersion = "1"`), usando `metadata.tenantId`, `metadata.productId`, `metadata.correlationId` e `body.openobserve` (`organization`, `stream`, `batchId`, `minTimestampMicros`, `maxTimestampMicros`). Ver `TelemetryIngestedBody.java:12-19` e `consumir_test.go:347,835-863`. Futuramente consome `log.checked` com `execId` (**D4**).
- **Leitura de conteúdo (OpenObserve):** `internal/adapter/out/openobserve/cliente.go:18-94` envia `POST /api/{organization}/_search` com Basic Auth (`pedido.Usuario`/`pedido.Senha`), filtrando `lhamalog_batch_id` no intervalo `[minTimestampMicros, maxTimestampMicros + 1]` (`LLT-270`), paginando com `from`/`size` e deduplicando por `lhamalog_record_id`.
- **Estado local de idempotência:** `batchId` (enquanto `log.ingested` v1 não possui `execId`, `finalizar.go:74-75`).
- **Persistência de ocorrências:** **nenhuma** no MongoDB pelo Finder (`ADR_062`, `spec 006 FR-007`); o Finder entrega `ResumoAnalise` ao Módulo Ocorrência.

## 6. Como Core e Front consomem

- **Web:** nunca acessa o Finder (`ADR_141`).
- **Core:** não consulta o Finder para montar métricas do dashboard; apenas **recebe** avisos operacionais do Finder (`POST /internal/v1/alerts/finder` quando o OpenObserve falha 3 vezes). Os resultados das análises do Finder chegam ao dashboard indiretamente após o **Módulo Ocorrência** persistir as `Ocorrencia`s (`LLT-104`).

## 7. Padrão de logs (D5/D6, Decidido (Michel, 25/11/2026))

O Finder **propaga** `X-Correlation-Id` (a partir de `metadata.correlationId` do Redis, ou gera um UUID se ausente) nas chamadas HTTP de saída e loga no fuso `America/Sao_Paulo` com referência à função.

Implementação alvo:
1. Configurar `slog.HandlerOptions{AddSource: true, ReplaceAttr: ...}` convertendo o campo `time` para `America/Sao_Paulo` (`2006-01-02T15:04:05.000-03:00`).
2. Extrair `metadata.correlationId` do envelope Redis, mantê-lo no `context.Context` / logger (`"correlationId"`), e enviar `req.Header.Set("X-Correlation-Id", correlationID)` em `modocorrencia/cliente.go` e `confirmacao/http.go`.

*Estado atual do código (`693be4f`):* `cmd/finder/main.go:24-25` ainda inicia `slog.NewJSONHandler(os.Stdout, nil)`, e os adaptadores HTTP (`modocorrencia/cliente.go:180-187`, `confirmacao/http.go:48-54`) ainda **não** enviam `X-Correlation-Id`. Essa lacuna vira tarefa de implementação (T010/T012), não mais decisão em aberto.

## 8. Decisões aplicadas

- **D1**, Decidido (Michel, 25/11/2026): o Finder **mantém** `Authorization: Bearer <JWT>` (`ADR_028`) em `modocorrencia/cliente.go` e `confirmacao/http.go`. Não migrar esses clientes para `X-LhamaLog-Service-Token`.
- **D2**, Decidido (Michel, 25/11/2026): atualizar as 4 rotas do Finder para `/internal/v1/occurrences/lookup`, `/internal/v1/analysis-summaries`, `/internal/v1/scans/completions` e `/internal/v1/alerts/finder`.
- **D5/D6**, Decidido (Michel, 25/11/2026): o Finder propaga `X-Correlation-Id` e loga no fuso `America/Sao_Paulo` com referência à função (`AddSource: true`).
