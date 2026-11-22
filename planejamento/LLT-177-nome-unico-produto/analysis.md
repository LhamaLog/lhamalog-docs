# Evidências, diferenças e próximos passos — LLT-177

## Evidências

| O quê | Onde |
|---|---|
| Regra e índice | Core #7, `specs/006-nome-unico-produto/` |
| Testes do Core | `ProductUniqueNameIntegrationTests` (19). Fazem parte do `mvnw verify` de 17/11/2026 (308 testes, 0 falhas) |
| Tela | Web #14, `specs/010-nome-unico-produto/` e `src/features/products/productErrors.ts` |
| Testes do Web | `tests/product-errors.test.mjs`. Na branch: 93 de 93. Em 21/11/2026, com a `Development` mesclada localmente: 114 de 114, build ok |

## Riscos

- **Bancos com produtos antigos:** documentos sem `normalizedName` podem impedir a criação do índice único na subida do Core. Antes de qualquer deploy num banco com produtos, seguir o procedimento de checagem de duplicatas e backfill do `quickstart.md` do Core (spec 006).
- **O Web depende do texto da mensagem** para reconhecer o 409 de nome. Se o texto mudar no Core, o erro volta a aparecer como erro genérico.

## Próximos passos

1. Core: mandar `code: "product_name_in_use"` nessa recusa, para o Web não depender do texto.
2. Executar a T008 do Web e mergear a Web #14 depois da #13.
3. Critério 3 do card: o Collector deixar de aceitar logs de produto arquivado.
