# Especificação: upload manual de arquivos de logs (Core → Collector)

**Branches de implementação**: `feature/LLT-292-manual-upload` no Core, publicada no PR [#15](https://github.com/LhamaLog/lhamalog-core/pull/15) (base `Development`, aberto, ainda não mesclado; ponta `f8f3f4aef1d31b514ed413760ceae12f0b02aba5`). No Collector, a implementação está num worktree local a partir de `feature/LLT-290-file-hash-dedup`, ainda sem commit.

**Data**: 2026-11-21

**Estado**: specify + clarify fechado (12/12); implementação do Core publicada (PR #15, 434 testes em 21/11/2026 12:48, America/Sao_Paulo); implementação do Collector no worktree local (480 testes, 21/11/2026 13:44, America/Sao_Paulo), ainda sem commit, aprovada pelo Consultor Review para commit com ressalvas; rascunhos de ADR 171–174 (números propostos).

**Fonte**: LLT-292; decisões do Michel em 20/11/2026 (16:59, 21:37 e clarify 22:45, America/Sao_Paulo); ADRs 015, 022, 026, 028, 030, 032, 041–056, 054 (028, 032 e 041 lidas no Drive pelo Review); spec 010 do Collector; review do Core em 20/11/2026 e rodadas seguintes; B1 da LLT-290 resolvida com a opção (b) em 21/11.

## Contexto

O front fala só com o Core (ADR_054). O arquivo entra pelo Collector e vai para a fila; não há caminho do Web direto ao Finder (USID_006). O card da LLT-292 (18/11) ainda fala em endpoint público no Collector, token OTLP e 5 MB — isso foi superado em 20/11 e não é a regra desta spec. O Jira não é alterado nesta etapa.

## Cenários de uso e validação

### 1. Enviar um arquivo válido e vê-lo enfileirado (P1)
Como usuário autenticado com acesso ao produto, quero enviar um `.log` (ou outro formato aceito) pelo Core e receber 202 depois que o Collector aceitar.

Validação independente: JWT válido, produto visível e não arquivado, arquivo dentro do teto; o Core chama o Collector com service token e o mesmo correlation id; 202 com `loteId` e `batchId`; um documento no OpenObserve e um `XADD` em `lhamalog:stream:logs` com `fileSource=upload`.

### 2. Recusar duplicata com 409 ou 503 retentável (P1)
Como sistema, não quero republicar o mesmo arquivo no mesmo tenant e produto pela origem `upload`.

Validação independente: segundo envio do mesmo conteúdo, com a chave já `done` → 409, sem segundo `XADD` e sem segunda reserva. Se o primeiro aceite ainda estiver em andamento (claim TTL de 2 min), o Collector responde HTTP **503 + `Retry-After`** / gRPC **`UNAVAILABLE`** (B1 da LLT-290, opção (b)); o Core espelha o 503. O mesmo MD5 com origem `otlp` **não** bloqueia o upload, e vice-versa (decisão 11 da LLT-290).

### 3. Validar tamanho, formato, binário óbvio e auth interna (P1)
Como plataforma, recuso extensão fora da lista, arquivo ou requisição acima de 100 MB, binário óbvio e chamada interna sem service token.

Validação independente: 400 / 413 no Core antes do repasse, quando couber; o Collector revalida e recusa MZ/ELF/Mach-O; 401 se faltar token, se o token não bater ou se vier `Authorization` de usuário no path interno.

### 4. Vários arquivos na mesma requisição (P1)
Como usuário, envio um multipart com vários arquivos e vejo o aceite por arquivo.

Validação independente: aceitos entram na fila; recusados aparecem no corpo do 202; se todos forem duplicata **concluída** (`done`), a resposta é 409.

## As 12 decisões (Michel, 20/11/2026 22:45, America/Sao_Paulo)

Confirmou as 12 recomendações do clarify, exatamente como escritas.

1. **Rota pública**: `POST /api/manual/upload` no Core, JWT Clerk (`Authorization: Bearer`). 401/403 seguem a ADR_032. Qualquer autenticado que já possa ver o produto no tenant da sessão pode enviar; produto arquivado, de outro tenant, sem acesso ou id desconhecido → **403** (não copia o 404 de `ProductService.get()`).
2. **Formatos**: `.txt`, `.json`, `.csv` e `.log`, lista configurável, revalidada no Core e no Collector. Proteção no MVP: só extensão, tamanho e magic bytes de binário óbvio; malware e prompt injection avançados ficam para depois, ainda no Collector.
3. **Vários arquivos**: multipart, aceite por arquivo, recusados listados no corpo do 202; lote inteiro duplicado (chave `done`) → 409.
4. **Teto provisório de 100 MB** por arquivo e, neste MVP, também por requisição, só em properties ou perfil, nunca em `.env`. Mesma cota, assinatura e rate limit do OTLP (429 sem saldo, 503 sem plano). O teto de 5 MB do caminho OTLP não se aplica aqui.
5. **Collector**: `POST /internal/manual/upload` na porta 8080 (`server.port`), só com `X-LhamaLog-Service-Token`. Segredo só por variável de ambiente (`LHAMALOG_CORE_COLLECTOR_TOKEN` no Core, `LHAMALOG_COLLECTOR_SERVICE_TOKEN` no Collector). Token OTLP de produtor não autentica este path.
6. **`signal=logs`**. MD5 dos bytes do arquivo recebido (sem gzip de transporte OTLP). Destino no MVP: a fila de leitura atual com `fileSource=upload`; FilaOrdenada e Finder depois do MVP. O Core **espera** o Collector aceitar e só então responde 202 ou o erro (409/413/429/503/504). O 503 do claim em andamento é herdado da LLT-290 (opção (b)) e o Core o espelha.

Demais fechamentos derivados (não reabrir): um `batchId` e uma mensagem na fila por arquivo aceito; `loteId` só agrupa a resposta HTTP; `idempotencyId = UUIDv3("<batchId>:logs:upload:<md5>")`; Redis fora no dedup = fail-open da spec 010; logs com correlation id, referência à função, aviso e data com fuso `America/Sao_Paulo`.

## Requisitos

- FR-001: expor `POST /api/manual/upload` com JWT Clerk.
- FR-002: autorizar o produto no tenant da sessão; 403 nos casos da decisão 1.
- FR-003: revalidar extensão e tetos de 100 MB no Core e no Collector.
- FR-004: corpo 202 com `loteId` e `files[]`; 409 se todos forem duplicata concluída (`done`).
- FR-005: o Core espera o Collector e espelha 202/400/409/413/429/503/504; nunca devolve 202 se o repasse falhar. O 503 de claim em andamento (B1 da LLT-290, opção (b)) entra nesse espelhamento.
- FR-006: endpoint interno na 8080 com service token; recusar `Authorization` de usuário.
- FR-007: reusar `FileDeduplication.claim(..., FileSource.UPLOAD, bytes)` depois da validação e antes da reserva.
- FR-008: gravar no OpenObserve e só então publicar `log.ingested` em `lhamalog:stream:logs`.
- FR-009: mesma cota, rate limit e assinatura do OTLP.
- FR-010: tetos e extensões em properties/perfil, nunca em `.env`.
- FR-011: recusar magic bytes MZ, ELF e Mach-O.
- FR-012: status por arquivo no corpo (`ACCEPTED`, `DUPLICATE`, `INVALID_EXTENSION`, `TOO_LARGE`, `OBVIOUS_BINARY`, `UNKNOWN`).
- FR-013: logs no padrão VI, sem segredo e sem MD5 completo (só prefixo de 8 caracteres).
- FR-014: não alterar os worktrees alheios (LLT-145 no Core, LLT-186/290 no Collector).

Caminhos no Core (publicados na ponta `f8f3f4aef1d31b514ed413760ceae12f0b02aba5`). Permalinks usam esse SHA; as âncoras são classe e método, sem número de linha:

- [`ManualUploadController.upload`](https://github.com/LhamaLog/lhamalog-core/blob/f8f3f4aef1d31b514ed413760ceae12f0b02aba5/src/main/java/br/com/lhamalog/core/upload/ManualUploadController.java): `POST /api/manual/upload`.
- [`ProductUploadAuthorizer.requireUploadable`](https://github.com/LhamaLog/lhamalog-core/blob/f8f3f4aef1d31b514ed413760ceae12f0b02aba5/src/main/java/br/com/lhamalog/core/upload/ProductUploadAuthorizer.java): 403 `product_forbidden`.
- [`ManualUploadValidator.validate`](https://github.com/LhamaLog/lhamalog-core/blob/f8f3f4aef1d31b514ed413760ceae12f0b02aba5/src/main/java/br/com/lhamalog/core/upload/ManualUploadValidator.java) e `allRefusedStatus`: tetos de 100 MB e status 400/413 do lote recusado.
- [`ManualUploadService.upload`](https://github.com/LhamaLog/lhamalog-core/blob/f8f3f4aef1d31b514ed413760ceae12f0b02aba5/src/main/java/br/com/lhamalog/core/upload/ManualUploadService.java) e `mapCollector`: espera o Collector e mapeia 202/409/400/413/429/503/504; 409 com recusa local vira 400 ou 413, alinhado a `allRefusedStatus` (inclusive `TOO_LARGE` local).
- [`RestCollectorManualUploadClient.forward`](https://github.com/LhamaLog/lhamalog-core/blob/f8f3f4aef1d31b514ed413760ceae12f0b02aba5/src/main/java/br/com/lhamalog/core/upload/RestCollectorManualUploadClient.java) (`SERVICE_TOKEN_HEADER`): `X-LhamaLog-Service-Token`, sem `Authorization`.
- [`ManualUploadProperties`](https://github.com/LhamaLog/lhamalog-core/blob/f8f3f4aef1d31b514ed413760ceae12f0b02aba5/src/main/java/br/com/lhamalog/core/config/ManualUploadProperties.java) (`maxFileBytes`, `maxRequestBytes`, `isUsableCollectorUrl`) e [`ManualUploadConfiguration.collectorManualUploadClient`](https://github.com/LhamaLog/lhamalog-core/blob/f8f3f4aef1d31b514ed413760ceae12f0b02aba5/src/main/java/br/com/lhamalog/core/config/ManualUploadConfiguration.java) (env `LHAMALOG_CORE_COLLECTOR_TOKEN`).
- [`application.properties`](https://github.com/LhamaLog/lhamalog-core/blob/f8f3f4aef1d31b514ed413760ceae12f0b02aba5/src/main/resources/application.properties), bloco “Manual upload” (inclui `server.tomcat.max-part-count` e `max-part-header-size`).
- [`ApiExceptionHandler.coded`](https://github.com/LhamaLog/lhamalog-core/blob/f8f3f4aef1d31b514ed413760ceae12f0b02aba5/src/main/java/br/com/lhamalog/core/shared/ApiExceptionHandler.java) (403 de negócio) e o handler de `MaxUploadSizeExceededException` (`containerUploadMessage`, 413 do contêiner).
- [README do Core](https://github.com/LhamaLog/lhamalog-core/blob/f8f3f4aef1d31b514ed413760ceae12f0b02aba5/README.md), seção “Upload manual (LLT-292)”.

Caminhos no Collector (worktree local, ainda sem commit): `ManualUploadController` (`POST /internal/manual/upload`), reusando `FileDeduplication.claim` e `FileSource.UPLOAD`. Claim em andamento herda o 503 retentável da opção (b); 409 só depois do `done`.

Contratos de trabalho: [`core-manual-upload.md`](https://github.com/LhamaLog/lhamalog-core/blob/f8f3f4aef1d31b514ed413760ceae12f0b02aba5/specs/011-manual-upload/contracts/core-manual-upload.md) e [`collector-internal-upload.md`](https://github.com/LhamaLog/lhamalog-core/blob/f8f3f4aef1d31b514ed413760ceae12f0b02aba5/specs/011-manual-upload/contracts/collector-internal-upload.md).

## Critérios de sucesso

- SC-001: arquivo válido + produto autorizado → 202 depois do aceite do Collector.
- SC-002: lote todo duplicado (`done`) → 409, sem republicar; claim em andamento → 503 retentável, herdado da LLT-290.
- SC-003: recusa parcial aparece no corpo do 202; só os aceitos entram na fila.
- SC-004: 403 para produto arquivado, de outro tenant, sem acesso ou id desconhecido.
- SC-005: 401 no path interno sem service token válido ou com `Authorization`.
- SC-006: extensão inválida → 400; acima de 100 MB → 413; binário óbvio recusado.
- SC-007: 429 sem saldo; 503 sem plano, Collector indisponível ou arquivo em andamento (B1, opção (b)).
- SC-008: o mesmo conteúdo por OTLP e por upload não é duplicata.
- SC-009: verify do Core verde após os commits (atingido: 434 testes, 0 falhas, 21/11/2026 12:48, America/Sao_Paulo).

## Decisões de 20/11 que divergem de ADRs aceitas

Os números 171–174 são **propostos** e aguardam confirmação do Michel. A conferência no Drive em 20/11/2026 23:30 (America/Sao_Paulo) mostrou que 167–170 já estavam ocupados; não havia 171 ou superior. Ver o [README](README.md).

1. Teto provisório de 100 MB por requisição e por arquivo, só em properties ou perfil, nunca em `.env`, mais os limites reais do Tomcat (`max-part-count` 50 / 49 arquivos, cabeçalho de parte 512 B, arquivo de exatamente 100 MB recusado porque o envelope conta). Complementa a ADR_050. Rascunho: ADR_171 proposta.
2. Autenticação Core → Collector no MVP por token de serviço estático, no lugar do JWT interno das ADR_028 e ADR_042. Cita [`RestCollectorManualUploadClient`](https://github.com/LhamaLog/lhamalog-core/blob/f8f3f4aef1d31b514ed413760ceae12f0b02aba5/src/main/java/br/com/lhamalog/core/upload/RestCollectorManualUploadClient.java) e [`research.md` (R5)](https://github.com/LhamaLog/lhamalog-core/blob/f8f3f4aef1d31b514ed413760ceae12f0b02aba5/specs/011-manual-upload/research.md). Rascunho: ADR_172 proposta.
3. Destino no MVP: fila de leitura `lhamalog:stream:logs` com `fileSource=upload` e conteúdo cru no OpenObserve, no lugar do fim da FilaOrdenada das ADR_041, ADR_042 e ADR_045. Cita [`research.md` (R1)](https://github.com/LhamaLog/lhamalog-core/blob/f8f3f4aef1d31b514ed413760ceae12f0b02aba5/specs/011-manual-upload/research.md) e [`data-model.md`](https://github.com/LhamaLog/lhamalog-core/blob/f8f3f4aef1d31b514ed413760ceae12f0b02aba5/specs/011-manual-upload/data-model.md). FilaOrdenada e Finder permanecem pós-MVP. Rascunho: ADR_173 proposta.

Complemento da ADR_053 (arquivo separado, ADR_174 proposta): 202 com recusas no corpo, 409 só na duplicata total concluída, 400/413 na recusa total, 503/504 sem 202 (o 503 de claim em andamento é herdado da LLT-290), e 403 (não 404) para produto desconhecido, de outro tenant, sem acesso ou arquivado (Q11). O 403 de negócio com `code` não revoga a sessão, em contraste com o texto literal da ADR_032. Cita [`ProductUploadAuthorizer`](https://github.com/LhamaLog/lhamalog-core/blob/f8f3f4aef1d31b514ed413760ceae12f0b02aba5/src/main/java/br/com/lhamalog/core/upload/ProductUploadAuthorizer.java), [`ManualUploadService.mapCollector`](https://github.com/LhamaLog/lhamalog-core/blob/f8f3f4aef1d31b514ed413760ceae12f0b02aba5/src/main/java/br/com/lhamalog/core/upload/ManualUploadService.java) e a seção “Upload manual” do [README do Core](https://github.com/LhamaLog/lhamalog-core/blob/f8f3f4aef1d31b514ed413760ceae12f0b02aba5/README.md).

## Premissas e limites

- Implementação do Collector está no worktree local, ainda sem commit, aprovada para commit com ressalvas. A B1 da LLT-290 já está resolvida com a opção (b): o upload herda 503 retentável no claim em andamento (TTL 2 min) e 409 só depois do `done`.
- Sem UI, WebSocket, OpenAPI, FilaOrdenada, Finder, Ocorrência/Sugestão nesta entrega.
- Não alterar ADRs existentes, Jira, `.env`, nem o limite de 5 MB do OTLP.
- `schemaVersion` da fila permanece 1.
- Esta pasta documenta; não substitui a spec 011 no repositório do Core.
