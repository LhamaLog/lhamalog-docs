# Tarefas — LLT-177

## Core

- [x] `normalizedName` e índice único por empresa, valendo para arquivados.
- [x] 409 com mensagem própria e log `event=`.
- [x] Testes, incluindo concorrência, e Core #7 mergeado.

## Web

- [x] Reconhecer o 409 de nome e mostrar o erro no campo nome.
- [x] Limpar o erro ao editar e não enviar o contexto quando o nome é recusado.
- [x] `npm test` e `npm run build` verdes, também com a `Development` atual mesclada localmente.
- [ ] T008: roteiro manual no navegador (aguarda as chaves da Clerk).
- [ ] Mergear a Web #14, depois da #13.

## Documentação

- [x] Publicar esta pasta no `lhamalog_docs`.
