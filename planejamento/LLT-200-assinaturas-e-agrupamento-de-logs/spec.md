# Aceite e identidade

Logs de mesma assinatura e produto devem atualizar a contagem e as primeiras e últimas ocorrências. A chave de partição contém assinatura, classe, tenantId e productId. O isolamento faz parte da identidade. O status retornado pelo Módulo Ocorrência é preservado. A reabertura de uma ocorrência fechada pertence ao Módulo.

# Normalização e serialização

A assinatura usa nível, mensagem normalizada, service.name e host, nessa ordem, separados por \|. traceId e correlationId ficam fora da assinatura. A normalização apara as bordas, ignora maiúsculas e substitui números, UUIDs, IPs, datas e hexadecimais por \<NUM\>, \<UUID\>, \<IP\>, \<DATE\> e \<HEX\>. \| literal é escapado como \\. A semântica de barra invertida literal ainda está pendente na fonte e Calcular retorna ErrEscapePendente nesse caminho.

# Partição e fusão

ParticionarLote agrupa por IdentidadeAchado e conta registros. As datas vêm dos timestamps dos logs. Fundir soma a contagem local à acumulada, toma o menor instante inicial e o maior final, preserva o status e propaga a revisão consultada. Mais de um estado para a mesma chave e contagem negativa ou com overflow geram erro. O resumo local é preservado para permitir recalcular o agrupamento após conflito de revisão.

# Portas e recorrência

A consulta do estado acontece uma vez por achado. O envio usa um ResumoAnalise por lote. O orquestrador separa Montar, Agrupar, Preparar e Executar. Uma porta ausente ou uma falha de consulta impede sucesso presumido.

A recorrência considera a mesma chave e máquina em pelo menos três lotes distintos, dentro dos 500 lotes mais recentes. Repetições em um lote contam uma vez. O histórico deve vir do mais recente ao mais antigo e incluir lotes sem equivalência para delimitar a janela.

# Falhas de histórico

Até três tentativas são feitas em falha temporária tipada. Erro crítico termina na primeira tentativa. Esgotamento solicita aviso ao Core com batchId e motivo. Uma consulta degradada mantém o resultado de recorrência desconhecido. HistoricoHTTPPendente retorna erro explícito. O contrato de aviso ao Core e a query histórica operacional precisam de definição verificável para implementação.

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
