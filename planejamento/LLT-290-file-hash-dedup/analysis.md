# Análise e impactos — LLT-290

## Evidências inspecionadas

Código do Collector **publicado** na branch [`feature/LLT-290-file-hash-dedup`](https://github.com/LhamaLog/lhamalog-collector/tree/feature/LLT-290-file-hash-dedup), ponta [`44d36b4c9b5045b9c860c1abc3b9b4f5d15f3e4e`](https://github.com/LhamaLog/lhamalog-collector/commit/44d36b4c9b5045b9c860c1abc3b9b4f5d15f3e4e), base `5fb3160`, push feito e **sem PR**. Material de apoio em `/workspace/rev/llt290/` (`review-llt290.md`, `review-llt290-b1.md`) e na spec 010 do próprio Collector. Permalinks usam o SHA da ponta, em caminhos confirmados nessa árvore; o restante é classe e método.

### Deduplicação

- [`FileFingerprint`](https://github.com/LhamaLog/lhamalog-collector/blob/44d36b4c9b5045b9c860c1abc3b9b4f5d15f3e4e/src/main/java/br/com/lhamalog/collector/dedup/FileFingerprint.java): MD5 dos bytes recebidos (já descomprimidos no HTTP).
- [`FileSource`](https://github.com/LhamaLog/lhamalog-collector/blob/44d36b4c9b5045b9c860c1abc3b9b4f5d15f3e4e/src/main/java/br/com/lhamalog/collector/dedup/FileSource.java): `OTLP("otlp")` e `UPLOAD("upload")`. HTTP e gRPC compartilham `otlp`.
- [`FileDeduplication`](https://github.com/LhamaLog/lhamalog-collector/blob/44d36b4c9b5045b9c860c1abc3b9b4f5d15f3e4e/src/main/java/br/com/lhamalog/collector/dedup/FileDeduplication.java): chave `lhamalog:dedup:file:{tenantId}:{productId}:{signal}:{source}:{md5}`; Redis fora → `STORE_UNAVAILABLE`, WARN `event=ingestion.file_dedup.store_unavailable`, a requisição segue; TTL final = `retentionDays` ou `fallbackTtl` (7 dias). Mapeia `FileHashStore.ClaimResult.DONE` → `FileClaim.Outcome.DUPLICATE` e o claim de outro dono → `IN_FLIGHT`.
- [`RedisFileHashStore.claim`](https://github.com/LhamaLog/lhamalog-collector/blob/44d36b4c9b5045b9c860c1abc3b9b4f5d15f3e4e/src/main/java/br/com/lhamalog/collector/dedup/RedisFileHashStore.java): script Lua atômico (`SET NX PX`; se a chave existir, `GET`). Devolve `CLAIMED`, `DONE` (valor `"done"`) ou `IN_FLIGHT`. Commit e release em Lua só se o dono ainda for o dono.
- [`FileClaim.Outcome`](https://github.com/LhamaLog/lhamalog-collector/blob/44d36b4c9b5045b9c860c1abc3b9b4f5d15f3e4e/src/main/java/br/com/lhamalog/collector/dedup/FileClaim.java): `CLAIMED | DUPLICATE | IN_FLIGHT | STORE_UNAVAILABLE | DISABLED`. `DUPLICATE` vale só para a chave `done`; `IN_FLIGHT` é o claim de outra requisição.
- [`BatchIngestion`](https://github.com/LhamaLog/lhamalog-collector/blob/44d36b4c9b5045b9c860c1abc3b9b4f5d15f3e4e/src/main/java/br/com/lhamalog/collector/ingestion/otlp/application/BatchIngestion.java): a checagem vem depois do limite de tamanho e **antes** de `admit` / reserva de cota. `IN_FLIGHT` vira `IngestionDecision.DuplicateInFlight` com `refused{reason=duplicate_in_flight}` e INFO `event=ingestion.file_dedup.in_flight`.
- [`OtlpHttpStatusMapper`](https://github.com/LhamaLog/lhamalog-collector/blob/44d36b4c9b5045b9c860c1abc3b9b4f5d15f3e4e/src/main/java/br/com/lhamalog/collector/ingestion/otlp/http/OtlpHttpStatusMapper.java): `DuplicateFile` → 409 / `ALREADY_EXISTS`; `DuplicateInFlight` → `unavailable` (HTTP 503 + `Retry-After` + `RetryInfo`).
- [`OtlpGrpcServer`](https://github.com/LhamaLog/lhamalog-collector/blob/44d36b4c9b5045b9c860c1abc3b9b4f5d15f3e4e/src/main/java/br/com/lhamalog/collector/ingestion/otlp/grpc/OtlpGrpcServer.java): `DuplicateInFlight` → `Status.UNAVAILABLE` com `RetryInfo`.
- [`FileIdentity`](https://github.com/LhamaLog/lhamalog-collector/blob/44d36b4c9b5045b9c860c1abc3b9b4f5d15f3e4e/src/main/java/br/com/lhamalog/collector/dedup/FileIdentity.java): `idempotencyId = UUIDv3("<batchId>:<signal>:<source>:<md5>")`.
- [`MetadataKeys`](https://github.com/LhamaLog/lhamalog-collector/blob/44d36b4c9b5045b9c860c1abc3b9b4f5d15f3e4e/src/main/java/br/com/lhamalog/collector/messaging/MetadataKeys.java) e [`TelemetryIngestedPublisher`](https://github.com/LhamaLog/lhamalog-collector/blob/44d36b4c9b5045b9c860c1abc3b9b4f5d15f3e4e/src/main/java/br/com/lhamalog/collector/ingestion/otlp/sink/TelemetryIngestedPublisher.java): metadata `fileMd5` e `fileSource`.
- [`IngestionObservability`](https://github.com/LhamaLog/lhamalog-collector/blob/44d36b4c9b5045b9c860c1abc3b9b4f5d15f3e4e/src/main/java/br/com/lhamalog/collector/ingestion/otlp/application/IngestionObservability.java): reasons `duplicate_file` (só `done`) e `duplicate_in_flight`.
- [`FileDedupProperties`](https://github.com/LhamaLog/lhamalog-collector/blob/44d36b4c9b5045b9c860c1abc3b9b4f5d15f3e4e/src/main/java/br/com/lhamalog/collector/dedup/FileDedupProperties.java) e [`application.properties`](https://github.com/LhamaLog/lhamalog-collector/blob/44d36b4c9b5045b9c860c1abc3b9b4f5d15f3e4e/src/main/resources/application.properties): `claim-ttl=2m`, `in-flight-retry-after=5s`.

### Saúde

- [`OtlpHttpServer`](https://github.com/LhamaLog/lhamalog-collector/blob/44d36b4c9b5045b9c860c1abc3b9b4f5d15f3e4e/src/main/java/br/com/lhamalog/collector/ingestion/otlp/http/OtlpHttpServer.java): `GET` e `HEAD /health`, sem token, **antes** do semáforo `inFlight`.
- [`OtlpGrpcServer`](https://github.com/LhamaLog/lhamalog-collector/blob/44d36b4c9b5045b9c860c1abc3b9b4f5d15f3e4e/src/main/java/br/com/lhamalog/collector/ingestion/otlp/grpc/OtlpGrpcServer.java): `grpc.health.v1`; `stop()` chama `enterTerminalState()` (`NOT_SERVING`).
- [`CollectorHealth`](https://github.com/LhamaLog/lhamalog-collector/blob/44d36b4c9b5045b9c860c1abc3b9b4f5d15f3e4e/src/main/java/br/com/lhamalog/collector/health/CollectorHealth.java) e [`CollectorHealthConfiguration`](https://github.com/LhamaLog/lhamalog-collector/blob/44d36b4c9b5045b9c860c1abc3b9b4f5d15f3e4e/src/main/java/br/com/lhamalog/collector/config/CollectorHealthConfiguration.java): 503 se Mongo, Redis ou OpenObserve cair.
- [`HealthProperties`](https://github.com/LhamaLog/lhamalog-collector/blob/44d36b4c9b5045b9c860c1abc3b9b4f5d15f3e4e/src/main/java/br/com/lhamalog/collector/health/HealthProperties.java) e [`CollectorHealthChecker`](https://github.com/LhamaLog/lhamalog-collector/blob/44d36b4c9b5045b9c860c1abc3b9b4f5d15f3e4e/src/main/java/br/com/lhamalog/collector/health/CollectorHealthChecker.java): timeout 2 s, cache 2 s, sondas em paralelo.

São evidências da branch publicada, ainda não da `Development`.

## Achados do Consultor Review e status

Primeira revisão em 20/11/2026 (`review-llt290.md`). O delta do B1 foi reavaliado em 21/11 (`review-llt290-b1.md`): apto para commit com ressalvas. Essas ressalvas (N1–N5) foram tratadas antes da publicação. Verify depois dos commits: **412 testes, 0 falhas**, 21/11/2026 13:13 (America/Sao_Paulo).

| Id | Gravidade | Resumo | Status em 21/11/2026 13:13 |
| --- | --- | --- | --- |
| **B1** | Resolvido | Opção (b): HTTP 503 + `Retry-After` / gRPC `UNAVAILABLE` + `RetryInfo` no `IN_FLIGHT`; 409 só no `done`. Claim TTL 2 min. T041–T046 concluídas e publicadas. | **Resolvido com a opção (b).** |
| I1–I5 | Importante | Contratos, memória do Redis, teste de `NOT_SERVING`, hipótese do `usage.enabled`. | **Fechados** (código ou documentação, conforme a rodada de 20/11 e o commit de docs). |
| **N1 / R18** | Ressalva de texto, resolvida | O risco residual não é só “uma publicação a mais”. | **Resolvido no R18 publicado:** se a requisição passar de 2 min, a cópia paralela **debita cota de novo** e **grava de novo no OpenObserve**; a premissa de duração “abaixo de 1 min” **não está demonstrada**. |
| N2–N5 | Menores | Fração em `in-flight-retry-after`; nome de teste no relato; assert de `IN_FLIGHT` na corrida Redis; volume de INFO. | **Resolvidos** no código ou na documentação publicada (N2 arredonda com WARN; N4 confere `IN_FLIGHT`; N3 era só o relato; N5 permanece documentado). |

## Risco residual N1 / R18 (explícito)

O B1 de crash/processo caído fica coberto: um claim órfão gera 503 retentável por até cerca de 2 min, e o reenvio depois da expiração é aceito. Se a primeira requisição **ultrapassar** o `claim-ttl` de 2 min enquanto ainda está em curso:

- ela perde o claim;
- uma cópia igual pode ser aceita em paralelo;
- essa cópia **debita cota de novo** no Core e **grava de novo no OpenObserve** (com os mesmos `recordId`), além de poder publicar de novo na fila com o mesmo `idempotencyId`;
- o `commit` da primeira devolve 0 (WARN `commit_failed`).

Não se resume esse efeito a “uma publicação a mais”. Não há perda de dados no sentido de sumir o lote, mas há débito e escrita duplicados. A justificativa de que a requisição mais lenta ficaria bem abaixo de 1 min **não está demonstrada**. O risco foi considerado baixo e aceitável para o MVP e permanece explícito no R18 publicado.

## Resultado

O código publicado cumpre as decisões 1–19 e 20–22 (B1, opção (b)). Verify depois dos commits: 412 testes, 0 falhas, 21/11/2026 13:13 (America/Sao_Paulo). N1–N5 estão resolvidos. A branch foi enviada sem PR. A LLT-292 reutiliza `FileSource.UPLOAD` e herda o 503 retentável no claim em andamento.
