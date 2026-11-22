# Evidências, diferenças e próximos passos — LLT-123

## Evidências

| O quê | Onde |
|---|---|
| API de edição e arquivamento | Core #3, `specs/002-editar-arquivar-produto/` |
| Testes do Core | `ProductEditArchiveIntegrationTests` (10). Fazem parte do `mvnw verify` de 17/11/2026 (308 testes, 0 falhas) |
| Telas do Web | Web #13, `specs/009-editar-arquivar-produto/` e `src/features/products/` |
| Testes do Web | `tests/product-view.test.mjs` e `tests/product-edit.test.mjs`. Na branch: 89 de 89. Em 21/11/2026, com a `Development` mesclada localmente: 110 de 110, build ok. A validação de PRs do GitHub também passou teste e build no merge com a `Development` |

## Diferenças conscientes

- **F1:** tipo, ambiente, responsável, e-mail e tags ficam só no navegador onde foram digitados. Em outro navegador, esses campos aparecem vazios, e a tela avisa isso.
- **F6:** arquivar não está no Figma. Entrou no rodapé da edição e em "Filtros" → Arquivados.
- **Confirmação:** usa `window.confirm`, como a desativação na tela de Equipe, porque o Figma não mostra o diálogo.

## Achados aceitos

- A paginação mostra "1–6" (componente compartilhado), e o Figma mostra "1 - 6".
- As opções de Área vêm só dos produtos ativos.
- Ficaram funções sem uso no `productListModel`. A limpeza fica para outra tarefa.

## Pendências para o Core

Guardar tipo, ambiente, responsável, e-mail da equipe e tags do produto, e oferecer status de integração, último log e os indicadores dos painéis.

## Próximos passos

1. Executar a T017 do Web e registrar no `quickstart.md`.
2. Mergear a Web #13 depois da #12.
3. Criar cards para as pendências do Core acima.
