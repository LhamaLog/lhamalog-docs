# Plano — LLT-290

## Entrega

Documentar no lhamalog-docs o dedup por hash de arquivo e os endpoints de saúde do Collector, com citações de classe e método ao código ainda não commitado. Nenhuma alteração em ADRs existentes, em `entrega-academica/` ou em outros repositórios a partir desta pasta.

A implementação vive no Collector (`feature/LLT-290-file-hash-dedup`) e já está **publicada** (push feito, **sem PR**, ponta `44d36b4c9b5045b9c860c1abc3b9b4f5d15f3e4e`). Os seis commits são: `3894325` (spec 010), `50aa8ee` (serviço de dedup), `f497633` (recusa 409/503), `04ee968` (`idempotencyId`), `c9f1a1b` (saúde) e `44d36b4` (docs). O B1 foi resolvido com a opção (b) (decisões 20–22, 21/11/2026 12:43, America/Sao_Paulo). N1–N5 estão resolvidos; o R18 registra o débito duplo de cota e a segunda escrita no OpenObserve.

## Etapas do Spec Kit (no Collector)

1. Specify: delimitar US1–US4 (dedup e saúde) na spec 010.
2. Clarify: decisões 1–19 do Michel (16:59 e 17:10, 20/11, America/Sao_Paulo) e decisões 20–22 sobre o B1 (12:43, 21/11, America/Sao_Paulo).
3. Plan / research / data-model / contratos: chave Redis, respostas 409 e 503 em andamento, health, `idempotencyId`.
4. Tasks: T001–T040 no Collector; T041–T046 do B1, concluídas (opção (b)).
5. Analyze: relatório da spec 010, depois confrontado com o Consultor Review (`review-llt290.md` e `review-llt290-b1.md`).
6. Implement: pacotes `dedup/` e `health/`, integração em `BatchIngestion`, mapeadores HTTP/gRPC, contratos 001/002/004/007, README e runbook. Ajustes I1–I5 e sugestões baratas do primeiro review, e depois o delta do B1 (Lua de claim, `DuplicateInFlight`, claim TTL 2 min), já aplicados no worktree.

Não foi instalado o Spec Kit neste repositório de documentação. As etapas ficam registradas aqui e, com mais detalhe, em `specs/010-file-hash-dedup/` no Collector.

## Validação proporcional

- Verify relatado depois dos commits, 21/11/2026 13:13 (America/Sao_Paulo): `mvnw clean verify`, BUILD SUCCESS, **412 testes, 0 falhas**. Não foi reexecutado nesta máquina ao preparar estes documentos.
- Conferência documental: citações de classe e método e, quando o caminho existe na ponta `44d36b4c9b5045b9c860c1abc3b9b4f5d15f3e4e`, permalinks nesse SHA. B1 resolvida com a opção (b); N1–N5 resolvidos; o risco residual do R18 permanece explícito (débito duplo de cota e dupla escrita no OpenObserve se a requisição passar de 2 min; premissa de “abaixo de 1 min” não demonstrada).
- Testes Maven não são necessários para esta alteração exclusivamente documental no lhamalog-docs e não serão reportados como executados.

## Publicação

Branch `LLT-290-292-planejamento` criada de `origin/main` (`fe59368`). O padrão de branches deste repositório é `LLT-NNN-slug` (ex.: `LLT-169-spike-definir-catalogo-de-cargos-e-matriz-de-permissoes`), sem prefixo `docs/`. Commit, push e PR desta pasta **não** foram autorizados nesta etapa. Quando o Michel autorizar o commit desta documentação, a sugestão (ADR_148) é commits separados nesta mesma branch: `LLT-290: …` e `LLT-292: …`.
