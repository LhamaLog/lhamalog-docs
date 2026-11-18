# Análise e impactos — LLT-169

## Evidências inspecionadas

Core local na base `4257739`, durante a investigação do spike:

- `src/main/java/br/com/lhamalog/core/member/domain/MemberRole.java`: DONO, ADMIN e MEMBRO; mapeia admin/member da Clerk e preserva DONO na sincronização. Comentário atribui criação do Dono ao fluxo de compra; execução desse fluxo não foi verificada.
- `src/main/java/br/com/lhamalog/core/identity/domain/OrganizationRole.java`: reconhece apenas admin/member, com ou sem prefixo org:. Não comprova suporte a org:owner.
- `src/main/java/br/com/lhamalog/core/shared/CompanySession.java`: indicador administrator deriva de OrganizationRole.ADMIN. O cargo de negócio DONO não comprova autorização equivalente em todos os endpoints.
- `src/main/java/br/com/lhamalog/core/product/ProductService.java`: limita consultas de não administradores por vínculo; criação não exige administrador nesse serviço; edição usa acesso ao produto.
- `src/main/java/br/com/lhamalog/core/member/CompanyMemberController.java`: gerenciamento exige administrador; CompanyMemberService protege o último administrador.

São evidências pontuais, não auditoria completa do software. Não foram consultadas outras tarefas do Jira. O conteúdo antigo do README do docs é histórico e não serve como prova do comportamento atual.

## Diferenças e implementação futura

- Core: conciliar cargo de negócio e identidade autenticada com Felipe; não presumir chave org:owner nem alterar dashboard neste spike.
- Core: aplicar a matriz por ação, empresa e produto; separar consulta de equipe da administração; restringir criação de produto a Dono/Administrador conforme matriz.
- Core: definir contagem de administradores efetivos, proteção do Dono e persistência usada para autorização; cargos conhecidos em um enum não resolvem essas garantias sozinhos.
- Web: apresentar Dono, Administrador e Membro; permitir consultas do Membro e operações autorizadas; não depender apenas de controles visuais.
- Funcionalidades ainda não implementadas devem usar a matriz ao definir seus contratos. Esta documentação não declara motor de notificações, varredura, tokens ou sugestões completos.
- Transferência de propriedade fica indisponível até fluxo próprio definido; nenhum endpoint ou rotina nova foi criado.

## Cenários para futuros testes

Para cada ação da matriz: permitir o cargo autorizado e negar o não autorizado. Acrescentar usuário de outra empresa, produto sem vínculo, usuário desativado, cargo desconhecido, produto arquivado, saldo insuficiente e tentativa de rebaixar/desativar Dono ou último administrador. Validar que listagens e agregações não revelem produtos sem acesso. Verificar servidor e interface separadamente.

## Resultado da análise documental

As seis áreas e os três cargos estão contemplados. Consultar não equivale a administrar; Membro pode operar nos produtos autorizados. A definição de negócio foi consolidada conforme esclarecimentos do usuário, mas a aplicação dessas regras requer trabalho posterior e revisão da equipe. Nenhuma funcionalidade foi testada ou implementada neste spike.
