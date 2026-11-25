# Plano — LLT-292

## Entrega

Documentar no lhamalog-docs o upload manual via Core, com as 12 decisões de 20/11/2026 22:45 (America/Sao_Paulo), a dependência da LLT-290 (B1 resolvida com a opção (b)) e, para o Consultor Review B2, o registro das decisões de 20/11 que divergem de ADRs aceitas. Nenhuma alteração em ADRs existentes, em `entrega-academica/` ou nos repositórios de código a partir desta pasta.

A implementação do Core está **publicada** na branch `feature/LLT-292-manual-upload`, no PR [#15](https://github.com/LhamaLog/lhamalog-core/pull/15) (base `Development`, aberto, ainda não mesclado). A implementação do Collector está num worktree local, ainda **sem commit** (verify relatado: 480 testes, 0 falhas, 21/11/2026 13:44, America/Sao_Paulo); o Consultor Review a aprovou para commit com ressalvas.

## Etapas do Spec Kit

1. Specify: caminho front → Core → Collector, fora do card desatualizado (token OTLP / 5 MB).
2. Clarify: 12 perguntas, todas confirmadas pelo Michel às 22:45 (America/Sao_Paulo).
3. Plan: pacotes `core/upload/` e `collector/upload/`; reuso de `dedup`, cota, OpenObserve e fila.
4. Tasks: T001 e T003–T015 feitas no Core e publicadas no PR #15; T002 criada no worktree local do Collector (base da LLT-290 publicada); implementação do Collector feita, ainda sem commit.
5. Analyze: relatório de 20/11/2026 ~22:55 (America/Sao_Paulo); depois, Review do Core (`review-core.md` e rodadas seguintes). O B2 pedia o registro no lhamalog-docs antes do PR; o rascunho existia e o PR #15 já foi aberto.
6. Implement (Core): publicada nos commits `0a202c8` (spec/contratos), `e44ee1d` (validação, propriedades e limites), `9ac348d` (encaminhamento ao Collector), `026c236` (endpoint e handler de 413) e `f8f3f4a` (README, compose e `.env.example`), ponta `f8f3f4aef1d31b514ed413760ceae12f0b02aba5`. Implement (Collector): feita no worktree local, ainda sem commit; Review aprovou com ressalvas.

Documentação B2 (esta pasta, sem commit; alinhada à publicação do Core e à B1 da LLT-290 resolvida com a opção (b)): rascunhos das ADR propostas 171–174 e atualização de `planejamento/LLT-292-manual-upload/` com permalinks no SHA da ponta e citações de classe e método.

Não foi instalado o Spec Kit neste repositório de documentação.

## Fases de implementação

1. **Core** (publicada no PR #15, ainda não mesclada): contrato público, autorização 403, validador, cliente HTTP, mapeamento de status; testes com Collector dublado. Verify depois dos commits: **434 testes, 0 falhas**, 21/11/2026 12:48 (America/Sao_Paulo). N1–N4 estão fechados (URL em branco ou sem esquema → WARN e 503; 413 do contêiner classificado pelos tipos e textos do Tomcat 11.0.24; merge por posição e filename, com `UNKNOWN`/`collector_result_missing`; teto de 64 KB testado com JSON válido e WARN). Limite conhecido: o 413 do contêiner é testado só no handler.
2. **Collector** (implementada no worktree local, ainda sem commit; verify 480 testes, 21/11/2026 13:44, America/Sao_Paulo; Review aprovou para commit com ressalvas): endpoint interno, magic bytes, dedup `upload`, cota, OpenObserve, fila; testes de aceitação. Herda a B1 da LLT-290 já resolvida com a opção (b): claim em andamento → **503 retentável** (HTTP 503 + `Retry-After` / gRPC `UNAVAILABLE`); 409 só depois do `done`. Claim TTL de 2 min.
3. **Integração local**, sem mexer nos outros worktrees.

## Validação proporcional

Nesta etapa documental: conferência das decisões × ADRs aceitas × código publicado do Core e alinhamento dos rascunhos 171–174 à B1 resolvida e ao PR #15. As citações do Core usam permalink com o SHA `f8f3f4aef1d31b514ed413760ceae12f0b02aba5` quando apontam arquivo, e classe e método no restante. Testes Maven desta pasta não se aplicam e não serão reportados como executados. O verify do Core é o relato acima (434 testes em 21/11/2026 12:48, America/Sao_Paulo); o do Collector entra na T034 depois da implementação.

## Publicação

Branch `LLT-290-292-planejamento` criada de `origin/main` (`fe59368`), no padrão `LLT-NNN-slug` deste repositório. Commit, push e PR **desta pasta** **não** foram autorizados nesta etapa. Os números de ADR 171–174 são propostos até o Michel confirmar. Quando houver OK para o commit desta documentação, a sugestão (ADR_148) é commits separados nesta mesma branch: `LLT-290: …` e `LLT-292: …`. A implementação do Core já está no PR [#15](https://github.com/LhamaLog/lhamalog-core/pull/15), aberto e ainda não mesclado.
