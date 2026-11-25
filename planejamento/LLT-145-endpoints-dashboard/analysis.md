# Análise: Evidências de código, lacunas e decisões (LLT-145)

**Data**: 2026-11-25 (America/Sao_Paulo)
**Escopo**: cruzamento entre o que já existe implementado no Core (`82e7725`), Web (`9adb018`), Collector (`5fb3160` + LLT-290/292) e Finder (`693be4f`) frente às ADRs, Jira e requisitos do Dashboard LLT-145 para os demais módulos. Atualizado com as decisões D1–D9 do Michel (25/11/2026 15:14, America/Sao_Paulo).

## 1. Matriz do que existe hoje vs. o que falta

| Componente | Estado atual verificado no código | Lacuna para o Dashboard LLT-145 e evolução pós-LLT-104 |
|---|---|---|
| **Web** (`lhamalog-web` `9adb018`) | Páginas `ProductDashboardPage` e `CompanyDashboardPage` consomem exclusivamente o Core (`fetchProductMetrics.ts`, `fetchCompanyMetrics.ts`) enviando Clerk JWT e `X-Correlation-Id` (`src/shared/services/api.ts:61-88`). Exibe *"não implementado ainda"* quando `occurrences` está ausente (`parseDashboardMetrics.ts:57-69, 186-193`). | Nenhuma chamada nova no Web para o MVP. Pós-LLT-104, `occurrences` passa a renderizar automaticamente assim que o Core enviar o campo em `SeriesPoint`. |
| **Core** (`lhamalog-core` `82e7725`) | Expõe `GET /api/dashboard/products/{productId}/metrics` e `GET /api/dashboard/company/metrics` (`DashboardMetricsController.java:29-47`). Job `SSID_011` (`DashboardAggregationJob.java`) consolida logs horários do OpenObserve no Mongo. `UsageMetricsAdapter` lê `UsageFact` e `PlanSubscription`. Recebe `POST /internal/usage-facts` e `/internal/usage-reservations/**` com `X-LhamaLog-Service-Token` (`UsageFactsSecurityConfiguration.java:26-108`). | 1) Falta receptor `POST /internal/v1/alerts/finder` já chamado pelo Finder (`aviso.go:31`), autenticado com `Authorization: Bearer <JWT>` (**D1**/**D2**).<br>2) Falta cliente HTTP para consultar `GET /internal/v1/occurrences/metrics` no Módulo Ocorrência com `X-LhamaLog-Service-Token` (pós-LLT-104) e preencher `SeriesPoint.occurrences`; o `SSID_011` soma essas ocorrências (**D3**/**D4**).<br>3) Falta receptor `POST /internal/v1/occurrences/notifications` (**D8**/**D9**).<br>4) Portão humano **T029** (revisão do Felipe de Clerk/papéis) aberto. |
| **Collector** (`lhamalog-collector` `5fb3160`) | Expõe OTLP (`POST /v1/logs`, `POST /v1/traces`), Actuator/Prometheus (`:9464/actuator/prometheus`), grava OpenObserve (`OpenObserveLogsSink`), publica `log.ingested`/`trace.ingested` (`LogIngestedPublisher.java:16-58`) e envia `UsageFact` ao Core. `LLT-290` (`44d36b4`) adiciona `GET /health` e dedup; `LLT-292` (worktree local) adiciona `POST /internal/manual/upload`. | **Não precisa expor endpoint de consulta para o dashboard.** O upload manual grava `UsageFact` (**D7**, Decidido (Michel, 25/11/2026)). Esta documentação registra a decisão; **o código do Collector não foi alterado e permanece parado**. |
| **Finder** (`lhamalog-finder` `693be4f`) | Worker Go que consome `lhamalog:stream:logs` (`log.ingested` v1), lê OpenObserve (`POST /api/{org}/_search`, `cliente.go:18-94`), classifica logs (`ERROR`/`WARNING`/`INFO`) e envia `ResumoAnalise` para Ocorrência. Só expõe `GET /health` (`health.go:7-14`). Os clientes HTTP de saída usam `Authorization: Bearer <JWT>` e rotas em português. | 1) **Não deve** expor API de consulta.<br>2) **Manter** `Authorization: Bearer <JWT>` (**D1**, Decidido (Michel, 25/11/2026)).<br>3) Atualizar as 4 rotas para inglês (**D2**): `/internal/v1/occurrences/lookup`, `/internal/v1/analysis-summaries`, `/internal/v1/scans/completions`, `/internal/v1/alerts/finder`.<br>4) Propagar `X-Correlation-Id` e formatar `slog` com `America/Sao_Paulo` e referência à função (**D5/D6**). |
| **Módulo Ocorrência** | **Sem repositório/código ainda** (não consta em `org:LhamaLog`). Apenas o contrato cliente no Finder (`proposta-dn-009-2.openapi.yaml`). | Implementar: recepção de `ResumoAnalise` + consulta unitária do Finder (rotas em inglês **D2**, JWT **D1**); consulta agregada e listagem para o Core (`GET /internal/v1/occurrences/metrics`, `GET /internal/v1/occurrences`, `GET /internal/v1/occurrences/{occurrenceId}` — **D3**, Service Token); envio de notificações `ERROR`/`WARNING` ao Core (**D8**/**D9**). |
| **Varredura** | **Sem repositório/código ainda** (não consta em `org:LhamaLog`). Apenas a chamada de saída no Finder (`finalizar.go:36`) e fluxos `SSID_005.1`/`006.1` + `ADR_057`/`061`. | Fora das consultas do dashboard no MVP (**D4**). Implementar consumo de `log.ingested`, emissão de `log.checked` **com `execId`** (**D4**), `POST /internal/v1/scans/completions` com JWT (**D1**/**D2**) e `GET /health`. |

## 2. Divergências entre o código atual e o contrato decidido

1. **Autenticação interna — exceção D1 (Decidido (Michel, 25/11/2026))**:
   - No Core (`UsageFactsSecurityConfiguration.java:85-98`), a presença do cabeçalho `Authorization` em `/internal/usage-facts/**` **rejeita a requisição com 401 (`authorization-header-present`)**. O mesmo padrão foi seguido na `LLT-292` (`ADR_172`) para `/internal/manual/upload` e vale para as rotas novas entre Core e Ocorrência.
   - No Finder (`internal/adapter/out/modocorrencia/cliente.go:184` e `internal/adapter/out/confirmacao/http.go:53`), as chamadas internas para Ocorrência, Varredura e o alerta no Core enviam `Authorization: Bearer <JWT>`. **Isso permanece**: é a exceção decidida. O receptor `POST /internal/v1/alerts/finder` no Core **não** pode reutilizar o filtro de `UsageFactsSecurityConfiguration` que rejeita `Authorization`.

2. **Idioma das rotas internas — D2 (Decidido (Michel, 25/11/2026))**:
   - Core e Collector já usam inglês (`/api/dashboard/...`, `/internal/usage-facts`, `/internal/manual/upload`).
   - A `spec 009` do Finder (`proposta-dn-009-2.openapi.yaml`) e seus adaptadores Go ainda usam português (`/internal/v1/ocorrencias/consultas`, `/internal/v1/resumos-analise`, `/internal/v1/execucoes/conclusoes`, `/internal/v1/alertas/finder`). O contrato alvo passou a ser inglês; o código do Finder precisa ser atualizado.

3. **Ausência do endpoint `POST /internal/v1/alerts/finder` no Core**:
   - `lhamalog-finder/internal/adapter/out/core/aviso.go:31` chama hoje `POST /internal/v1/alertas/finder`. Após **D2**, a rota alvo é `/internal/v1/alerts/finder`.
   - Na varredura de controladores do `lhamalog-core` (`82e7725`), não existe nenhum controller para essa rota.

4. **Contrato `log.checked` com `execId` — D4 (Decidido (Michel, 25/11/2026))**:
   - Enquanto `log.checked` não existir, o Finder lê `log.ingested` v1 diretamente usando `batchId`. O evento `log.checked` / `trace.checked` deve levar `execId` para desbloquear `ADR_061`.

5. **Padrão de logs e `X-Correlation-Id` no Finder — D5/D6 (Decidido (Michel, 25/11/2026))**:
   - Java (Core e Collector) já possuem `CorrelationIdFilter` / `CorrelationId`, fuso `America/Sao_Paulo` e `%logger{40}.%M`.
   - Go (`lhamalog-finder/cmd/finder/main.go:24`) ainda usa `slog.NewJSONHandler(os.Stdout, nil)` sem fuso `America/Sao_Paulo`, sem `AddSource` e sem enviar `X-Correlation-Id`. Lacuna de implementação, decisão fechada.

## 3. Catálogo das decisões D1–D9 (Decidido (Michel, 25/11/2026 15:14, America/Sao_Paulo))

| ID | Tema | Decisão |
|---|---|---|
| **D1** | Autenticação interna | O Finder **mantém** `Authorization: Bearer <JWT>` nas chamadas dele, sem trocar para `X-LhamaLog-Service-Token`. Exceção decidida para as rotas que o Finder chama (Ocorrência, Varredura e o alerta no Core). As rotas novas entre Core e Ocorrência continuam com `X-LhamaLog-Service-Token`. |
| **D2** | Idioma das rotas do Finder | As rotas passam para inglês: `/internal/v1/occurrences/lookup`, `/internal/v1/analysis-summaries`, `/internal/v1/scans/completions` e `/internal/v1/alerts/finder`. |
| **D3** | Endpoints de consulta do Módulo Ocorrência | Aprovadas `GET /internal/v1/occurrences/metrics`, `GET /internal/v1/occurrences` e `GET /internal/v1/occurrences/{occurrenceId}`. |
| **D4** | `SSID_011`, Varredura e `log.checked` | O `SSID_011` agrega no Core e soma as ocorrências pela rota `metrics`. A Varredura fica fora do dashboard no MVP. O `log.checked` leva `execId`. |
| **D5/D6** | `X-Correlation-Id` e `slog` no Finder | O Finder propaga o `X-Correlation-Id` e loga no fuso `America/Sao_Paulo` com referência à função. |
| **D7** | `UsageFact` no upload manual (I3 da LLT-292) | O upload manual grava `UsageFact`. A decisão está nesta documentação; o código do Collector **não foi alterado** e permanece parado. |
| **D8** | Notificação Ocorrência → Core | Aprovada a rota `POST /internal/v1/occurrences/notifications` no Core, com `X-LhamaLog-Service-Token`. |
| **D9** | `INFO` gera `Ocorrencia`? | `INFO` entra só nos contadores, sem gerar ocorrência nem notificação. |

Ainda em aberto (não é decisão de contrato desta pasta): o portão humano **T029** do Core (revisão do Felipe sobre Clerk/papéis/`AcessoProduto` na spec 011).
