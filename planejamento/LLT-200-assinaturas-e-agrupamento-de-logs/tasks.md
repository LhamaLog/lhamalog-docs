# Rastreabilidade

A spec 008 registra 55 tarefas, com o histórico anterior indicando 48 verificadas, quatro parciais e três bloqueadas. Esse estado histórico pertence à composição anterior. A compilação isolada atual foi corrigida e executada nesta rodada, conforme o plano deste pacote.

# Normalizador e assinatura

NormalizarMensagem e Calcular são a implementação canônica. TestNormalizarMarcadoresCanonicos, TestComposicaoCanonicaEEscape e TestNormalizacaoDeterministicaIdempotente passaram. Os marcadores e a composição seguem as decisões da spec 008.

# Agrupamento e estado

TestParticionarIsolaChaveEContaTimestampLog cobre identidade e extremos temporais. TestFusaoEntreLotesNaoAlteraStatus cobre a fusão com preservação do estado. TestOrquestrarConsultaPorAchadoEnviaUmResumo cobre uma consulta por achado e um envio por resumo. TestConsultaMemoriaCopiaEstadoEContaChamadas cobre o adaptador em memória.

# Recorrência e falhas

TestRecorrenciaDistintaMesmaMaquinaJanela500 e TestJanelaContaLotesNaoRegistros cobrem a janela. TestRecorrenciaTresTentativasSemFalsoNegativo e TestErroTemporarioPonteiroTambemRepeteTres cobrem as falhas temporárias. O cliente histórico e o aviso Core reais seguem como pendências próprias.

# Contratos compartilhados

O commit 531e3a1 acrescenta nove arquivos de tipos, portas e delegação canônica. A suíte completa antes da mudança falhava com símbolos indefinidos. Após a mudança, passou isoladamente. Isso verifica a dependência de compilação e as regras já exercitadas pelos testes existentes.

[<u>Tarefas originais e histórico</u>](https://github.com/LhamaLog/lhamalog-finder/blob/531e3a1576f9247c906c251ae73cd0c3b80d4efb/specs/008-agrupar-logs-ocorrencia/tasks.md)

[<u>Testes do agrupamento</u>](https://github.com/LhamaLog/lhamalog-finder/blob/531e3a1576f9247c906c251ae73cd0c3b80d4efb/internal/application/agrupar/agrupar_test.go#L10)

[<u>Testes do normalizador</u>](https://github.com/LhamaLog/lhamalog-finder/blob/531e3a1576f9247c906c251ae73cd0c3b80d4efb/internal/application/assinatura/normalizar_mensagem_test.go#L5)

[<u>Testes da janela de recorrência</u>](https://github.com/LhamaLog/lhamalog-finder/blob/531e3a1576f9247c906c251ae73cd0c3b80d4efb/internal/application/recorrencia/avaliar_test.go#L9)

# Referências do código no HEAD 531e3a1

[<u>NormalizarMensagem, internal/application/assinatura/normalizar_mensagem.go, linha 23</u>](https://github.com/LhamaLog/lhamalog-finder/blob/531e3a1576f9247c906c251ae73cd0c3b80d4efb/internal/application/assinatura/normalizar_mensagem.go#L23)

[<u>Calcular, internal/application/assinatura/calcular.go, linha 14</u>](https://github.com/LhamaLog/lhamalog-finder/blob/531e3a1576f9247c906c251ae73cd0c3b80d4efb/internal/application/assinatura/calcular.go#L14)

[<u>ParticionarComAssinador, internal/application/agrupar/particionar_lote.go, linha 12</u>](https://github.com/LhamaLog/lhamalog-finder/blob/531e3a1576f9247c906c251ae73cd0c3b80d4efb/internal/application/agrupar/particionar_lote.go#L12)

[<u>Fundir, internal/application/agrupar/fusao_entre_lotes.go, linha 9</u>](https://github.com/LhamaLog/lhamalog-finder/blob/531e3a1576f9247c906c251ae73cd0c3b80d4efb/internal/application/agrupar/fusao_entre_lotes.go#L9)

[<u>Orquestrador.Agrupar, internal/application/agrupar/orquestrar.go, linha 39</u>](https://github.com/LhamaLog/lhamalog-finder/blob/531e3a1576f9247c906c251ae73cd0c3b80d4efb/internal/application/agrupar/orquestrar.go#L39)

[<u>Avaliar recorrência, internal/application/recorrencia/avaliar.go, linha 9</u>](https://github.com/LhamaLog/lhamalog-finder/blob/531e3a1576f9247c906c251ae73cd0c3b80d4efb/internal/application/recorrencia/avaliar.go#L9)

[<u>Recorrencia.ConsultarRecorrencia, internal/adapter/out/openobserve/recorrencia.go, linha 26</u>](https://github.com/LhamaLog/lhamalog-finder/blob/531e3a1576f9247c906c251ae73cd0c3b80d4efb/internal/adapter/out/openobserve/recorrencia.go#L26)

[<u>Tipos compartilhados, internal/domain/tipos_classificacao.go, linha 7</u>](https://github.com/LhamaLog/lhamalog-finder/blob/531e3a1576f9247c906c251ae73cd0c3b80d4efb/internal/domain/tipos_classificacao.go#L7)

[<u>Identidade e estado, internal/domain/consulta_achado.go, linha 6</u>](https://github.com/LhamaLog/lhamalog-finder/blob/531e3a1576f9247c906c251ae73cd0c3b80d4efb/internal/domain/consulta_achado.go#L6)

Evidência da validação isolada de 21/11/2026

Imagem golang:1.27.0 Linux/amd64. Comandos executados em sequência, com exit final 0: go test -race -count=1 -v ./... && go vet ./... && go build ./...

Redis 8.2.10 exclusivo de teste, FINDER_REDIS_INTEGRATION=1, count=2, block=100ms, ociosidade=100ms. A consulta histórica OpenObserve real não é implementada nesta branch.

go: downloading github.com/redis/go-redis/v9 v9.23.0

go: downloading github.com/joho/godotenv v1.5.1

go: downloading go.uber.org/atomic v1.12.0

go: downloading golang.org/x/sys v0.48.0

go: downloading github.com/cespare/xxhash/v2 v2.3.0

=== RUN TestServidorAtendeHealth

--- PASS: TestServidorAtendeHealth (0.03s)

PASS

ok github.com/LhamaLog/lhamalog-finder/cmd/finder 1.044s

=== RUN TestHealth

--- PASS: TestHealth (0.00s)

PASS

ok github.com/LhamaLog/lhamalog-finder/internal/adapter/in/http 1.020s

=== RUN TestItemDaMensagem

--- PASS: TestItemDaMensagem (0.00s)

=== RUN TestLiberarDevolveOMesmoItem

--- PASS: TestLiberarDevolveOMesmoItem (0.00s)

=== RUN TestNovaSemNomes

--- PASS: TestNovaSemNomes (0.00s)

=== RUN TestNovaLoteRecusaParametroAusente

--- PASS: TestNovaLoteRecusaParametroAusente (0.00s)

=== RUN TestNomeDaChaveUsaPrefixoExterno

--- PASS: TestNomeDaChaveUsaPrefixoExterno (0.00s)

=== RUN TestDescarteMapaVazioNaoFicaNoMapa

2026/11/22 02:18:43 INFO item descartado id=1-0

--- PASS: TestDescarteMapaVazioNaoFicaNoMapa (0.00s)

=== RUN TestConclusaoParcialEFalhaNoRedis

--- PASS: TestConclusaoParcialEFalhaNoRedis (0.04s)

=== RUN TestInstanciaParadaDevolveNoLugarOriginal

--- PASS: TestInstanciaParadaDevolveNoLugarOriginal (0.02s)

=== RUN TestConsumidorVivoNaoPerdeOItem

--- PASS: TestConsumidorVivoNaoPerdeOItem (0.02s)

=== RUN TestOrdemDeEntradaComUmaInstancia

--- PASS: TestOrdemDeEntradaComUmaInstancia (0.02s)

=== RUN TestDuasInstanciasReservamItensDiferentes

--- PASS: TestDuasInstanciasReservamItensDiferentes (0.01s)

=== RUN TestMesmoCodigoUmaConclusao

--- PASS: TestMesmoCodigoUmaConclusao (0.02s)

=== RUN TestDescarteInvalidoEItemAceito

2026/11/22 02:18:43 INFO item descartado id=1795313923668-0

2026/11/22 02:18:43 INFO item descartado id=1795313923670-0

--- PASS: TestDescarteInvalidoEItemAceito (0.02s)

=== RUN TestGrupoLeEntradaAnteriorSemDolar

--- PASS: TestGrupoLeEntradaAnteriorSemDolar (0.02s)

=== RUN TestDoisGruposObservamAMesmaEntrada

--- PASS: TestDoisGruposObservamAMesmaEntrada (0.02s)

=== RUN TestInvalidaSaiDaPendenciaSemChaveConcluida

2026/11/22 02:18:43 INFO entrada inválida id=1795313923735-0 desfecho="entrada inválida" motivo="event diferente de log.ingested" idempotencyId=batch-1

--- PASS: TestInvalidaSaiDaPendenciaSemChaveConcluida (0.02s)

=== RUN TestChaveEmProcessamentoSemPrazo

2026/11/22 02:18:43 INFO referência entregue id=1795313923751-0 desfecho="referência entregue" idempotencyId=batch-1

--- PASS: TestChaveEmProcessamentoSemPrazo (0.02s)

=== RUN TestChaveConcluidaDuraVinteCincoHorasSemRenovar

2026/11/22 02:18:43 INFO efeito concluído id=1795313923765-0 desfecho="efeito concluído" idempotencyId=batch-1

--- PASS: TestChaveConcluidaDuraVinteCincoHorasSemRenovar (1.12s)

=== RUN TestSegundaEntradaNaoRepeteEfeito

2026/11/22 02:18:44 INFO referência entregue id=1795313924890-0 desfecho="referência entregue" idempotencyId=batch-1

2026/11/22 02:18:44 INFO entrada pendente id=1795313924896-0 desfecho="entrada pendente" idempotencyId=batch-1

2026/11/22 02:18:44 INFO entrada pendente id=1795313924890-0 desfecho="entrada pendente" idempotencyId=batch-1

--- PASS: TestSegundaEntradaNaoRepeteEfeito (0.19s)

=== RUN TestRedisFechadoNaoConfirma

--- PASS: TestRedisFechadoNaoConfirma (0.02s)

=== RUN TestReivindicacaoRespeitaQuantidade

--- PASS: TestReivindicacaoRespeitaQuantidade (0.52s)

PASS

ok github.com/LhamaLog/lhamalog-finder/internal/adapter/in/queue 3.109s

? github.com/LhamaLog/lhamalog-finder/internal/adapter/out/mongo \[no test files\]

=== RUN TestRecorrenciaTresTentativasSemFalsoNegativo

--- PASS: TestRecorrenciaTresTentativasSemFalsoNegativo (0.00s)

=== RUN TestErroTemporarioPonteiroTambemRepeteTres

--- PASS: TestErroTemporarioPonteiroTambemRepeteTres (0.00s)

PASS

ok github.com/LhamaLog/lhamalog-finder/internal/adapter/out/openobserve 1.029s

=== RUN TestExecutarDevolveRegistroInteiro

--- PASS: TestExecutarDevolveRegistroInteiro (0.00s)

=== RUN TestExecutarSemApontamento

--- PASS: TestExecutarSemApontamento (0.00s)

=== RUN TestExecutarParadaNoMeioNaoDeixaPronto

--- PASS: TestExecutarParadaNoMeioNaoDeixaPronto (0.00s)

=== RUN TestExecutarApontamentoVazioNaoConsulta

--- PASS: TestExecutarApontamentoVazioNaoConsulta (0.00s)

=== RUN TestExecutarLogAusente

--- PASS: TestExecutarLogAusente (0.00s)

=== RUN TestExecutarInacessivel

--- PASS: TestExecutarInacessivel (0.00s)

=== RUN TestExecutarSobrepostas

--- PASS: TestExecutarSobrepostas (0.00s)

=== RUN TestExecutarApontamentoRepetido

--- PASS: TestExecutarApontamentoRepetido (0.00s)

=== RUN TestExecutarErroComEstadoProntoNaoGuarda

--- PASS: TestExecutarErroComEstadoProntoNaoGuarda (0.00s)

=== RUN TestExecutarRegistroVazioNaoFicaPronto

--- PASS: TestExecutarRegistroVazioNaoFicaPronto (0.00s)

=== RUN TestExecutarCancelamentoNoMeioDevolveErro

--- PASS: TestExecutarCancelamentoNoMeioDevolveErro (0.00s)

=== RUN TestExecutarParadaDuranteLeituraNaoGuarda

--- PASS: TestExecutarParadaDuranteLeituraNaoGuarda (0.00s)

=== RUN TestExecutarConcluiEDisponibilizaUmaVez

--- PASS: TestExecutarConcluiEDisponibilizaUmaVez (0.00s)

=== RUN TestExecutarSegundoCodigoNaoConclui

--- PASS: TestExecutarSegundoCodigoNaoConclui (0.00s)

=== RUN TestExecutarParadaDoWorkerLibera

--- PASS: TestExecutarParadaDoWorkerLibera (0.00s)

=== RUN TestExecutarFilaVaziaEFalhaDeLeitura

--- PASS: TestExecutarFilaVaziaEFalhaDeLeitura (0.00s)

=== RUN TestExecutarParcialDepoisCompletaSemSegundaContagem

--- PASS: TestExecutarParcialDepoisCompletaSemSegundaContagem (0.00s)

=== RUN TestExecutarDescartaSemPrender

--- PASS: TestExecutarDescartaSemPrender (0.00s)

=== RUN TestExecutarConteudoExtraNaoConclui

--- PASS: TestExecutarConteudoExtraNaoConclui (0.00s)

=== RUN TestInterpretacaoEntregaSemConfirmar

=== RUN TestInterpretacaoEntregaSemConfirmar/um_registro_com_trace

=== RUN TestInterpretacaoEntregaSemConfirmar/varios_sem_trace

--- PASS: TestInterpretacaoEntregaSemConfirmar (0.00s)

--- PASS: TestInterpretacaoEntregaSemConfirmar/um_registro_com_trace (0.00s)

--- PASS: TestInterpretacaoEntregaSemConfirmar/varios_sem_trace (0.00s)

=== RUN TestEntradaInvalidaConfirmaUmaVezSemConcluir

--- PASS: TestEntradaInvalidaConfirmaUmaVezSemConcluir (0.00s)

=== RUN TestSegundaEntradaEsperaEEfeitoConcluidoNaoRepete

--- PASS: TestSegundaEntradaEsperaEEfeitoConcluidoNaoRepete (0.00s)

=== RUN TestQuedaAntesEDepoisDoEfeito

--- PASS: TestQuedaAntesEDepoisDoEfeito (0.00s)

=== RUN TestReassumirEntradaAbandonada

--- PASS: TestReassumirEntradaAbandonada (0.00s)

=== RUN TestCorrelationEIdRedisNaoDeduplicam

--- PASS: TestCorrelationEIdRedisNaoDeduplicam (0.00s)

=== RUN TestFeedbackProcessamentoNoTerminal

=== RUN TestFeedbackProcessamentoNoTerminal/leitura_sem_entrada

=== RUN TestFeedbackProcessamentoNoTerminal/falha_de_leitura

=== RUN TestFeedbackProcessamentoNoTerminal/referência_entregue_sem_porta

=== RUN TestFeedbackProcessamentoNoTerminal/referência_entregue_efeito_não_concluído

=== RUN TestFeedbackProcessamentoNoTerminal/efeito_concluído

=== RUN TestFeedbackProcessamentoNoTerminal/confirmada_sem_repetir_efeito

=== RUN TestFeedbackProcessamentoNoTerminal/entrada_pendente

=== RUN TestFeedbackProcessamentoNoTerminal/entrada_inválida_uma_linha

--- PASS: TestFeedbackProcessamentoNoTerminal (0.00s)

--- PASS: TestFeedbackProcessamentoNoTerminal/leitura_sem_entrada (0.00s)

--- PASS: TestFeedbackProcessamentoNoTerminal/falha_de_leitura (0.00s)

--- PASS: TestFeedbackProcessamentoNoTerminal/referência_entregue_sem_porta (0.00s)

--- PASS: TestFeedbackProcessamentoNoTerminal/referência_entregue_efeito_não_concluído (0.00s)

--- PASS: TestFeedbackProcessamentoNoTerminal/efeito_concluído (0.00s)

--- PASS: TestFeedbackProcessamentoNoTerminal/confirmada_sem_repetir_efeito (0.00s)

--- PASS: TestFeedbackProcessamentoNoTerminal/entrada_pendente (0.00s)

--- PASS: TestFeedbackProcessamentoNoTerminal/entrada_inválida_uma_linha (0.00s)

PASS

ok github.com/LhamaLog/lhamalog-finder/internal/application 1.035s

=== RUN TestParticionarIsolaChaveEContaTimestampLog

--- PASS: TestParticionarIsolaChaveEContaTimestampLog (0.00s)

=== RUN TestFusaoEntreLotesNaoAlteraStatus

--- PASS: TestFusaoEntreLotesNaoAlteraStatus (0.00s)

=== RUN TestOrquestrarConsultaPorAchadoEnviaUmResumo

--- PASS: TestOrquestrarConsultaPorAchadoEnviaUmResumo (0.00s)

=== RUN TestConsultaMemoriaCopiaEstadoEContaChamadas

--- PASS: TestConsultaMemoriaCopiaEstadoEContaChamadas (0.00s)

PASS

ok github.com/LhamaLog/lhamalog-finder/internal/application/agrupar 1.025s

=== RUN TestNormalizarMarcadoresCanonicos

--- PASS: TestNormalizarMarcadoresCanonicos (0.00s)

=== RUN TestComposicaoCanonicaEEscape

--- PASS: TestComposicaoCanonicaEEscape (0.00s)

=== RUN TestNormalizacaoDeterministicaIdempotente

--- PASS: TestNormalizacaoDeterministicaIdempotente (0.00s)

PASS

ok github.com/LhamaLog/lhamalog-finder/internal/application/assinatura 1.031s

? github.com/LhamaLog/lhamalog-finder/internal/application/port/in \[no test files\]

? github.com/LhamaLog/lhamalog-finder/internal/application/port/out \[no test files\]

=== RUN TestRecorrenciaDistintaMesmaMaquinaJanela500

--- PASS: TestRecorrenciaDistintaMesmaMaquinaJanela500 (0.00s)

=== RUN TestJanelaContaLotesNaoRegistros

--- PASS: TestJanelaContaLotesNaoRegistros (0.00s)

PASS

ok github.com/LhamaLog/lhamalog-finder/internal/application/recorrencia 1.028s

=== RUN TestCarregarPadrao

--- PASS: TestCarregarPadrao (0.00s)

=== RUN TestCarregarWorkers

--- PASS: TestCarregarWorkers (0.00s)

=== RUN TestAplicarArquivoEnv

--- PASS: TestAplicarArquivoEnv (0.01s)

=== RUN TestAplicarArquivoEnvAusente

--- PASS: TestAplicarArquivoEnvAusente (0.00s)

=== RUN TestCarregarNaoCriaParametrosDeConsumo

--- PASS: TestCarregarNaoCriaParametrosDeConsumo (0.00s)

=== RUN TestCarregarIgnoraArquivoEnvComoPadrao

--- PASS: TestCarregarIgnoraArquivoEnvComoPadrao (0.00s)

=== RUN TestValidarRecusaCadaParametroNumerico

=== RUN TestValidarRecusaCadaParametroNumerico/sem_quantidade

=== RUN TestValidarRecusaCadaParametroNumerico/sem_bloqueio

=== RUN TestValidarRecusaCadaParametroNumerico/sem_ociosidade

--- PASS: TestValidarRecusaCadaParametroNumerico (0.00s)

--- PASS: TestValidarRecusaCadaParametroNumerico/sem_quantidade (0.00s)

--- PASS: TestValidarRecusaCadaParametroNumerico/sem_bloqueio (0.00s)

--- PASS: TestValidarRecusaCadaParametroNumerico/sem_ociosidade (0.00s)

=== RUN TestValidarRecusaNaoPositivoEStreamForaDoContrato

--- PASS: TestValidarRecusaNaoPositivoEStreamForaDoContrato (0.00s)

=== RUN TestValidarAceitaConsumoInformado

--- PASS: TestValidarAceitaConsumoInformado (0.00s)

=== RUN TestConfiguracaoHistoricoSemDefaults

--- PASS: TestConfiguracaoHistoricoSemDefaults (0.00s)

PASS

ok github.com/LhamaLog/lhamalog-finder/internal/config 1.035s

=== RUN TestQuadroSemApontamento

--- PASS: TestQuadroSemApontamento (0.00s)

=== RUN TestConcluirGuardaRegistroInteiro

--- PASS: TestConcluirGuardaRegistroInteiro (0.00s)

=== RUN TestParadaNoMeioNaoDeixaPronto

--- PASS: TestParadaNoMeioNaoDeixaPronto (0.00s)

=== RUN TestDepoisQueInstanciaParaNaoExigeLog

--- PASS: TestDepoisQueInstanciaParaNaoExigeLog (0.00s)

=== RUN TestApontamentoVazioEInutilizavel

--- PASS: TestApontamentoVazioEInutilizavel (0.00s)

=== RUN TestAusenteNaoCriaRegistroVazio

--- PASS: TestAusenteNaoCriaRegistroVazio (0.00s)

=== RUN TestInacessivelDistintoDeAusente

--- PASS: TestInacessivelDistintoDeAusente (0.00s)

=== RUN TestMesmoApontamentoUmLogPronto

--- PASS: TestMesmoApontamentoUmLogPronto (0.00s)

=== RUN TestChaveReservaConcluiENaoRenova

--- PASS: TestChaveReservaConcluiENaoRenova (0.00s)

=== RUN TestEnvelopeValidoComESemTrace

--- PASS: TestEnvelopeValidoComESemTrace (0.00s)

=== RUN TestEnvelopeOpcionalAusenteContinuaValido

--- PASS: TestEnvelopeOpcionalAusenteContinuaValido (0.00s)

=== RUN TestEnvelopeInvalido

=== RUN TestEnvelopeInvalido/json_metadata

=== RUN TestEnvelopeInvalido/json_body

=== RUN TestEnvelopeInvalido/tenant_ausente

=== RUN TestEnvelopeInvalido/event

=== RUN TestEnvelopeInvalido/origin

=== RUN TestEnvelopeInvalido/schema_2

=== RUN TestEnvelopeInvalido/signal

=== RUN TestEnvelopeInvalido/productId_divergente

=== RUN TestEnvelopeInvalido/batch_diferente

=== RUN TestEnvelopeInvalido/faixa

=== RUN TestEnvelopeInvalido/recordCount_zero

=== RUN TestEnvelopeInvalido/recordCount_negativo

=== RUN TestEnvelopeInvalido/um_sem_recordId

=== RUN TestEnvelopeInvalido/varios_com_recordId

=== RUN TestEnvelopeInvalido/publishedAt

=== RUN TestEnvelopeInvalido/publishedAt_sem_zona

--- PASS: TestEnvelopeInvalido (0.01s)

--- PASS: TestEnvelopeInvalido/json_metadata (0.00s)

--- PASS: TestEnvelopeInvalido/json_body (0.00s)

--- PASS: TestEnvelopeInvalido/tenant_ausente (0.00s)

--- PASS: TestEnvelopeInvalido/event (0.00s)

--- PASS: TestEnvelopeInvalido/origin (0.00s)

--- PASS: TestEnvelopeInvalido/schema_2 (0.00s)

--- PASS: TestEnvelopeInvalido/signal (0.00s)

--- PASS: TestEnvelopeInvalido/productId_divergente (0.00s)

--- PASS: TestEnvelopeInvalido/batch_diferente (0.00s)

--- PASS: TestEnvelopeInvalido/faixa (0.00s)

--- PASS: TestEnvelopeInvalido/recordCount_zero (0.00s)

--- PASS: TestEnvelopeInvalido/recordCount_negativo (0.00s)

--- PASS: TestEnvelopeInvalido/um_sem_recordId (0.00s)

--- PASS: TestEnvelopeInvalido/varios_com_recordId (0.00s)

--- PASS: TestEnvelopeInvalido/publishedAt (0.00s)

--- PASS: TestEnvelopeInvalido/publishedAt_sem_zona (0.00s)

=== RUN TestFimConcluiNoMesmoPasso

--- PASS: TestFimConcluiNoMesmoPasso (0.00s)

=== RUN TestFimNaoConcluiSeCodigoJaConcluido

--- PASS: TestFimNaoConcluiSeCodigoJaConcluido (0.00s)

=== RUN TestFimParadaDoWorkerNaoConclui

--- PASS: TestFimParadaDoWorkerNaoConclui (0.00s)

=== RUN TestConcluirJuntosUmaConclusao

--- PASS: TestConcluirJuntosUmaConclusao (0.00s)

=== RUN TestItemForaDeContrato

--- PASS: TestItemForaDeContrato (0.00s)

=== RUN TestSemConsumoNaoConclui

--- PASS: TestSemConsumoNaoConclui (0.00s)

=== RUN TestReservaExclusivaELiberacaoSemPrazo

--- PASS: TestReservaExclusivaELiberacaoSemPrazo (0.00s)

=== RUN TestSegundoTomadorRecebeOutroItem

--- PASS: TestSegundoTomadorRecebeOutroItem (0.00s)

PASS

ok github.com/LhamaLog/lhamalog-finder/internal/domain 1.039s
