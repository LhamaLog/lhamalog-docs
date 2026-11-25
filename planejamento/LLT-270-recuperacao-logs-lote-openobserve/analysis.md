# Decisões e consequências

A spec 005 determina paginação até a página curta e removeu o teto de corpo de 32 MiB em T031. O cliente lê o corpo integral e o serviço acumula os documentos da recuperação. Uma resposta grande ou uma sequência sempre cheia pode aumentar o consumo de memória e prolongar a execução. O timeout limita cada consulta. O cancelamento do contexto interrompe a operação.

Ordenação instável pode pular ou repetir documentos entre páginas. Deduplicar remove cópias já recebidas, mas não recupera um registro que foi pulado. A configuração operacional precisa manter ordenação estável durante a busca. O código permite literais numéricos sem aspas para IDs compostos somente por dígitos. Os testes unitários cobrem a montagem desse SQL, enquanto a prova real executada utiliza IDs de lote textuais.

As políticas de quantidade de tentativas, intervalo, prazo total, DLQ e tratamento definitivo de lote incompleto seguem pendentes nas fontes. Esta entrega mantém a entrada sem efeito concluído nos casos temporários descritos. A correção dessas políticas exige definição própria e não recebe valores novos neste documento.

# Origem da decisão de confirmação

A clarificação de 08/11/2026 na spec 005, linha 15, autoriza que lote completo e falhas que pedem correção sejam tratados como efeito concluído. A spec 004, linha 183, registra a escolha Q1 A de esperar o efeito definido pela recuperação. Essas são as fontes verificáveis da ligação atual. A atribuição histórica é a registrada nas specs. Este documento não acrescenta uma aprovação nominal do Michel.

[<u>Clarificação da spec 005, linha 15</u>](https://github.com/LhamaLog/lhamalog-finder/blob/a7952222e1cf2c710f17629ddfb248cd8ca72630/specs/005-recuperar-logs-lote/spec.md#L15)

[<u>Origem da decisão na spec 004, linha 183</u>](https://github.com/LhamaLog/lhamalog-finder/blob/a7952222e1cf2c710f17629ddfb248cd8ca72630/specs/004-capturar-referencia-lote/spec.md#L183)

# Destino documental e cronologia

Após o parecer de 22h39, o solicitante orientou nesta execução que as atualizações documentais fossem feitas somente no Drive e pediu a continuação da sequência. A orientação foi transmitida ao tópico do Discord em mensagem de 22h48. O registro execucao.md do HEAD a795222 descreve o impedimento encontrado antes dessa orientação. O registro posterior é este pacote no Drive. A escolha do destino documental não equivale à aprovação técnica do HEAD.

[<u>Orientação registrada no tópico, mensagem de 22h48</u>](https://discord.com/channels/1477078665920647280/1573872898806911066/1573877843371364552)

# Validação e limites

Em 21/11/2026, go test -count=1 ./..., go vet ./... e go build ./... passaram com Go 1.27.0 Windows/amd64. go test -race -count=1 -v ./... passou na imagem golang:1.27.0 Linux/amd64 com Redis 8.2.10 e OpenObserve 1.1.2 reais em contêineres exclusivos de teste, com integrações opt-in habilitadas e sem skips. git diff --check passou e os arquivos Go da PR foram conferidos com gofmt.

A execução cobre lote unitário e múltiplo, paginação e cópias, contagens divergentes, isolamento, configuração ausente, erros HTTP, timeout, corpo truncado, sufixo JSON inválido e resposta acima de 32 MiB. O race nativo no Windows falhou pelo compilador C sem suporte 64 bits. A validação com detector de corridas foi concluída em Linux.

[<u>Saída integral da suíte com race e integrações</u>](https://github.com/LhamaLog/lhamalog-finder/blob/a7952222e1cf2c710f17629ddfb248cd8ca72630/specs/005-recuperar-logs-lote/evidencias/revisao-2026-11-21-race.txt)

O HEAD da PR \#7 em 3b26753 não é ancestral da branch da PR \#8. As correções exclusivas dessa branch anterior não foram incorporadas. A prova executada na própria branch da \#8 não atesta a futura composição 004 + 005. Na consulta ao GitHub, a PR estava aberta, integrável e sem check runs configurados.

O parecer do Discord para b7eb540 apontou inconsistências documentais e solicitou registrar as decisões estruturais. a795222 corrigiu README, rastreabilidade T029/T030 e o seletor do Spec Kit, além de alinhar a descrição da PR às provas reproduzidas. Este documento publica no Drive o contrato, as decisões, as consequências e os limites da entrega. A aprovação do HEAD atual depende de novo parecer explícito.

[<u>Histórico da revisão no Discord</u>](https://discord.com/channels/1477078665920647280/1565511601753165955/threads/1573872898806911066)

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

Resultado da segunda rodada em 21/11/2026, 22h57

O parecer completo de sete partes confirmou o HEAD a7952222e1cf2c710f17629ddfb248cd8ca72630. Reconheceu o fechamento dos ajustes internos, rebaixou a confirmação sem encaminhamento dos registros a risco documentado e confirmou que os cinco documentos do Drive cobrem o conteúdo solicitado. O veredito permaneceu “Apto para merge: NÃO”. O parecer declarou como único bloqueio a exigência de publicação em lhamalog-docs e condicionou a aceitação do Drive à confirmação do Michel no tópico. A execução mantém a orientação do solicitante de atualizar a documentação somente no Drive. O avanço da sequência está aguardando decisão sobre a regra de aprovação obrigatória.

Parecer completo da segunda rodada — https://discord.com/channels/1477078665920647280/1573872898806911066/1573880093116473474
