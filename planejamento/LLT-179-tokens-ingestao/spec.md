# Escopo e critérios de aceite — LLT-179

## Objetivo

Cada produto tem tokens de ingestão, que os exporters OpenTelemetry do cliente usam para mandar logs e traces ao Collector. O Web mostra a Chave de API e a configuração da aplicação na aba "Integração OpenTelemetry".

## Regras (Core)

- Só DONO e ADMIN gerenciam tokens. Membro comum recebe 403 com o código `not_admin`. Produto de outra empresa ou inexistente responde 404.
- **Gerar:** o token tem o prefixo `llt_` e 32 bytes aleatórios. O banco guarda só o SHA-256, na coleção `product_tokens`, no formato que o Collector lê. O valor aparece uma única vez, na resposta da criação.
- **Revogar:** o token fica `REVOKED`, com data e autor, e nunca é apagado. O Collector deixa de aceitá-lo em até 30 s (cache).
- **Rotacionar:** gera um token novo, e o antigo expira ao fim da transição (padrão 24 h, de 1 a 168 h). Durante a transição, os dois valem.
- Produto arquivado: gerar e rotacionar respondem 409; revogar é aceito.
- Auditoria em `ProductTokenAudit` e logs `event=ingestion_token.created/revoked/rotated`, sem o valor nem o hash do token.

## Regras (Web)

- **Aba igual ao Figma (`04-produto-integracao-otel.png`):** endpoint de recebimento com Copiar, Chave de API, sinais, nível mínimo, configuração da aplicação e status. Saem protocolo, nome do serviço, cabeçalhos e coleta ativa.
- **Chave de API (F5):** "Gerar nova" cria a chave ou, se já existir uma, rotaciona com 24 h de transição, sempre com confirmação e só para admin. A chave aparece uma vez, com Copiar, fica só na memória da tela e nunca vai para `sessionStorage`, `localStorage`, console ou exemplo de configuração.
- **Endpoint (F4):** vem da variável pública opcional `VITE_OTLP_ENDPOINT`, no Vite e no `/config.js` do Docker.
- **Exemplo de configuração:** usa o cabeçalho `Authorization: Bearer`, que é o que o Collector aceita, com logs e traces e métricas desligadas.
- **Dados sem API (F1):** sinais e nível mínimo ficam no rascunho local. O status fica neutro e "Testar conexão" fica desabilitado.
- A revogação existe no Core, mas fica pendente de tela no Figma.

## Pronto quando

- O Core gera, revoga e rotaciona com testes verdes (feito no Core #8).
- A aba do Web fica igual ao Figma, a chave não fica em nenhum armazenamento do navegador, e `npm test` e `npm run build` ficam verdes.
- O roteiro manual do Web (T011), com a conferência no DevTools, foi executado e registrado.
