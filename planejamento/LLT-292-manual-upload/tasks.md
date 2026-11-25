# Tarefas — LLT-292

Resumo de T001–T034 da spec 011. Detalhe e paths no [`tasks.md`](https://github.com/LhamaLog/lhamalog-core/blob/f8f3f4aef1d31b514ed413760ceae12f0b02aba5/specs/011-manual-upload/tasks.md) de trabalho no Core. Nenhuma tarefa de código foi executada a partir desta pasta. Commit/push **desta documentação** só com OK do Michel.

## Fase 0 — worktrees

- [x] T001 [Core] Copiar a spec 011 para o worktree `lhamalog-core-llt292` (criado em 20/11/2026 a partir de `origin/Development` `23a69d9`). Não alterar o checkout da LLT-145. A branch `feature/LLT-292-manual-upload` foi publicada no PR [#15](https://github.com/LhamaLog/lhamalog-core/pull/15).
- [x] T002 [Coll] Worktree local criado a partir da branch publicada `feature/LLT-290-file-hash-dedup`. A implementação do Collector está nesse worktree, ainda **sem commit**.

## Fase 1 — fundação Core (~6 h)

- [x] T003–T010 (publicadas no PR #15): multipart/Tomcat 100 MB; [`ManualUploadProperties`](https://github.com/LhamaLog/lhamalog-core/blob/f8f3f4aef1d31b514ed413760ceae12f0b02aba5/src/main/java/br/com/lhamalog/core/config/ManualUploadProperties.java) / configuração; autorizador 403; validador de extensão e tamanho; cliente com `X-LhamaLog-Service-Token` e `X-Correlation-Id`; mapeamento de respostas; `POST /api/manual/upload`; logs no padrão VI. Commits: `e44ee1d` (validação, propriedades e limites), `9ac348d` (encaminhamento) e `026c236` (endpoint e handler de 413).

## Fase 2 — testes Core (~8 h)

- [x] T011–T015 (publicadas no PR #15): 401, 202 com dublê, 403 (outro tenant, sem acesso, arquivado, id inexistente), 400/413, mapeamento 409/429/503/timeout, multipart com dois arquivos. N1–N4 estão fechados: URL em branco ou sem esquema ([`ManualUploadProperties.isUsableCollectorUrl`](https://github.com/LhamaLog/lhamalog-core/blob/f8f3f4aef1d31b514ed413760ceae12f0b02aba5/src/main/java/br/com/lhamalog/core/config/ManualUploadProperties.java), [`ManualUploadStartupChecks.warnings`](https://github.com/LhamaLog/lhamalog-core/blob/f8f3f4aef1d31b514ed413760ceae12f0b02aba5/src/main/java/br/com/lhamalog/core/config/ManualUploadStartupChecks.java)) com token + URL ruim → 503; 413 do contêiner classificado em [`ApiExceptionHandler.containerUploadMessage`](https://github.com/LhamaLog/lhamalog-core/blob/f8f3f4aef1d31b514ed413760ceae12f0b02aba5/src/main/java/br/com/lhamalog/core/shared/ApiExceptionHandler.java) pelos tipos e textos do Tomcat 11.0.24 (`ApiExceptionHandlerUploadTest`); merge em [`ManualUploadValidator.mergeCollector`](https://github.com/LhamaLog/lhamalog-core/blob/f8f3f4aef1d31b514ed413760ceae12f0b02aba5/src/main/java/br/com/lhamalog/core/upload/ManualUploadValidator.java) / `takeCollectorResult` por posição e filename, com placeholder `UNKNOWN`/`collector_result_missing` se o Collector omitir uma parte aceita; teto de 64 KB em [`RestCollectorManualUploadClient.readBody`](https://github.com/LhamaLog/lhamalog-core/blob/f8f3f4aef1d31b514ed413760ceae12f0b02aba5/src/main/java/br/com/lhamalog/core/upload/RestCollectorManualUploadClient.java) testado com JSON válido e WARN. Limite conhecido: o 413 do contêiner é testado só no handler, porque o MockMvc não aplica os limites do Tomcat.

## Fase 3 — fundação Collector (~10 h, depois de T002)

- [x] T016–T024 (no worktree local do Collector, **sem commit**): multipart; security do path interno; `ObviousBinaryDetector`; serviço (validação → claim `FileSource.UPLOAD` → cota → OpenObserve → fila); publicação com `fileSource=upload` e `idempotencyId` composto; controller; métricas `duplicate_file` e `duplicate_in_flight`. O Consultor Review aprovou para commit com ressalvas.

## Fase 4 — testes Collector (~12 h)

- [x] T025–T031 (no worktree local, **sem commit**): testes de aceitação relatados no verify de **480 testes, 0 falhas**, 21/11/2026 13:44 (America/Sao_Paulo).
- [x] T032 (no worktree local, **sem commit**): claim em andamento → 503 + `Retry-After` / `UNAVAILABLE` (B1, opção (b)); 409 só depois do `done`.

## Fase 5 — docs e verify (~2 h)

- [x] T033 [Core] (publicada em [`f8f3f4aef1d31b514ed413760ceae12f0b02aba5`](https://github.com/LhamaLog/lhamalog-core/commit/f8f3f4aef1d31b514ed413760ceae12f0b02aba5)): seção “Upload manual (LLT-292)” no [README do Core](https://github.com/LhamaLog/lhamalog-core/blob/f8f3f4aef1d31b514ed413760ceae12f0b02aba5/README.md) (rota, limites, token por env, 403), além de compose e `.env.example`. Sem OpenAPI. A nota no README do Collector continua pendente (T033 [Coll]).
- [x] T034 [Core]: `./mvnw -B verify` relatado **depois dos commits**: **434 testes, 0 falhas**, 21/11/2026 12:48 (America/Sao_Paulo). Não reexecutado nesta máquina ao redigir estes documentos. T034 [Coll] continua pendente.

## Documentação no lhamalog-docs (Review B2)

- [x] Consolidar spec, plano, tarefas e análise com as 12 decisões, a publicação do Core (PR #15) e a dependência da LLT-290 (B1 resolvida com a opção (b)).
- [x] Registrar as três decisões de 20/11 que divergem de ADRs aceitas, com permalinks no SHA `f8f3f4aef1d31b514ed413760ceae12f0b02aba5` e citações de classe e método.
- [x] Rascunhar as ADR propostas 171–174 em `Documentações/Diagrama ADR/` (números sugeridos, status Proposto, até o Michel confirmar). Não editar ADRs existentes nem `entrega-academica/`.
- [ ] Commit, push e PR desta pasta: não executados (sem autorização nesta etapa).
