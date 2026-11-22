# Evidências, diferenças e próximos passos — LLT-179

## Evidências

| O quê | Onde |
|---|---|
| API de tokens | Core #8, `specs/010-tokens-ingestao/` e o pacote `ingestiontoken` |
| Testes do Core | 31 testes da feature, dentro do `mvnw clean verify` de 18/11/2026 (339 testes, 0 falhas) |
| Tela | Web #15, `specs/011-tokens-ingestao/` e `src/features/products/` |
| Testes do Web | Na branch: 110 de 110. Em 21/11/2026, com a `Development` mesclada localmente: 131 de 131, build ok. A busca por `llt_` só acha o valor falso `llt_teste` dos testes |

## Diferenças de propósito em relação ao Figma

- A ajuda do nível mínimo não promete filtro.
- O texto solto "Ative para relacionar logs a traces..." saiu, porque não tem controle na tela.
- O comentário Java virou a aba "Java (agente)".
- No produto arquivado, o modo só leitura da LLT-123 desabilita a aba inteira.

## Riscos e observações

- **Collector × Core:** o Collector procura o produto na coleção `products`, pelo campo `productId`, mas o Core grava na `Produto`, com `_id`. Enquanto isso não for alinhado, não dá para testar os tokens de ponta a ponta.
- Os componentes `.tsx` não têm teste automático. A lógica está em `tokenContract.ts` e `otelSnippet.ts`, que são testados.

## Pendências geradas

- **Core:** status da integração e último log por produto, logs das últimas 24 h, rota para "Testar conexão" e guardar sinais e nível mínimo.
- **Figma:** cabeçalho `Authorization: Bearer` no exemplo, Métricas não recebido, ajuda do nível mínimo, texto solto sem controle e tela de revogação da chave.
- **Collector:** confirmar se `/v1/metrics` continua fora. Se entrar, a caixa Métricas pode ser liberada.
- **ADR:** publicar a ADR do token a partir da proposta do Core.

## Próximos passos

1. Executar a T011 do Web e mergear a Web #15 depois da #14.
2. Alinhar `products` × `Produto` entre Collector e Core.
3. Publicar a ADR do token.
