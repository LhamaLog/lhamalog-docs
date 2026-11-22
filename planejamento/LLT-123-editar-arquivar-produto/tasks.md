# Tarefas — LLT-123

## Core

- [x] `PUT /api/products/{id}` com controle de `version`.
- [x] Arquivar e desarquivar, só DONO e ADMIN, idempotentes.
- [x] Listagem de arquivados e bloqueio de edição em produto arquivado.
- [x] Testes de integração e Core #3 mergeado.

## Web

- [x] Lista igual ao Figma com os componentes do Vinicius e sem a `ProductTable`.
- [x] Aba "Informações do produto" igual ao Figma, com o rascunho local para os dados sem Core (F1).
- [x] Edição só do que mudou, com `version` encadeada e "Recarregar produto" no 409.
- [x] Arquivar e desarquivar no rodapé, só admin; arquivado só para leitura.
- [x] `npm test` e `npm run build` verdes, também com a `Development` atual mesclada localmente.
- [ ] T017: roteiro manual no navegador e comparação com o Figma (aguarda as chaves da Clerk).
- [ ] Mergear a Web #13, depois da #12.

## Documentação

- [x] Publicar esta pasta no `lhamalog_docs`.
