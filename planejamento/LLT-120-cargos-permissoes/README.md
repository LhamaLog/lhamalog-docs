# LLT-120 — Cargos e permissões

Documentação da Feature [LLT-120](https://logviewer2026.atlassian.net/browse/LLT-120) (épico "Usuários, cargos e configurações do usuário"), consolidada em 25/11/2026. Cobre o Core e o Web.

- [Escopo e critérios de aceite](spec.md)
- [Plano](plan.md)
- [Tarefas e validação](tasks.md)
- [Evidências, divergências e próximos passos](analysis.md)

## Onde está cada parte

| Parte | Repositório | PR | Spec detalhada |
|---|---|---|---|
| Papel de acesso, matriz de permissões, acesso por produto, cargos de notificação e proteção do Dono | `lhamalog-core` | [Core #18](https://github.com/LhamaLog/lhamalog-core/pull/18) (mergeado em 25/11/2026) | `specs/011-cargos-permissoes/` |
| Telas: papel na Equipe, convite, acesso por produto, Cargos e Permissões | `lhamalog-web` | aberto em 25/11/2026 | `specs/012-cargos-permissoes/` |

## Relação com a LLT-169

A matriz de referência é a da [LLT-169](../LLT-169-catalogo-cargos-matriz-permissoes/matriz-permissoes.md). Este diretório não copia a matriz. Ele registra como o Core a implementou e onde o código diverge dela, na seção "Divergências" da [análise](analysis.md). As divergências ficam para decisão do time.

Branch: `LLT-120-cargos-permissoes`. Base: `main`.
