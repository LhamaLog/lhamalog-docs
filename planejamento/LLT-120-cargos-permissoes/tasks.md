# Tarefas — LLT-120

## Core

- [x] Papel de acesso e matriz de permissões, com as rotas de consulta.
- [x] Acesso por produto para Membros.
- [x] Cargos de notificação e atribuição de pessoas.
- [x] Proteção do Dono na desativação.
- [x] Decisões C1 a C7 confirmadas pelo Pedro (22/11/2026).
- [x] Merge da `Development` com a LLT-289 e teste do Dono criado pela compra.
- [x] `mvnw clean verify` verde: 437 testes, 0 falhas (22/11/2026).
- [x] Revisão do desenvolvedor (`revisao.md`), exigida pela constituição.
- [x] Core #18 mergeado (25/11/2026).

## Web

- [x] Papel da sessão e menus pelas permissões (`AccessProvider`).
- [x] Dono identificado e protegido na Equipe; convite conforme o papel de quem convida.
- [x] Acesso por produto de um Membro, aba Cargos e aba Permissões.
- [x] `npm test` e `npm run build` verdes, também com a `Development` atual mesclada localmente (160 testes, 25/11/2026).
- [x] Roteiro manual com Core, Web e Clerk: 18 de 19 passos OK (24 e 25/11/2026).
- [ ] Botão Arquivar pela permissão `PRODUCTS_ARCHIVE` em vez do `orgRole` (passo 15 do roteiro).
- [ ] Mergear o PR do Web.

## Time

- [ ] Decidir as divergências com a matriz da LLT-169 (ver [análise](analysis.md)).
- [ ] Unificar as coleções `member` (LLT-163) e `CompanyMember` (LLT-168) e escrever a ADR da D1.
- [ ] Emendar a constituição sobre o nome da branch (`feature/` × `LLT-XXX-slug`).

## Documentação

- [x] Publicar esta pasta no `lhamalog-docs`.
