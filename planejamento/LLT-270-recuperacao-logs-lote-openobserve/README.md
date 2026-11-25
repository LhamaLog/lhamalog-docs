# Documentos do pacote

[<u>Spec — escopo e contrato</u>](https://docs.google.com/document/d/1RnawCpInSi_VL6PnonhhFImSM-iKl31Fhq7yydExJX4/edit?usp=drivesdk)

[<u>Plan — implementação e validação</u>](https://docs.google.com/document/d/1FK0DbIqUH4jOZEQZAF8EFdNjCg3slYJysb84P7M6MK0/edit?usp=drivesdk)

[<u>Tasks — rastreabilidade e evidências</u>](https://docs.google.com/document/d/1hKXQ1QfB3bmaslFjBOvPKBbzDQClOSMcgrkSWE5Lp8M/edit?usp=drivesdk)

[<u>Analysis — decisões, riscos e cronologia</u>](https://docs.google.com/document/d/1cCFY4wuz2C5gl6w2WfvlogK82AqW2Q0sLE2rIBbstQc/edit?usp=drivesdk)

# Escopo e referência

Este documento consolida a especificação, o contrato de integração, o plano, as tarefas e a análise da LLT-270 no Drive da equipe. Em 21/11/2026, o responsável pela execução determinou que as atualizações documentais desta sequência de PRs sejam publicadas somente no Google Drive. Esse é o destino documental desta entrega.

A PR \#8 entrega a recuperação de um lote pela referência recebida do Redis. O recorte inclui consulta, paginação, deduplicação, isolamento e classificação do resultado. A branch de origem é LLT-270-implementar-recuperacao-dos-logs-no-open-observe-pela-referencia-do-lote, com destino Development. A referência de código documentada é a7952222e1cf2c710f17629ddfb248cd8ca72630.

[<u>PR \#8 e código de referência</u>](https://github.com/LhamaLog/lhamalog-finder/pull/8)

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

# Decisões e consequências

A spec 005 determina paginação até a página curta e removeu o teto de corpo de 32 MiB em T031. O cliente lê o corpo integral e o serviço acumula os documentos da recuperação. Uma resposta grande ou uma sequência sempre cheia pode aumentar o consumo de memória e prolongar a execução. O timeout limita cada consulta. O cancelamento do contexto interrompe a operação.

Ordenação instável pode pular ou repetir documentos entre páginas. Deduplicar remove cópias já recebidas, mas não recupera um registro que foi pulado. A configuração operacional precisa manter ordenação estável durante a busca. O código permite literais numéricos sem aspas para IDs compostos somente por dígitos. Os testes unitários cobrem a montagem desse SQL, enquanto a prova real executada utiliza IDs de lote textuais.

As políticas de quantidade de tentativas, intervalo, prazo total, DLQ e tratamento definitivo de lote incompleto seguem pendentes nas fontes. Esta entrega mantém a entrada sem efeito concluído nos casos temporários descritos. A correção dessas políticas exige definição própria e não recebe valores novos neste documento.

# Plano e tarefas

O domínio concentra ConsultaSQL, Deduplicar, Isolado e Fechar em internal/domain/recuperacao.go. A aplicação percorre as páginas em internal/application/recuperar.go. A porta out.Busca está em internal/application/port/out/busca.go. O adaptador HTTP está em internal/adapter/out/openobserve/cliente.go e consulta.go. internal/config/config.go lê os parâmetros. cmd/finder/main.go liga o serviço ao consumo.

T001–T030 cobrem o desenho e a implementação original, testes, configuração e documentação. T029 descreve o papel do pacote OpenObserve. T030 exige executar e registrar a prova sintética. T031 remove o teto de corpo. T032 distingue falhas de transporte/status de JSON de sucesso inválido. As evidências e a relação por tarefa estão no histórico da spec 005.

[<u>Spec 005 no commit documentado</u>](https://github.com/LhamaLog/lhamalog-finder/tree/a7952222e1cf2c710f17629ddfb248cd8ca72630/specs/005-recuperar-logs-lote)

# Validação reproduzida e análise

Em 21/11/2026, go test -count=1 ./..., go vet ./... e go build ./... passaram com Go 1.27.0 Windows/amd64. go test -race -count=1 -v ./... passou na imagem golang:1.27.0 Linux/amd64 com Redis 8.2.10 e OpenObserve 1.1.2 reais em contêineres exclusivos de teste, com integrações opt-in habilitadas e sem skips. git diff --check passou e os arquivos Go da PR foram conferidos com gofmt.

A execução cobre lote unitário e múltiplo, paginação e cópias, contagens divergentes, isolamento, configuração ausente, erros HTTP, timeout, corpo truncado, sufixo JSON inválido e resposta acima de 32 MiB. O race nativo no Windows falhou pelo compilador C sem suporte 64 bits. A validação com detector de corridas foi concluída em Linux.

[<u>Saída integral da suíte com race e integrações</u>](https://github.com/LhamaLog/lhamalog-finder/blob/a7952222e1cf2c710f17629ddfb248cd8ca72630/specs/005-recuperar-logs-lote/evidencias/revisao-2026-11-21-race.txt)

O HEAD da PR \#7 em 3b26753 não é ancestral da branch da PR \#8. As correções exclusivas dessa branch anterior não foram incorporadas. A prova executada na própria branch da \#8 não atesta a futura composição 004 + 005. Na consulta ao GitHub, a PR estava aberta, integrável e sem check runs configurados.

O parecer do Discord para b7eb540 apontou inconsistências documentais e solicitou registrar as decisões estruturais. a795222 corrigiu README, rastreabilidade T029/T030 e o seletor do Spec Kit, além de alinhar a descrição da PR às provas reproduzidas. Este documento publica no Drive o contrato, as decisões, as consequências e os limites da entrega. A aprovação do HEAD atual depende de novo parecer explícito.

[<u>Histórico da revisão no Discord</u>](https://discord.com/channels/1477078665920647280/1565511601753165955/threads/1573872898806911066)
