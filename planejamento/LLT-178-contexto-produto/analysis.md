# Evidências, diferenças e próximos passos — LLT-178

## Evidências

| O quê | Onde |
|---|---|
| API, versões e compensação | Core #9, `specs/009-contexto-produto/` e `src/main/java/br/com/lhamalog/core/product/` |
| Testes do Core | `ProductContextIntegrationTests` (10), `ProductContextRevisionCompensationTests` (3) e os testes de produto ajustados. `mvnw verify` em 17/11/2026: 308 testes, 0 falhas |
| Aba do Web | Web #12, `specs/008-contexto-produto/` e `src/features/products/` |
| Testes do Web | `tests/product-context.test.mjs` (8 testes das funções puras). Em 21/11/2026, com a `Development` mesclada localmente: 78 de 78, build ok. A validação de PRs do GitHub também passou `npm ci`, `npm test` e `npm run build` no merge com a `Development` |

## Diferenças conscientes

- **Descrição funcional obrigatória só no Web (F2).** O Core aceita vazio, e o Web exige, seguindo o Figma. Se o time quiser que isso valha também para a API, é uma mudança no Core e, por ser regra de negócio permanente, merece uma ADR nova.
- **Histórico e texto para a IA sem tela (F3).** Ficam pendentes até haver tela no Figma.

## Diferenças em relação ao Figma (Web)

- A trilha "Administração › Produtos › Cadastrar produto" é do `AppLayout`, fora desta tarefa.
- A Descrição funcional fica um pouco mais alta, pela altura mínima do `Textarea` compartilhado.
- O "+" abre um campo para digitar o item, porque o Figma não mostra esse estado.
- "Mover para cima/baixo" aparece ao passar o mouse ou com Tab, por acessibilidade.
- Na edição, a tela usa "Editar produto" e "Salvar alterações" (F7).

## Riscos e observações

- Os testes do Web não carregam `.tsx`. O envio (`POST`/`PUT`, 409 e `fieldErrors`) e o visual são conferidos no roteiro T011, que ainda não rodou.
- O arrastar usa a API nativa do navegador. Em alguns navegadores, como o Firefox, o soltar pode falhar sem `dataTransfer.setData` no `dragstart`. Os botões "Mover para cima/baixo" continuam funcionando.
- Bancos com produtos antigos: o campo `problemSolved` é ignorado na leitura, e o texto que estava nele deixa de aparecer. Conferir antes de qualquer deploy com `db.Produto.countDocuments({ "context.problemSolved": { $exists: true } })`, que deve dar 0.

## Próximos passos

1. Executar a T011 do Web e registrar o resultado no `quickstart.md`.
2. Mergear a Web #12, antes das #13, #14 e #15.
3. LLT-212: juntar o contexto do produto com o da empresa no prompt da Sugestão.
4. Decidir com o time se a Descrição funcional obrigatória vira regra do Core (e ADR).
