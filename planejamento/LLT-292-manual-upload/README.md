# LLT-292 — Upload manual (Core → Collector)

Entrega documental da [LLT-292](https://logviewer2026.atlassian.net/browse/LLT-292), atualizada em 21/11/2026 (America/Sao_Paulo). Resume a spec 011 e as 12 decisões confirmadas pelo Michel às 22:45 de 20/11 (America/Sao_Paulo). A pasta permanece `planejamento/LLT-292-manual-upload/` (o review cita `LLT-292-upload-manual` só como redação; o nome não foi alterado).

A parte do **Core está publicada** na branch `feature/LLT-292-manual-upload`, no PR [#15](https://github.com/LhamaLog/lhamalog-core/pull/15) (base `Development`, aberto, ainda não mesclado). A parte do **Collector está implementada** num worktree local (verify relatado: **480 testes, 0 falhas**, 21/11/2026 13:44, America/Sao_Paulo), ainda **sem commit**, e o Consultor Review a aprovou para commit com ressalvas (`/workspace/rev/llt292/review-collector.md`). Esta pasta é a referência no lhamalog-docs; a spec canônica de trabalho segue em `specs/011-manual-upload/` no Core.

- [Escopo, 12 decisões e critérios de aceite](spec.md)
- [Plano](plan.md)
- [Tarefas (T001–T034)](tasks.md)
- [Análise, review B2 e pendências](analysis.md)

**Dependência da LLT-290:** o endpoint interno no Collector reutiliza o pacote `dedup` (`FileSource.UPLOAD`, `FileDeduplication.claim`), sobre a branch publicada `feature/LLT-290-file-hash-dedup`. A [B1 da LLT-290](../LLT-290-file-hash-dedup/analysis.md) está **resolvida com a opção (b)**: enquanto o arquivo está em andamento, o Collector responde HTTP **503 + `Retry-After`** / gRPC **`UNAVAILABLE`**; **409 só depois do `done`**. O claim TTL é **2 min**. O upload manual herda esse **503 retentável** para duplicata em andamento, e não mais um 409 concorrente. A implementação do Collector da 292 está no worktree local (480 testes em 21/11 13:44), sem commit, aprovada para commit com ressalvas.

## Publicação do Core

PR: [LhamaLog/lhamalog-core#15](https://github.com/LhamaLog/lhamalog-core/pull/15). Commits em `feature/LLT-292-manual-upload`:

- [`0a202c8a6087bed74f4987cd90c47a99dd7b2b3c`](https://github.com/LhamaLog/lhamalog-core/commit/0a202c8a6087bed74f4987cd90c47a99dd7b2b3c) — spec e contratos
- [`e44ee1de434115ae87322ae62398d8264d548f76`](https://github.com/LhamaLog/lhamalog-core/commit/e44ee1de434115ae87322ae62398d8264d548f76) — validação, propriedades e limites
- [`9ac348d81df8598fcbe7d3e34d02aa5db9f45be7`](https://github.com/LhamaLog/lhamalog-core/commit/9ac348d81df8598fcbe7d3e34d02aa5db9f45be7) — encaminhamento ao Collector
- [`026c236045f8fc30122d0983e8c6300ebed3c4fb`](https://github.com/LhamaLog/lhamalog-core/commit/026c236045f8fc30122d0983e8c6300ebed3c4fb) — endpoint e o handler de 413
- [`f8f3f4aef1d31b514ed413760ceae12f0b02aba5`](https://github.com/LhamaLog/lhamalog-core/commit/f8f3f4aef1d31b514ed413760ceae12f0b02aba5) — README, compose e `.env.example` (ponta da branch)

Verify depois desses commits: **434 testes, 0 falhas**, 21/11/2026 12:48 (America/Sao_Paulo). As citações do Core, quando apontam arquivo, usam permalink com o SHA da ponta `f8f3f4aef1d31b514ed413760ceae12f0b02aba5`; o restante segue por classe e método.

## Três decisões de 20/11 que divergem de ADRs aceitas

Registradas aqui e nos rascunhos de ADR abaixo. As ADRs originais não foram editadas.

1. **Teto provisório de 100 MB por requisição** (além do teto por arquivo da ADR_050), só em properties ou perfil, nunca em `.env`, com os limites reais do Tomcat (I2). Ver [ADR_171 proposta](../../Documentações/Diagrama%20ADR/[ADR_171]%20-%20Upload%20manual_%20teto%20provisório%20de%20100%20MB%20por%20requisição%20(complementa%20a%20ADR_050).docx).
2. **Autenticação Core → Collector** no MVP por token de serviço estático (`X-LhamaLog-Service-Token`), no lugar do JWT interno das ADR_028 e ADR_042. Ver [ADR_172 proposta](../../Documentações/Diagrama%20ADR/[ADR_172]%20-%20Upload%20manual_%20autenticação%20Core_Collector%20por%20token%20de%20serviço%20no%20MVP%20(no%20lugar%20do%20JWT%20da%20ADR_028%20e%20ADR_042).docx).
3. **Destino no MVP:** fila de leitura existente (`lhamalog:stream:logs`, `fileSource=upload`) e conteúdo cru no OpenObserve, no lugar do fim da FilaOrdenada das ADR_041, ADR_042 e ADR_045. FilaOrdenada e Finder permanecem pós-MVP. Ver [ADR_173 proposta](../../Documentações/Diagrama%20ADR/[ADR_173]%20-%20Upload%20manual_%20destino%20na%20fila%20de%20leitura%20no%20MVP%20(no%20lugar%20da%20FilaOrdenada%20das%20ADR_041,%20ADR_042%20e%20ADR_045).docx).

A ADR_053 deixava [INFERIDO] o que acontece quando todos os arquivos são bloqueados. Isso, as respostas 202/409/400/413/503/504 e o 403 de produto (Q11, sessão não revogada, em contraste com o texto da ADR_032) estão na [ADR_174 proposta](../../Documentações/Diagrama%20ADR/[ADR_174]%20-%20Upload%20manual_%20respostas%20202,%20409,%20400_413,%20503_504%20e%20403%20de%20produto%20(complementa%20a%20ADR_053).docx) (complemento da ADR_053, arquivo separado).

## Numeração proposta das ADRs

Inventário neste repositório (`Documentações/Diagrama ADR/`): 56 arquivos rastreados, o mais alto é a **ADR_166**. Há 110 números livres entre 1 e 166; vários desses ADRs existem só no Drive (o Review confirmou ao menos ADR_028, ADR_032 e ADR_041). Por isso **não se reutilizam lacunas**.

Conferência no Google Drive (pasta de ADRs) em **20/11/2026 23:30 (America/Sao_Paulo)**: as ADR_167 a ADR_170 já existem lá (ADR_167 Finder com IA própria; ADR_168 Substituição do Elasticsearch pelo OpenObserve; ADR_169 Nomes aceitos dos níveis de prioridade; ADR_170 Taxonomia vigente da classificação). Não há ADR_171 ou superior no Drive. Os rascunhos desta pasta usam então os números **171 a 174**, **propostos até o Michel confirmar**.

Uma ADR de hash MD5 por arquivo (LLT-290) permanece só como proposta no [README da LLT-290](../LLT-290-file-hash-dedup/README.md); não foi criado arquivo, porque este B2 é da LLT-292. Se for numerada depois, o próximo número livre após 174 seria o 175 (também a confirmar no Drive na ocasião).

Branch desta pasta no lhamalog-docs: `LLT-290-292-planejamento`, a partir de `main` (`fe59368`). Sem commit, push ou PR **desta documentação**. Quando o Michel autorizar o commit desta pasta, a sugestão (ADR_148, um commit por card) é fazer commits separados nesta mesma branch, no formato `LLT-290: …` e `LLT-292: …`. Nada é commitado nesta etapa.
