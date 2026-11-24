# Critérios de aceite

A LLT-270 exige recuperar lotes unitários e múltiplos, inclusive com cópias físicas e várias páginas. Cada lhamalog_record_id lógico deve aparecer uma vez. A consulta e a conferência de cada documento devem preservar o tenant confiável da referência e o produto. O lote fica completo quando a quantidade de identificadores distintos coincide com recordCount e nenhuma falha de maior precedência foi encontrada.

[<u>Tarefa LLT-270</u>](https://logviewer2026.atlassian.net/browse/LLT-270)

# Contrato de entrada e consulta

A entrada é uma Referencia já validada pelo consumo do envelope log.ingested v1. Ela contém tenantId e productId confiáveis, organização, stream do OpenObserve, batchId, recordId no lote unitário, minTimestampMicros, maxTimestampMicros, recordCount, idempotencyId, correlationId e o identificador da entrada Redis. O conteúdo dos logs permanece no OpenObserve.

O adaptador envia POST /api/{organization}/\_search. O corpo JSON contém query.sql, query.start_time, query.end_time, query.from e query.size. A faixa começa em minTimestampMicros e termina em maxTimestampMicros + 1. A organização e o stream vêm da referência. A chave lhamalog:stream:logs identifica o transporte Redis.

O SQL seleciona o stream da referência e filtra lhamalog_batch_id, os campos configurados de tenant e produto e, quando RecordID está presente, lhamalog_record_id. Nomes de campos e valores recusados pelo validador impedem a consulta. O cliente usa autenticação Basic, timeout por requisição e rejeita redirecionamentos. A resposta de sucesso precisa ser um JSON completo com hits interpretável como lista de objetos.

[<u>Contrato do Consumidor log.ingested v1, especialmente seção 7</u>](https://docs.google.com/document/d/14yLd8WA7pRm6es4okYiOnUjHfZp0T_4uyUnVkFk2tQk/edit)

[<u>ADR_168 — OpenObserve e isolamento por tenant</u>](https://docs.google.com/document/d/1cq0KUW2gWsIq6Mv54SZhXcWIoHlKCqwqUG5XHD3rVFs/edit)

# Paginação, deduplicação e isolamento

from começa em zero e avança pelo tamanho configurado da página. Uma página cheia leva à consulta seguinte. A leitura termina ao receber menos hits do que o tamanho pedido. size é uma configuração da consulta e não usa recordCount como limite. Essa regra permite encontrar registros lógicos que aparecem depois de cópias físicas.

Os documentos são agrupados por lhamalog_record_id. Diferenças restritas aos campos listados em FINDER_OO_CAMPOS_COPIA representam cópias físicas, das quais uma é disponibilizada. Diferenças fora dessa lista indicam conteúdo divergente, sem escolher uma versão. Documento sem identificador fica fora da contagem válida e gera uma classificação própria.

Os campos de tenant e produto são conferidos no topo de cada documento contra os valores confiáveis da referência. Atributos internos do log não substituem essa identidade. Qualquer incoerência gera isolamento. O conjunto de registros só acompanha o resultado de lote completo.

# Configuração de acesso

Os nove parâmetros FINDER_OO\_\* abaixo vêm do ambiente. Os valores numéricos e os nomes usados em testes são específicos da prova sintética.

FINDER_OO_URL — URL base HTTP ou HTTPS do OpenObserve.

FINDER_OO_USUARIO e FINDER_OO_SENHA — credenciais Basic. A senha não entra nos registros operacionais.

FINDER_OO_TIMEOUT — duração positiva por consulta, interpretada pelo formato de duração do Go.

FINDER_OO_PAGINA — quantidade positiva de documentos físicos por página.

FINDER_OO_CAMPOS_COPIA — nomes separados por vírgula. Variável ausente impede a consulta. Presente e vazia exige igualdade de conteúdo completo entre cópias do mesmo identificador.

FINDER_OO_ORDEM — expressão SQL de ordenação estável. O operador deve fornecer uma ordem total adequada aos dados. A implementação recusa ponto e vírgula, CR, LF e NUL nessa expressão.

FINDER_OO_CAMPO_TENANT e FINDER_OO_CAMPO_PRODUTO — nomes dos campos confiáveis no documento armazenado. A ausência de qualquer um gera isolamento antes da consulta.

URL, credenciais, timeout, página, lista de cópia ou ordenação ausentes resultam em configuração de acesso ausente, sem consulta e com EfeitoConcluido falso.

# Classificação, efeito e confirmação Redis

A precedência de classificação registrada na spec 005 é autenticação/autorização, resposta inválida, isolamento/identidade, documento sem identificador, conteúdo divergente, excesso de registros e lote incompleto. Falhas de acesso são consideradas conforme essa precedência e a existência de páginas anteriores. Uma falha que pede correção já observada pode prevalecer sobre uma falha temporária posterior.

Lote completo, autenticação recusada, resposta inválida, isolamento, documento sem identificador, conteúdo divergente e excesso retornam EfeitoConcluido verdadeiro. Lote incompleto, indisponibilidade, timeout e falha de página, quando não há falha de maior precedência, mantêm EfeitoConcluido falso. Falha de página após páginas bem-sucedidas é distinguida de indisponibilidade na primeira consulta.

ServicoRecuperacao.Recuperar devolve a classificação, o contexto e as quantidades calculadas. No sucesso, também devolve os registros lógicos. O ato de confirmar a entrada Redis pertence a ConsumoReferencia. ServicoRecuperacao.Executar devolve ao consumo apenas a marca EfeitoConcluido. A confirmação pelo consumo usa o identificador da entrada Redis. A deduplicação de negócio usa idempotencyId.

No executável desta PR, main liga Executar ao consumo. Assim, lote completo e falha que pede correção podem ser confirmados sem encaminhamento do conteúdo recuperado à classificação ou ao resumo. Esse é o recorte atual da spec 005. A composição das etapas seguintes precisa tratar o destino dos registros e o momento do efeito completo antes da homologação do fluxo integral. A prova desta PR cobre a recuperação e não representa homologação dessa composição.

# Referências de código verificadas

[<u>Classificação e efeito, internal/domain/recuperacao.go, linha 139</u>](https://github.com/LhamaLog/lhamalog-finder/blob/a7952222e1cf2c710f17629ddfb248cd8ca72630/internal/domain/recuperacao.go#L139)

[<u>SQL e faixa temporal, internal/domain/recuperacao.go, linha 168</u>](https://github.com/LhamaLog/lhamalog-finder/blob/a7952222e1cf2c710f17629ddfb248cd8ca72630/internal/domain/recuperacao.go#L168)

[<u>Deduplicação, internal/domain/recuperacao.go, linha 272</u>](https://github.com/LhamaLog/lhamalog-finder/blob/a7952222e1cf2c710f17629ddfb248cd8ca72630/internal/domain/recuperacao.go#L272)

[<u>Isolamento, internal/domain/recuperacao.go, linha 359</u>](https://github.com/LhamaLog/lhamalog-finder/blob/a7952222e1cf2c710f17629ddfb248cd8ca72630/internal/domain/recuperacao.go#L359)

[<u>Executar e Recuperar, internal/application/recuperar.go, linhas 22 e 32</u>](https://github.com/LhamaLog/lhamalog-finder/blob/a7952222e1cf2c710f17629ddfb248cd8ca72630/internal/application/recuperar.go#L22)

[<u>POST e corpo integral, internal/adapter/out/openobserve/cliente.go, linhas 25 e 107</u>](https://github.com/LhamaLog/lhamalog-finder/blob/a7952222e1cf2c710f17629ddfb248cd8ca72630/internal/adapter/out/openobserve/cliente.go#L25)

[<u>Configuração, internal/config/config.go, linhas 63, 147 e 166</u>](https://github.com/LhamaLog/lhamalog-finder/blob/a7952222e1cf2c710f17629ddfb248cd8ca72630/internal/config/config.go#L63)

[<u>Ligação do serviço ao consumo, cmd/finder/main.go, linha 70</u>](https://github.com/LhamaLog/lhamalog-finder/blob/a7952222e1cf2c710f17629ddfb248cd8ca72630/cmd/finder/main.go#L70)

[<u>Confirmação após efeito, internal/application/consumir.go, linha 192</u>](https://github.com/LhamaLog/lhamalog-finder/blob/a7952222e1cf2c710f17629ddfb248cd8ca72630/internal/application/consumir.go#L192)
