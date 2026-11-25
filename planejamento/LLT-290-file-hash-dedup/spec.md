# Especificação: hash MD5 por arquivo e saúde do Collector

**Branch de implementação**: `feature/LLT-290-file-hash-dedup` (spec 010 no Collector)

**Data**: 2026-11-21

**Estado**: decisões 1–19 e 20–22 (B1, opção (b)) registradas; código **publicado** na branch `feature/LLT-290-file-hash-dedup` (ponta `44d36b4c9b5045b9c860c1abc3b9b4f5d15f3e4e`, push feito, sem PR). Verify depois dos commits: **412 testes, 0 falhas**, 21/11/2026 13:13 (America/Sao_Paulo). N1–N5 resolvidos; o R18 registra o débito duplo de cota e a segunda escrita no OpenObserve.

**Fonte**: LLT-290, spec `010-file-hash-dedup` do Collector, material exportado em `/workspace/rev/llt290/` (`review-llt290-b1.md`, `llt290-delta-b1.diff`, `verify-summary-v3.txt`), decisões do Michel às 16:59 e 17:10 de 20/11 e à 12:43 de 21/11/2026 (America/Sao_Paulo).

## Cenários de uso e validação

### 1. Recusar o mesmo arquivo duas vezes (P1)
Como produtor OTLP, quero que um reenvio idêntico do mesmo corpo, no mesmo tenant e produto, seja recusado e não entre de novo na fila nem debite saldo — **depois** que o primeiro aceite tiver sido gravado (`done`).

Validação independente: o mesmo payload por HTTP e por gRPC; 200 no primeiro e 409/`ALREADY_EXISTS` no segundo; o stream cresce 1; nenhuma reserva no Core no segundo envio.

Aceite: o hash usa os bytes descomprimidos (gzip e identity colidem); HTTP e gRPC compartilham a origem `otlp`; tenants ou produtos diferentes com o mesmo corpo são aceitos; origem `upload` (reservada à LLT-292) não colide com `otlp`. 409 só depois do marcador `done`.

### 2. Expirar com a retenção, soltar o claim em falha e recusar em andamento de forma retentável (P1)
Como operador, quero que o hash viva o tempo da retenção do tenant, que uma falha retentável não prenda o arquivo e que um segundo envio enquanto o primeiro ainda processa seja recusado de forma retentável.

Validação independente: TTL de 30 dias quando o Core informa `retentionDays`; 7 dias de fallback; após expirar, o mesmo corpo é aceito; falha antes de gravar libera o claim; claim em andamento → HTTP 503 + `Retry-After` / gRPC `UNAVAILABLE` + `RetryInfo`, sem reserva nem publicação; depois do `release`, o reenvio é aceito.

Aceite: Redis fora não recusa a ingestão (fail-open, com WARN). Claim em andamento **não** é 409: é a decisão 20 (B1, opção (b)).

### 3. Saúde HTTP e gRPC (P1)
Como balanceador ou operador, quero saber se o Collector está apto, sem token, nas mesmas portas do OTLP.

Validação independente: `GET` e `HEAD /health` na porta OTLP/HTTP; `grpc.health.v1` (Check e Watch) na porta OTLP/gRPC, fora do interceptor de token; 503 / `NOT_SERVING` se Mongo, Redis ou OpenObserve cair; `stop()` vai para `NOT_SERVING`.

Aceite: o `/health` responde antes do limite de requisições em voo; o corpo HTTP é só `ok` ou `not ok`; o Actuator da porta 9464 não muda.

## Requisitos

- FR-001: calcular MD5 dos bytes descomprimidos do export (logs e traces; HTTP após gzip; gRPC via serialização do `Export*ServiceRequest`).
- FR-002: chave Redis `lhamalog:dedup:file:{tenantId}:{productId}:{signal}:{source}:{md5}`; `source` é `otlp` (HTTP e gRPC juntos) ou `upload` (LLT-292).
- FR-003: claim atômico em Lua em `RedisFileHashStore.claim` (`SET NX PX`; se a chave existir, `GET`): devolve `CLAIMED`, `DONE` ou `IN_FLIGHT`. Commit e release em Lua só se o dono ainda for o dono. TTL de claim 2 min (`lhamalog.file-dedup.claim-ttl`). TTL final = retenção do tenant ou fallback de 7 dias.
- FR-004: checagem depois do limite de tamanho e antes da reserva de cota (`BatchIngestion`, inclusive no caminho `IN_FLIGHT`).
- FR-005: chave `done` → HTTP 409 com `google.rpc.Status` `ALREADY_EXISTS` / gRPC `ALREADY_EXISTS` (`IngestionDecision.DuplicateFile`); sem publicação e sem reserva.
- FR-005b: claim em andamento → `IngestionDecision.DuplicateInFlight`: HTTP 503 + `Retry-After` (padrão 5 s, `lhamalog.file-dedup.in-flight-retry-after`) via `OtlpHttpStatusMapper.unavailable`; gRPC `UNAVAILABLE` com `RetryInfo` em `OtlpGrpcServer`; métrica `refused{reason=duplicate_in_flight}`; também sem reserva, gravação ou publicação.
- FR-006: Redis indisponível no dedup → segue a ingestão, com WARN e métrica (fail-open). Isso é propositalmente diferente do health (FR-011).
- FR-007: `idempotencyId = UUIDv3("<batchId>:<signal>:<source>:<md5>")`; metadata `fileMd5` e `fileSource`. Com o dedup desligado, o id volta a ser o `batchId`.
- FR-008: métricas `lhamalog.ingestion.refused{reason=duplicate_file}` (só `done`) e `refused{reason=duplicate_in_flight}` (em andamento).
- FR-009: propriedades `lhamalog.file-dedup.enabled`, `fallback-ttl`, `claim-ttl` (padrão `2m`) e `in-flight-retry-after` (padrão `5s`, mínimo 1 s).
- FR-010: pacotes `dedup/` e `health/` no Collector.
- FR-011: `GET`/`HEAD /health` e `grpc.health.v1`; 503 se Mongo, Redis **ou** OpenObserve estiver fora; sondas em paralelo, timeout e cache de 2 s.

### Entidades conceituais

- Identidade do arquivo: `signal`, `source` e fingerprint MD5, no escopo de tenant e produto.
- Claim: chave provisória com token de dono (`FileHashStore.ClaimResult`: `CLAIMED` / `DONE` / `IN_FLIGHT`); depois `done` (commit) ou removida (release). `FileClaim.Outcome.DUPLICATE` vale só para `done`; `IN_FLIGHT` é o claim de outra requisição.
- Saúde do Collector: retrato das três dependências, cacheado por poucos segundos.

## Critérios de sucesso

- SC-001: segundo envio idêntico, com a chave já `done`, recebe 409/`ALREADY_EXISTS` e não publica de novo.
- SC-002: a duplicata concluída e o claim em andamento não chamam reserva de cota.
- SC-003: TTL final da chave segue a retenção ou 7 dias; TTL de claim é 2 min.
- SC-004: Redis fora no dedup não derruba a ingestão.
- SC-005: `/health` e `grpc.health.v1` devolvem 503/`NOT_SERVING` com qualquer uma das três dependências fora.
- SC-006: verify do Collector verde após os commits (atingido: 412 testes, 0 falhas, 21/11/2026 13:13, America/Sao_Paulo).
- SC-007: segundo envio com o claim ainda vivo recebe HTTP 503 + `Retry-After` / gRPC `UNAVAILABLE` + `RetryInfo`; depois do `release`, o reenvio é aceito.

## Premissas e limites

- Upload manual fica na LLT-292; esta feature só reserva `FileSource.UPLOAD` e deixa o serviço reaproveitável.
- `schemaVersion` da mensagem e `openobserve.batchId` não mudam.
- `/ping` permanece removido (ADR_118). Health do Core e Actuator 9464 ficam como estão.
- Não alterar ADRs existentes, Jira ou `.env` versionado.
- Esta pasta documenta; não substitui a spec 010 no repositório do Collector.
- **Risco residual N1 / R18 (explícito):** se uma requisição ultrapassar os 2 min do `claim-ttl`, ela perde o claim e uma cópia igual pode ser aceita em paralelo. Essa cópia **debita cota de novo** e **grava de novo no OpenObserve** (além de poder publicar de novo na fila, com o mesmo `idempotencyId`). O commit da primeira devolve 0 (WARN). A justificativa dos 2 min no research R18 do Collector afirma que a requisição mais lenta fica bem abaixo de 1 min; **essa premissa não está demonstrada** no material (depende dos timeouts do sink do OpenObserve e das retentativas de `AbstractStreamPublisher`). Não se descreve o risco residual só como “uma publicação a mais”. O Consultor Review considerou o risco baixo e aceitável para o MVP, mas pediu que esses efeitos fiquem registrados. Um exportador com `max_elapsed_time` menor que cerca de 2 min, ou com retry desligado, ainda pode desistir diante de um claim órfão.

## Esclarecimentos (Michel, 20/11/2026)

Registro das decisões 1–19, às 16:59 e 17:10 (America/Sao_Paulo), repassadas pelo BimBot Escola de TI. Texto completo na spec 010 do Collector.

1. MD5 dos bytes descomprimidos, logs e traces, HTTP e gRPC.
2. Sem `retentionDays`, TTL de 7 dias (configurável).
3. Redis fora no dedup: deixa passar, com WARN.
4. Duplicata **concluída** (`done`): 409 / `ALREADY_EXISTS`.
5. Checagem antes da reserva de cota.
6. MD5 composto com o `batchId`, não o substitui sozinho.
7. Saúde entregue junto com a LLT-290; depois LLT-292; depois LLT-291.
8. `/health` responde 503 se Mongo, OpenObserve **ou** Redis estiver fora (diferente do fail-open da ingestão).
9. Rotas em inglês no padrão do código; auth interna por `X-LhamaLog-Service-Token` (sem mudança nesta feature).
10. LLT-292 segue as ADRs (Core `POST /manual/upload` no desenho original); o serviço de hash fica reaproveitável. O contrato público foi precisado depois, na LLT-292, como `POST /api/manual/upload`.
11–12. A chave inclui `signal` e `source`; `otlp` une HTTP e gRPC; `upload` é outra origem.
13. `idempotencyId = UUIDv3("<batchId>:<signal>:<source>:<md5>")`; metadata `fileMd5` e `fileSource`.
14. ~~Claim TTL de 10 min.~~ **Substituído pela decisão 21** (2 min, 21/11). O reenvio depois de publicação parcial (`done`) continua recebendo 409 (aceito; a decisão 19 não muda).
15. Saúde sem card próprio; aviso ao João Pedro (LLT-270) sobre o `idempotencyId` fica com o BimBot.
16. Com `lhamalog.file-dedup.enabled=false`, não há claim e o `idempotencyId` permanece o `batchId`.
17. Com Redis fora, o MD5 ainda entra no `idempotencyId`; só o claim é pulado.
18. UUIDv3 no mesmo padrão de `RecordIds`: `UUID.nameUUIDFromBytes(...)`.
19. A decisão 14 já fechava o 409 após publicação parcial (`publishedBeforeFailure`); isso permanece, agora só para a chave `done`.

## Esclarecimentos (Michel, 21/11/2026 12:43) — B1, opção (b)

Registro: decidido pelo Michel em 21/11/2026 às 12:43 (America/Sao_Paulo), repassado pelo BimBot Escola de TI. Opção **(b)** do Review B1; substitui a parte de “claim em andamento” da decisão 14 e o TTL de 10 min.

20. **Claim em andamento é retentável:** enquanto a chave guarda o claim de outra requisição, o mesmo arquivo recebe HTTP **503 + `Retry-After`** (`lhamalog.file-dedup.in-flight-retry-after`, padrão 5 s) com `google.rpc.Status` `UNAVAILABLE` + `RetryInfo`, e gRPC **`UNAVAILABLE` + `RetryInfo`**. **409 / `ALREADY_EXISTS` só quando a chave está `done`.**
21. **Claim TTL de 2 min** (`lhamalog.file-dedup.claim-ttl`, padrão `2m`). O TTL final não muda (retenção do tenant ou 7 dias). A justificativa de que 2 min cobrem a requisição mais lenta está no research R18 do Collector; a premissa de “bem abaixo de 1 min” **não está demonstrada** (ver risco residual N1 / R18 acima).
22. Falha sem gravar continua liberando o claim (release com conferência do dono); Redis fora continua pulando a checagem com WARN. `idempotencyId` e a métrica `duplicate_file` não mudam; entra a razão `refused{reason=duplicate_in_flight}`.
