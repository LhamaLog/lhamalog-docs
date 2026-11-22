# Tarefas — LLT-179

## Core

- [x] Gerar, revogar e rotacionar, só com o hash guardado.
- [x] Auditoria e logs `event=` sem segredo.
- [x] Adaptar à LLT-163 (`sessions.current()`, `TestTenants` e código `not_admin`).
- [x] `mvnw verify` verde e Core #8 mergeado.
- [ ] Transformar a `proposta-adr.md` em ADR (substitui a ADR_113 e partes da ADR_106 e da ADR_107).

## Web

- [x] Aba "Integração OpenTelemetry" igual ao Figma.
- [x] Chave de API ligada aos tokens do Core, mostrada uma vez e nunca guardada.
- [x] `VITE_OTLP_ENDPOINT` no Vite e no Docker, documentado.
- [x] `npm test` e `npm run build` verdes, também com a `Development` atual mesclada localmente.
- [ ] T011: roteiro manual no navegador, com a conferência no DevTools (aguarda as chaves da Clerk).
- [ ] Mergear a Web #15, depois da #14.

## Documentação

- [x] Publicar esta pasta no `lhamalog_docs`.
