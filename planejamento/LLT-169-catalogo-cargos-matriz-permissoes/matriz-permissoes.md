# Matriz de cargos e permissões — LLT-169

## Decisões e alcance

Catálogo escolhido e regras esclarecidas com Vinicius em 17/11/2026. Documento para revisão da equipe, sem implementação funcional neste spike.

- **Dono**: responsável pela propriedade e decisões financeiras da empresa, com administração operacional.
- **Administrador**: administra operação, produtos e equipe; não altera propriedade nem desativa ou rebaixa o Dono.
- **Membro**: consulta informações da empresa e executa ações operacionais somente nos produtos aos quais tem acesso. Não administra assinatura, tokens, usuários, permissões ou arquivamento.

“Sim” sempre se restringe à empresa ativa. “Produto” exige acesso explícito ao produto daquela empresa. O Membro não vê produtos sem acesso, nem seus logs, tokens, consumo, varreduras ou sugestões. Consultas gerais da empresa não podem revelar detalhes desses produtos. Dados pessoais desnecessários, credenciais e segredos não fazem parte de “consultar tudo”.

## Matriz

| Área / ação | Dono | Administrador | Membro |
|---|---|---|---|
| Assinatura: consultar plano e informações gerais de consumo | Sim | Sim | Sim, sem detalhes de produtos não autorizados |
| Assinatura: contratar, alterar, cancelar e gerir cobrança | Sim | Não | Não |
| Tokens: consultar metadados, nunca segredos existentes | Sim | Sim | Produto |
| Tokens: emitir, rotacionar e revogar | Sim | Sim | Não |
| Produtos: consultar dados, logs e ocorrências | Sim | Sim | Produto |
| Produtos: criar | Sim | Sim | Não |
| Produtos: editar dados e contexto | Sim | Sim | Produto |
| Produtos: arquivar e restaurar | Sim | Sim | Não |
| Produtos: conceder e remover acesso | Sim | Sim | Não |
| Varredura: consultar execução e resultados | Sim | Sim | Produto |
| Varredura: iniciar, agendar e cancelar | Sim | Sim | Produto |
| Sugestão: consultar | Sim | Sim | Produto |
| Sugestão: solicitar geração com consumo | Sim | Sim | Produto |
| Sugestão: avaliar, aceitar ou rejeitar | Sim | Sim | Produto |
| Usuários: consultar lista de equipe e cargos | Sim | Sim | Sim |
| Usuários: convidar e reenviar convite | Sim | Sim | Não |
| Usuários: mudar cargo entre Administrador e Membro | Sim, exceto Dono | Sim, exceto Dono | Não |
| Usuários: desativar e reativar | Sim, exceto Dono | Sim, exceto Dono | Não |
| Propriedade: transferir | Não disponível até definição de fluxo específico | Não | Não |
| Perfil e preferências pessoais | Próprios | Próprios | Próprios |

## Condições obrigatórias

- Negar acesso entre empresas, independentemente do cargo.
- Usuário desativado não recebe acesso por possuir cargo.
- Não permitir remoção ou rebaixamento do último administrador efetivo. A implementação precisa definir a contagem considerando a representação do Dono.
- Administrador não pode rebaixar, desativar ou substituir o Dono. Alterações comuns de cargo também não transferem propriedade.
- Produtos arquivados não aceitam mutações operacionais; restauração é administrativa.
- Permissão para iniciar operações não elimina limites de saldo, plano, consumo ou validade do recurso.
- Cargo desconhecido não recebe privilégios administrativos automaticamente.
- Consultar tokens significa consultar metadados. Não permite recuperar segredos existentes.
- Interface e servidor devem usar a mesma política; esconder controles no Web não substitui autorização no Core.

## Esclarecimentos registrados

1. Três cargos: Dono, Administrador e Membro; não adicionar Gestor ou Visualizador.
2. Membro pode consultar todas as áreas, respeitando o acesso aos produtos.
3. Membro pode editar dados/contexto, iniciar varreduras e solicitar/avaliar sugestões nos produtos autorizados.
4. Membro não administra assinatura, tokens, usuários ou permissões, nem arquiva produtos.
5. Administrador mantém a proposta apresentada; cobrança permanece com o Dono.
6. A transferência de propriedade permanece indisponível até definição específica. O spike não inventa um fluxo de transferência.
