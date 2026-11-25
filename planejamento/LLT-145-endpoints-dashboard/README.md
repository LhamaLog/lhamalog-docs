# LLT-145 — Endpoints dos módulos para o Dashboard

Entrega documental da [LLT-145](https://logviewer2026.atlassian.net/browse/LLT-145) (relacionada às issues [LLT-222](https://logviewer2026.atlassian.net/browse/LLT-222), [LLT-223](https://logviewer2026.atlassian.net/browse/LLT-223), [LLT-104](https://logviewer2026.atlassian.net/browse/LLT-104), [LLT-159](https://logviewer2026.atlassian.net/browse/LLT-159), [LLT-270](https://logviewer2026.atlassian.net/browse/LLT-270), [LLT-171](https://logviewer2026.atlassian.net/browse/LLT-171) e [LLT-158](https://logviewer2026.atlassian.net/browse/LLT-158)), consolidada em **25/11/2026 (America/Sao_Paulo)** e atualizada no mesmo dia com as decisões do Michel (15:14, America/Sao_Paulo).

O objetivo desta pasta é dar aos demais membros da equipe a referência única — sem inventar contratos não decididos — para implementar e alinhar os endpoints nos outros módulos (**Collector**, **Finder**, **Ocorrência**, **Varredura**, além dos ganchos do **Core** e **Notificação**) que sustentam o Dashboard da LLT-145 no MVP e na evolução pós-LLT-104.

- **Branch local (sem upstream até o push autorizado):** `LLT-145-endpoints-dashboard`
- **Base no `lhamalog-docs`:** `origin/main` (`d603189`)
- **Estado:** documentação pronta para revisão, com as decisões D1–D9 do Michel (25/11/2026 15:14, America/Sao_Paulo) já aplicadas. Nenhuma implementação de código dos módulos foi feita nesta entrega. O código do Collector da LLT-292 permanece parado, sem alteração.

## Navegação

- [Especificação (spec.md)](spec.md)
- [Plano arquitetural e padrões transversais (plan.md)](plan.md)
- [Lista de tarefas por módulo (tasks.md)](tasks.md)
- [Análise de lacunas, divergências de código e decisões (analysis.md)](analysis.md)
- [Módulo Collector (endpoints-collector.md)](endpoints-collector.md)
- [Módulo Finder (endpoints-finder.md)](endpoints-finder.md)
- [Módulo Ocorrência (endpoints-ocorrencia.md)](endpoints-ocorrencia.md)
- [Módulo Varredura (endpoints-varredura.md)](endpoints-varredura.md)
- [Core (rotas internas/públicas) e Notificação (endpoints-core-notificacao.md)](endpoints-core-notificacao.md)

## Fontes inspecionadas

- **Core:** [`lhamalog-core`](https://github.com/LhamaLog/lhamalog-core/tree/82e7725) na branch `LLT-145-consulta-metricas-dashboard` (HEAD `82e7725`), `specs/011-consulta-metricas-dashboard/` e código Java.
- **Web:** [`lhamalog-web`](https://github.com/LhamaLog/lhamalog-web/tree/9adb018) na branch `LLT-145-dashboards-produto-empresa` (HEAD `9adb018`), `specs/007-dashboards-produto-empresa/` e código TypeScript.
- **Collector:** [`lhamalog-collector`](https://github.com/LhamaLog/lhamalog-collector/tree/5fb3160) na branch `Development` (HEAD `5fb3160`), mais o estado documentado da LLT-290 (`feature/LLT-290-file-hash-dedup`, `44d36b4`) e da LLT-292 (`origin/LLT-290-292-planejamento` em `c2aa1fc`).
- **Finder:** [`lhamalog-finder`](https://github.com/LhamaLog/lhamalog-finder/tree/693be4f) na branch `Development` (HEAD `693be4f`), `specs/006`, `specs/008`, `specs/009` e clientes Go.
- **ADRs consultadas:** `ADR_101`, `ADR_112`, `ADR_118`, `ADR_123`, `ADR_131`, `ADR_141`, `ADR_162`, `ADR_166`, `ADR_170` (em `Documentações/Diagrama ADR/` e pasta do Drive `1SsRGM7_f7WD8L0O4GnozbosImt8zReTs`), além de `ADR_028`, `ADR_057`, `ADR_061`, `ADR_062`, `ADR_102`, `ADR_103`, `ADR_146 v2` e rascunhos `ADR_171`–`174` (em `origin/LLT-290-292-planejamento`).
- **Planilhas e modelo:** `LhamaLog casos de uso.xlsx` (`SSID_005.1`, `SSID_006.1`, `SSID_009.1`, `SSID_010`, `SSID_011`, `USID_031`, `USID_034`) e `Modelo de Classes LhamaLog.xlsx` (`Ocorrencia`, `Varredura`, `Arquivo Varredura`, `DashboardProduto`, `DashboardEmpresarial`, `FiltroOcorrenciaEmpresarial`, `RelatorioDashboard`, `Agregação`, `Métrica`).

## Resumo dos endpoints por módulo

| Módulo | Método e Rota | Autenticação | Finalidade | Quem consome | Situação |
|---|---|---|---|---|---|
| **Collector** | `POST /v1/logs` e `POST /v1/traces` | `Bearer <productToken>` | Recepção OTLP HTTP/gRPC (grava no OpenObserve e publica `log.ingested`/`trace.ingested`) | SDKs / agentes do cliente | Implementado (`Development` `5fb3160`) |
| **Collector** | `GET /health` (+ gRPC `Health`) | Nenhuma (ADR_118) | Saúde do serviço | Orquestração / infra | Implementado na LLT-290 (`44d36b4`, sem PR) |
| **Collector** | `GET /actuator/prometheus` | Nenhuma (porta `9464`) | Métricas operacionais PromQL | Prometheus / Grafana | Implementado (`Development` `5fb3160`) |
| **Collector** | `POST /internal/manual/upload` | `X-LhamaLog-Service-Token` | Upload manual de arquivos via Core; grava `UsageFact` no Core (**D7**, Decidido (Michel, 25/11/2026)) | Core (`PR #15`) | Implementado no worktree LLT-292 (sem commit; código do Collector permanece parado) |
| **Collector** | *(Consulta de dashboard no Collector)* | — | **Não necessária no MVP**: Core lê OpenObserve e `UsageFact` diretamente | — | Confirmado na spec 011 |
| **Finder** | `GET /health` | Nenhuma (ADR_118) | Saúde do worker Go | Orquestração / infra | Implementado (`Development` `693be4f`) |
| **Finder** | *(Consulta HTTP de logs/ocorrências)* | — | **Não expõe API de consulta**: worker lê `log.ingested` e OpenObserve e envia achados para Ocorrência | — | Confirmado (`ADR_062` / spec 008–009) |
| **Ocorrência** | `POST /internal/v1/occurrences/lookup` | `Authorization: Bearer <JWT>` (**D1**, exceção decidida para rotas que o Finder chama) | Consultar estado de achado único antes do envio do lote | Finder (`cliente.go`; rota atual no código ainda é `/internal/v1/ocorrencias/consultas`, a atualizar para inglês — **D2**) | A implementar (contrato DN-009-2 existe no Finder) |
| **Ocorrência** | `POST /internal/v1/analysis-summaries` | `Authorization: Bearer <JWT>` (**D1**, exceção decidida) | Receber `ResumoAnalise` + `AchadoAnalise` e persistir `Ocorrencia` | Finder (`cliente.go`; rota atual no código ainda é `/internal/v1/resumos-analise`, a atualizar — **D2**) | A implementar (contrato DN-009-2 existe no Finder) |
| **Ocorrência** | `GET /internal/v1/occurrences/metrics` | `X-LhamaLog-Service-Token` | Série e totais de ocorrências por produto/empresa/severidade para `SSID_011` e `SeriesPoint.occurrences` | Core (`DashboardMetricsService` / job `SSID_011`) | Decidido (Michel, 25/11/2026) (**D3**/**D4**); a implementar após a LLT-104 |
| **Ocorrência** | `GET /internal/v1/occurrences` e `GET /internal/v1/occurrences/{occurrenceId}` | `X-LhamaLog-Service-Token` | Listar/detalhar ocorrências nos 3 níveis (`ADR_101`/`ADR_162`) garantindo consistência `LLT-222` | Core → Web (`LLT-104`) | Decidido (Michel, 25/11/2026) (**D3**); a implementar após a LLT-104 |
| **Varredura** | `POST /internal/v1/scans/completions` | `Authorization: Bearer <JWT>` (**D1**, exceção decidida) | Confirmar conclusão de arquivo ligado a `execId` (`ADR_061`) | Finder (`finalizar.go`; rota atual no código ainda é `/internal/v1/execucoes/conclusoes`, a atualizar — **D2**) | A implementar (só ativo quando houver `execId` / `log.checked`) |
| **Varredura** | `GET /health` | Nenhuma (ADR_118) | Saúde do serviço | Orquestração / infra | A implementar (serviço sem repo ainda) |
| **Varredura** | `GET /internal/v1/scans/summary` | — | Resumo de execução (`VarreduraResumo`) | — | **Fora do dashboard no MVP** (**D4**, Decidido (Michel, 25/11/2026)) |
| **Core** | `GET /api/dashboard/products/{productId}/metrics` | Clerk JWT (`Bearer`) | Métricas de produto do dashboard (`LLT-222`) | Web (`fetchProductMetrics.ts`) / Mobile (`LLT-159`) | Implementado (`82e7725`), sem `occurrences` até a LLT-104 |
| **Core** | `GET /api/dashboard/company/metrics` | Clerk JWT (`Bearer`) | Métricas da empresa (`LLT-223`) | Web (`fetchCompanyMetrics.ts`) / Mobile (`LLT-159`) | Implementado (`82e7725`), sem `occurrences` até a LLT-104 |
| **Core** | `POST /internal/usage-facts`, `GET /internal/usage-facts/**`, `POST /internal/usage-reservations/**` | `X-LhamaLog-Service-Token` | Gravar fatos/reservas de uso consumidos pelo dashboard (`volumeUsedBytes`, `traces`), inclusive do upload manual (**D7**) | Collector | Implementado (`82e7725`) |
| **Core** | `POST /internal/v1/alerts/finder` | `Authorization: Bearer <JWT>` (**D1**, exceção decidida) | Receber alerta do Finder após 3 falhas de leitura no OpenObserve | Finder (`aviso.go`; rota atual no código ainda é `/internal/v1/alertas/finder`, a atualizar — **D2**) | A implementar no Core |
| **Core** | `POST /internal/v1/occurrences/notifications` | `X-LhamaLog-Service-Token` | Receber ocorrência `ERROR`/`WARNING` do Módulo Ocorrência (`SSID_009.1`) e publicar na stream de notificação; `INFO` não gera ocorrência nem notificação (**D9**) | Módulo Ocorrência | Decidido (Michel, 25/11/2026) (**D8**/**D9**); a implementar |

## Decisões do Michel (25/11/2026 15:14, America/Sao_Paulo)

1. **D1 — Autenticação das rotas que o Finder chama:** o Finder **mantém** `Authorization: Bearer <JWT>` nas chamadas dele, sem trocar para `X-LhamaLog-Service-Token`. Essa é uma **exceção decidida** para as rotas que o Finder chama: `POST /internal/v1/occurrences/lookup`, `POST /internal/v1/analysis-summaries` (Ocorrência), `POST /internal/v1/scans/completions` (Varredura) e `POST /internal/v1/alerts/finder` (alerta no Core). As rotas novas entre **Core e Ocorrência** (`GET /internal/v1/occurrences/metrics`, `GET /internal/v1/occurrences`, `GET /internal/v1/occurrences/{occurrenceId}` e `POST /internal/v1/occurrences/notifications`) continuam com `X-LhamaLog-Service-Token` (comparação em tempo constante, rejeitando `Authorization`).
2. **D2 — Idioma das rotas do Finder:** as rotas passam para inglês: `/internal/v1/occurrences/lookup`, `/internal/v1/analysis-summaries`, `/internal/v1/scans/completions` e `/internal/v1/alerts/finder`. O código atual do Finder (`693be4f`) ainda usa as rotas em português e precisa ser atualizado.
3. **D3 — Contrato do Módulo Ocorrência pós-LLT-104:** aprovadas as rotas `GET /internal/v1/occurrences/metrics`, `GET /internal/v1/occurrences` e `GET /internal/v1/occurrences/{occurrenceId}`.
4. **D4 — `SSID_011`, Varredura e `log.checked`:** o `SSID_011` agrega no Core (logs no OpenObserve/Mongo) e soma as ocorrências pela rota `GET /internal/v1/occurrences/metrics`. A Varredura fica **fora do dashboard no MVP**. O evento `log.checked` leva `execId`.
5. **D5/D6 — Correlação e logs no Finder:** o Finder propaga o `X-Correlation-Id` (a partir de `metadata.correlationId` do Redis) e loga no fuso `America/Sao_Paulo` com referência à função.
6. **D7 (= I3 da LLT-292) — `UsageFact` no upload manual:** o upload manual grava `UsageFact`. Esta decisão fica registrada nesta documentação; o código do Collector **não foi alterado** e permanece parado.
7. **D8/D9 — Notificação e `INFO`:** aprovada a rota `POST /internal/v1/occurrences/notifications` no Core (`X-LhamaLog-Service-Token`). `INFO` entra só nos contadores, sem gerar ocorrência nem notificação.

Ainda aguarda revisão humana (não é decisão de contrato desta pasta): o portão **T029** do Core (revisão do Felipe sobre Clerk/papéis/`AcessoProduto` na spec 011).
