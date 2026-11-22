# Escopo e critérios de aceite — LLT-178

## Objetivo

Cada produto guarda um contexto que a IA usa para entender o sistema do cliente. O contexto é salvo por produto, tem histórico de versões e vai para a LLM junto com o contexto da empresa quando o usuário pede uma sugestão.

## Critérios do card

1. O contexto é salvo por produto e versionado.
2. O contexto é enviado à LLM junto com o contexto da empresa ao pedir sugestão.

## Campos do contexto (tela "Contexto para IA" do Figma)

Estes campos substituem os da 001 (problema resolvido, público-alvo, diferenciais, palavras-chave e restrições), que deixaram de existir.

| Campo | Tipo | Limite | Padrão |
|---|---|---|---|
| `functionalDescription` (Descrição funcional) | texto | 2.000 caracteres | vazio |
| `personality` (Personalidade) | `SIMPLE`, `STANDARD` ou `DETAILED` | — | `STANDARD` |
| `responseLanguage` (Idioma da resposta) | código de idioma | 20 caracteres, formato `pt-BR` | `pt-BR` |
| `architecture` (Arquitetura) | lista | 30 itens de até 80 caracteres | vazia |
| `scope` (Escopo) | lista ordenada | 30 itens de até 200 caracteres | vazia |
| `sensitiveData` (Dados sensíveis) | lista ordenada | 30 itens de até 200 caracteres | vazia |

Textos têm os espaços das pontas removidos. Itens vazios ou repetidos (sem diferenciar maiúsculas) são descartados, mantendo o primeiro.

## Regras

- **Core:** todos os campos são opcionais. Cada mudança no contexto gera uma versão numerada, com data e autor. Salvar sem mudança não gera versão. Produto arquivado não aceita mudança de contexto (409), mas as versões continuam legíveis. Quem não pode ver o produto recebe 404.
- **Web (F2):** a Descrição funcional é obrigatória no cadastro e ao salvar o contexto, como no Figma. A Personalidade sempre tem valor. É uma regra de tela: o Core continua aceitando vazio.
- **Idioma (W1):** a tela oferece `pt-BR`, `en-US` e `es-ES`. Um código já gravado fora dessa lista aparece como opção extra e é mantido.
- **Ordem (W2):** Escopo e Dados sensíveis podem ser reordenados, arrastando ou pelo teclado, e a ordem é gravada.

## Fora desta entrega

- **F3:** a tela do histórico de versões e do texto para a IA. As rotas existem no Core, mas o Figma não tem tela para elas.
- **Critério 2 do card:** juntar o contexto do produto com o da empresa no prompt é da LLT-212 ("Montar o prompt com contexto da empresa, do produto e do usuário"). O Core já monta a seção do produto (`GET /api/products/{id}/context/prompt`), sem chamar a LLM.

## Pronto quando

- O Core salva e versiona o contexto com os campos novos e tem testes verdes (feito no Core #9).
- A aba do Web envia e lê os campos novos sem perder dados, fica igual ao Figma e tem `npm test` e `npm run build` verdes.
- O roteiro manual do Web (T011) foi executado e registrado.
