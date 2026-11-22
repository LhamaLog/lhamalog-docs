# Plano — LLT-123

## Core (`lhamalog-core`, Core #3)

- `Product.archivedAt` novo. Rotas `PUT /api/products/{id}`, `POST /{id}/archive`, `POST /{id}/unarchive` e o filtro `GET ?archived=true`.
- Arquivos principais: `src/main/java/br/com/lhamalog/core/product/` (`Product.java`, `ProductService.java`, `ProductController.java`, `ProductRepository.java`). Testes em `ProductEditArchiveIntegrationTests`.

## Web (`lhamalog-web`, Web #13)

- `src/features/products/productView.ts`: monta as props dos componentes da lista a partir do produto do Core e do rascunho local.
- `src/features/products/productEdit.ts`: decide o que mudou (`changedParts`) e encadeia a `version` entre `PUT /api/products/{id}` e `PUT .../context`.
- `src/features/products/useOwnerOptions.ts`: lista de responsáveis com `getMemberships`, a mesma chamada da tela de Equipe.
- `src/features/products/draft.ts`: o rascunho local ganha `owner`, `teamEmail` e `tags`.
- `src/features/products/components/`: `ProductsPage.tsx` passa a usar `ProductsView`. `ProductCard`, `ProductsSummary`, `ProductsByEnvironment` e `ProductsView` só ganharam props opcionais. `ProductTable.tsx` foi apagada. `ProductForm.tsx` ganhou a aba "Informações", a edição e o arquivar.
- Testes: `tests/product-view.test.mjs` e `tests/product-edit.test.mjs`.

## Ordem de merge no Web

**#12 (LLT-178) → #13 (LLT-123) → #14 (LLT-177) → #15 (LLT-179).** A #13 sai da branch da LLT-178.

## Validação

`npm test` e `npm run build`. A conferência visual e o fluxo completo ficam no roteiro manual do `quickstart.md` do Web (T017).
