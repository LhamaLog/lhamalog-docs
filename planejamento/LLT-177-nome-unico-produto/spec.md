# Escopo e critérios de aceite — LLT-177

## Critérios do card

1. O nome do produto é único dentro da empresa (tenant).
2. A quantidade de produtos respeita o plano. **Fora:** decisão do dono do produto de não ter limite por enquanto.
3. Produto arquivado deixa de aceitar logs e some das listas, mantendo o histórico. **Parcial:** sumir das listas veio na LLT-123; parar de aceitar logs depende do Collector.

## Regras (Core)

- A comparação usa `normalizedName`: espaços das pontas removidos e minúsculas (`Locale.ROOT`). Acentos e espaços internos contam ("Ação" e "Acao" são nomes diferentes).
- Índice único `{tenantId, normalizedName}`, que também vale para produtos arquivados: um arquivado continua ocupando o nome.
- Nome repetido no cadastro ou na edição responde 409 com "Já existe um produto com este nome nesta empresa. Ele pode estar arquivado.".
- Empresas diferentes podem repetir o nome. Renomear libera o nome antigo.
- A recusa gera log INFO `event=product.create.name_in_use` ou `event=product.update.name_in_use`, sem o nome digitado.

## Regras (Web)

- O 409 de nome é reconhecido pela mensagem do contrato.
- O erro aparece embaixo do campo "Nome do produto", e a aba "Informações do produto" abre sozinha. O topo mostra "Nada foi salvo: confira o nome do produto.", sem o botão "Recarregar produto".
- Editar o nome limpa o erro. Nada do que foi digitado se perde.
- Na edição com nome e contexto alterados, a recusa do nome impede o envio do contexto.

## Pronto quando

- O Core recusa nome repetido com índice único e testes verdes (feito no Core #7).
- O Web mostra o erro no campo, com `npm test` e `npm run build` verdes.
- O roteiro manual do Web (T008) foi executado e registrado.
