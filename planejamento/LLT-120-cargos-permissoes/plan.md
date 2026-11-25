# Plano — LLT-120

## Core (`lhamalog-core`, `specs/011-cargos-permissoes/`)

**Módulo `access`** (novo): papel de acesso, matriz e acesso por produto.
- `application`: `AccessRole` (OWNER, ADMIN, MEMBER), `Permission` (a matriz), `AccessService` (resolve o papel da sessão e confere a permissão), `ProductAccessService` e `MemberRoleDirectory`.
- `infrastructure`: `MongoMemberRoleDirectory`, o único ponto que lê o papel de outra pessoa nas coleções `member` (LLT-163) e `CompanyMember` (LLT-168). É o lugar a trocar quando o time unificar as duas.
- `api`, com as rotas:
  - `GET /api/company/access/me` (papel e permissões da sessão);
  - `GET /api/company/access` (catálogo e matriz);
  - `GET` e `PUT /api/company/members/{userId}/products` (acesso por produto).

**Módulo `notificationrole`** (novo): cargos de notificação.
- Coleção `NotificationRole`, com as listas de gravidades, tipos de alerta e membros dentro do documento (ADR_142).
- Rotas em `/api/company/notification-roles` (criar, ler, renomear, excluir e trocar gravidades, tipos e membros) e `GET /api/company/members/{userId}/notification-roles`.

**Mudanças pequenas em outras features:**
- `member/CompanyMemberController` (LLT-168): bloqueia a desativação do Dono.
- `product/ProductRepository` e `ProductAccessRepository`: consultas para o acesso por produto.

Os eventos de negócio e os avisos geram log no padrão `event=` da constituição 2.1.0 (por exemplo, `product_access.updated`, `notification_role.created` e `access.owner.not_admin`), sem id de usuário em claro.

## Web (`lhamalog-web`, `specs/012-cargos-permissoes/`)

- `src/features/access/`: `AccessProvider` e `useAccess` chamam `GET /api/company/access/me` ao abrir o workspace e a cada troca de empresa. Menus e ações passam a depender das permissões, não do `orgRole` da Clerk. `accessContract.ts` valida a resposta do Core. `PermissionsMatrix.tsx` mostra a matriz (só leitura).
- `src/features/team/`: a Equipe ganha as abas Pessoas, Cargos e Permissões (`TeamTabs.tsx`, rotas `/equipe/cargos` e `/equipe/permissoes`). O Dono aparece com o selo "Dono" e sem Desativar nem rebaixar (`ownerRules.ts`). O convite só oferece Administrador para o Dono, ou para o Administrador enquanto a empresa não tem Dono (W4). O painel Produtos de um Membro usa o acesso por produto do Core (`MemberProductsPanel.tsx`, `productAccess.ts`).
- `src/features/notification-roles/`: aba Cargos para listar, criar, renomear, configurar e excluir cargos e atribuir pessoas (`NotificationRolesPage.tsx`, `RoleForm.tsx`, `RoleMembersPanel.tsx`, `roleContract.ts`, `roleValidation.ts`).
- Também mudam `AppRoutes.tsx`, `CompanyWorkspace.tsx`, `TeamPage.tsx` (LLT-168) e `shared/services/api.ts`, sempre com o menor recorte (W3).
- Sem chave secreta, sem chamada nova à Clerk e sem mudança no login.

## Validação

**Core:** `mvnw clean verify` com Testcontainers. Testes novos: `AccessHttpTests`, `AccessPolicyTest`, `MemberProductAccessHttpTests`, `AccessPurchaseOwnerIntegrationTests`, `NotificationRoleHttpTests` e `NotificationRoleMembersHttpTests`.

**Web:** `npm test` e `npm run build`, com testes das funções puras em `tests/access-contract.test.mjs`, `access-refusals.test.mjs`, `notification-roles.test.mjs`, `owner-rules.test.mjs` e `product-access.test.mjs`, mais o roteiro manual do `quickstart.md` com Core, Web e Clerk.
