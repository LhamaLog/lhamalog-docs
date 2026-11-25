# Evidências, divergências e próximos passos — LLT-120

## Evidências

| O quê | Onde |
|---|---|
| Spec, contrato, modelo de dados e roteiro de revisão | `lhamalog-core/specs/011-cargos-permissoes/` (`spec.md`, `contracts/api.md`, `data-model.md`, `revisao.md`) |
| Testes novos | 43: `AccessHttpTests` (11), `AccessPolicyTest` (5), `MemberProductAccessHttpTests` (7), `AccessPurchaseOwnerIntegrationTests` (4), `NotificationRoleHttpTests` (10) e `NotificationRoleMembersHttpTests` (6) |
| Suíte completa | `mvnw clean verify` em 22/11/2026, já com a `Development` mesclada (LLT-289 e LLT-285): 437 testes, 0 falhas, 0 ignorados. `CompanyMemberHttpTests` (LLT-168) passou sem mudança |

## Divergências com a matriz da LLT-169

A matriz da LLT-169 foi consolidada em 17/11/2026, no mesmo dia em que a spec 011 foi escrita, e a spec não a usou como fonte. O código seguiu as ADRs e as decisões do clarify. Ficam para decisão do time:

| Ação | Matriz da LLT-169 | Código da LLT-120 | Origem no código |
|---|---|---|---|
| Membro cria produto | Não | Sim, e ganha acesso ao que cria | C7: é o comportamento atual; mudar exige decisão do time |
| Membro vê a lista da equipe e os cargos | Sim | Não: `MEMBERS_VIEW` só para Dono e Administrador | Rota de membros da LLT-168, que já era só de administrador |
| Membro vê os metadados dos tokens dos produtos dele | Sim | Não: só Dono e Administrador listam tokens | LLT-179 (Core #8, ADR_109) |
| Administrador convida outro administrador | Sim (a 169 não separa o cargo do convite) | Não: `MEMBERS_INVITE_ADMIN` só para o Dono (aplicado no Web) | ADR_114 |

O que bate com a LLT-169: tokens só administrativos para emitir, rotacionar e revogar; arquivar só para Dono e Administrador; acesso por produto concedido por Dono e Administrador; Dono protegido contra desativação; transferência de propriedade fora do escopo; acesso negado entre empresas; desativado não ganha acesso por ter cargo.

**Cargos de notificação × "não adicionar Gestor":** os cargos Gestor e Supervisor da LLT-120 são cargos de **notificação** (ADR_136), que só decidem quem recebe alertas e não dão nenhuma permissão. Eles não são cargos de acesso e não contrariam os três cargos de acesso da LLT-169.

## Riscos

- Duas coleções de membro (`member` e `CompanyMember`) até o time unificar. Só o `MongoMemberRoleDirectory` lê as duas.
- O papel do token prevalece: se alguém rebaixar o Dono direto na Clerk, ele passa a valer como Membro, com um WARN `event=access.owner.not_admin` no log.
- Mais de um `member` DONO ativo na mesma empresa gera WARN `event=access.owner.duplicated`, e o Core usa o menor id.

## Próximos passos

1. Revisão do desenvolvedor (`revisao.md`) e merge do PR do Core.
2. Time: decidir as divergências acima e atualizar a matriz da LLT-169 ou o código.
3. Web: telas da LLT-120.
4. Time: unificar `member` × `CompanyMember` e escrever a ADR da D1.
