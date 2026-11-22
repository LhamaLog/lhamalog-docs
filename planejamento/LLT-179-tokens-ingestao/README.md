# LLT-179 — Tokens de ingestão do produto

Documentação da tarefa [LLT-179](https://logviewer2026.atlassian.net/browse/LLT-179), consolidada em 21/11/2026. Cobre o Core e o Web.

- [Escopo e critérios de aceite](spec.md)
- [Plano](plan.md)
- [Tarefas e validação](tasks.md)
- [Evidências, diferenças e próximos passos](analysis.md)

## Onde está cada parte

| Parte | Repositório | PR | Spec detalhada |
|---|---|---|---|
| Gerar, revogar e rotacionar tokens, com auditoria | `lhamalog-core` | [Core #8](https://github.com/LhamaLog/lhamalog-core/pull/8) (mergeado em 18/11/2026) | `specs/010-tokens-ingestao/` |
| Aba "Integração OpenTelemetry" e Chave de API | `lhamalog-web` | [Web #15](https://github.com/LhamaLog/lhamalog-web/pull/15) (aberto) | `specs/011-tokens-ingestao/` |

A proposta de ADR do token (só hash, exibido uma vez, rotação por prazo) está em `lhamalog-core/specs/010-tokens-ingestao/proposta-adr.md` e ainda precisa virar ADR.

Branch: `LLT-179-tokens-ingestao`. Base: `main`.
