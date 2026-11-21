# Tarefas — LLT-178

## Core

- [x] Trocar os campos do `Product.Context` pelos seis da tela "Contexto para IA".
- [x] Criar o histórico de versões (`ProductContextRevision`) e as rotas de leitura.
- [x] Criar a rota do texto para a IA, sem chamar a LLM.
- [x] Compensar a gravação da versão e logar no padrão `event=`.
- [x] Adaptar à LLT-163 (`sessions.current()` e `TestTenants`).
- [x] `mvnw verify` verde e Core #9 mergeado.

## Web

- [x] Trocar o tipo do contexto e apagar os campos antigos de `src/features/products` e dos testes de produto.
- [x] Funções puras de leitura, limpeza, limites e erros, com testes (`tests/product-context.test.mjs`).
- [x] Aba "Contexto para IA" igual ao Figma, com reordenação acessível por teclado.
- [x] Envio no cadastro (`POST`) e na edição (`PUT .../context` com `version`).
- [x] `npm test` e `npm run build` verdes, também com a `Development` atual mesclada localmente.
- [ ] T011: roteiro manual no navegador e comparação lado a lado com o Figma (aguarda as chaves da Clerk para subir o ambiente local).
- [ ] Mergear a Web #12.

## Documentação

- [x] Publicar esta pasta no `lhamalog_docs` e atualizar os campos do contexto do produto em [empresa-produtos.md](../empresa-produtos.md).
