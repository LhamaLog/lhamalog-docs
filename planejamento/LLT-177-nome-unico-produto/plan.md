# Plano — LLT-177

## Core (`lhamalog-core`, Core #7)

- `Product.normalizedName` e o índice único `product_tenant_normalized_name`. O índice é a única garantia: não há consulta antes de gravar, o que cobre gravações simultâneas.
- `ProductService.saveWithUniqueName` traduz a `DuplicateKeyException` em 409 com a mensagem própria e o log `event=`.
- Testes em `ProductUniqueNameIntegrationTests` (19), inclusive corrida de 8 cadastros simultâneos.

## Web (`lhamalog-web`, Web #14)

- `src/features/products/productErrors.ts`: `isNameInUse` e as funções que montam o erro do campo e o aviso do topo.
- `src/features/products/components/ProductForm.tsx`: liga o erro ao campo nome e abre a aba certa.
- Testes: `tests/product-errors.test.mjs`.

## Ordem de merge no Web

**#12 (LLT-178) → #13 (LLT-123) → #14 (LLT-177) → #15 (LLT-179).** A #14 sai da branch da LLT-123.

## Validação

`npm test` e `npm run build`. A ligação na tela é conferida no roteiro manual do `quickstart.md` do Web (T008).
