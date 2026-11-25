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

## Validação

`mvnw clean verify` com Testcontainers. Testes novos: `AccessHttpTests`, `AccessPolicyTest`, `MemberProductAccessHttpTests`, `AccessPurchaseOwnerIntegrationTests`, `NotificationRoleHttpTests` e `NotificationRoleMembersHttpTests`.
