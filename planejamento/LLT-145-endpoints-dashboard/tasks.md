# Tarefas: Endpoints dos módulos para o Dashboard (LLT-145)

**Entrada**: [spec.md](spec.md), [plan.md](plan.md), [analysis.md](analysis.md) e guias por módulo (`endpoints-*.md`).
**Nota**: Esta entrega é exclusivamente documental. As decisões D1–D9 do Michel (25/11/2026 15:14, America/Sao_Paulo) já estão aplicadas nesta pasta. Nenhuma task de implementação de código foi executada aqui. O código do Collector da LLT-292 permanece parado (**D7**).

## Fase 1 — Decisões do Michel (fechadas em 25/11/2026) e portão humano restante

- [x] **T001** **D1** — Decidido (Michel, 25/11/2026): o Finder **mantém** `Authorization: Bearer <JWT>` nas chamadas dele. Exceção documentada para as rotas que o Finder chama (Ocorrência, Varredura e o alerta no Core). As rotas novas entre Core e Ocorrência continuam com `X-LhamaLog-Service-Token`.
- [x] **T002** **D2** — Decidido (Michel, 25/11/2026): as rotas do Finder passam para inglês: `/internal/v1/occurrences/lookup`, `/internal/v1/analysis-summaries`, `/internal/v1/scans/completions` e `/internal/v1/alerts/finder`. Resta atualizar o código do Finder e os servidores.
- [x] **T003** **D3** — Decidido (Michel, 25/11/2026): aprovadas `GET /internal/v1/occurrences/metrics`, `GET /internal/v1/occurrences` e `GET /internal/v1/occurrences/{occurrenceId}`.
- [x] **T004** **D4** — Decidido (Michel, 25/11/2026): o `SSID_011` agrega no Core e soma as ocorrências pela rota `metrics`; a Varredura fica fora do dashboard no MVP; o `log.checked` leva `execId`.
- [x] **T005** **D5/D6** — Decidido (Michel, 25/11/2026): o Finder propaga o `X-Correlation-Id` e loga no fuso `America/Sao_Paulo` com referência à função. Resta implementar no `lhamalog-finder`.
- [ ] **T006** Fechar o portão humano **T029** do Core (`Felipe`): revisão de Clerk, papéis (`DONO`/`ADMIN`/`MEMBRO`) e `AcessoProduto` na spec 011 (`lhamalog-core/specs/011-consulta-metricas-dashboard/tasks.md:101`). *(Não é decisão de contrato desta pasta; permanece em aberto.)*

## Fase 2 — Collector (`lhamalog-collector`)

- [x] **T007** **D7** (= I3 da LLT-292) — Decidido (Michel, 25/11/2026): o upload manual grava `UsageFact`. A decisão está registrada nesta documentação. **O código do Collector não foi alterado e permanece parado.**
- [ ] **T008** Quando o Collector da LLT-292 for retomado (fora desta entrega), validar em ambiente integrado que todo lote aceito (OTLP HTTP/gRPC e upload manual) grava no OpenObserve com `tenantId`, `productId`, `severityNumber`, `severityText`, `serviceName`, `_timestamp` e envia `POST /internal/usage-facts` para o Core com `X-Correlation-Id`.

## Fase 3 — Finder (`lhamalog-finder`)

- [ ] **T009** Manter apenas `GET /health` como endpoint HTTP de entrada (não criar API de consulta de logs/ocorrências no Finder).
- [ ] **T010** Propagar `X-Correlation-Id` (originado de `metadata.correlationId` do Redis) nos clientes `modocorrencia/cliente.go`, `finalizacao/finalizar.go` e `core/aviso.go` (**D5/D6**, Decidido (Michel, 25/11/2026)).
- [ ] **T011** Atualizar `modocorrencia/cliente.go`, `finalizacao/finalizar.go`, `core/aviso.go` e `confirmacao/http.go` para as rotas em inglês (**D2**): `/internal/v1/occurrences/lookup`, `/internal/v1/analysis-summaries`, `/internal/v1/scans/completions` e `/internal/v1/alerts/finder`. **Manter** `Authorization: Bearer <JWT>` (**D1**, Decidido (Michel, 25/11/2026)); não migrar esses clientes para `X-LhamaLog-Service-Token`.
- [ ] **T012** Ajustar logger `slog` em `cmd/finder/main.go` para incluir fuso `America/Sao_Paulo`, referência à função (`AddSource: true`) e `correlationId` (**D5/D6**, Decidido (Michel, 25/11/2026)).

## Fase 4 — Módulo Ocorrência (novo módulo / `LLT-104`)

- [ ] **T013** Implementar `GET /health` sem autenticação (`ADR_118`).
- [ ] **T014** Implementar duas cadeias de autenticação no mesmo serviço, conforme **D1** (Decidido (Michel, 25/11/2026)):
  - `Authorization: Bearer <JWT>` nas rotas que o Finder chama (`POST /internal/v1/occurrences/lookup` e `POST /internal/v1/analysis-summaries`);
  - `X-LhamaLog-Service-Token` (comparação em tempo constante, rejeitando `Authorization`) nas rotas novas consumidas pelo Core (`GET /internal/v1/occurrences/metrics`, `GET /internal/v1/occurrences`, `GET /internal/v1/occurrences/{occurrenceId}`).
  - Em todas: filtro de `X-Correlation-Id` + log em `America/Sao_Paulo`.
- [ ] **T015** Implementar `POST /internal/v1/occurrences/lookup` para consulta unitária do Finder (`DN-009-2`, rota em inglês **D2**).
- [ ] **T016** Implementar `POST /internal/v1/analysis-summaries` (rota em inglês **D2**) com idempotência por `batchId` (ou `batchId + execId`), cálculo de gravidade (`ADR_062`) e persistência de `Ocorrencia` no MongoDB apenas para `ERROR` e `WARNING` (**D9**, Decidido (Michel, 25/11/2026)). `INFO` entra só nos contadores do `ResumoAnalise`.
- [ ] **T017** Implementar `GET /internal/v1/occurrences/metrics` para alimentar `SeriesPoint.occurrences` e a soma do `SSID_011` no Core (**D3**/**D4**, Decidido (Michel, 25/11/2026)).
- [ ] **T018** Implementar `GET /internal/v1/occurrences` e `GET /internal/v1/occurrences/{occurrenceId}` nos 3 níveis (`ADR_101`, `ADR_162`, `LLT-222`), garantindo que os filtros batam 1:1 com os números do dashboard (**D3**, Decidido (Michel, 25/11/2026)).
- [ ] **T019** Implementar envio de ocorrências `ERROR`/`WARNING` ao Core (`SSID_009.1`) via `POST /internal/v1/occurrences/notifications` (**D8**/**D9**, Decidido (Michel, 25/11/2026)). Não enviar `INFO`.

## Fase 5 — Varredura (novo módulo)

- [ ] **T020** Implementar `GET /health` sem autenticação (`ADR_118`) e autenticação `Authorization: Bearer <JWT>` na rota que o Finder chama (**D1**), mais `X-Correlation-Id` + log em `America/Sao_Paulo`.
- [ ] **T021** Implementar consumidor de `lhamalog:stream:logs` / `lhamalog:stream:traces` (`log.ingested` / `trace.ingested`), ordenação por Produto (`ADR_057`), varredura de dados sensíveis/prompt-injection e publicação de `log.checked` / `trace.checked` **com `execId`** (**D4**, Decidido (Michel, 25/11/2026)).
- [ ] **T022** Implementar `POST /internal/v1/scans/completions` (rota em inglês **D2**) consumido pelo Finder com `Authorization: Bearer <JWT>` (**D1**, `ADR_061`).
- [x] **T023** **D4** — Decidido (Michel, 25/11/2026): a Varredura fica **fora do dashboard no MVP**. `GET /internal/v1/scans/summary` **não** entra nesta entrega.

## Fase 6 — Core e Notificação (`lhamalog-core` / futuro módulo Notificação)

- [ ] **T024** Implementar no Core o receptor `POST /internal/v1/alerts/finder` (rota em inglês **D2**) já esperado pelo Finder, autenticado com `Authorization: Bearer <JWT>` (**D1**, Decidido (Michel, 25/11/2026)) — exceção em relação ao filtro de `/internal/usage-facts`, que rejeita `Authorization`.
- [ ] **T025** *(Pós-LLT-104)* Criar `OccurrenceMetricsPort` / `OccurrenceMetricsAdapter` no Core para consultar `GET /internal/v1/occurrences/metrics` no Módulo Ocorrência com `X-LhamaLog-Service-Token` e preencher `SeriesPoint.occurrences`. O `SSID_011` no Core continua agregando logs e soma as ocorrências por essa rota (**D3**/**D4**, Decidido (Michel, 25/11/2026)).
- [ ] **T026** *(Pós-LLT-104)* Implementar receptor `POST /internal/v1/occurrences/notifications` no Core com `X-LhamaLog-Service-Token`, repassando `ERROR`/`WARNING` para a stream do módulo Notificação (`ADR_146`/`ADR_165`). Recusar ou ignorar `INFO` (**D8**/**D9**, Decidido (Michel, 25/11/2026)).
- [ ] **T027** *(Opcional se houver tela no Web)* Expor endpoints públicos `/api/occurrences/**` no Core (`ADR_141`) consumindo `GET /internal/v1/occurrences/**` com Clerk JWT e checagem de `AcessoProduto` (`LLT-171`).

## Fase 7 — Validação integrada

- [ ] **T028** Validar ponta a ponta: OTLP/Upload → Collector (`OpenObserve` + `UsageFact` + `log.ingested`) → Varredura (`log.checked` com `execId`) → Finder (`X-Correlation-Id` + JWT + rotas em inglês) → Ocorrência → Core (`/api/dashboard/...`, com `occurrences` somadas pelo `SSID_011`) → Web (`LLT-222`/`LLT-223`), conferindo rastreabilidade pelo mesmo `X-Correlation-Id` nos logs de todos os módulos.
