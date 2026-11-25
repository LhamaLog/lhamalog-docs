# Tarefas e evidências

Os itens T001–T032 estão marcados no arquivo de tarefas da spec 005. Esta consolidação agrupa sua rastreabilidade. O estado dos testes corresponde à execução de 21/11/2026 documentada no HEAD a795222. A aprovação do PR continua dependendo do parecer explícito.

# T001–T007 — Dependências, ambiente, tipos e porta de busca

A consulta utiliza net/http, com as dependências existentes no go.mod. .env.example e internal/config/config.go expõem os nove FINDER_OO\_\*. Os testes distinguem configuração ausente de lista de cópia vazia. internal/domain/recuperacao.go contém os tipos e internal/application/port/out/busca.go define a busca. A integração OpenObserve é opt-in e recebe a configuração da prova.

# T008–T013 — Consulta de lote unitário e múltiplo

consulta_test.go verifica SQL, faixa e corpo. cliente.go faz POST com Basic e timeout. recuperar.go trata a página curta e a configuração ausente. integracao_test.go verifica organização, stream, lote, faixa e recordId. Referências de prova incluem TestPaginaCurtaEntregaLoteENaoConfirmaRedis, recuperar_test.go linha 13, e TestLoteUnitarioFiltraRecordID, linha 65.

# T014–T017 — Paginação e cópias físicas

A página seguinte avança from pelo size e a leitura termina em página curta. Deduplicar compara cópias conforme a lista configurada. Os testes exercitam múltiplo exato do tamanho de página, ausência de teto, cópias entre páginas e um identificador após as cópias. TestPaginacaoDedupEContagem começa em recuperar_test.go linha 153.

# T018–T020 — Completude

Fechar compara IDs válidos distintos com recordCount e informa as quantidades quando calculadas. Os testes cobrem igualdade, falta, excesso, vazio e subconjunto aceito de lote misto. TestFecharCompletudeEPrecedencia começa em recuperacao_test.go linha 61 e TestCompletudeNaoAfirmaCausa em recuperar_test.go linha 222.

# T021–T023 — Isolamento

A consulta filtra tenant e produto e cada documento é conferido. Falta de nome impede a consulta e gera isolamento. As provas cobrem atributos internos inadequados e dois tenants. TestIsoladoNaoUsaAtributoInterno está em recuperacao_test.go linha 173 e TestIsolamentoDeDocumentoECredencial em recuperar_test.go linha 267.

# T024–T028 — Falhas e porta de efeito

A classificação aplica a precedência da spec. O cliente distingue credencial recusada, JSON inválido, timeout, indisponibilidade e falha de página. O serviço entrega EfeitoConcluido à porta usada pelo consumo. TestFalhaClassificadaSemParcial começa em recuperar_test.go linha 282. O ato de confirmar fica em ConsumoReferencia, consumir.go linha 192.

# T029–T030 — Documentação e prova

O comentário de pacote descreve o papel do adaptador. A prova sintética com Redis 8.2.10 e OpenObserve 1.1.2 reais passou com Go 1.27.0 Linux/amd64, detector de corridas e integrações habilitadas, sem skips. A execução está versionada em evidencias/revisao-2026-11-21-race.txt. Os registros de rastreabilidade foram corrigidos em a795222.

# T031–T032 — Corpo e falhas de transporte

T031 removeu o teto de 32 MiB. T032 preserva pendência em erro de leitura e status HTTP não previsto. As regressões estão em cliente_regressao_test.go, linhas 16, 30, 41, 55 e 68.

[<u>Tarefas originais da spec 005</u>](https://github.com/LhamaLog/lhamalog-finder/blob/a7952222e1cf2c710f17629ddfb248cd8ca72630/specs/005-recuperar-logs-lote/tasks.md)

[<u>Evidência da execução final</u>](https://github.com/LhamaLog/lhamalog-finder/blob/a7952222e1cf2c710f17629ddfb248cd8ca72630/specs/005-recuperar-logs-lote/evidencias/revisao-2026-11-21-race.txt)

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
