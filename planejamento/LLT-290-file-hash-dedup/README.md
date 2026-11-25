# LLT-290 — Hash MD5 por arquivo e saúde do Collector

Entrega documental da [LLT-290](https://logviewer2026.atlassian.net/browse/LLT-290), atualizada em 21/11/2026 (America/Sao_Paulo) após a publicação no Collector. Cobre o dedup por hash do arquivo no Collector e os endpoints de saúde (ADR_118 e ADR_141), incluídos nesta feature por decisão do Michel.

O trabalho está **publicado** na branch [`feature/LLT-290-file-hash-dedup`](https://github.com/LhamaLog/lhamalog-collector/tree/feature/LLT-290-file-hash-dedup), com push feito e **sem PR**, conforme o combinado com o Michel. Ponta `44d36b4c9b5045b9c860c1abc3b9b4f5d15f3e4e`, base `5fb3160` (`origin/Development`).

- [Escopo, decisões e critérios de aceite](spec.md)
- [Plano](plan.md)
- [Tarefas e validação](tasks.md)
- [Achados do Consultor Review, evidências de código e pendências](analysis.md)

As citações do Collector, quando apontam arquivo, usam permalink com o SHA da ponta `44d36b4c9b5045b9c860c1abc3b9b4f5d15f3e4e`; o restante segue por classe e método. O verify depois dos commits foi relatado em **412 testes, 0 falhas**, 21/11/2026 13:13 (America/Sao_Paulo).

**B1 (resolvido, opção (b)):** claim em andamento recebe HTTP **503 + `Retry-After`** (padrão 5 s, `lhamalog.file-dedup.in-flight-retry-after`) / gRPC **`UNAVAILABLE` com `RetryInfo`**. **409 / `ALREADY_EXISTS` só depois do marcador `done`.** O claim TTL é **2 min** (`lhamalog.file-dedup.claim-ttl`); o TTL final não muda (retenção do tenant ou fallback de 7 dias). O script atômico no Redis devolve `CLAIMED` / `DONE` / `IN_FLIGHT`. A recusa em andamento ocorre antes da reserva de cota, com a métrica `refused{reason=duplicate_in_flight}`. Decisões 20–22 do Michel em 21/11/2026 12:43 (America/Sao_Paulo), repassadas pelo BimBot. N1–N5 estão resolvidos. O R18 registra o débito duplo de cota e a segunda escrita no OpenObserve se a requisição passar de 2 min; a premissa de duração “abaixo de 1 min” não está demonstrada.

## Commits no Collector

Na branch `feature/LLT-290-file-hash-dedup` (sem PR):

- [`3894325d0eeeca833b4def4422eceb41bea233b2`](https://github.com/LhamaLog/lhamalog-collector/commit/3894325d0eeeca833b4def4422eceb41bea233b2) — spec 010
- [`50aa8ee576d4ca877cc918e1c2f558e6ac400bfe`](https://github.com/LhamaLog/lhamalog-collector/commit/50aa8ee576d4ca877cc918e1c2f558e6ac400bfe) — serviço de dedup
- [`f497633af68ba37e71914e0530e7f977cb795040`](https://github.com/LhamaLog/lhamalog-collector/commit/f497633af68ba37e71914e0530e7f977cb795040) — recusa 409/503
- [`04ee96820f3e877c358063ef160db15c6d2febb8`](https://github.com/LhamaLog/lhamalog-collector/commit/04ee96820f3e877c358063ef160db15c6d2febb8) — `idempotencyId`
- [`c9f1a1b1755ae49b3f14524af7e0890d48986be5`](https://github.com/LhamaLog/lhamalog-collector/commit/c9f1a1b1755ae49b3f14524af7e0890d48986be5) — saúde
- [`44d36b4c9b5045b9c860c1abc3b9b4f5d15f3e4e`](https://github.com/LhamaLog/lhamalog-collector/commit/44d36b4c9b5045b9c860c1abc3b9b4f5d15f3e4e) — docs (ponta da branch)

## Proposta de ADR (não criada)

Não foi aberto um arquivo novo em `Documentações/Diagrama ADR/` para o dedup. A saúde já está nas ADR_118 e ADR_141.

Conferência no Google Drive (pasta de ADRs) em **20/11/2026 23:30 (America/Sao_Paulo)**: as ADR_167 a ADR_170 já existem lá; não há ADR_171 ou superior. Os rascunhos da LLT-292 usam os números propostos 171–174. Uma futura ADR de **deduplicação por hash MD5 do arquivo no Redis** usaria o próximo número livre depois de 174 (ou seja, 175), ainda sujeito a nova conferência no Drive e à confirmação do Michel.

Quando for criada, essa ADR deve registrar identidade (`tenant`, `produto`, `signal`, `source`, MD5 dos bytes descomprimidos), chave `lhamalog:dedup:file:…`, claim atômico em Lua (`SET NX PX` e, se a chave existir, `GET` → `CLAIMED` / `DONE` / `IN_FLIGHT`), 409/`ALREADY_EXISTS` só com a chave `done`, claim em andamento → 503 + `Retry-After` / gRPC `UNAVAILABLE` + `RetryInfo`, claim TTL de 2 min, TTL final inalterado, fail-open se o Redis cair, `idempotencyId` composto, a decisão B1 (opção (b), 21/11) e o risco residual do R18 (débito duplo de cota e dupla escrita no OpenObserve se a requisição passar de 2 min; a premissa de “abaixo de 1 min” não está demonstrada). Não alterar ADRs existentes.

Branch desta pasta no lhamalog-docs: `LLT-290-292-planejamento`, a partir de `main` (`fe59368`). Sem commit, push ou PR desta documentação até o OK do Michel. Quando autorizado, a sugestão (ADR_148, um commit por card) é fazer commits separados nesta mesma branch, no formato `LLT-290: …` e `LLT-292: …`.
