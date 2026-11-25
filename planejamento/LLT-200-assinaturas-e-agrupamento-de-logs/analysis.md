# Decisões vigentes

A spec 008 define o normalizador canônico e a serialização da assinatura. ADR_170 estabelece ERROR, WARNING e INFO. As fontes antigas sobre SPAM são históricas. ADR_063 trata recorrência como atributo. A spec 008 adapta a janela para 500 lotes e preserva a responsabilidade de reabertura no Módulo Ocorrência.

# Pendências funcionais

O histórico operacional permanece representado por HistoricoHTTPPendente, que retorna ErrQueryHistoricaPendente. A consulta em memória é uma prova da semântica do estado, sem ligação ao bootstrap de produção. O aviso ao Core usa uma porta semântica e mantém o erro quando o cliente real está ausente.

O escape de barra invertida literal e os casos formais P-010-27 permanecem pendentes nas fontes. O código conserva o erro explícito. A prova sintética da janela em memória não comprova consulta histórica real. A entrega atual também exige integração com o Módulo e o Core para homologação do fluxo completo.

# Dependências e compatibilidade

A falha de compilação isolada foi reproduzida no HEAD d90bbf0. A correção coordenada foi autorizada pelo solicitante nesta execução. Os contratos da \#9 vieram da implementação existente da \#11. As dependências levadas à \#11 reutilizam os arquivos canônicos da \#9, \#10 e \#8. O objetivo é manter as interfaces e os caminhos iguais na integração futura.

# Commits da correção coordenada

PR \#9 — 531e3a1576f9247c906c251ae73cd0c3b80d4efb — LLT-200: disponibilizar contratos comuns de analise.

PR \#10 — 28735a6b1032542cdf061ffe07954fac04f599e5 — LLT-202: mover teste integrado para a branch de analise.

PR \#11 — 3ab74025bfad96ee1b1b167e41af89a808bd1b9a — LLT-199: explicitar dependencias compartilhadas da analise.

# Destino documental e aprovação

O solicitante determinou que a documentação desta sequência seja atualizada somente no Google Drive. Autorizou avançar da \#8 com a pendência de destino documental registrada. A aprovação técnica de cada HEAD continua dependendo do parecer e das validações. As pendências funcionais descritas neste documento têm tratamento próprio e não são convertidas em aprovação pela escolha do destino documental.

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

# Fontes

[<u>LLT-200 — critérios de agrupamento</u>](https://logviewer2026.atlassian.net/browse/LLT-200)

[<u>Spec 008, decisões e contratos do projeto</u>](https://github.com/LhamaLog/lhamalog-finder/blob/531e3a1576f9247c906c251ae73cd0c3b80d4efb/specs/008-agrupar-logs-ocorrencia/spec.md)

[<u>ADR_170 — ERROR, WARNING e INFO</u>](https://docs.google.com/document/d/12SGFJs3Ue-XG9eRCBrRqVnq9IIYs2uacrCL0tH0dtTU/edit)

[<u>ADR_062 — AchadoAnalise e ResumoAnalise</u>](https://docs.google.com/document/d/16XOz3bMdXwRTDHIkY0zuGx6faDSi8COtD84e-zecpR8/edit)

[<u>ADR_063 — atributo de recorrência</u>](https://docs.google.com/document/d/1zHBgNKh_Mt5mALSsz4zK87_XUghdKgRqGaV3vo2K7NU/edit)

Acompanhamento da revisão — 21/11/2026, 23h40

A solicitação /simple-review da PR \#9, HEAD 531e3a1576f9247c906c251ae73cd0c3b80d4efb, foi publicada no tópico da LLT-200 às 23h25min37s (America/Sao_Paulo). O bot confirmou o recebimento e o encaminhamento. O limite de 15 minutos terminou às 23h40min37s. A última conferência após esse limite ainda mostrava somente a solicitação e a confirmação do bot, sem parecer conclusivo. A sequência foi interrompida por essa condição de parada, preservando os commits e as branches.

Tópico da solicitação — https://discord.com/channels/1477078665920647280/1565511601753165955/threads/1573887122992271410

A PR \#8 permanece com a pendência de destino documental, cujo avanço foi autorizado pelo solicitante. A \#9 tem os contratos corrigidos e as validações isoladas aprovadas, mas está sem aprovação explícita. As \#10 e \#11 receberam apenas os ajustes coordenados de dependências, já enviados, e aguardam suas revisões completas. As \#12 e \#13 ainda não foram iniciadas. O teste de desempenho na VM-A da \#11 permanece sem execução naquele ambiente. A retomada da sequência depende de orientação do solicitante sobre a revisão pendente da \#9.
