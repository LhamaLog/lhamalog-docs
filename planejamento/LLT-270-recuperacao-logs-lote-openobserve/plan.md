# Plano da entrega e validação

A implementação segue a arquitetura hexagonal do Finder. A sequência começa na configuração e na porta de busca, acrescenta a consulta e as regras de domínio, conecta a recuperação ao consumo e termina com prova sintética e revisão. A base da PR é Development em 6e8b0fd. O HEAD documentado é a795222.

O domínio concentra ConsultaSQL, Deduplicar, Isolado e Fechar em internal/domain/recuperacao.go. A aplicação percorre as páginas em internal/application/recuperar.go. A porta out.Busca está em internal/application/port/out/busca.go. O adaptador HTTP está em internal/adapter/out/openobserve/cliente.go e consulta.go. internal/config/config.go lê os parâmetros. cmd/finder/main.go liga o serviço ao consumo.

T001–T030 cobrem o desenho e a implementação original, testes, configuração e documentação. T029 descreve o papel do pacote OpenObserve. T030 exige executar e registrar a prova sintética. T031 remove o teto de corpo. T032 distingue falhas de transporte/status de JSON de sucesso inválido. As evidências e a relação por tarefa estão no histórico da spec 005.

[<u>Spec 005 no commit documentado</u>](https://github.com/LhamaLog/lhamalog-finder/tree/a7952222e1cf2c710f17629ddfb248cd8ca72630/specs/005-recuperar-logs-lote)

# Sequência e dependências

A referência e a porta de efeito vêm da spec 004. A recuperação fica na spec 005. As próximas entregas da sequência tratam normalização, mascaramento, classificação, avaliação e publicação do resumo. A PR \#7 em 3b26753 não é ancestral da \#8. A validação desta branch não substitui a prova da composição futura.

As correções ficam na branch de origem da PR. A documentação solicitada nesta rodada é mantida exclusivamente no Drive por orientação do solicitante. A nova revisão deve se referir ao HEAD documentado e ter retorno conclusivo em até 15 minutos desde o envio confirmado.

# Validação executada

Em 21/11/2026, go test -count=1 ./..., go vet ./... e go build ./... passaram com Go 1.27.0 Windows/amd64. go test -race -count=1 -v ./... passou na imagem golang:1.27.0 Linux/amd64 com Redis 8.2.10 e OpenObserve 1.1.2 reais em contêineres exclusivos de teste, com integrações opt-in habilitadas e sem skips. git diff --check passou e os arquivos Go da PR foram conferidos com gofmt.

A execução cobre lote unitário e múltiplo, paginação e cópias, contagens divergentes, isolamento, configuração ausente, erros HTTP, timeout, corpo truncado, sufixo JSON inválido e resposta acima de 32 MiB. O race nativo no Windows falhou pelo compilador C sem suporte 64 bits. A validação com detector de corridas foi concluída em Linux.

[<u>Saída integral da suíte com race e integrações</u>](https://github.com/LhamaLog/lhamalog-finder/blob/a7952222e1cf2c710f17629ddfb248cd8ca72630/specs/005-recuperar-logs-lote/evidencias/revisao-2026-11-21-race.txt)

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
