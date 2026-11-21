# Plano — LLT-178

## Core (`lhamalog-core`, Core #9)

- `Product.Context` passa a ter os seis campos novos. O construtor do record normaliza textos e listas e aplica os padrões, inclusive na leitura de documentos antigos.
- Coleção nova `ProductContextRevision`, com índice único `productId` + `revision`. Uma versão por mudança, com `createdAt` e `actorUserId`.
- Rotas novas em `ProductController`:
  - `GET /api/products/{id}/context/revisions`;
  - `GET /api/products/{id}/context/revisions/{revision}`;
  - `GET /api/products/{id}/context/prompt`, que devolve `{prompt, executed:false}` e não chama a LLM.
- Se a gravação da versão falhar depois do produto, a gravação do produto é desfeita (compensação), com log no padrão `event=` da constituição 2.1.0.
- Arquivos principais: `src/main/java/br/com/lhamalog/core/product/` (`Product.java`, `ProductService.java`, `ProductController.java`, `ProductContextRevision.java`, `ProductContextPrompt.java`).

## Web (`lhamalog-web`, Web #12)

- `src/features/products/context.ts`: funções puras de leitura (`readProductContext`), limpeza, limites, erros por campo (`contextErrorFor`), opções de idioma e movimentação das listas.
- `src/features/products/components/`: `ProductContextFields.tsx` (a aba), `ChipListField.tsx`, `ReorderListField.tsx`, `NewItemInput.tsx` e `SegmentedControl.tsx`. O `ProductForm.tsx` ganhou a moldura comum (Voltar, abas e rodapé).
- `src/features/products/types.ts`: o tipo do contexto passa a ter só os campos do Core.
- `src/shared/ui/`: props opcionais `hint` em `Input`, `Textarea` e `Select`, e `showCount` no `Textarea`.
- Envio: `POST /api/products` com o `context` novo no cadastro e `PUT /api/products/{id}/context` com `version` na edição. Os `fieldErrors` `context.*` aparecem no campo certo, e o 409 mostra só a mensagem do Core.

## Ordem de merge no Web

A Web #12 é a primeira de uma pilha que mexe no mesmo `ProductForm.tsx`: **#12 (LLT-178) → #13 (LLT-123) → #14 (LLT-177) → #15 (LLT-179)**.

## Validação

- **Core:** `mvnw verify` com Testcontainers, em 17/11/2026: 308 testes, 0 falhas, 0 pulados.
- **Web:** `npm test` e `npm run build`. A conferência visual com o Figma e o fluxo completo ficam no roteiro manual do `quickstart.md` do Web (T011).
