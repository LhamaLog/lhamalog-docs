# Tarefas — LLT-290

Estado no Collector, em 21/11/2026 (America/Sao_Paulo). Esta lista documenta o andamento; não reabre o Spec Kit.

- [x] T001–T024: fundação, dedup (US1–US2), saúde HTTP/gRPC (US3–US4) e polish no worktree.
- [x] T025: `mvnw clean verify` — 393 testes, 20/11/2026 17:37 (America/Sao_Paulo).
- [x] T026: revisão do princípio VI e proposta dos commits (não executados).
- [x] T027–T040: ajustes do Consultor Review (I1–I5, S1–S3, S6, S8–S10; S4, S5 e S7 só documentados). Verify pós-review: 400 testes, 20/11/2026 18:01 (America/Sao_Paulo).
- [x] T041 [B1]: decisão do Michel (21/11/2026 12:43, America/Sao_Paulo): **opção (b)**; implementada em T042–T046.
- [x] T042 [B1]: `FileHashStore.ClaimResult` (`CLAIMED` / `DONE` / `IN_FLIGHT`); `RedisFileHashStore.claim` em Lua (`SET NX PX`, senão `GET`); `FileClaim.Outcome.IN_FLIGHT`; `FileDeduplication` mapeia `DONE` → `DUPLICATE` e o claim de outro dono → `IN_FLIGHT`.
- [x] T043 [B1]: `IngestionDecision.DuplicateInFlight(retryAfterSeconds)`; HTTP 503 + `Retry-After` + `RetryInfo` (`OtlpHttpStatusMapper.unavailable`); gRPC `UNAVAILABLE` + `RetryInfo` (`OtlpGrpcServer`); `BatchIngestion` recusa antes da reserva, com `refused{reason=duplicate_in_flight}` e INFO `event=ingestion.file_dedup.in_flight`.
- [x] T044 [B1]: `lhamalog.file-dedup.claim-ttl` 10m → **2m**; nova `lhamalog.file-dedup.in-flight-retry-after` (padrão **5s**, mínimo 1 s) em `FileDedupProperties` e `application.properties`.
- [x] T045 [B1]: testes de 503 / `UNAVAILABLE`, 409 só para `done`, claim expirado e liberação (`OtlpDuplicateFileTransportTest`, `BatchIngestionFileDedupTest`, `RedisFileHashStoreTest`, `FileDeduplicationTest`, `OtlpHttpQuotaStatusMapperTest`, `IngestionDecisionOutcomesTest`).
- [x] T046 [B1]: docs da spec 010 (decisões 20–22, FR, R18 com débito duplo de cota e segunda escrita no OpenObserve, contratos, README, runbook) publicadas em `44d36b4`. `mvnw clean verify` relatado **depois dos commits**: **412 testes, 0 falhas**, 21/11/2026 13:13 (America/Sao_Paulo). N1–N5 resolvidos.

Publicação no Collector: commits no formato `LLT-290: descricao`, push da branch `feature/LLT-290-file-hash-dedup` já feitos, **sem PR**, conforme o Michel. Ponta `44d36b4c9b5045b9c860c1abc3b9b4f5d15f3e4e`. Nada na `Development`.

Nesta pasta do lhamalog-docs:

- [x] Consolidar spec, plano, tarefas e análise com citações de classe e método.
- [x] Registrar B1 como resolvido com a opção (b), o verify de 412 testes depois dos commits, N1–N5 resolvidos e o risco residual do R18 (débito duplo de cota e dupla escrita no OpenObserve se a requisição passar de 2 min; premissa de “abaixo de 1 min” não demonstrada).
- [x] Propor ADR de dedup no README, sem criar arquivo; a proposta já inclui a decisão B1 e o risco residual do R18.
- [ ] Commit, push e PR: não executados (sem autorização nesta etapa).
