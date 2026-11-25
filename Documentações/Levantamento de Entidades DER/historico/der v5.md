# DER LhamaLog — v5 (v4 + matriz de alertas por empresa)

**Versão 5 (12/10/2026).** `PapelNotificacao` e `PapelSeveridade` (ADR_134): papéis de notificação por tenant e gravidades associadas. Versão 4 em `v4/`.

**Versão 4 (12/10/2026).** `TabelaPrecificacao` com os campos da ADR_131 (base: planilha Plano de Monetização); `Membro.status` com `ACESSO_PENDENTE` por até 24 h (ADR_132). Versão 3 em `v3/`.

**Versão 3 (12/10/2026).** Aplica o modelo SaaS pool multi-tenant (ADR_121 a ADR_130). Entidades novas com o comentário
`NOVO v3` e destaque azul no PNG. Nada foi removido: `Empresa`, `Usuario`, `Acesso`, `PermissaoProduto`, `Gestor`,
`Vinculo` e `CredencialIngestao` ficam marcadas como **substituídas** (ligação tracejada "substituido por"):
- `Empresa` → `Tenant` (empresa cliente = Organization da Clerk, `clerkOrgId`) — ADR_121
- `Usuario` / `Acesso` / `Gestor` / `Vinculo` → `Membro` (tenantId, clerkUserId, papel DONO/ADMIN/MEMBRO) — ADR_122/123
- `PermissaoProduto` → `AcessoProduto` (membroId, produtoId; DONO/ADMIN veem todos) — ADR_122
- `CredencialIngestao` / `ExternalToken` → `Produtor` + `TokenApi` (token AES-256-GCM, hash SHA-256, revokedAt) — ADR_113/122
- `Assinatura` ganha `tenantId` e `limites` (IA, retenção, créditos); downgrade altera só ela (ADR_124) e excedentes ficam `ACESSO_PENDENTE` (ADR_129)
- `EventoGateway` ganha `origem`, `status` EXECUTADO/FALHA, `erro` e reprocessamento individual (ADR_125)
- `TabelaPrecificacao` (módulo Assinatura, ADR_127) e `ChaveLLMTenant` (coleção do **módulo Sugestão**, BYOK cifrada, ADR_128)
- Todas as demais entidades levam `tenantId` `[INFERIDO — campo não desenhado em cada uma]`.

**Versão 2 — revisão r3 (02/10/2026, 22h40).** Base: `der_v1.md` (transcrição fiel do frame DER do Miro "Database Schema").
Nomes alinhados ao Modelo de Classes original (`MotorAnalise`, `ClassificadorAnalise`, enum `Tipo`, `AchadoAnalise`) e às decisões
do Michel de 02/10 (r3). A v2 **adiciona** entidades, campos e ligações, altera **uma** cardinalidade e **move** quatro campos da
`Ocorrencia` para a nova entidade `AchadoAnalise` (tudo marcado abaixo). As ligações `[INFERIDO]` da v1 continuam marcadas.

Alinhado com: ADR_004 a ADR_020 (as decisões da r3 estão nas **ADR_016 a ADR_020**), diagramas de sequência
(`Atualização - 02/10 > Diagramas de Sequencia v2`: `varredura_v2.png`, `finder_v2.png` r3) e planilha `Modelo de Classes LhamaLog v2` (abas v2/r2).
**Atenção:** por decisão do Michel, a planilha e o `diagrama_classes_varredura_finder_v2` **não foram atualizados na r3**; onde divergirem
(ex.: enum `Tipo` com INFO, `informacaoIdentificados`, `AchadoAnalise` sem tipo/gravidade/linha, GatewayLLM marcada como do módulo Sugestão),
valem este DER, o `finder_v2` e as ADR_016 a ADR_020. Nomes em camelCase como no Miro.

**Destaque visual:** no PNG, as 6 entidades novas estão com **fundo amarelo e borda laranja grossa**; campos novos têm o comentário `NOVO v2`;
campos movidos têm `MOVIDO da Ocorrencia do Miro`; ligações novas têm o rótulo `(NOVO v2)`; a cardinalidade alterada tem `(ALTERADO v2 ...)`.

## Decisões do Michel aplicadas na r3 (registradas nas ADR_016 a ADR_020)
1. Enum `Tipo` do `ClassificadorAnalise`: **ERRO, WARNING, SPAM** (+ RECORRENTE `[PENDENTE]`, revisão 03/10 14h). **INFO foi removido**: o que era INFO passa a ser SPAM (**ADR_019**, complementa a ADR_012).
2. **Grão:** a `Ocorrencia` segue o modelo de classes = **resumo por Arquivo**, com a lista de achados. `tipo`, `gravidade`, `linha` (e `conteudo`)
   são características de **cada achado** → nova entidade `AchadoAnalise`. São essas características que vão como contexto para a IA quando o
   usuário pedir uma `Sugestao` (o módulo Sugestão lê a Ocorrencia e seus achados pelo seu próprio caminho) (**ADR_020**).
3. **Todo Arquivo gera uma Ocorrencia-resumo** (relatório final), inclusive quando só tem spam — nesse caso, sem achados (`achadosIdentificados = 0`).
   Registrado na **ADR_020**, que substitui o trecho "monta a Ocorrência, se houver" da ADR_011 e complementa o ponto "spam não gera Ocorrências" da ADR_012 (ADRs antigas não editadas).
4. A `GatewayLLM` do Finder é exclusiva do Finder/MotorAnalise, sem ligação com o módulo Sugestão (**ADR_018**); o Finder chama `classificarAnalise()` e orquestra a análise (**ADR_017**); nomes do modelo de classes original prevalecem (**ADR_016**).

## Changelog v2 (o que é novo em relação à v1 / Miro)

### Entidades novas (6)
| Entidade | Módulo | Campos | Observação |
|---|---|---|---|
| **AchadoAnalise** | MOD_FINDER | id, ocorrenciaId (FK), tipo, gravidade, linha, conteudo, traceId (FK), correlationId, hostName, moduloId (FK), chaveAchado (UK), vetorRef [PENDENTE] | achado de um log/série dentro da Ocorrencia-resumo; recebe `tipo`, `gravidade`, `linha`, `conteudo` que no Miro estavam na Ocorrencia; contexto da Sugestão |
| **Trace** | MOD_COLETOR | id, traceId (UK, trace_id OTel), correlationId, prioridade, geradoEm | Arquivo agrupa traces; prioridade herdada do Modulo mais prioritário (ADR_008) |
| **Modulo** | MOD_VARREDURA | id, serviceName (UK), nome, prioridade (padrão MEDIUM), criadoEm | autocadastro pelo `service.name` com nome numérico (ADR_007/008) |
| **TraceModulo** | MOD_COLETOR | id, traceId (FK → Trace.traceId), moduloId (FK) | associativa N:M Trace × Modulo |
| **TravaVarredura** [INFERIDO] | MOD_VARREDURA | id, varreduraId (FK), escopo [PENDENTE], adquiridaEm, expiraEm [PENDENTE] | impede duas varreduras simultâneas (ADR_010); só vira tabela se a trava for persistida no banco |
| **RecorrenciaLog** [INFERIDO] | MOD_FINDER | id, achadoAnaliseId (FK), assinaturaLog, hostName, arquivosSeguidos (3 ou 4 [PENDENTE]), primeiraEm, ultimaEm | recorrência = mesmo log, mesma máquina, 3–4 arquivos seguidos (ADR_013) |

### Ocorrencia: de "achado" (Miro) para "resumo por Arquivo" (v2)
| Campo do Miro | Na v2 |
|---|---|
| `id`, `status`, `descobertaEm`, `arquivada` | mantidos na `Ocorrencia` |
| `tipo` | **MOVIDO** para `AchadoAnalise.tipo` (valores do enum `Tipo` que geram achado: ERRO, WARNING, RECORRENTE [PENDENTE]) |
| `gravidade` | **MOVIDO** para `AchadoAnalise.gravidade` ([PENDENTE] valores e quem define a criticidade — ADR_011) |
| `linha` | **MOVIDO** para `AchadoAnalise.linha` |
| `conteudo` | **MOVIDO** para `AchadoAnalise.conteudo` |

Campos novos da `Ocorrencia` (resumo, iguais ao modelo de classes): `arquivoId` (FK), `chaveIdempotencia` (UK, = arquivoId — ADR_014),
`registrosProcessados`, `achadosIdentificados`, `spamIdentificados` (substitui `informacaoIdentificados` do modelo de classes, já que INFO virou SPAM),
`dadosSensiveisIdentificados`, `recorrentesIdentificados` [INFERIDO], `statusProcessamento` [A CONFERIR valores].
Os campos por log da revisão anterior (`traceId`, `correlationId`, `classificacao`, `recorrente`, `hostName`, `moduloId`, `vetorRef`) saíram da
Ocorrencia e foram para `AchadoAnalise` (`classificacao` virou `tipo`).

### Campos novos nas outras entidades da v1
- **Varredura**: `agendamentoId` (FK, **opcional** — null em varredura disparada pelo limite da fila ou forçada), `trigger` (SCHEDULED, QUEUE_SIZE, FORCED [INFERIDO]), `snapshotEm` (corte da FilaDesordenada no disparo). Valores de `status`: PENDING, PROCESSING, COMPLETED, COMPLETED_WITH_ERROR.
- **ArquivoVarredura**: `prioridade` (NivelPrioridade [INFERIDO]), `ordem` (posição na FilaOrdenada [INFERIDO]), `maxTentativas` [PENDENTE]. Mesmos valores de `status`.
- **Agendamento**: `status` (ACTIVE, ... — planilha v2) [INFERIDO; o Miro tem `ativo Boolean`, mantido].
- **Arquivo**: `geradoEm` (desempate da ordenação: mais antigo primeiro), `traceCount` [INFERIDO].

### NivelPrioridade
Não vira tabela: é enum `VERY_HIGH, HIGH, MEDIUM, LOW, VERY_LOW` (padrão MEDIUM) usado como campo `prioridade` em Modulo, Trace e ArquivoVarredura.

### Ligações novas e alterada
| A | Rótulo | Card. A / B | B | Observação |
|---|---|---|---|---|
| Arquivo | agrupa | 1 / 0..* | Trace | NOVO v2: Arquivo agrupa traces e logs |
| Trace | passa por | 1 / 1..* | TraceModulo | NOVO v2 |
| Modulo | aparece em | 1 / 0..* | TraceModulo | NOVO v2 |
| Produto | autocadastra | 1 / 0..* | Modulo | NOVO v2: por service.name [INFERIDO Produto como dono] |
| Arquivo | resumo | 1 / 0..1 | Ocorrencia | NOVO v2: Ocorrencia.arquivoId = chaveIdempotencia (uma Ocorrencia-resumo por Arquivo) |
| Ocorrencia | achados | 1 / 0..* | AchadoAnalise | NOVO v2: achados vazios quando o Arquivo só tem spam |
| Trace | origem | 0..1 / 0..* | AchadoAnalise | NOVO v2: AchadoAnalise.traceId (null quando o log não tem trace) |
| Modulo | afeta | 0..1 / 0..* | AchadoAnalise | NOVO v2: AchadoAnalise.moduloId |
| AchadoAnalise | recorrência | 1 / 0..* | RecorrenciaLog | NOVO v2 [INFERIDO] |
| Varredura | segura | 1 / 0..1 | TravaVarredura | NOVO v2 [INFERIDO]: impede duas varreduras simultâneas |
| Agendamento | dispara | **0..1** / 0..* (era 1 / 0..*) | Varredura | **ALTERADO v2**: o Agendamento não aponta para uma única Varredura; cada Varredura aponta (opcionalmente) para o Agendamento que a disparou |

As ligações da v1 que chegam à `Ocorrencia` (`Varredura identifica`, `Produto`, `HistoricoOcorrencia`, `Sugestao`, `Notificacao origina`) continuam
na Ocorrencia-resumo. `[PENDENTE]` se a `Sugestao` passa a apontar também para um `AchadoAnalise` específico.

### O que NÃO virou entidade (e por quê)
- **FilaDesordenada / FilaOrdenada**: filas em memória/broker (ADR_007/009). O que precisa sobreviver fica em `ArquivoVarredura` (status, prioridade, ordem, tentativas) e em `Varredura.snapshotEm`.
- **MotorAnalise** e a interface **GatewayLLM do Finder** (exclusiva do Finder/MotorAnalise, sem ligação com o módulo Sugestão — ADR_018): serviço/integração com a LLM.
- **BancoVetorial**: armazenamento externo de vetores, fora do banco relacional; `AchadoAnalise.vetorRef` [PENDENTE] se for preciso apontar para o vetor.
- **ClassificadorAnalise** (serviço com o enum `Tipo`): o resultado vira `AchadoAnalise.tipo` e os contadores da Ocorrencia.
- **ScannerSegurança, ContextoAnalise, LogNormalizado**: serviço, objeto transiente e intermediário (levantamento); o ScannerSegurança alimenta `Ocorrencia.dadosSensiveisIdentificados`.
- **Finder, ModuloOcorrencia, AgendamentoVarredura.dispatch()**: serviços/comportamento.

## Código Mermaid

```mermaid
---
title: DER LhamaLog v5 - multi-tenant, TabelaPrecificacao e matriz de alertas (NOVO v3 e v5 em azul)
---
erDiagram
    %% ===== MOD_ASSINATURA_PAGAMENTO =====
    Plano {
        UUID id
        String nome
        Decimal precoMensal
        Integer armazenamento
        Integer retencao
        Boolean recursoIA
        Boolean dashboard
    }
    Assinatura {
        UUID id
        String status
        DateTime inicioVigencia
        DateTime fimVigencia
        DateTime canceladaEm
    }
    Pagamento {
        UUID id
        Decimal valor
        String status
        String referenciaExterna
        DateTime processadoEm
    }
    Reembolso {
        UUID id
        Decimal valor
        String motivo
        String status
        DateTime solicitadoEm
    }
    EventoGateway {
        UUID id
        String origem
        String operacao
        String resultado
        String motivoFalha
        String payload
        DateTime recebidoEm
    }
    %% ===== MOD_LEGADO =====
    Executavel {
        UUID id
        String versao
        String status
        String pastaMonitorada
        DateTime heartbeat
    }
    ExternalToken {
        UUID id
        String status
        DateTime criadoEm
        DateTime revogadoEm
    }
    %% ===== MOD_PRODUTO_CONTEXTO =====
    Produto {
        UUID id
        String nome
        String descricao
        String status
        DateTime criadoEm
    }
    ContextoEmpresa {
        UUID id
        String conteudo
        DateTime atualizadoEm
    }
    ContextoProduto {
        UUID id
        String conteudo
        DateTime atualizadoEm
    }
    PoliticaRetencao {
        UUID id
        String tipoDado
        Integer diasRetencao
        Boolean ativo
    }
    ConfiguracaoProduto {
        UUID id
        Boolean ativo
        Boolean varreduraAvancada
        Map parametros
    }
    %% ===== MOD_OPENTELEMETRY =====
    IntegracaoOpenTelemetry {
        UUID id
        String protocolo
        String endpoint
        Boolean logsHabilitados
        Boolean metricasHabilitadas
        Boolean tracesHabilitados
        String status
        DateTime ultimaValidacao
    }
    FonteTelemetria {
        UUID id
        String nome
        String tipo
        String ambiente
        String serviceName
        String namespace
        String status
        DateTime ultimaComunicacao
    }
    CredencialIngestao {
        UUID id
        String tipo
        String identificador
        String status
        DateTime criadaEm
        DateTime expiraEm
        DateTime revogadaEm
    }
    %% ===== MOD_COLETOR =====
    Arquivo {
        UUID id
        String nome
        String bucketUrl
        String extensao
        Decimal tamanhoMb
        DateTime importadoEm
        Boolean excluido
        DateTime geradoEm "NOVO v2 - desempate da ordenação (mais antigo primeiro)"
        Integer traceCount "NOVO v2 [INFERIDO]"
    }
    LoteAgrupador {
        UUID id
        String status
        DateTime criadoEm
        Integer quantidadeItens
    }
    LogRecebido {
        UUID id
        DateTime recebidoEm
        String origem
        String severidade
        String conteudo
    }
    %% NOVO v2: Trace
    Trace {
        UUID id "NOVO v2"
        String traceId UK "trace_id OTel"
        String correlationId
        String prioridade "herda o Modulo mais prioritário"
        DateTime geradoEm
    }
    %% NOVO v2: TraceModulo
    TraceModulo {
        UUID id "NOVO v2"
        String traceId FK "Trace.traceId"
        UUID moduloId FK "Modulo.id"
    }
    %% ===== MOD_EMPRESA_IDENTIDADE =====
    Usuario {
        UUID id
        String nome
        String email
        String status
        DateTime criadoEm
    }
    Configuracao2FA {
        UUID id
        Boolean habilitado
        String metodo
        DateTime atualizadoEm
    }
    Gestor {
        UUID id
        String nome
        String status
    }
    Empresa {
        UUID id
        String cnpj
        String razaoSocial
        String nomeFantasia
        String status
        Endereco endereco
    }
    Vinculo {
        UUID id
        String papel
        DateTime inicioVigencia
        DateTime fimVigencia
    }
    Endereco {
        UUID id
        String tipo
        String logradouro
        String cidade
        String estado
        String cep
    }
    Acesso {
        UUID id
        String perfil
        Boolean bloqueado
        DateTime ultimoAcesso
    }
    PermissaoProduto {
        UUID id
        String papel
        String nivelPermissao
        String status
        DateTime inicioVigencia
        DateTime fimVigencia
    }
    %% ===== MOD_RELATORIOS =====
    Relatorio["Relatório"] {
        texto caixa_sem_atributos
    }
    ExportacaoRelatorio {
        UUID id
        String formato
        String status
        DateTime criadaEm
        String arquivoUrl
    }
    GeracaoRelatorioAgendada {
        UUID id
        String cron
        Boolean ativa
        DateTime proximaExecucao
    }
    RelatorioConsolidado {
        UUID id
        DateTime periodoInicio
        DateTime periodoFim
        DateTime geradoEm
    }
    %% ===== MOD_VARREDURA =====
    Agendamento {
        UUID id
        String cron
        Boolean ativo
        DateTime criadoEm
        DateTime proximaExecucao
        String status "v2 - ACTIVE, ... (planilha v2: AgendamentoVarreduraStatus) [INFERIDO]"
    }
    Varredura {
        UUID id
        String status "PENDING, PROCESSING, COMPLETED, COMPLETED_WITH_ERROR"
        DateTime iniciadaEm
        DateTime finalizadaEm
        Boolean avancada
        UUID agendamentoId FK "NOVO v2 - opcional (null em varredura por limite da fila ou forçada)"
        String trigger "NOVO v2 - SCHEDULED, QUEUE_SIZE, FORCED [INFERIDO]"
        DateTime snapshotEm "NOVO v2 - corte da FilaDesordenada no disparo"
    }
    ArquivoVarredura {
        UUID id
        String status "PENDING, PROCESSING, COMPLETED, COMPLETED_WITH_ERROR"
        Integer tentativas
        String erro
        DateTime iniciadaEm
        DateTime finalizadaEm
        String prioridade "NOVO v2 - NivelPrioridade VERY_HIGH..VERY_LOW [INFERIDO]"
        Integer ordem "NOVO v2 - posição na FilaOrdenada [INFERIDO]"
        Integer maxTentativas "NOVO v2 [PENDENTE] limite de retentativas"
    }
    %% NOVO v2: TravaVarredura
    TravaVarredura {
        UUID id "NOVO v2 [INFERIDO]"
        UUID varreduraId FK
        String escopo "[PENDENTE] global ou por Produto"
        DateTime adquiridaEm
        DateTime expiraEm "[PENDENTE]"
    }
    %% NOVO v2: Modulo
    Modulo {
        UUID id "NOVO v2"
        String serviceName UK "service.name do OTel - autocadastro"
        String nome "nome numérico no autocadastro"
        String prioridade "NivelPrioridade - padrão MEDIUM"
        DateTime criadoEm
    }
    %% ===== MOD_FINDER =====
    Ocorrencia {
        UUID id
        String status
        DateTime descobertaEm
        Boolean arquivada
        UUID arquivoId FK "NOVO v2 - um resumo por Arquivo (todo Arquivo gera, inclusive só spam)"
        String chaveIdempotencia UK "NOVO v2 - = arquivoId (ADR_014)"
        Integer registrosProcessados "NOVO v2"
        Integer achadosIdentificados "NOVO v2"
        Integer spamIdentificados "NOVO v2 - substitui informacaoIdentificados (INFO removido)"
        Integer dadosSensiveisIdentificados "NOVO v2"
        Integer recorrentesIdentificados "NOVO v2 [INFERIDO]"
        String statusProcessamento "NOVO v2 [A CONFERIR] valores"
    }
    HistoricoOcorrencia {
        UUID id
        String acao
        String estadoAnterior
        String estadoNovo
        String observacao
        DateTime dataHora
    }
    %% NOVO v2: AchadoAnalise
    AchadoAnalise {
        UUID id PK "NOVO v2"
        UUID ocorrenciaId FK "Ocorrencia-resumo do Arquivo"
        String tipo "ERRO, WARNING, RECORRENTE [PENDENTE] - MOVIDO da Ocorrencia do Miro"
        String gravidade "MOVIDO da Ocorrencia do Miro - [PENDENTE] valores / quem define"
        Integer linha "MOVIDO da Ocorrencia do Miro"
        String conteudo "MOVIDO da Ocorrencia do Miro - até 512 caracteres"
        String traceId FK "null se o log não tiver trace"
        String correlationId
        String hostName "mesma máquina (recorrência)"
        UUID moduloId FK "Modulo mais prioritário do trace"
        String chaveAchado UK "ocorrenciaId + traceId + linha [INFERIDO]"
        String vetorRef "[PENDENTE] referência no BancoVetorial"
    }
    %% NOVO v2: RecorrenciaLog
    RecorrenciaLog {
        UUID id "NOVO v2 [INFERIDO]"
        UUID achadoAnaliseId FK
        String assinaturaLog "log normalizado/hash"
        String hostName "mesma máquina"
        Integer arquivosSeguidos "3 ou 4 [PENDENTE]"
        DateTime primeiraEm
        DateTime ultimaEm
    }
    %% ===== MOD_NOTIFICACOES =====
    Notificacao {
        UUID id
        String canal
        String titulo
        String conteudo
        String status
        Boolean lida
        DateTime criadaEm
    }
    TentativaEntrega {
        UUID id
        String status
        String motivoFalha
        DateTime executadaEm
    }
    PreferenciaNotificacao {
        UUID id
        Boolean email
        Boolean push
        Boolean web
        String severidadeMinima
    }
    DispositivoPush {
        UUID id
        String token
        String plataforma
        DateTime registradoEm
        DateTime ultimoUso
    }
    %% ===== MOD_IA =====
    Sugestao {
        UUID id
        String conteudo
        String status
        Integer tokensConsumidos
        DateTime criadaEm
        DateTime fechadaEm
    }
    AvaliacaoSugestao {
        UUID id
        Integer nota
        String comentario
        DateTime criadaEm
    }
    %% ===== MOD_CREDITOS =====
    Credito {
        UUID id
        Decimal quantidade
        DateTime expiraEm
        String status
    }
    Transacao {
        UUID id
        String tipo
        Decimal quantidade
        String descricao
        DateTime criadaEm
    }
    %% ===== RELACIONAMENTOS =====
    Empresa ||--o{ Assinatura : "contrata"
    Plano ||--o{ Assinatura : "plano"
    Assinatura ||--o{ Pagamento : "cobranças"
    Pagamento ||--o{ Reembolso : "reembolso"
    Reembolso |o--o{ EventoGateway : "eventos"
    Executavel ||--o{ ExternalToken : "LEGADO"
    Produto ||--o{ ContextoEmpresa : "contexto"
    Produto ||--o{ PoliticaRetencao : "retenção"
    Produto ||--o{ ConfiguracaoProduto : "configura"
    IntegracaoOpenTelemetry ||--o{ CredencialIngestao : "autentica"
    IntegracaoOpenTelemetry ||--|{ FonteTelemetria : "configura"
    FonteTelemetria ||--o{ LogRecebido : "envia"
    LoteAgrupador ||--|{ LogRecebido : "agrupa"
    Usuario ||--o| Configuracao2FA : "configura"
    Usuario ||--o| Acesso : "perfil"
    Gestor ||--o{ Empresa : "participa"
    Empresa ||--o{ Vinculo : "possui"
    Empresa ||--o{ Endereco : "possui"
    Usuario ||--o{ Sugestao : "solicita"
    Usuario ||--o{ ContextoEmpresa : "contexto"
    GeracaoRelatorioAgendada ||--o{ RelatorioConsolidado : "gera"
    %% ALTERADO v2: era 1/0..* no Miro; Varredura.agendamentoId opcional
    Agendamento |o--o{ Varredura : "dispara (ALTERADO v2: Agendamento opcional)"
    Varredura ||--o{ ArquivoVarredura : "processa"
    Ocorrencia ||--o{ HistoricoOcorrencia : "histórico"
    Notificacao ||--o{ TentativaEntrega : "entregas"
    Sugestao ||--o{ AvaliacaoSugestao : "avaliações"
    %% [INFERIDO] origem ilegível; doc: Varredura 1:N Ocorrencia
    Varredura ||--o{ Ocorrencia : "identifica [INFERIDO]"
    %% [INFERIDO] doc: Empresa 1:N Produto
    Empresa ||--o{ Produto : "possui [INFERIDO]"
    %% [INFERIDO] doc: Empresa 1:N Usuario
    Empresa ||--o{ Usuario : "possui [INFERIDO]"
    %% [INFERIDO] doc: Empresa 1:N Credito
    Empresa ||--o{ Credito : "possui [INFERIDO]"
    %% [INFERIDO] doc: Produto 1:1/N ContextoProduto (única 'possui 1/0..1')
    Produto ||--o| ContextoProduto : "possui [INFERIDO]"
    %% [INFERIDO] doc: Produto 1:N Executavel no modelo antigo
    Produto ||--o{ Executavel : "LEGADO [INFERIDO]"
    %% [INFERIDO] tracejada; doc: ExternalToken -> generalizar para CredencialIngestao
    ExternalToken ||..o{ CredencialIngestao : "substituir [INFERIDO]"
    %% [INFERIDO] tracejada, alvo ilegível; doc: substituir por fonte/exportador (alternativa: IntegracaoOpenTelemetry)
    Executavel ||..o{ FonteTelemetria : "substituir [INFERIDO]"
    %% [INFERIDO] doc: IntegracaoOpenTelemetry.produtoId
    Produto ||--o{ IntegracaoOpenTelemetry : "integração [INFERIDO]"
    %% [INFERIDO] doc: Produto 1:N FonteTelemetria
    Produto ||--o{ FonteTelemetria : "fontes [INFERIDO]"
    %% [INFERIDO] doc: Usuario 1:N Notificacao
    Usuario ||--o{ Notificacao : "recebe [INFERIDO]"
    %% [INFERIDO] doc: Usuario 1:N PreferenciaNotificacao
    Usuario ||--o{ PreferenciaNotificacao : "configura [INFERIDO]"
    %% [INFERIDO] doc: Usuario 1:N DispositivoPush
    Usuario ||--o{ DispositivoPush : "dispositivos [INFERIDO]"
    %% [INFERIDO] doc 8: Sugestao relacionada ao usuário avaliador
    Usuario ||--o{ AvaliacaoSugestao : "avalia [INFERIDO]"
    %% [INFERIDO] doc 7.4: HistoricoOcorrencia.usuarioId
    Usuario ||--o{ HistoricoOcorrencia : "realiza [INFERIDO]"
    %% [INFERIDO] doc: Produto 1:N Agendamento
    Produto ||--o{ Agendamento : "agenda [INFERIDO]"
    %% [INFERIDO] doc: Produto 1:N Varredura
    Produto ||--o{ Varredura : "executa [INFERIDO]"
    %% [INFERIDO] doc: histórico de movimentações de créditos
    Credito ||--o{ Transacao : "movimentações [INFERIDO]"
    %% [INFERIDO] doc: Sugestao 0..1:N Transacao
    Sugestao |o--o{ Transacao : "consumoIA [INFERIDO]"
    %% [INFERIDO] doc 8: Notificacao relacionada a Ocorrencia quando aplicável
    Ocorrencia |o--o{ Notificacao : "origina [INFERIDO]"
    %% [INFERIDO] sem rótulo; doc: Arquivo N:M Varredura via ArquivoVarredura
    Arquivo ||--o{ ArquivoVarredura : "(sem rótulo) [INFERIDO]"
    %% [INFERIDO] sem rótulo; doc: Produto 1:N Ocorrencia
    Produto ||--o{ Ocorrencia : "(sem rótulo) [INFERIDO]"
    %% [INFERIDO] sem rótulo; doc: Ocorrencia 1:N Sugestao
    Ocorrencia ||--o{ Sugestao : "(sem rótulo) [INFERIDO]"
    %% [INFERIDO] sem rótulo; doc: Pagamento/Assinatura 1:N EventoGateway
    Pagamento |o--o{ EventoGateway : "(sem rótulo) [INFERIDO]"
    %% [INFERIDO] sem rótulo; doc: Pagamento/Assinatura 1:N EventoGateway
    Assinatura |o--o{ EventoGateway : "(sem rótulo) [INFERIDO]"
    %% [INFERIDO] doc: Produto 1:N Arquivo (confiança baixa no rótulo)
    Produto ||--o{ Arquivo : "pertence [INFERIDO]"
    %% [INFERIDO] doc 7.2: PermissaoProduto = Gestor x Produto (confiança baixa)
    Produto ||--o{ PermissaoProduto : "concede [INFERIDO]"
    %% [INFERIDO] Gestor recebe [?]; doc 7.2 (confiança baixa)
    Gestor ||--o{ PermissaoProduto : "recebe [INFERIDO]"
    %% [INFERIDO] doc: Vinculo associa Gestor x Empresa (confiança baixa)
    Gestor ||--o{ Vinculo : "possui [INFERIDO]"
    %% ===== NOVO v2 (Varredura e Finder) =====
    %% NOVO v2: Arquivo agrupa traces e logs
    Arquivo ||--o{ Trace : "agrupa (NOVO v2)"
    %% NOVO v2
    Trace ||--|{ TraceModulo : "passa por (NOVO v2)"
    %% NOVO v2
    Modulo ||--o{ TraceModulo : "aparece em (NOVO v2)"
    %% NOVO v2: por service.name [INFERIDO Produto como dono]
    Produto ||--o{ Modulo : "autocadastra (NOVO v2)"
    %% NOVO v2: Ocorrencia.arquivoId = chaveIdempotencia (uma Ocorrencia-resumo por Arquivo)
    Arquivo ||--o| Ocorrencia : "resumo (NOVO v2)"
    %% NOVO v2: achados vazios quando o Arquivo só tem spam
    Ocorrencia ||--o{ AchadoAnalise : "achados (NOVO v2)"
    %% NOVO v2: AchadoAnalise.traceId (null quando o log não tem trace)
    Trace |o--o{ AchadoAnalise : "origem (NOVO v2)"
    %% NOVO v2: AchadoAnalise.moduloId
    Modulo |o--o{ AchadoAnalise : "afeta (NOVO v2)"
    %% NOVO v2 [INFERIDO]
    AchadoAnalise ||--o{ RecorrenciaLog : "recorrência (NOVO v2)"
    %% NOVO v2 [INFERIDO]: impede duas varreduras simultâneas
    Varredura ||--o| TravaVarredura : "segura (NOVO v2)"
    %% ===== NOVO v3 (multi-tenant, ADR_121-130) =====
    Tenant {
        string tenantId PK "NOVO v3"
        string clerkOrgId UK
        string nome
        string status
    }
    Membro {
        string membroId PK "NOVO v3"
        string tenantId FK
        string clerkUserId
        string papel "DONO ADMIN MEMBRO"
        string status "ATIVO ACESSO_PENDENTE bloqueado ate aprovacao 24h"
    }
    AcessoProduto {
        string membroId FK "NOVO v3"
        string produtoId FK
    }
    Produtor {
        string producerId PK "NOVO v3"
        string tenantId FK
        string produtoId FK
    }
    TokenApi {
        string producerId FK "NOVO v3"
        string tokenCifrado "AES-256-GCM"
        string hashSha256 UK
        date revokedAt
    }
    TabelaPrecificacao {
        string plano PK "NOVO v3 ADR_131"
        string volumeIngestao
        string nivelInterpretacao
        int retencaoDias
        string extraDashboard
        string rateLimit "PENDENTE"
        number precoMensal
        int limiteProdutos "PENDENTE"
        int limiteMembros "PENDENTE"
        number creditosIA "PENDENTE"
        number custoAddOnClerk "PENDENTE"
        number margemAddOn "PENDENTE"
        number precoAddOn
    }
    ChaveLLMTenant {
        string tenantId FK "NOVO v3 modulo Sugestao"
        string provedor
        string chaveCifrada "AES-256-GCM"
        date revokedAt
    }
    Tenant ||--|| Assinatura : "possui (NOVO v3)"
    Tenant ||--o{ Membro : "membros (NOVO v3)"
    Tenant ||--o{ Produto : "produtos (NOVO v3)"
    Membro ||--o{ AcessoProduto : "recebe (NOVO v3)"
    Produto ||--o{ AcessoProduto : "libera (NOVO v3)"
    Produto ||--o{ Produtor : "produtores (NOVO v3)"
    Produtor ||--o{ TokenApi : "tokens (NOVO v3)"
    Tenant ||--o{ ChaveLLMTenant : "byok (NOVO v3)"
    Tenant ||--o{ EventoGateway : "eventos (NOVO v3)"
    TabelaPrecificacao ||--o{ Assinatura : "preco (NOVO v3)"
    Membro ||--o{ Notificacao : "recebe por papel (NOVO v3)"
    Empresa ||..|| Tenant : "substituido por (v3)"
    Usuario ||..|| Membro : "substituido por (v3)"
    PermissaoProduto ||..|| AcessoProduto : "substituido por (v3)"
    CredencialIngestao ||..|| TokenApi : "substituido por (v3)"
    PapelNotificacao {
        string papelNotificacaoId PK "NOVO v5 ADR_134"
        string tenantId FK
        string nome
    }
    PapelSeveridade {
        string tenantId FK "NOVO v5"
        string papelNotificacaoId FK
        string gravidade
    }
    Tenant ||--o{ PapelNotificacao : "define (NOVO v5)"
    PapelNotificacao ||--o{ PapelSeveridade : "recebe gravidades (NOVO v5)"
    Membro }o--o{ PapelNotificacao : "participa (NOVO v5)"
    classDef novo3 fill:#DCEBFF,stroke:#1D4ED8,stroke-width:4px
    class Tenant,Membro,AcessoProduto,Produtor,TokenApi,TabelaPrecificacao,ChaveLLMTenant,PapelNotificacao,PapelSeveridade novo3
    %% destaque visual das entidades NOVO v2
    classDef novo fill:#FFE8A3,stroke:#D97706,stroke-width:4px
    class AchadoAnalise,Modulo,RecorrenciaLog,Trace,TraceModulo,TravaVarredura novo
```

## Pendências e decisões em aberto
1. `[PENDENTE]` RECORRENTE como valor do enum `Tipo` ou atributo (revisão 03/10 14h); `recorrentesIdentificados` depende disso.
2. `[PENDENTE]` valores de `AchadoAnalise.gravidade` e quem define a criticidade (Finder ou módulo de Ocorrência — ADR_011).
3. Opcional: atualizar o texto das ADR_011/012 (ou marcá-las como complementadas) para apontar para a ADR_020; nesta rodada elas não foram editadas.
4. `TravaVarredura`: tabela, lock no broker/cache ou advisory lock? Escopo global ou por Produto? Tempo de expiração?
5. `maxTentativas` e o limite de disparo por tamanho da fila (configuração interna — ex.: 10) não estão nas ADRs.
6. `RecorrenciaLog`: 3 ou 4 arquivos seguidos? `assinaturaLog` = hash do log normalizado?
7. `Modulo` pertence a `Produto` (assumido) ou a `FonteTelemetria` (que já tem `serviceName` no Miro)?
8. `Trace` como tabela própria ou só `traceId` no AchadoAnalise/ArquivoVarredura?
9. `statusProcessamento` da Ocorrencia: valores não definidos. `chaveAchado` (ocorrenciaId + traceId + linha) é inferida.
10. Sugestão por Ocorrencia-resumo ou por AchadoAnalise; destino/retenção das linhas SPAM (hoje só contadas em `spamIdentificados`).
11. Ligações [INFERIDO] de confiança baixa herdadas da v1 (ver `der_v1.md`) e `Relatório`/`ExportacaoRelatorio` sem ligação.
10. `[PENDENTE]` campos de `EventoGateway.payload`/tentativas, valores da `TabelaPrecificacao` e prazo do `ACESSO_PENDENTE`.
11. `[INFERIDO]` `tenantId` em todas as entidades; `Arquivo.owner_id`/`company_id` = `tenantId`.
12. `[PENDENTE]` lacunas da `TabelaPrecificacao` (ADR_131) e o que ocorre após 24 h de `ACESSO_PENDENTE` (ADR_132).
13. `[PENDENTE]` Membro N:M PapelNotificacao: tabela de ligação própria ou lista de membroIds no papel `[INFERIDO: lista]`.
14. ACESSO_PENDENTE bloqueia até aprovação do DONO em 24 h; sem aprovação expira (ADR_135).
