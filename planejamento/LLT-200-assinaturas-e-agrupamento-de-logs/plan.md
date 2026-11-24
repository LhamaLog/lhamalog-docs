# Plano e limites

A sequência funcional é normalizar a assinatura, particionar o lote, consultar o estado de cada achado, fundir contagens e datas, consultar recorrência e enviar um resumo. O classificador e a segurança são componentes consumidores/fornecedores dos contratos compartilhados.

# Correção das dependências

Os DTOs e portas necessários foram trazidos da implementação existente na PR \#11, sem criar novos campos. Os tipos de classificação foram extraídos para tipos_classificacao.go. A \#11 conserva o algoritmo de classificação no arquivo original e passa a usar esse arquivo de tipos. O normalizador e a partição canônicos da \#9 são reutilizados pela análise. A segurança e os auxiliares de recuperação necessários à \#11 mantêm os caminhos de suas implementações de origem.

O teste TestFronteira010AntesDaClassificacaoEAssinaturaCanonica foi transferido da \#10 para a \#11. Ele foi executado com sucesso nessa branch. Os testes próprios do scanner continuam na \#10. A transferência remove a dependência circular dos testes sem apagar a prova do fluxo integrado.

# Validação

As três branches foram testadas separadamente, em sequência. Na \#9, todos os testes passaram com race, Redis real habilitado, vet e build. Na \#10, testes com race, vet e build também passaram. Na \#11, passaram os testes de recuperação e análise com Redis/OpenObserve reais, race, vet e build. TestAceiteDesempenhoVMA ficou ignorado porque exige VM-A real, todos os serviços e lote de 1000. Esse aceite permanece pendente para a revisão própria da \#11.

# Próximos requisitos verificáveis

A query histórica do OpenObserve exige organização, stream, campos, critérios de ordenação e projeção autorizados pelo contrato. O aviso ao Core exige rota, payload e credencial definidos. Os textos atuais da spec 008 mantêm essas definições pendentes. Uma implementação dessas integrações deve ser sustentada por suas fontes e pela prova real correspondente.

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
