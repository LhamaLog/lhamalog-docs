# Especificação: Endpoints dos módulos para o Dashboard (LLT-145)

**Branch**: `LLT-145-endpoints-dashboard`
**Data**: 2026-11-25 (America/Sao_Paulo)
**Estado**: especificação documental de integração multi-módulos, com as decisões D1–D9 do Michel (25/11/2026 15:14, America/Sao_Paulo) já aplicadas.
**Fontes**: Jira (`LLT-145`, `222`, `223`, `104`, `159`, `270`, `171`, `158`), ADRs (`101`, `112`, `118`, `123`, `131`, `141`, `162`, `166`, `170`, `171`–`174`), `lhamalog-core` (`82e7725`), `lhamalog-web` (`9adb018`), `lhamalog-collector` (`5fb3160` + LLT-290/292) e `lhamalog-finder` (`693be4f`).

## Contexto e problema

O Dashboard da LLT-145 já possui implementação mínima no **Core** (`lhamalog-core` branch `LLT-145-consulta-metricas-dashboard`, `82e7725`) e no **Web** (`lhamalog-web` branch `LLT-145-dashboards-produto-empresa`, `9adb018`). Contudo:

1. O gráfico e os contadores de **Ocorrências** estão marcados como *"não implementado ainda"* no Web (`ProductDashboardPage.tsx:336-342`) porque o Core omite `occurrences` em `SeriesPoint` (`DashboardMetricsResponses.java:38-40`) até existir o **Módulo Ocorrência** (`LLT-104`).
2. Os demais módulos (**Collector**, **Finder**, **Ocorrência** e **Varredura**) possuem papéis distintos na arquitetura (`ADR_141`, `ADR_061`, `ADR_062`). Esta pasta é o guia único indicando para a equipe:
   - quais módulos **realmente precisam** expor novos endpoints HTTP e quais são apenas workers/ingestores;
   - quais contratos já estão codificados em clientes existentes (como os clientes Go do Finder na spec `009`) e o alinhamento decidido com o padrão do Core/Collector (`X-LhamaLog-Service-Token` nas rotas novas entre Core e Ocorrência; **exceção D1** de `Authorization: Bearer <JWT>` nas rotas que o Finder chama; rotas em inglês **D2**; `X-Correlation-Id` e logs em `America/Sao_Paulo`);
   - de onde vêm os dados de cada métrica exibida no dashboard (OpenObserve, Redis Streams `ingested`/`checked`, MongoDB e `/internal/usage-facts`).

## Cenários de uso e validação

### 1. Entregar métricas de logs e uso no MVP sem acoplar Web aos módulos internos (P1)
Como equipe do Core e do Collector, precisamos que o Web fale apenas com o Core (`ADR_141`) usando JWT do Clerk, enquanto o Core obtém volumes e traces dos fatos de uso (`POST /internal/usage-facts`) gravados pelo Collector — inclusive no upload manual (**D7**, Decidido (Michel, 25/11/2026)) — e contagens de logs diretamente do OpenObserve (`POST /api/{org}/_search`) + agregados horários no Mongo (`SSID_011`).

- **Validação independente**: conferir que o Web chama apenas `GET /api/dashboard/products/{productId}/metrics` e `GET /api/dashboard/company/metrics` (`fetchProductMetrics.ts`, `fetchCompanyMetrics.ts`) e que o Collector não precisa de novo endpoint de consulta de métricas no MVP.
- **Aceite**: Collector entrega `POST /internal/usage-facts` (também no upload manual) e grava no OpenObserve com `tenantId`, `productId`, `severityNumber`, `severityText` e `serviceName`; Core agrega e responde ao Web com `retentionDays`, `volumeIngestaoBytes` e séries sem `occurrences` até a LLT-104.

### 2. Desbloquear o indicador e a série de Ocorrências pós-LLT-104 (P1)
Como desenvolvedor do **Módulo Ocorrência**, preciso implementar os endpoints internos que recebem `ResumoAnalise` do Finder (`DN-009-2`, rotas em inglês **D2**, autenticadas com `Authorization: Bearer <JWT>` — **D1**) e os endpoints internos de consulta/agregação autenticados com `X-LhamaLog-Service-Token` que o Core consumirá para preencher `SeriesPoint.occurrences` (**D3**, Decidido (Michel, 25/11/2026)) e garantir que os números do dashboard batam com a lista de ocorrências para os mesmos filtros (`LLT-222`, `ADR_101`, `ADR_162`). O `SSID_011` no Core continua agregando logs e soma as ocorrências pela rota `GET /internal/v1/occurrences/metrics` (**D4**). `INFO` entra só nos contadores, sem gerar `Ocorrencia` nem notificação (**D9**).

- **Validação independente**: simular um `ResumoAnalise` enviado pelo Finder, persistir a `Ocorrencia` apenas para `ERROR`/`WARNING`, consultar o resumo agregado pelo Core via `X-LhamaLog-Service-Token` e conferir consistência entre o total de ocorrências no dashboard e na listagem filtrada.
- **Aceite**: o Core passa a preencher `occurrences` por bucket e o Web remove automaticamente o placeholder *"não implementado ainda"* (`parseDashboardMetrics.ts:57-69`).

### 3. Integrar Finder e Varredura na esteira `ingested` → `checked` sem criar APIs de consulta indevidas no Finder (P1)
Como desenvolvedor de **Finder** ou **Varredura**, preciso saber que o Finder é um worker Go sem API HTTP de consulta (`GET /health` apenas), e que a evolução de `log.ingested` (Collector) para `log.checked` (Varredura) fornece `execId` (**D4**, Decidido (Michel, 25/11/2026)) para acionar `POST /internal/v1/scans/completions` (`ADR_061`) sem alterar o contrato do Web. A Varredura permanece fora do dashboard no MVP (**D4**).

- **Validação independente**: revisar os fluxos do Finder (`internal/adapter/in/queue/redisStream.go` e `internal/adapter/out/`) e da Varredura (`SSID_005.1`/`006.1`).
- **Aceite**: nenhuma rota pública ou de dashboard é criada no Finder ou na Varredura sem passar pelo Core; as rotas de saída do Finder estão em inglês (**D2**), autenticadas com `Authorization: Bearer <JWT>` (**D1**), e propagam `X-Correlation-Id` (**D5/D6**).

### 4. Garantir rastreabilidade, isolamento e segurança padrão em todas as chamadas (P2)
Como responsável por segurança e observabilidade, preciso que:
- as rotas `/internal/**` chamadas pelo **Finder** aceitem `Authorization: Bearer <JWT>` (**D1**, exceção decidida);
- as rotas novas entre **Core e Ocorrência** validem `X-LhamaLog-Service-Token` em tempo constante (rejeitando `Authorization`);
- todos os módulos isolem os dados por `tenantId` e `productId` (`LLT-158`, `LLT-171`), propaguem `X-Correlation-Id` (o Finder inclusive — **D5/D6**) e gravem logs com id de correlação, referência à função, mensagem e timestamp em `America/Sao_Paulo`.

- **Validação independente**: testar envio sem token, com token inválido e, nas rotas com Service Token, com cabeçalho `Authorization` indevido (401); testar acesso cross-tenant e produto não autorizado (404 no Core para o front / 403 ou 404 conforme regra interna).

### Casos de borda

- Produto sem dados no período → 200 com totais zerados e listas vazias (sem erro 404).
- `MEMBRO` sem `AcessoProduto` ao `productId` ou produto de outro tenant → **404** no Core (`DashboardMetricsControllerIntegrationTest` / decisão Michel 18/11) para não vazar existência do recurso (`LLT-158`).
- Divergência de horário entre OpenObserve (UTC / microssegundos `_timestamp`) e exibição ao usuário (`America/Sao_Paulo` ou fuso do perfil) → APIs trafegam UTC ISO-8601 (`Instant`) e logs de servidor usam `America/Sao_Paulo`.
- Falha no OpenObserve durante leitura do intervalo aberto do dashboard → Core retorna 5xx sem corromper `DashboardLogHourlyAggregate` já consolidado e registra log com `X-Correlation-Id`.
- Finder falha 3 vezes ao consultar OpenObserve → **sem DLQ** no `log.ingested` (`DLQ B`, spec 008/009); Finder aciona Core via `POST /internal/v1/alerts/finder` com `Authorization: Bearer <JWT>` (**D1**/**D2**).
- Lote de `log.ingested` v1 sem `execId` → Finder usa `batchId` como chave de idempotência e **não** chama Varredura (`efeito_analise.go:48`) até existir `log.checked` com `execId` (**D4**).

## Requisitos funcionais

- **FR-001**: O **Web** comunica-se exclusivamente com o **Core** (`ADR_141`), utilizando Clerk JWT (`Authorization: Bearer`) e enviando `X-Correlation-Id`.
- **FR-002**: Autenticação interna (**D1**, Decidido (Michel, 25/11/2026)):
  - rotas que o **Finder chama** (`POST /internal/v1/occurrences/lookup`, `POST /internal/v1/analysis-summaries`, `POST /internal/v1/scans/completions`, `POST /internal/v1/alerts/finder`) usam `Authorization: Bearer <JWT>` (exceção decidida; o Finder **não** troca para `X-LhamaLog-Service-Token`);
  - rotas novas entre **Core e Ocorrência** (`GET /internal/v1/occurrences/metrics`, `GET /internal/v1/occurrences`, `GET /internal/v1/occurrences/{occurrenceId}`, `POST /internal/v1/occurrences/notifications`) e as demais rotas internas já padronizadas (`/internal/usage-facts`, `/internal/usage-reservations`, `/internal/manual/upload`) usam `X-LhamaLog-Service-Token` com comparação em tempo constante, rejeitando `Authorization` (`ADR_172`).
- **FR-003**: Rotas internas seguem o prefixo `/internal/...` (ou `/internal/v1/...`) em inglês. As rotas do Finder ficam (**D2**, Decidido (Michel, 25/11/2026)): `/internal/v1/occurrences/lookup`, `/internal/v1/analysis-summaries`, `/internal/v1/scans/completions` e `/internal/v1/alerts/finder`. O código atual do Finder (`693be4f`) ainda usa as rotas em português e deve ser atualizado.
- **FR-004**: Cada módulo documenta explicitamente contratos JSON de request e response, códigos HTTP de erro, origem dos dados (`OpenObserve`, `Redis Streams`, `MongoDB`, `usage-facts`), consumo por Core/Web e padrão de logs.
- **FR-005**: Nenhuma métrica ou contrato do dashboard deve expor selos de impacto em MVP (`ADR_166`, `spec 011`), nem usar a categoria legada `SPAM` ou "não classificado" (`ADR_170`: apenas `ERROR`, `WARNING`, `INFO`). `INFO` entra só nos contadores, sem gerar `Ocorrencia` nem notificação (**D9**, Decidido (Michel, 25/11/2026)).
- **FR-006**: O Finder propaga `X-Correlation-Id` nas chamadas HTTP de saída e formata os logs em `America/Sao_Paulo` com referência à função (**D5/D6**, Decidido (Michel, 25/11/2026)).

## Entidades e fontes de dados

| Fonte | O que armazena / trafega | Quem grava | Quem lê para o Dashboard / Pipeline |
|---|---|---|---|
| **OpenObserve** (org `lhamalog`, stream por tenant `logs_<tenant_slug>`) | Logs e traces OTLP crus + upload manual (`fileSource=upload`), colunas em minúsculas (`tenantid`, `productid`, `severitynumber`, `severitytext`, `servicename`, `_timestamp`, `lhamalog_batch_id`, `lhamalog_record_id`) | **Collector** (`OpenObserveLogsSink`) | **Core** (`OpenObserveLogQueryAdapter`: intervalo aberto e job `SSID_011`) e **Finder** (`openobserve/cliente.go`: leitura por lote e recorrência) |
| **Redis Streams** (`lhamalog:stream:logs`, `lhamalog:stream:traces`, `:dlq`, futura `checked`) | Referências de lote (`log.ingested`, `trace.ingested`, futuro `log.checked`/`trace.checked` com `execId` — **D4**) e eventos de notificação | **Collector** (`LogIngestedPublisher`), **Varredura** (futuro `checked`), **Core** (notificações) | **Varredura** (consome `ingested`), **Finder** (consome `log.ingested` v1 / futuro `log.checked`), **Notificação** |
| **MongoDB** | `DashboardLogHourlyAggregate`, `DashboardAggregationWatermark`, `UsageFact`, `QuotaReservation`, `PlanSubscription`, `Product`, `AcessoProduto`, `product_tokens`, futuros `Ocorrencia`, `Varredura`, `ArquivoVarredura` | **Core**, **Ocorrência** (futuro), **Varredura** (futuro) | **Core** (agregados, uso, planos, permissões), **Collector** (leitura `product_tokens`/`products`), **Ocorrência**, **Varredura** |
| **API interna `usage-facts`** (`POST/GET /internal/usage-facts`) | Registros idempotentes por lote de `acceptedRecordCount` e `acceptedBytes` (`LOGS` e `TRACES`), inclusive do upload manual (**D7**) | **Collector** envia para o **Core** | **Core** (`UsageMetricsAdapter` soma `volumeUsedBytes` e `traces` para o dashboard) |

## Critérios de sucesso

- **SC-001**: Todos os módulos envolvidos (`Collector`, `Finder`, `Ocorrência`, `Varredura`, `Core`/`Notificação`) possuem documento próprio com rotas, método, auth, JSON de request/response, códigos de erro, origem de dados, consumo e padrão de logs.
- **SC-002**: 100% das rotas e schemas já existentes em código (`Core 82e7725`, `Web 9adb018`, `Collector 5fb3160`, `Finder 693be4f`) estão citados com caminho de arquivo e linha, e as rotas decididas em D2–D3–D8 estão documentadas no contrato alvo (inglês).
- **SC-003**: As decisões D1–D9 do Michel (25/11/2026) estão aplicadas nas tabelas, nos contratos e no `tasks.md`; o portão humano T029 (revisão do Felipe) permanece explícito e em aberto.
- **SC-004**: Nenhum arquivo preexistente do repositório `lhamalog-docs`, de `entrega-academica/` ou de `Documentações/Diagrama ADR/` é modificado.
