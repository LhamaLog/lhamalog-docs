# Escopo e critérios de aceite — LLT-123

## Objetivo

Permitir editar os dados gerais de um produto e arquivá-lo sem apagar nada, e trazer a lista e o cadastro de produtos do Web para o Figma validado.

## Regras (Core)

- Quem tem acesso ao produto edita nome, descrição, categoria e versão de negócio (`PUT /api/products/{id}`), com controle de `version`. Versão desatualizada responde 409.
- Só DONO e ADMIN arquivam e desarquivam (`POST /api/products/{id}/archive` e `/unarchive`). Repetir a operação não tem efeito.
- Arquivar preserva dados, contexto e vínculos de acesso. O produto some da listagem padrão e aparece em `GET /api/products?archived=true`.
- Produto arquivado recusa qualquer alteração de dados gerais ou de contexto (409).
- Nada é excluído definitivamente. Recusa de permissão ou conflito não encerra a sessão.
- O limite de produtos por plano saiu desta tarefa por decisão do dono do produto.

## Regras (Web)

- **Lista (`01-produtos-lista.png`):** `/produtos` usa os componentes da demonstração do Vinicius (`ProductsView` e afins, LLT-237) no lugar da tabela, com 6 produtos por página e filtro de Ativos/Arquivados.
- **Aba "Informações do produto" (`02-produto-informacoes.png`):** seção única igual ao Figma. Saem Criticidade, Projeto, Aplicação principal, Nível de log e Produto ativo.
- **Dados que o Core não tem (F1):** tipo, ambiente, responsável, e-mail da equipe e tags ficam no rascunho local do navegador, com aviso na tela. Indicadores sem API mostram estado neutro ("—"), sem número inventado.
- **Edição (F7, W1):** a edição usa a mesma tela, com o título "Editar produto", e envia só o que mudou, com a `version` encadeada entre dados gerais e contexto. O 409 de versão mostra "Recarregar produto".
- **Arquivar (F6):** Arquivar e Desarquivar ficam no rodapé da edição, só para admin, com confirmação. Produto arquivado abre só para leitura.

## Pronto quando

- O Core edita, arquiva e desarquiva com testes verdes (feito no Core #3).
- A lista e a aba do Web ficam iguais ao Figma, com `npm test` e `npm run build` verdes.
- O roteiro manual do Web (T017) foi executado e registrado.
