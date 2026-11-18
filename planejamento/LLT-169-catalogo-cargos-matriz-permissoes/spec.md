# Especificação: catálogo de cargos e matriz de permissões

**Branch**: `LLT-169-spike-definir-catalogo-de-cargos-e-matriz-de-permissoes`
**Data**: 2026-11-17
**Estado**: esclarecimentos consolidados com o usuário; entrega documental para revisão.
**Fonte**: LLT-169, consultada isoladamente no Jira.

## Cenários de uso e validação

### 1. Entender os cargos (P1)
Como responsável pelo produto, quero distinguir Dono, Administrador e Membro para decidir quem pode realizar cada ação.

Validação independente: revisar o catálogo e identificar a responsabilidade de cada cargo sem consultar código.

Aceite: cada cargo possui descrição, escopo por empresa e limites explícitos; uma proposta não é apresentada como regra aprovada.

### 2. Decidir permissões (P1)
Como equipe, quero uma matriz das seis áreas da tarefa: assinatura, tokens, produtos, varredura, sugestão e usuários.

Validação independente: para cada ação, consultar a permissão de cada cargo e as condições de acesso ao produto.

Aceite: nenhuma célula fica sem definição na versão aprovada; ações de consulta e alteração são separadas; exceções sobre Dono e último administrador são explícitas.

### 3. Planejar a adoção (P2)
Como desenvolvedor, quero conhecer as diferenças entre o comportamento atual e a matriz aprovada.

Validação independente: conferir evidências de código e os impactos documentados no Core e no Web.

Aceite: distinguir autorização no servidor, apresentação na interface e configuração de identidade; não declarar implementadas as regras propostas.

### Casos de borda

- Usuário de outra empresa, desativado ou sem acesso ao produto.
- Cargo desconhecido, divergência entre identidade e cargo de negócio.
- Administrador tentando alterar ou desativar o Dono.
- Remoção do último administrador e transferência de propriedade.
- Produto arquivado e operações que geram consumo.

## Requisitos

- FR-001: propor os cargos Dono, Administrador e Membro, conforme direção escolhida pelo usuário.
- FR-002: cobrir as seis áreas da LLT-169 com ações concretas e condições de escopo.
- FR-003: documentar proteção do Dono, continuidade administrativa e isolamento entre empresas.
- FR-004: registrar separadamente evidências atuais, propostas e decisões aprovadas.
- FR-005: documentar impactos no Core e Web sem implementar autorização ou alterar a Clerk neste spike.
- FR-006: definir cenários de validação para futura implementação; não afirmar execução de testes inexistentes.
- FR-007: submeter a matriz ao usuário antes de tratar as permissões como decisões finais.

### Entidades conceituais

- Cargo: responsabilidade de um membro dentro de uma empresa.
- Permissão: ação autorizada sobre um recurso, sujeita a condições.
- Vínculo com produto: limitação de acesso a produtos de uma mesma empresa.
- Proprietário: membro com responsabilidade de propriedade; não presumir uma chave Clerk específica.

## Critérios de sucesso propostos

- SC-001: três cargos descritos e revisados.
- SC-002: 100% das seis áreas representadas na matriz.
- SC-003: cada ação possui decisão para os três cargos e condição de escopo.
- SC-004: diferenças de implementação e dependências registradas com referências locais.
- SC-005: decisões de negócio aprovadas explicitamente antes do fechamento do spike.

## Premissas e limites

- Jira não fornece critérios de aceite explícitos; os acima são propostos.
- Entrega documental no lhamalog_docs, com impactos no Core e Web; sem migração, nova dependência ou mudança em serviços.
- Não consultar tarefas relacionadas ou Drive sem autorização.
- Commit e push autorizados; não abrir PR.
- Documentação migrada do Core para planejamento/LLT-169-catalogo-cargos-matriz-permissoes no lhamalog_docs.

## Esclarecimentos

- 2026-11-17: usuário escolheu propor Dono, Administrador e Membro para revisão. Isso aprova a direção do catálogo, não as permissões de cada ação.
- A matriz em `matriz-permissoes.md` consolida os esclarecimentos: Membro consulta todas as áreas respeitando acesso aos produtos e pode executar operações nesses produtos, sem administrar assinatura, tokens, equipe, permissões ou arquivamento.
