# Matriz de Rastreabilidade — Diagrama de Classes (LhamaLog)

**Versão 3 (17/10/2026).** Gerada a partir do `DC-10-diagrama-de-classes.md` **versão 8** (13 módulos). A versão 2, feita sobre o DC-10 v2 e os diagramas de sequência, foi para `v2/`. A planilha `rastreabilidade.xlsx` traz as mesmas tabelas em formato visual.

## Como ler

- **IDs**: classe `CL`, enum `ES`, relação `RE`, cardinalidade `CA`, operação `OP`, conflito ou pendência `CP`. Os IDs da v2 não valem mais: o diagrama mudou.
- **Módulo (§)**: a seção do DC-10 em que o elemento é definido, com atributos e métodos. Nas outras seções a classe aparece só como caixa de referência.
- **Base**: a aba da planilha do Modelo de Classes v2, a entidade do DER v9 ou a ADR que sustenta o elemento.
- **Requisitos**: USID e SSID da planilha "LhamaLog casos de uso" (71 requisitos, sem alteração desde 31/08). "(inferido)" marca uma ligação feita por nós, não escrita na fonte. Uma relação herda os requisitos comuns às duas classes; uma operação é rastreada pela classe.
- **Situação** (a pendência mais forte que a fonte registra para o elemento):
  - `[CONFIRMADO]` a fonte afirma o elemento e não há pendência aberta sobre ele;
  - `[CONFLITO]` duas fontes divergem; `[PENDENTE]` a fonte reconhece que falta definir; `[A CONFERIR]` erro ou dúvida da própria planilha;
  - `[PROPOSTO]` vem de ADR com status Proposta (inclui as ADR_154 a ADR_162, escritas para as decisões de fechamento do diagrama, e a ADR_149 do Asaas); `[SUBSTITUÍDA]` classe mantida só para mostrar o que a substitui; `[LEGADO]` módulo 13 (SDK e Executável).
- **Cobertura do requisito**: Coberto = ao menos uma classe ativa, ligada diretamente, sem conflito ou pendência aberta; Parcial = só há classes com pendência aberta ou ligação inferida; Só legado = só classes do módulo 13 ou substituídas.
- **Isolamento** (ADR_121, todo dado leva `tenantId`): se a classe tem `tenantId` próprio ou chega ao Tenant por outra classe.
- **Impacto**: Alto = 5 ou mais relações, ou conflito aberto numa classe com 2 ou mais relações; Médio = 2 a 4 relações ou pendência aberta; Baixo = o resto.
- **Fontes**: DC-10 v8 (que segue o Modelo de Classes v2, as ADRs até a 147, o DER v9 e a pauta de 03/10), a planilha de casos de uso, as ADR_154 a ADR_162 (propostas) e a ADR_149 (Asaas, proposta de 17/10, só como pendência). **Não usados**: os diagramas de sequência, que serão atualizados.

| § | Módulo | Classes | Enums |
|---|---|---|---|
| §1 | Tenant, Membro e Produto | 13 | 1 |
| §2 | Papéis de notificação — matriz de alertas | 3 | 0 |
| §3 | Assinatura e Pagamento | 11 | 9 |
| §4 | Créditos | 5 | 3 |
| §5 | Coletor | 11 | 0 |
| §6 | Varredura | 9 | 5 |
| §7 | Finder | 11 | 2 |
| §8 | Ocorrência | 4 | 0 |
| §9 | Sugestão | 8 | 1 |
| §10 | Notificação | 9 | 3 |
| §11 | Dashboard | 8 | 0 |
| §12 | Relatório | 6 | 1 |
| §13 | Legado | 16 | 2 |

## Sumário

1. Resumo de cobertura
2. Requisito → diagrama
3. ADR → elementos
4. Requisitos sem representação ou só no legado
5. Elementos sem requisito
6. Conflitos e pendências (CP)
7. Matriz de classes
8. Matriz de enums
9. Matriz de relações
10. Matriz de cardinalidades
11. Matriz de operações
12. Removidos e substituídos
13. Sugestões ainda em aberto
14. Artefatos

## 1. Resumo de cobertura

- **Elementos**: 114 classes (16 no legado, 6 substituídas), 27 enums, 248 relações (43 com cardinalidade), 256 operações, 134 conflitos e pendências.
- **Requisitos**: 71 (51 USID e 20 SSID). Coberto 55, Parcial 12, Só legado 4.
- **Situação das classes e enums**: `[CONFIRMADO]` 58, `[CONFLITO]` 25, `[PROPOSTO]` 18, `[LEGADO]` 17, `[PENDENTE]` 13, `[SUBSTITUÍDA]` 6, `[A CONFERIR]` 4.
- **Conflitos e pendências**: `[PENDENTE]` 52, `[CONFLITO]` 49, `[PROPOSTO]` 25, `[A CONFERIR]` 8.
- **O que falta para fechar as pendências**: Precisa de decisão do time 16; Aguarda aprovação de ADR 25; Atualizar DER ou planilha 33; Detalhe em aberto 52; Conferir na planilha 8. Uma pendência por linha marcada do DC-10, então o mesmo assunto pode aparecer em mais de uma.
- **ADRs**: 129 das ADRs citadas no DC-10 estão ligadas a pelo menos uma classe ou pendência. As que só aparecem como contexto estão na seção 3.
- **Novidades no Drive em 17/10**: ADR_148 (padrão de commit), ADR_149 (log de inicialização), outra ADR_149 (Asaas, proposta), ADR_150 (versão do Java) ADR_151 (perfis de execução), ADR_152 (Elasticsearch como banco vetorial, implementação do `BancoVetorial`) e ADR_153 (caminho do módulo Go do Finder). Só a do Asaas afeta a estrutura de classes (CP-134). O número 149 está duplicado no Drive. As ADRs escritas para o diagrama são as ADR_154 a ADR_162.

## 2. Requisito → diagrama

| Requisito | Título | Cobertura | Classes | Módulos | Pendências abertas |
|---|---|---|---|---|---|
| USID_001 | Visualizar Ocorrências Processados | **Parcial** | CL-066 `Ocorrencia` | §8 | CP-76, CP-77, CP-114, CP-130 |
| USID_002 | Consultar Ocorrência | **Parcial** | CL-066 `Ocorrencia` | §8 | CP-76, CP-77, CP-114, CP-130 |
| USID_003 | Marcar Ocorrência | **Parcial** | CL-066 `Ocorrencia` | §8 | CP-76, CP-77, CP-114, CP-130 |
| USID_004 | Arquivar Ocorrência | **Parcial** | CL-066 `Ocorrencia` | §8 | CP-76, CP-77, CP-114, CP-130 |
| USID_005 | Filtrar Ocorrência | **Parcial** | CL-066 `Ocorrencia` | §8 | CP-76, CP-77, CP-114, CP-130 |
| USID_006 | Importar Arquivo | **Coberto** | CL-033 `Coletor` (inferido), CL-039 `Arquivo`, CL-055 `LogNormalizado` (inferido) | §5, §7 | CP-41, CP-42, CP-43, CP-55, CP-121 |
| USID_007 | Consultar Arquivos Processados | **Coberto** | CL-039 `Arquivo`, CL-046 `ArquivoVarredura`, CL-065 `ResumoArquivo`, ES-16 `ArquivoScanStatus` | §5, §6, §8 | CP-41, CP-42, CP-43, CP-54, CP-55, CP-73, CP-120, CP-121 |
| USID_008 | Configurar Periodo de Retenção de Arquivos | **Parcial** | CL-018 `Plano`, CL-039 `Arquivo` (inferido) | §3, §5 | CP-23, CP-41, CP-42, CP-43, CP-55, CP-121, CP-124 |
| USID_009 | Receber Notificação Email | **Coberto** | CL-076 `Notificacao`, CL-077 `PreferenciaNotificacao`, CL-080 `EnviadorEmail`, CL-084 `TentativaEntrega`, ES-22 `CanalNotificacao`, ES-24 `StatusEnvioNotificacao` | §10 | CP-89, CP-97, CP-99, CP-100, CP-123, CP-126 |
| USID_010 | Receber Notificação Push | **Coberto** | CL-076 `Notificacao`, CL-077 `PreferenciaNotificacao`, CL-081 `EnviadorPush`, CL-083 `DispositivoPush`, CL-084 `TentativaEntrega`, ES-22 `CanalNotificacao`, ES-23 `PlataformaDispositivo`, ES-24 `StatusEnvioNotificacao` | §10 | CP-89, CP-97, CP-99, CP-100, CP-123, CP-126 |
| USID_011 | Receber Notificação Web | **Coberto** | CL-076 `Notificacao`, CL-077 `PreferenciaNotificacao`, CL-082 `EnviadorWeb`, CL-084 `TentativaEntrega`, ES-22 `CanalNotificacao`, ES-24 `StatusEnvioNotificacao` | §10 | CP-89, CP-94, CP-97, CP-99, CP-100, CP-123, CP-126 |
| USID_012 | Configurar recepção de notificação | **Coberto** | CL-014 `PapelNotificacao` (inferido), CL-015 `PapelSeveridade` (inferido), CL-016 `PapelTipoAlerta` (inferido), CL-077 `PreferenciaNotificacao`, ES-22 `CanalNotificacao` | §2, §10 | CP-97, CP-126 |
| USID_013 | Visualizar Notificação | **Parcial** | CL-076 `Notificacao`, CL-082 `EnviadorWeb` | §10 | CP-89, CP-94, CP-99, CP-123 |
| USID_014 | Visualizar Notificação (Mobile) | **Coberto** | CL-076 `Notificacao`, CL-081 `EnviadorPush` | §10 | CP-89, CP-99, CP-123 |
| USID_015 | Implementar SDK | **Parcial** | CL-004 `Produto`, CL-099 `LogSDK`, CL-100 `ConfiguracaoSdk`, CL-102 `IdentificadorProduto`, CL-105 `ClienteColetor`, CL-114 `FonteTelemetria` (inferido) | §1, §13 | CP-03 |
| USID_016 | Gerenciar Tokens | **Coberto** | CL-004 `Produto`, CL-034 `GerenciadorRequisicao`, CL-041 `Produtor`, CL-042 `TokenApi`, CL-043 `CredencialIngestao`, CL-101 `CredencialIngestao (SDK)`, CL-114 `FonteTelemetria` (inferido) | §1, §5, §13 | CP-03, CP-37 |
| USID_017 | Baixar SDK | **Só legado** | CL-099 `LogSDK` | §13 | — |
| USID_018 | Baixar Executavel | **Só legado** | CL-113 `Executavel`, ES-26 `SistemaOperacional` | §13 | — |
| USID_019 | Configurar Executavel | **Só legado** | CL-113 `Executavel`, ES-27 `StatusExecutavel` | §13 | — |
| USID_020 | Iniciar Execução | **Só legado** | CL-113 `Executavel`, ES-27 `StatusExecutavel` | §13 | — |
| USID_021 | Manter Informações Empresarial | **Coberto** | CL-008 `Empresa`, CL-009 `Endereco` (inferido), ES-01 `TipoEndereco` (inferido) | §1 | CP-05, CP-06 |
| USID_022 | Manter Contexto de atuação empresarial | **Coberto** | CL-007 `ContextoEmpresa` | §1 | CP-04 |
| USID_023 | Manter Contexto de Produto | **Coberto** | CL-004 `Produto`, CL-005 `ContextoProduto` | §1 | CP-03 |
| USID_024 | Implementar Produto | **Coberto** | CL-004 `Produto`, CL-006 `ConfiguracaoProduto` | §1 | CP-03 |
| USID_025 | Forçar execução de Varredura | **Coberto** | CL-044 `Varredura`, CL-051 `TravaVarredura`, ES-15 `VarreduraTrigger` | §6 | CP-49, CP-118, CP-120, CP-129 |
| USID_026 | Configurar Agendamento de Varredura | **Coberto** | CL-047 `AgendamentoVarredura`, CL-052 `HistoricoVarredura` (inferido), ES-17 `AgendamentoVarreduraStatus` | §6 | CP-53, CP-57, CP-127 |
| USID_027 | Habilitar Varredura Avançada | **Coberto** | CL-006 `ConfiguracaoProduto` (inferido), CL-054 `ContextoAnalise`, CL-063 `ScannerSeguranca`, ES-20 `Nivel` | §1, §7 | — |
| USID_028 | Abrir o link do Agente LLM | **Parcial** | CL-068 `Sugestao` | §9 | CP-83, CP-122 |
| USID_029 | Manter Gestor | **Coberto** | CL-002 `Membro`, CL-011 `Gestor`, CL-012 `Vinculo` | §1 | CP-02 |
| USID_030 | Controle de Acesso dos gestores aos Produtos | **Coberto** | CL-003 `AcessoProduto`, CL-011 `Gestor`, CL-012 `Vinculo`, CL-013 `Acesso` | §1 | — |
| USID_031 | Visualizar Dashboard | **Coberto** | CL-085 `Metrica`, CL-088 `DashboardProduto` | §11 | — |
| USID_032 | Filtrar Dashboard | **Coberto** | CL-086 `Periodo`, CL-087 `FiltroDashboard`, CL-088 `DashboardProduto` | §11 | — |
| USID_033 | Exportar Relatório | **Coberto** | CL-093 `RelatorioDashboard`, CL-096 `ExportacaoRelatorio`, CL-098 `GeradorArquivo`, ES-25 `FormatoArquivo` | §12 | CP-108, CP-110 |
| USID_034 | Visualizar Dashboard Empresarial | **Coberto** | CL-085 `Metrica`, CL-089 `DashboardEmpresarial`, CL-092 `Agregacao` | §11 | CP-104 |
| USID_035 | Exportar Relatório Empresarial | **Coberto** | CL-094 `RelatorioEmpresarial`, CL-096 `ExportacaoRelatorio`, CL-098 `GeradorArquivo`, ES-25 `FormatoArquivo` | §12 | CP-108, CP-110 |
| USID_036 | Filtrar Dashboard Empresarial | **Coberto** | CL-086 `Periodo`, CL-087 `FiltroDashboard`, CL-089 `DashboardEmpresarial` | §11 | — |
| USID_037 | Filtrar Ocorrências Empresarial (Multi-Produto) | **Coberto** | CL-066 `Ocorrencia`, CL-090 `FiltroOcorrenciaEmpresarial` | §8, §11 | CP-76, CP-77, CP-103, CP-114, CP-130 |
| USID_038 | Visualizar Dashboard (Mobile) | **Coberto** | CL-091 `ResumoDashboardMobile` | §11 | — |
| USID_039 | Visualizar Assinatura | **Coberto** | CL-017 `GerenciadorAssinatura`, CL-018 `Plano`, CL-019 `TabelaPrecificacao`, CL-021 `ProdutoRecursoIA` (inferido), CL-023 `GatewayPagamento`, ES-02 `TipoPlano`, ES-03 `RecursosAnaliseIA`, ES-04 `TipoDashboard`, ES-05 `Periodicidade` | §3 | CP-19, CP-21, CP-22, CP-23, CP-124, CP-127, CP-131 |
| USID_040 | Contratar Assinatura | **Coberto** | CL-001 `Tenant` (inferido), CL-017 `GerenciadorAssinatura`, CL-018 `Plano`, CL-020 `Assinatura`, CL-022 `ProcessamentoPagamento`, CL-025 `Pagamento` | §1, §3 | CP-01, CP-15, CP-16, CP-23, CP-124 |
| USID_041 | Alterar Assinatura | **Coberto** | CL-017 `GerenciadorAssinatura`, CL-018 `Plano`, CL-020 `Assinatura` | §3 | CP-16, CP-23, CP-124 |
| USID_042 | Cancelar Assinatura | **Coberto** | CL-017 `GerenciadorAssinatura`, CL-020 `Assinatura`, ES-06 `StatusAssinatura` | §3 | CP-16, CP-18 |
| USID_043 | Reembolsar Assinatura | **Coberto** | CL-017 `GerenciadorAssinatura`, CL-020 `Assinatura`, CL-025 `Pagamento`, CL-026 `Reembolso`, ES-08 `StatusReembolso` | §3 | CP-16 |
| USID_044 | Solicitar Sugestão | **Coberto** | CL-018 `Plano` (inferido), CL-021 `ProdutoRecursoIA` (inferido), CL-028 `Credito` (inferido), CL-030 `Saldo` (inferido), CL-064 `ModuloOcorrencia` (inferido), CL-068 `Sugestao`, CL-070 `ContextoSugestao`, CL-075 `ModuloSugestao`, ES-03 `RecursosAnaliseIA` (inferido) | §3, §4, §8, §9 | CP-19, CP-21, CP-23, CP-83, CP-122, CP-124, CP-127, CP-131 |
| USID_045 | Visualizar Sugestão | **Coberto** | CL-068 `Sugestao`, ES-21 `StatusSugestao` | §9 | CP-83, CP-122 |
| USID_046 | Avaliar Sugestão | **Coberto** | CL-068 `Sugestao`, CL-069 `AvaliacaoSugestao`, ES-21 `StatusSugestao` | §9 | CP-83, CP-122 |
| USID_047 | Fechar Sugestão | **Coberto** | CL-068 `Sugestao`, ES-21 `StatusSugestao` | §9 | CP-83, CP-122 |
| USID_048 | Manter Usuário | **Coberto** | CL-002 `Membro`, CL-010 `Usuario` | §1 | CP-02 |
| USID_049 | Logar na Web | **Parcial** | CL-002 `Membro` (inferido), CL-010 `Usuario`, CL-013 `Acesso` | §1 | CP-02 |
| USID_050 | Logar Mobile | **Parcial** | CL-002 `Membro` (inferido) | §1 | CP-02 |
| USID_051 | Manter 2FA | **Parcial** | CL-002 `Membro` (inferido), CL-010 `Usuario` | §1 | CP-02 |
| SSID_001 | Conectar o Utilitario | **Coberto** | CL-033 `Coletor`, CL-034 `GerenciadorRequisicao`, CL-041 `Produtor`, CL-042 `TokenApi`, CL-101 `CredencialIngestao (SDK)`, CL-103 `EventoLog`, CL-104 `EnvelopeIngestao`, CL-105 `ClienteColetor`, CL-106 `SerializadorIngestao`, CL-107 `ValidadorEventoLog`, CL-108 `ResultadoValidacao`, CL-110 `RespostaColetor`, CL-111 `ResultadoEnvio`, CL-112 `ResultadoConexao` | §5, §13 | CP-37 |
| SSID_002 | Manter Logs | **Coberto** | CL-001 `Tenant` (inferido), CL-033 `Coletor`, CL-035 `LogRecebido`, CL-036 `GerenciadorLote`, CL-037 `LoteAgrupador` | §1, §5 | CP-01, CP-15 |
| SSID_003 | Enfileirar Logs | **Coberto** | CL-033 `Coletor`, CL-038 `EnfileiradorLogs`, CL-039 `Arquivo`, CL-049 `FilaDesordenada` | §5, §6 | CP-41, CP-42, CP-43, CP-55, CP-121 |
| SSID_004 | Marcar como Analisado | **Coberto** | CL-039 `Arquivo`, CL-044 `Varredura` (inferido), CL-046 `ArquivoVarredura`, CL-065 `ResumoArquivo`, ES-16 `ArquivoScanStatus` | §5, §6, §8 | CP-41, CP-42, CP-43, CP-54, CP-55, CP-73, CP-120, CP-121 |
| SSID_005 | Executar Varredura (Forçar Varredura) | **Coberto** | CL-044 `Varredura`, ES-15 `VarreduraTrigger` | §6 | CP-120 |
| SSID_006 | Executar Varredura Agendada | **Coberto** | CL-044 `Varredura`, CL-047 `AgendamentoVarredura`, CL-052 `HistoricoVarredura` (inferido), ES-15 `VarreduraTrigger` | §6 | CP-53, CP-120, CP-127 |
| SSID_007 | Identificar Ocorrencia | **Coberto** | CL-053 `Finder`, CL-055 `LogNormalizado`, CL-056 `MotorAnalise`, CL-057 `GatewayLLMFinder`, CL-060 `AchadoAnalise`, CL-061 `ResumoAnalise`, CL-062 `ClassificadorAnalise`, CL-066 `Ocorrencia`, ES-19 `Tipo` | §7, §8 | CP-63, CP-65, CP-69, CP-76, CP-77, CP-114, CP-115, CP-116, CP-127, CP-130, CP-133 |
| SSID_008 | Executar Varredura Avançada | **Coberto** | CL-053 `Finder` (inferido), CL-054 `ContextoAnalise`, CL-063 `ScannerSeguranca`, ES-20 `Nivel` | §7 | — |
| SSID_009 | Enviar Ocorrências | **Coberto** | CL-014 `PapelNotificacao` (inferido), CL-015 `PapelSeveridade` (inferido), CL-016 `PapelTipoAlerta` (inferido), CL-061 `ResumoAnalise`, CL-064 `ModuloOcorrencia`, CL-066 `Ocorrencia`, CL-076 `Notificacao`, CL-084 `TentativaEntrega` (inferido), ES-19 `Tipo` | §2, §7, §8, §10 | CP-76, CP-77, CP-89, CP-99, CP-114, CP-116, CP-123, CP-127, CP-130 |
| SSID_010 | Registrar Ocorrencia | **Coberto** | CL-001 `Tenant` (inferido), CL-064 `ModuloOcorrencia`, CL-066 `Ocorrencia`, CL-067 `Mapper` | §1, §8 | CP-01, CP-15, CP-76, CP-77, CP-114, CP-130 |
| SSID_011 | Gerar Relátorios | **Coberto** | CL-086 `Periodo`, CL-092 `Agregacao`, CL-095 `RelatorioConsolidado`, CL-097 `GeracaoRelatorioAgendada` | §11, §12 | CP-104, CP-109 |
| SSID_012 | Criar Agendamento de Varredurar | **Coberto** | CL-047 `AgendamentoVarredura` | §6 | — |
| SSID_013 | Enviar Arquivo(Importado) para Varredura | **Coberto** | CL-039 `Arquivo`, CL-053 `Finder` | §5, §7 | CP-41, CP-42, CP-43, CP-55, CP-121 |
| SSID_014 | Manter Tokens de Conexão | **Coberto** | CL-034 `GerenciadorRequisicao`, CL-041 `Produtor`, CL-042 `TokenApi`, CL-043 `CredencialIngestao` | §5 | CP-37 |
| SSID_015 | Usar Contexto | **Coberto** | CL-005 `ContextoProduto`, CL-007 `ContextoEmpresa`, CL-070 `ContextoSugestao`, CL-075 `ModuloSugestao` | §1, §9 | CP-04 |
| SSID_016 | Manter Assinatura | **Coberto** | CL-017 `GerenciadorAssinatura`, CL-020 `Assinatura`, CL-022 `ProcessamentoPagamento`, CL-027 `EventoGateway`, ES-06 `StatusAssinatura`, ES-09 `TipoOperacaoGateway`, ES-10 `ResultadoEventoGateway` | §3 | CP-16, CP-18, CP-25, CP-125 |
| SSID_017 | Integração de Autenticação | **Coberto** | CL-001 `Tenant`, CL-002 `Membro`, CL-010 `Usuario` | §1 | CP-01, CP-02, CP-15 |
| SSID_018 | Integração de Pagamento | **Coberto** | CL-020 `Assinatura`, CL-022 `ProcessamentoPagamento`, CL-023 `GatewayPagamento`, CL-024 `ApiPagamento`, CL-025 `Pagamento`, CL-027 `EventoGateway`, ES-07 `StatusPagamento`, ES-10 `ResultadoEventoGateway` | §3 | CP-16, CP-25, CP-125 |
| SSID_019 | Integração de Notificação | **Coberto** | CL-014 `PapelNotificacao` (inferido), CL-076 `Notificacao`, CL-078 `GatewayNotificacao`, CL-079 `GatewayNotificacaoFactory` | §2, §10 | CP-89, CP-99, CP-123 |
| SSID_020 | Integração de LLM | **Coberto** | CL-028 `Credito`, CL-030 `Saldo`, CL-031 `Transacao`, CL-032 `Controle`, CL-056 `MotorAnalise`, CL-057 `GatewayLLMFinder`, CL-071 `GatewayLLMSugestao`, CL-072 `GatewayLLMPadrao`, CL-073 `RespostaLLM`, CL-074 `ChaveLLMTenant`, CL-075 `ModuloSugestao`, ES-11 `TipoTransacao` (inferido), ES-12 `StatusTransacao` (inferido), ES-13 `StatusOperacao` (inferido) | §4, §7, §9 | CP-34, CP-69, CP-85, CP-86 |

## 3. ADR → elementos

ADRs citadas no DC-10 v7, com as classes que elas sustentam e as pendências em que aparecem. ADRs sem classe tratam de infraestrutura, front-end ou processo, ou só contextualizam uma seção.

| ADR | Título | Seções do DC-10 | Classes | Pendências |
|---|---|---|---|---|
| ADR_001 | Utilização do banco de dados | — | — | — |
| ADR_003 | Relacionamento Empresa/Usuário | — | CL-011 `Gestor`, CL-012 `Vinculo` | — |
| ADR_004 | O que é uma Varredura | — | CL-044 `Varredura` | — |
| ADR_006 | Formato de agendamento | §6 | CL-047 `AgendamentoVarredura` | — |
| ADR_007 | Ordenação da fila pela Varredura | §0, §6, §13 | CL-033 `Coletor`, CL-039 `Arquivo`, CL-044 `Varredura`, CL-049 `FilaDesordenada`, CL-050 `FilaOrdenada`, CL-099 `LogSDK`, CL-100 `ConfiguracaoSdk`, CL-101 `CredencialIngestao (SDK)`, CL-102 `IdentificadorProduto`, CL-103 `EventoLog`, CL-104 `EnvelopeIngestao`, CL-105 `ClienteColetor`, CL-106 `SerializadorIngestao`, CL-107 `ValidadorEventoLog`, CL-108 `ResultadoValidacao`, CL-109 `RedatorDadosSensiveis`, CL-110 `RespostaColetor`, CL-111 `ResultadoEnvio`, CL-112 `ResultadoConexao`, CL-113 `Executavel`, ES-26 `SistemaOperacional`, ES-27 `StatusExecutavel` | — |
| ADR_008 | Níveis de prioridade | §6 | CL-048 `Modulo`, ES-18 `NivelPrioridade` | — |
| ADR_009 | Prioridade definida por módulo | §6 | CL-040 `Trace`, CL-048 `Modulo`, ES-18 `NivelPrioridade` | — |
| ADR_010 | Disparo da Varredura | §6 | CL-044 `Varredura`, CL-047 `AgendamentoVarredura`, CL-049 `FilaDesordenada`, CL-051 `TravaVarredura`, ES-15 `VarreduraTrigger` | CP-48 |
| ADR_011 | Papel do Finder e montagem do contexto para a LLM | §7 | CL-050 `FilaOrdenada`, CL-054 `ContextoAnalise`, CL-056 `MotorAnalise` | — |
| ADR_012 | Taxonomia da classificação | §7 | CL-062 `ClassificadorAnalise`, ES-19 `Tipo` | — |
| ADR_013 | Regra de recorrência | §7 | CL-040 `Trace`, CL-059 `RecorrenciaLog` | CP-67 |
| ADR_014 | Confiabilidade do Finder: idempotência e reprocessamento | §7, §8 | CL-039 `Arquivo`, CL-040 `Trace`, CL-046 `ArquivoVarredura`, CL-049 `FilaDesordenada`, ES-16 `ArquivoScanStatus` | CP-74 |
| ADR_015 | Arquivo como pacote de traces | §5, §7 | CL-033 `Coletor`, CL-039 `Arquivo`, CL-040 `Trace` | — |
| ADR_016 | Nomes do modelo de classes original no Finder | §7 | CL-055 `LogNormalizado`, CL-056 `MotorAnalise`, CL-063 `ScannerSeguranca`, ES-20 `Nivel` | — |
| ADR_017 | Finder orquestra a análise do Arquivo e chama classificarAnalise() | §7 | CL-056 `MotorAnalise`, CL-060 `AchadoAnalise`, CL-062 `ClassificadorAnalise` | — |
| ADR_018 | GatewayLLM exclusivo do Finder | §7 | CL-056 `MotorAnalise`, CL-057 `GatewayLLMFinder`, CL-071 `GatewayLLMSugestao` | — |
| ADR_019 | Enum Tipo da classificação: ERRO, WARNING e SPAM | §7, §8 | CL-062 `ClassificadorAnalise`, CL-065 `ResumoArquivo`, ES-19 `Tipo` | CP-73 |
| ADR_020 | Ocorrência como resumo por Arquivo | §8 | CL-060 `AchadoAnalise` | CP-72, CP-74 |
| ADR_021 | Clerk como provedor de identidade e autenticação | §1 | CL-010 `Usuario`, CL-011 `Gestor`, CL-012 `Vinculo`, CL-013 `Acesso` | CP-07 |
| ADR_022 | Integração do backend Java com a Clerk | — | CL-010 `Usuario` | — |
| ADR_025 | Gestão de tokens internos e app móvel em standby | §10, §11 | CL-043 `CredencialIngestao`, CL-081 `EnviadorPush`, CL-083 `DispositivoPush`, CL-091 `ResumoDashboardMobile`, ES-23 `PlataformaDispositivo` | — |
| ADR_028 | Tokens internos próprios, sem M2M nem API keys da Clerk | — | CL-043 `CredencialIngestao` | — |
| ADR_030 | Multi-tenant com Organizations, Tenant mestre e mapeamento do clerk_user_id | §1 | CL-001 `Tenant`, CL-004 `Produto`, CL-010 `Usuario`, CL-011 `Gestor`, CL-013 `Acesso`, CL-017 `GerenciadorAssinatura`, CL-018 `Plano`, CL-020 `Assinatura` | CP-01 |
| ADR_032 | Tratamento de erros 401/403 e renovação da sessão | §1 | CL-003 `AcessoProduto` | — |
| ADR_035 | Ocorrência concreta e vínculo de 1 Ocorrência para N Sugestões | §0, §8, §9 | CL-039 `Arquivo`, CL-065 `ResumoArquivo`, CL-066 `Ocorrencia`, CL-068 `Sugestao` | CP-72, CP-74, CP-114 |
| ADR_036 | Gatilho da Sugestão: automático por plano e manual com fila de menor prioridade | §0, §8, §9 | CL-018 `Plano`, CL-064 `ModuloOcorrencia`, CL-068 `Sugestao`, CL-075 `ModuloSugestao`, CL-076 `Notificacao`, ES-03 `RecursosAnaliseIA`, ES-21 `StatusSugestao` | CP-78, CP-88 |
| ADR_037 | Falhas na geração da Sugestão: aviso na notificação, retry e estado FALHA | §9 | CL-068 `Sugestao`, CL-076 `Notificacao`, ES-21 `StatusSugestao` | — |
| ADR_038 | Consumo de créditos/tokens da Sugestão por reserva | §0, §4, §8, §9 | CL-028 `Credito`, CL-030 `Saldo`, CL-031 `Transacao`, CL-032 `Controle`, CL-064 `ModuloOcorrencia`, CL-068 `Sugestao`, CL-073 `RespostaLLM`, CL-075 `ModuloSugestao`, ES-11 `TipoTransacao`, ES-13 `StatusOperacao` | CP-30, CP-78, CP-87, CP-88 |
| ADR_039 | Avaliação das Sugestões, realimentação do contexto e GatewayLLMSugestao | §8, §9 | CL-005 `ContextoProduto`, CL-007 `ContextoEmpresa`, CL-064 `ModuloOcorrencia`, CL-068 `Sugestao`, CL-069 `AvaliacaoSugestao`, CL-070 `ContextoSugestao`, CL-071 `GatewayLLMSugestao`, CL-072 `GatewayLLMPadrao`, CL-075 `ModuloSugestao`, ES-21 `StatusSugestao` | CP-78, CP-85, CP-88 |
| ADR_040 | Confirmações da Sugestão: automático síncrono com prioridade e AchadoAnalise como DTO da Ocorrência | §0, §7, §8, §9 | CL-060 `AchadoAnalise`, CL-064 `ModuloOcorrencia`, CL-065 `ResumoArquivo`, CL-066 `Ocorrencia`, CL-067 `Mapper`, CL-068 `Sugestao` | CP-63, CP-72, CP-73, CP-74, CP-75, CP-114, CP-115 |
| ADR_041 | Upload manual: rota POST /manual/upload e enfileiramento direto no fim da FilaOrdenada | §0, §5 | — | CP-46 |
| ADR_042 | Coletor como porta única de entrada com seção paralela manual, proteção contra binário/prompt injection no backend e erro crítico | §5 | — | CP-46 |
| ADR_043 | Upload manual: formatos aceitos (lista extensível) e limite de 100 MB checados no front | §5 | — | CP-46 |
| ADR_044 | Upload manual: Produto vindo do card e tratamento do nome/ID do Arquivo (Arquivo ganha nome) | §5 | CL-039 `Arquivo` | — |
| ADR_045 | Upload manual: vários arquivos numa requisição, agrupados em um único lote no fim da FilaOrdenada | §5 | — | CP-46 |
| ADR_046 | Upload manual: feedback ao usuário (enfileirado + notificação) e DLQ com 3 tentativas | §6 | ES-16 `ArquivoScanStatus` | CP-54, CP-58 |
| ADR_047 | Upload manual: notificações de progresso e "varredura finalizada" por WebSocket | §6 | — | — |
| ADR_048 | Upload manual: bloqueio individual do arquivo reprovado na proteção, o resto do lote continua | §5, §6 | — | CP-46 |
| ADR_049 | Upload manual: erro de leitura/parsing é crítico sem retry e DLQ reenvia ao fim da FilaOrdenada | §6 | ES-16 `ArquivoScanStatus` | CP-54 |
| ADR_050 | Upload manual: sem limite por requisição por enquanto, só 100 MB por arquivo | §6 | — | — |
| ADR_051 | API Core (assinatura, tenant, alertas) recebe os alertas do Coletor e do Finder e os envia ao front por WebSocket | §0, §6 | — | — |
| ADR_052 | Upload manual: um alerta consolidado por lote, sem notificação por arquivo | §6 | — | — |
| ADR_053 | Upload manual: resposta 202 Accepted no aceite do POST /manual/upload | §5, §6 | — | CP-46 |
| ADR_054 | Backend Java e API Core são o mesmo serviço; 5 serviços de backend com o mesmo MongoDB | §6 | — | — |
| ADR_055 | Upload manual: alertas sempre por lote (aceito, proteção, relatório final por arquivo) | §6, §12 | — | — |
| ADR_056 | Upload manual: lote com todos os arquivos bloqueados não entra na fila | §6 | — | — |
| ADR_057 | Varredura por Produto: uma FilaDesordenada por Produto e gatilho por tamanho opcional por cliente (padrão 500) | §0, §6 | — | CP-48 |
| ADR_058 | Trava da Varredura em coleção chave-valor no MongoDB (tenantId + loteId + arquivoId) | §6 | CL-051 `TravaVarredura` | CP-49, CP-118, CP-127, CP-129 |
| ADR_059 | DLQ com 3 tentativas para varreduras automáticas e opção do usuário de devolver o arquivo à FilaDesordenada | §0, §6, §7 | ES-16 `ArquivoScanStatus` | CP-54, CP-58 |
| ADR_060 | Alertas da Varredura por lote só por WebSocket, histórico de execuções e push/email reservados | §0, §6, §7, §10 | CL-052 `HistoricoVarredura` | CP-53, CP-127 |
| ADR_061 | Fim da Varredura pela API da Varredura: o Finder avisa cada arquivo e a Varredura fecha sozinha | §0, §6, §7 | ES-14 `VarreduraStatus` | CP-51, CP-56 |
| ADR_062 | Finder emite só AchadoAnalise e ResumoAnalise; Ocorrências e gravidade pertencem ao Módulo Ocorrência | §0, §6, §7, §8 | CL-053 `Finder`, CL-058 `BancoVetorial`, CL-060 `AchadoAnalise`, CL-061 `ResumoAnalise`, CL-064 `ModuloOcorrencia`, CL-065 `ResumoArquivo`, CL-066 `Ocorrencia`, CL-067 `Mapper` | CP-62, CP-63, CP-64, CP-68, CP-73, CP-77, CP-78, CP-79, CP-114, CP-115, CP-127, CP-130 |
| ADR_063 | Recorrência no Finder: flag recorrente no AchadoAnalise e janela dos últimos 500 arquivos no BancoVetorial | §6, §7, §8 | CL-059 `RecorrenciaLog`, CL-060 `AchadoAnalise`, CL-065 `ResumoArquivo` | CP-63, CP-66, CP-67, CP-73, CP-117 |
| ADR_064 | Mascaramento no validarSeguranca(): emails substituídos, linhas com senha/token/secret removidas com marcador | §6, §7 | — | CP-70 |
| ADR_065 | Idempotência por arquivoId + varreduraId e workers paralelos independentes no Finder | §6, §7 | — | CP-71, CP-116 |
| ADR_066 | Spam não é armazenado nem vira Ocorrência; só fica como contexto do erro/warning | §6, §7 | — | CP-119 |
| ADR_067 | Renomear a interface de LLM do Finder para GatewayLLMFinder | §6, §7 | CL-057 `GatewayLLMFinder` | — |
| ADR_068 | Sem trava por Produto: workers consomem a fila do Produto em qualquer ordem e em paralelo | §6, §7 | CL-051 `TravaVarredura` | CP-49, CP-71, CP-118, CP-129 |
| ADR_069 | Formato da chave lock por arquivo e execId V/M | §6, §7 | CL-051 `TravaVarredura` | CP-49, CP-50, CP-118, CP-129 |
| ADR_070 | Manual chama a API da Varredura (execId M), idempotência arquivoId + execId e API rápida true/false de fim de execução | §0, §6, §7, §8 | CL-051 `TravaVarredura`, CL-061 `ResumoAnalise` | CP-49, CP-50, CP-51, CP-71, CP-74, CP-116 |
| ADR_071 | Retenção de 3 meses para histórico de execuções e notificações | §6, §7, §10 | CL-052 `HistoricoVarredura` | CP-53 |
| ADR_072 | TTL das chaves lock = tempo estimado + 10% pela API de Estimativa | §6, §7 | CL-051 `TravaVarredura` | CP-49, CP-52, CP-118 |
| ADR_073 | Correção da ADR_059: após 3 falhas o usuário só pode enviar um novo arquivo | §6, §7 | ES-16 `ArquivoScanStatus` | CP-54, CP-58 |
| ADR_074 | BancoVetorial isolado por Produto | §6, §7 | CL-058 `BancoVetorial` | CP-66, CP-68, CP-117 |
| ADR_075 | Coletor pede o execId manual à API da Varredura e IDs de execução em UUID (V<uuid>/M<uuid>) | §0, §5, §6 | — | CP-46, CP-50 |
| ADR_076 | Sugestão automática habilitada por Produto (ProdutoRecursoIA) | §0, §3, §8, §9 | CL-021 `ProdutoRecursoIA`, ES-03 `RecursosAnaliseIA` | CP-19, CP-21, CP-124, CP-127, CP-131 |
| ADR_077 | Timeout de 30 s sem retry e notificação única de falha da Sugestão automática | §9, §10 | ES-21 `StatusSugestao` | CP-91, CP-122 |
| ADR_078 | Reserva de tokens da Sugestão: fórmula, liquidação e expiração | §0, §4, §9 | CL-030 `Saldo`, ES-21 `StatusSugestao` | CP-30, CP-32, CP-88 |
| ADR_079 | Mascaramento da Sugestão igual ao do Finder | §9 | — | CP-84 |
| ADR_080 | Provedor da LLM em aberto e token próprio do cliente (BYOK) na Sugestão | §4, §7, §9 | CL-057 `GatewayLLMFinder`, CL-071 `GatewayLLMSugestao`, CL-074 `ChaveLLMTenant` | CP-31, CP-85, CP-86 |
| ADR_081 | Tipos de Notificação: OCORRENCIA e OCORRENCIA_COM_SUGESTAO | §9, §10 | CL-076 `Notificacao` | CP-89, CP-123, CP-132 |
| ADR_082 | Status da Ocorrência e endpoint de mudança manual | §8, §9 | CL-066 `Ocorrencia` | CP-76 |
| ADR_083 | Rota da Sugestão manual com 202 Accepted e sem limite por Ocorrência | §9 | — | — |
| ADR_085 | Saldo insuficiente na Sugestão manual: recusa imediata no pedido | §9 | — | — |
| ADR_086 | WebSocket para a Sugestão manual: atualização da tela e aviso de falha | §9, §10 | CL-076 `Notificacao` | CP-89, CP-132 |
| ADR_087 | Contexto da Sugestão manual: últimas 5 Sugestões da mesma Ocorrência | §9 | — | CP-84 |
| ADR_088 | Avaliação da Sugestão: 1 a 5 estrelas e comentário | §0, §9 | CL-068 `Sugestao`, CL-069 `AvaliacaoSugestao` | CP-82, CP-83 |
| ADR_089 | Fechamento da Sugestão e status da Ocorrência (complementa a ADR_082) | §8 | CL-066 `Ocorrencia` | CP-76 |
| ADR_090 | Sugestão com falha fica fora da lista da Ocorrência e não bloqueia o fechamento | §8, §9 | CL-066 `Ocorrencia` | CP-76 |
| ADR_091 | Status PENDENTE da Sugestão substitui DISPONIVEL | §8, §9 | CL-066 `Ocorrencia`, ES-21 `StatusSugestao` | CP-76 |
| ADR_092 | Saldo insuficiente na Sugestão manual retorna 402 Payment Required | §9 | — | — |
| ADR_093 | Timeout de 30 s também na Sugestão manual | §9 | — | — |
| ADR_094 | Retry da Sugestão manual: 3 retentativas com espera crescente (corrige a ADR_084) | §9 | — | — |
| ADR_095 | Aviso "aceita" da Sugestão manual por WebSocket e histórico | §9 | — | — |
| ADR_096 | Status AGUARDANDO_REVISAO da Sugestão (renomeia o PENDENTE da ADR_091) | §8, §9 | CL-066 `Ocorrencia`, ES-21 `StatusSugestao` | CP-76, CP-122 |
| ADR_097 | Falha da Sugestão automática também fica só no histórico | §9 | — | — |
| ADR_098 | Nova reserva a cada retentativa com substituição atômica | §0, §4, §9 | CL-030 `Saldo` | CP-30, CP-32, CP-88 |
| ADR_099 | Status do Arquivo: PROCESSANDO, CONCLUIDO e FALHA | §5, §6 | CL-039 `Arquivo`, CL-046 `ArquivoVarredura` | CP-41, CP-55, CP-120, CP-121 |
| ADR_100 | Listagem de arquivos no card do Produto, com origem e lotes | §5 | CL-039 `Arquivo` | CP-42, CP-121 |
| ADR_101 | Ocorrências em três níveis (Produto, lote, arquivo) | §5, §8 | — | CP-80 |
| ADR_102 | Contadores do resumo a partir do ResumoAnalise | §5, §7 | CL-061 `ResumoAnalise` | — |
| ADR_103 | Detalhe da falha e arquivo em processamento | §5 | — | CP-45 |
| ADR_104 | Retenção de arquivos e Ocorrências por plano | §3, §5, §8 | CL-020 `Assinatura` | CP-16, CP-81 |
| ADR_105 | Modelo de tenant hierárquico chave-valor (hash e metadata) | §1, §5 | CL-001 `Tenant` | CP-01 |
| ADR_106 | Token de API para produtores de logs | §5 | CL-041 `Produtor`, CL-042 `TokenApi` | CP-37, CP-38 |
| ADR_107 | Sem regeneração especial de token | §5 | CL-041 `Produtor`, CL-042 `TokenApi` | CP-37 |
| ADR_108 | Protocolo OTLP HTTP e gRPC e endpoint de ingestão | §5 | — | CP-36 |
| ADR_109 | Permissões da gestão de tokens: só administradores | §5 | CL-041 `Produtor`, CL-042 `TokenApi` | CP-37 |
| ADR_111 | Remoção das classes legadas de token e tabela CredencialIngestao | §1, §5, §13 | CL-043 `CredencialIngestao`, CL-113 `Executavel` | CP-08, CP-39, CP-128 |
| ADR_113 | Token Bearer do produtor: AES-256-GCM e índice SHA-256 | §5 | CL-034 `GerenciadorRequisicao`, CL-041 `Produtor`, CL-042 `TokenApi` | CP-37, CP-40 |
| ADR_114 | Convite de membros e promoção a administrador (só backend) | §1 | — | CP-10 |
| ADR_115 | producerId gerado com o token | §5 | CL-041 `Produtor`, CL-042 `TokenApi` | CP-37 |
| ADR_116 | Elasticsearch para logs e MongoDB como banco core | §5 | CL-035 `LogRecebido` | — |
| ADR_117 | Token na planilha de créditos e nome Créditos | §0, §4, §5, §9 | CL-030 `Saldo`, CL-034 `GerenciadorRequisicao` | CP-30, CP-31, CP-40, CP-87 |
| ADR_118 | Saúde do serviço só por GET /health e respostas OTLP padrão (substitui parcialmente a ADR_112) | §5, §9 | — | CP-36 |
| ADR_119 | Caminhos OTLP padrão e Produto resolvido pelo token (substitui parcialmente a ADR_108) | §5, §9 | — | CP-36 |
| ADR_120 | Retry-After de 120 segundos em sobrecarga | §5, §9 | — | CP-36 |
| ADR_121 | Modelo multi-tenant SaaS pool com tenant = empresa cliente (substitui a ADR_105) | §1, §3, §5, §8, §9 | CL-001 `Tenant`, CL-008 `Empresa`, CL-035 `LogRecebido` | CP-01, CP-06, CP-08, CP-09, CP-15, CP-44, CP-75 |
| ADR_122 | Coleções do modelo multi-tenant | §0, §1, §3, §4, §5, §9 | CL-001 `Tenant`, CL-002 `Membro`, CL-003 `AcessoProduto`, CL-004 `Produto`, CL-006 `ConfiguracaoProduto`, CL-010 `Usuario`, CL-011 `Gestor`, CL-012 `Vinculo`, CL-013 `Acesso`, CL-020 `Assinatura`, CL-041 `Produtor`, CL-042 `TokenApi`, CL-043 `CredencialIngestao` | CP-01, CP-07, CP-08, CP-15, CP-16, CP-37, CP-39, CP-128 |
| ADR_123 | Clerk Organizations gratuitas e papéis na coleção Membro | §1, §9 | CL-001 `Tenant`, CL-002 `Membro`, CL-010 `Usuario`, CL-011 `Gestor`, CL-012 `Vinculo`, CL-013 `Acesso` | CP-07, CP-08 |
| ADR_124 | Downgrade altera só a Assinatura | §1, §3, §9 | CL-020 `Assinatura` | CP-16 |
| ADR_125 | EventoGateway com status e reprocessamento individual | §1, §3, §9 | CL-027 `EventoGateway` | CP-25, CP-27, CP-125 |
| ADR_126 | Negação simples para não-membro ou Produto errado na URL | §1, §9 | CL-003 `AcessoProduto` | — |
| ADR_127 | Limites da Clerk cobertos por plano via TabelaPrecificacao | §1, §3, §9 | CL-019 `TabelaPrecificacao` | CP-22 |
| ADR_128 | Chave BYOK guardada no módulo Sugestão | §1, §9 | CL-074 `ChaveLLMTenant` | CP-86 |
| ADR_129 | Downgrade acima dos limites gera ACESSO_PENDENTE | §1, §3 | CL-004 `Produto` | CP-03, CP-24 |
| ADR_130 | Notificações por papel com agregação dos canais | §0, §1, §2, §10 | CL-014 `PapelNotificacao` | CP-12, CP-93 |
| ADR_131 | TabelaPrecificacao com base no Plano de Monetização | §1, §2, §3 | CL-014 `PapelNotificacao`, CL-019 `TabelaPrecificacao` | CP-22 |
| ADR_132 | Prazo de 24 horas para regularizar ACESSO_PENDENTE | §1, §2, §3 | CL-002 `Membro`, CL-014 `PapelNotificacao` | CP-02, CP-24 |
| ADR_133 | Rotas internas de reprocessamento do EventoGateway (proposta) | §1, §2, §3 | CL-014 `PapelNotificacao` | CP-27 |
| ADR_134 | Matriz de alertas configurável por empresa | §0, §1, §2, §10 | CL-014 `PapelNotificacao`, CL-015 `PapelSeveridade`, CL-016 `PapelTipoAlerta`, CL-077 `PreferenciaNotificacao` | CP-93, CP-97, CP-126 |
| ADR_135 | ACESSO_PENDENTE bloqueia até a aprovação do DONO | §1, §2, §3 | CL-002 `Membro`, CL-014 `PapelNotificacao` | CP-02, CP-24 |
| ADR_136 | Papéis de notificação padrão e filtro por gravidade, tipo e Produto | §2, §10 | CL-014 `PapelNotificacao` | CP-12, CP-13, CP-93, CP-126 |
| ADR_137 | Confirmações sobre os papéis de notificação | §1, §2 | CL-001 `Tenant`, CL-014 `PapelNotificacao` | CP-01, CP-12 |
| ADR_138 | Exclusão de papel de notificação | §2 | CL-014 `PapelNotificacao` | — |
| ADR_139 | Papel excluído é definitivo e rotas /papeis da matriz de alertas (proposta) | §2 | CL-014 `PapelNotificacao` | CP-13, CP-14 |
| ADR_140 | Sem listagem de papéis excluídos e Membros de Dono e Administrador pelo papel do Membro | §2 | CL-014 `PapelNotificacao` | CP-11, CP-13, CP-14 |
| ADR_141 | Segmentação de rede dos módulos | §0, §2, §9, §10 | CL-014 `PapelNotificacao`, CL-082 `EnviadorWeb` | CP-94 |
| ADR_142 | Papel de notificação com várias gravidades e vários tipos de alerta | §2 | CL-014 `PapelNotificacao`, CL-015 `PapelSeveridade`, CL-016 `PapelTipoAlerta` | CP-13 |
| ADR_143 | Redis Streams como broker das filas e eventos (título resumido; o documento só tem o número) | §6, §9, §10 | — | CP-60, CP-88, CP-95 |
| ADR_144 | Build com Maven (título resumido; o documento só tem o número) | — | — | — |
| ADR_145 | Classe base de consumidor copiada em cada repositório, sem biblioteca comum (título resumido; o documento só tem o número) | §6 | — | CP-60 |
| ADR_146 | Padrão de nomes, envelope e consumo das streams (título resumido; o documento só tem o número) | §6, §9, §10 | — | CP-60, CP-88, CP-95 |
| ADR_147 | Agendador @Scheduled + ShedLock e coleção varredura_schedules (título resumido; o documento só tem o número) | §6 | CL-052 `HistoricoVarredura` | CP-53, CP-61 |
| ADR_148 | Padrão de mensagem de commit | — | — | — |
| ADR_149 | Log padrão de inicialização dos serviços / Asaas como gateway de pagamento (proposta) — número duplicado no Drive | — | CL-017 `GerenciadorAssinatura`, CL-020 `Assinatura`, CL-023 `GatewayPagamento`, CL-024 `ApiPagamento`, CL-025 `Pagamento`, CL-027 `EventoGateway`, ES-06 `StatusAssinatura`, ES-09 `TipoOperacaoGateway` | CP-134 |
| ADR_150 | Versão do Java dos módulos | — | — | — |
| ADR_151 | Perfis de execução e ambiente local (docker-compose) | — | — | — |
| ADR_152 | Elasticsearch como banco vetorial do Finder | — | CL-058 `BancoVetorial` | — |
| ADR_153 | Caminho do módulo Go do Finder | — | — | — |
| ADR_154 | Remoção da classe TokenMetadata (complementa a ADR_111) (proposta) | §1 | — | CP-08 |
| ADR_155 | Token da requisição do Coletor é o TokenApi (complementa a ADR_113 e a ADR_117) (proposta) | §5 | CL-034 `GerenciadorRequisicao`, CL-042 `TokenApi`, CL-043 `CredencialIngestao` | CP-39, CP-40, CP-128 |
| ADR_156 | Classe ModuloSugestao para o módulo de Sugestão (complementa as ADR_036, ADR_038 e ADR_039) (proposta) | §0, §4, §9 | CL-075 `ModuloSugestao` | CP-30, CP-88 |
| ADR_157 | Remoção da classe SaldoTokens: a Sugestão usa o Saldo de Créditos (complementa as ADR_038 e ADR_117) (proposta) | §0, §4, §9 | CL-030 `Saldo` | CP-30, CP-87 |
| ADR_158 | Empresa como cadastro da empresa cliente, 1:1 com o Tenant (complementa a ADR_121 e a ADR_122) (proposta) | §0, §1, §3, §11, §12 | CL-001 `Tenant`, CL-007 `ContextoEmpresa`, CL-008 `Empresa`, CL-094 `RelatorioEmpresarial` | CP-04, CP-06, CP-15, CP-107, CP-111 |
| ADR_159 | Destinatário e autor por membroId (complementa as ADR_088 e ADR_122) (proposta) | §0, §1, §9, §10 | CL-002 `Membro`, CL-010 `Usuario`, CL-011 `Gestor`, CL-012 `Vinculo`, CL-013 `Acesso`, CL-069 `AvaliacaoSugestao`, CL-077 `PreferenciaNotificacao` | CP-07, CP-82, CP-92, CP-96 |
| ADR_160 | Nome ResumoArquivo e ocorrenciaIds no resumo por Arquivo (complementa as ADR_035 e ADR_040) (proposta) | §8 | CL-065 `ResumoArquivo` | CP-72, CP-73 |
| ADR_161 | Entrada do Módulo Ocorrência: receberResumo, dispararSugestaoAutomatica e Mapper (complementa as ADR_036, ADR_040 e ADR_062) (proposta) | §0, §7, §8 | CL-053 `Finder`, CL-064 `ModuloOcorrencia`, CL-067 `Mapper` | CP-62, CP-78, CP-79 |
| ADR_162 | Dashboard empresarial consulta as Ocorrências (proposta) | §0, §11 | CL-090 `FiltroOcorrenciaEmpresarial` | CP-103 |

**ADRs não citadas no DC-10** (não mudam classes: banco, linguagem, front-end, infraestrutura ou processo): ADR_002, ADR_005, ADR_023, ADR_024, ADR_026, ADR_027, ADR_029, ADR_031, ADR_033, ADR_034, ADR_084, ADR_110, ADR_112.

## 4. Requisitos sem representação ou só no legado

| Requisito | Título | Situação | Observação |
|---|---|---|---|
| USID_017 | Baixar SDK | Só legado | SDK e Executável foram substituídos pelo OpenTelemetry Collector (ADR_007); `FonteTelemetria` ocupa o lugar do Executável (pauta ING-06). |
| USID_018 | Baixar Executavel | Só legado | SDK e Executável foram substituídos pelo OpenTelemetry Collector (ADR_007); `FonteTelemetria` ocupa o lugar do Executável (pauta ING-06). |
| USID_019 | Configurar Executavel | Só legado | SDK e Executável foram substituídos pelo OpenTelemetry Collector (ADR_007); `FonteTelemetria` ocupa o lugar do Executável (pauta ING-06). |
| USID_020 | Iniciar Execução | Só legado | SDK e Executável foram substituídos pelo OpenTelemetry Collector (ADR_007); `FonteTelemetria` ocupa o lugar do Executável (pauta ING-06). |

Requisitos com cobertura **Parcial**: USID_001 (CP-76, CP-77, CP-114, CP-130), USID_002 (CP-76, CP-77, CP-114, CP-130), USID_003 (CP-76, CP-77, CP-114, CP-130), USID_004 (CP-76, CP-77, CP-114, CP-130), USID_005 (CP-76, CP-77, CP-114, CP-130), USID_008 (CP-23, CP-41, CP-42, CP-43…), USID_013 (CP-89, CP-94, CP-99, CP-123), USID_015 (CP-03), USID_028 (CP-83, CP-122), USID_049 (CP-02), USID_050 (CP-02), USID_051 (CP-02).

## 5. Elementos sem requisito

Classes e enums ativos que nenhum requisito cita. Em geral são classes técnicas pedidas por ADR (filas, locks, DTOs, enums de status).

| ID | Elemento | § | Base |
|---|---|---|---|
| CL-029 | `PlanoCreditos` | §4 | aba Cópia de Modelo Padrão (classe "Plano") |
| CL-040 | `Trace` | §5 | aba Trace (v2) |
| CL-045 | `VarreduraResumo` | §6 | aba Varredura v2 (tipo de retorno) |
| CL-048 | `Modulo` | §6 | aba Modulo (v2) |
| CL-050 | `FilaOrdenada` | §6 | aba FilaOrdenada (v2) |
| CL-058 | `BancoVetorial` | §7 | aba BancoVetorial (v2) |
| CL-059 | `RecorrenciaLog` | §7 | aba RecorrenciaLog (v2) |
| ES-14 | `VarreduraStatus` | §6 | aba Varredura v2 |
| ES-18 | `NivelPrioridade` | §6 | aba NivelPrioridade (v2) |

## 6. Conflitos e pendências (CP)

Cada linha do DC-10 que tem um marcador vira um CP, mais os conflitos DER v9 × ADRs, os da pauta e a ADR_149 do Asaas. A coluna "Elementos" liga o CP às classes da matriz. A coluna "O que falta" diz como a pendência fecha: decisão do time, aprovação de ADR, atualização do DER ou da planilha, detalhe a definir ou conferência na planilha.


### §1 Tenant, Membro e Produto

| CP | Situação | O que falta | Ponto | Descrição | Elementos | ADRs |
|---|---|---|---|---|---|---|
| CP-01 | `[PENDENTE]` | Detalhe em aberto | `Tenant` | ADR_121/122 e DER v9: o tenant é só a empresa cliente e espelha a Organization da Clerk (`clerkOrgId`). Nasce na compra da assinatura e o comprador vira `Membro` `DONO` (ADR_121, ADR_137). Todo documento no MongoDB e todo log no Elasticsearch leva `tenantId` (ADR_121). Valores de `status` `[PENDENTE]`. Substitui o `Tenant` da ADR_030 (empresa + usuário + produto) e o modelo hash da ADR_105. | CL-001 `Tenant`, CL-002 `Membro` | ADR_030, ADR_105, ADR_121, ADR_122, ADR_137 |
| CP-02 | `[PENDENTE]` | Detalhe em aberto | `Membro.status` | DER v9 e ADR_132/135: `ATIVO` ou `ACESSO_PENDENTE`. Com `ACESSO_PENDENTE` o acesso fica bloqueado até o DONO aprovar em até 24 h; sem aprovação o pedido expira. O valor depois de expirar não está definido `[PENDENTE]`. | CL-002 `Membro` | ADR_132, ADR_135 |
| CP-03 | `[PENDENTE]` | Detalhe em aberto | `Produto.status` | Planilha (Guia): ativo, suspenso, em configuração. A ADR_129 acrescenta o estado `ACESSO_PENDENTE` para Produtos acima do limite depois de um downgrade. Sem nome de enum `[PENDENTE]`. | CL-004 `Produto` | ADR_129 |
| CP-04 | `[PROPOSTO]` | Aguarda aprovação de ADR | `ContextoEmpresa` | `[CONFLITO]` na planilha pertence à `Empresa` (`empresa: Empresa`); no DER v9 está ligado ao `Produto` e ao `Usuario`. `[PROPOSTO]` ADR_158: vale a planilha (ligado à `Empresa`, que agora é o cadastro do Tenant). É usado no prompt da Sugestão (módulo 9). | CL-007 `ContextoEmpresa`, CL-008 `Empresa`, CL-004 `Produto`, CL-010 `Usuario` | ADR_158 |
| CP-05 | `[CONFLITO]` | Precisa de decisão do time | `Empresa.endereco` × `Endereco` | `[CONFLITO]` a planilha guarda um endereço na `Empresa`; o DER liga `Empresa 1:0..*` `Endereco`. O Mermaid usa o DER. | CL-008 `Empresa`, CL-009 `Endereco` | — |
| CP-06 | `[PROPOSTO]` | Aguarda aprovação de ADR | `Empresa` (cadastro) | O DER v9 marcava `Empresa` → `Tenant` como substituída (base: ADR_121), mas nenhuma fonte dava destino aos dados cadastrais, ao `Endereco` e ao `ContextoEmpresa`. `[PROPOSTO]` ADR_158: a `Empresa` deixa de ser substituída e passa a ser o cadastro da empresa cliente, ligado 1:1 ao `Tenant` (o Tenant continua sendo a identidade, espelho da Organization da Clerk). `[CONFLITO]` com o DER v9 até o DER ser atualizado. `Produto.empresa`, `DashboardEmpresarial.empresa` e `RelatorioEmpresarial.empresa` passam a ser válidos por esse cadastro. | CL-008 `Empresa`, CL-001 `Tenant`, CL-009 `Endereco`, CL-007 `ContextoEmpresa`, CL-004 `Produto`, CL-089 `DashboardEmpresarial`, CL-094 `RelatorioEmpresarial` | ADR_121, ADR_158 |
| CP-07 | `[PROPOSTO]` | Aguarda aprovação de ADR | `Usuario`, `Gestor`, `Vinculo`, `Acesso` `<<substituida>>` | DER v9: substituídas por `Membro` (ADR_122/123). Senha, sessão e MFA ficam na Clerk (ADR_021). Os campos estão na versão 2. A `PermissaoProduto` (só no DER) foi substituída por `AcessoProduto`. `[PROPOSTO]` ADR_159: os campos `usuario_id` das classes de Notificação e da `AvaliacaoSugestao` passam a `membroId`. | CL-010 `Usuario`, CL-011 `Gestor`, CL-012 `Vinculo`, CL-013 `Acesso`, CL-002 `Membro`, CL-003 `AcessoProduto`, CL-069 `AvaliacaoSugestao` | ADR_021, ADR_122, ADR_123, ADR_159 |
| CP-08 | `[PROPOSTO]` | Aguarda aprovação de ADR | `TokenMetadata` | Removida: a única classe que a usava (`Autorizador`) saiu pela ADR_111, e nada no modelo atual lê os metadados da Clerk (ADR_121/122/123). Registrada na ADR_154 `[PROPOSTO]`. | — | ADR_111, ADR_121, ADR_122, ADR_123, ADR_154 |
| CP-09 | `[PENDENTE]` | Detalhe em aberto | Cadeia de validação | ADR_121: identidade na Clerk → papel no `Membro` → `AcessoProduto` → limites da `Assinatura` → filtro `tenantId`, numa camada centralizada do Core. Nenhuma classe representa essa camada `[PENDENTE]`. | CL-002 `Membro`, CL-003 `AcessoProduto`, CL-020 `Assinatura` | ADR_121 |
| CP-10 | `[PENDENTE]` | Detalhe em aberto | Convite e promoção | ADR_114: só backend, por `DONO` ou `ADMIN`. Rotas `[PENDENTE]`. | — | ADR_114 |

### §2 Papéis de notificação — matriz de alertas

| CP | Situação | O que falta | Ponto | Descrição | Elementos | ADRs |
|---|---|---|---|---|---|---|
| CP-11 | `[PENDENTE]` | Detalhe em aberto | Membros do papel | DER v9: `Membro }o--o{ PapelNotificacao`. Se é tabela de ligação ou lista no papel `[PENDENTE]` (DER v9, pendência 13). Os Membros de Dono e Administrador vêm do `Membro.papel`, não das rotas de Membros (ADR_140). | CL-002 `Membro` | ADR_140 |
| CP-12 | `[PENDENTE]` | Detalhe em aberto | Entrega | ADR_130/136: o alerta vai a quem atende ao mesmo tempo à gravidade, ao tipo e ao Produto (o Membro precisa de `AcessoProduto`). Dono e Administrador recebem alertas de todos os Produtos (ADR_137). A "consulta de agregação" da ADR_130 não tem classe `[PENDENTE]`. | CL-003 `AcessoProduto` | ADR_130, ADR_136, ADR_137 |
| CP-13 | `[PENDENTE]` | Detalhe em aberto | Valores | Lista de tipos de alerta, de gravidades e os padrões de cada papel `[PENDENTE]` (ADR_136). Se Dono e Administrador recebem sempre tudo `[PENDENTE]` (ADR_139/140/142). | — | ADR_136, ADR_139, ADR_140, ADR_142 |
| CP-14 | `[PROPOSTO]` | Aguarda aprovação de ADR | Rotas `/papeis` | `[PROPOSTO]` ADR_139, no Core, só Dono e Administrador. `GET`/`POST /papeis`; `GET`/`PATCH`/`DELETE /papeis/{papelId}`; `PUT /papeis/{papelId}/severidades`, `/tipos-alerta`, `/membros`; `POST`/`DELETE /papeis/{papelId}/membros/{membroId}`. Sem listagem de excluídos (ADR_140). | — | ADR_139, ADR_140 |

### §3 Assinatura e Pagamento

| CP | Situação | O que falta | Ponto | Descrição | Elementos | ADRs |
|---|---|---|---|---|---|---|
| CP-15 | `[PROPOSTO]` | Aguarda aprovação de ADR | `Tenant 1 -- 1 Assinatura` | DER v9 e ADR_121/122. O DER v9 ainda tem também `Empresa \|\|--o{ Assinatura` (v1/v2) `[CONFLITO]`. `[PROPOSTO]` ADR_158: a Assinatura é só do `Tenant`; a ligação com a `Empresa` saiu. | CL-001 `Tenant`, CL-008 `Empresa` | ADR_121, ADR_122, ADR_158 |
| CP-16 | `[PENDENTE]` | Detalhe em aberto | `Assinatura.tenantId`, `limites` | ADR_122: limites de IA, retenção e créditos. A estrutura de `limites` e o tipo `[PENDENTE]`. O downgrade altera só a `Assinatura` (ADR_124). Retenção de arquivos e Ocorrências por plano, padrão 3 meses (ADR_104). | CL-020 `Assinatura` | ADR_104, ADR_122, ADR_124 |
| CP-17 | `[PENDENTE]` | Detalhe em aberto | Duas versões dos métodos | Planilha: `contratarPlano`, `verificarInadimplencia` e `calcularValorProporcional` por `empresa_id` e por `tenantId`. A pauta (ASS-15) deixou a escolha em aberto `[PENDENTE]`. | — | — |
| CP-18 | `[PENDENTE]` | Detalhe em aberto | `StatusAssinatura` | O enum existe na aba, mas sem valores. O Guia das Classes descreve o status como Ativa, Pendente, Inadimplente, Suspensa, Cancelamento Agendado ou Cancelada. Os nomes dos valores no enum não estão escritos `[PENDENTE]` (pauta ASS-09, sem decisão). | ES-06 `StatusAssinatura` | — |
| CP-19 | `[CONFLITO]` | Precisa de decisão do time | `RecursosAnaliseIA.SUGESTAO` | Pauta SUG-04: criar o item `SUGESTAO` no enum; se o plano tiver `SUGESTAO`, a Sugestão automática é gerada; no DER, `recursoIA` (Boolean) vira lista de recursos. `[CONFLITO]` a ADR_076 (posterior) diz que o local da flag estava `[PENDENTE]` e cria o `ProdutoRecursoIA` com `planoTemIA`. As fontes não dizem como `SUGESTAO` e `planoTemIA` se relacionam. O DER v9 ainda tem `recursoIA` Boolean. | ES-03 `RecursosAnaliseIA`, CL-021 `ProdutoRecursoIA` | ADR_076 |
| CP-20 | `[A CONFERIR]` | Conferir na planilha | `Plano.recursosHabilitados` | O atributo diz `RecursoAnaliseIA` e o enum se chama `RecursosAnaliseIA` `[A CONFERIR]`. | CL-018 `Plano`, ES-03 `RecursosAnaliseIA` | — |
| CP-21 | `[CONFLITO]` | Precisa de decisão do time | `ProdutoRecursoIA` | ADR_076: tabela de controle e relacionamento entre Produto e Plano, com `planoTemIA` e `produtoAtivouIA`. A Sugestão automática só roda com os dois verdadeiros. No downgrade, a automática de todos os Produtos é desligada. Os campos de ligação não estão escritos `[PENDENTE]`. `[CONFLITO]` não está no DER v9. | CL-021 `ProdutoRecursoIA` | ADR_076 |
| CP-22 | `[PENDENTE]` | Detalhe em aberto | `TabelaPrecificacao` | ADR_127/131 e DER v9. Valores da aba Planos do Plano de Monetização: FREE 1GB/7 dias/0; Starter 10GB/15 dias/200; Pro 100GB/30 dias/350; Business 500GB/90 dias/800; Enterprise 1TB/90 dias/1500. `rateLimit`, `limiteProdutos`, `limiteMembros`, `creditosIA`, `custoAddOnClerk` e `margemAddOn` `[PENDENTE]`. | CL-019 `TabelaPrecificacao` | ADR_127, ADR_131 |
| CP-23 | `[PENDENTE]` | Detalhe em aberto | `Plano` × `TabelaPrecificacao` | Os dois têm nome do plano, volume, retenção, dashboard e preço. Nenhuma fonte diz se a tabela substitui o `Plano`; o DER v9 mantém os dois `[PENDENTE]`. | CL-018 `Plano`, CL-019 `TabelaPrecificacao` | — |
| CP-24 | `[PENDENTE]` | Detalhe em aberto | Acima do limite | ADR_129/132/135: Produtos e Membros acima do novo limite ficam `ACESSO_PENDENTE`, bloqueados, até o DONO aprovar em 24 h; sem aprovação, o pedido expira. Se o DONO pode reabrir `[PENDENTE]`. | — | ADR_129, ADR_132, ADR_135 |
| CP-25 | `[CONFLITO]` | Atualizar DER ou planilha | `EventoGateway.status`, `erro` | ADR_125 e DER v9 (texto da v3): o evento é marcado `EXECUTADO` ou `FALHA`, e a `FALHA` guarda o erro. Vale para eventos de qualquer gateway (webhooks da Clerk, pagamento e outros). `[CONFLITO]` a planilha tem `resultado` (`SUCESSO`/`FALHA`) e `motivoFalha`, e o bloco do DER v9 ainda tem `resultado` e `motivoFalha`. Os campos aparecem lado a lado até o time escolher. `TipoOperacaoGateway` só tem operações de pagamento; os tipos dos eventos da Clerk `[PENDENTE]`. | CL-027 `EventoGateway`, ES-09 `TipoOperacaoGateway` | ADR_125 |
| CP-26 | `[A CONFERIR]` | Conferir na planilha | Enums do `EventoGateway` | Na aba, os dois estão rotulados "Enum StatusReembolso" (cópia) `[A CONFERIR]`. | CL-027 `EventoGateway` | — |
| CP-27 | `[PROPOSTO]` | Aguarda aprovação de ADR | Reprocessamento | ADR_125: um evento com `FALHA` pode ser reprocessado sozinho por uma API interna. `[PROPOSTO]` ADR_133: `POST /internal/eventos-gateway/{eventoId}/reprocessar` e `GET /internal/eventos-gateway?status=FALHA`. Nenhum método da planilha cobre isso. | — | ADR_125, ADR_133 |
| CP-28 | `[A CONFERIR]` | Conferir na planilha | `Reembolso` | A aba está com o título "Nome da classe" `[A CONFERIR]`. | CL-026 `Reembolso` | — |

### §4 Créditos

| CP | Situação | O que falta | Ponto | Descrição | Elementos | ADRs |
|---|---|---|---|---|---|---|
| CP-29 | `[PENDENTE]` | Detalhe em aberto | Serviço | Nenhuma ADR diz em qual serviço fica o módulo Créditos `[PENDENTE]`. | — | — |
| CP-30 | `[PROPOSTO]` | Aguarda aprovação de ADR | Nome | ADR_117: o usuário compra Créditos, não tokens; "o nome é Créditos" resolve o pendente `SaldoTokens` × Créditos. `[PROPOSTO]` ADR_157: a classe `SaldoTokens` (módulo 9) sai e a Sugestão usa o `Saldo` deste módulo; quem reserva e liquida é o módulo de Sugestão (ADR_038), representado pela `ModuloSugestao` `[PROPOSTO]` ADR_156. Os métodos de reserva, liquidação e substituição atômica (ADR_078/098) continuam `[PENDENTE]`. | CL-030 `Saldo`, CL-075 `ModuloSugestao` | ADR_038, ADR_078, ADR_098, ADR_117, ADR_156, ADR_157 |
| CP-31 | `[PENDENTE]` | Detalhe em aberto | "Token" da planilha de créditos | ADR_117: refere-se a tokens de API de LLM (BYOK) cadastrados como fonte de crédito, e não ao token do produtor. Como o BYOK entra na reserva e na cobrança `[PENDENTE]` (ADR_080). | — | ADR_080, ADR_117 |
| CP-32 | `[PENDENTE]` | Detalhe em aberto | Reserva | ADR_078: reserva = (tokens do prompt + teto de resposta, ex.: 1000) × 1,2. O consumo real liquida a cobrança e a diferença volta ao saldo. A reserva expira em 30,6 s e é liberada na falha da LLM. ADR_098: cada retentativa faz uma nova reserva, com substituição atômica da anterior; "o módulo de Créditos precisa de uma operação de substituição atômica de reserva ligada à Sugestão". Nenhum método ou valor de enum da planilha representa reserva, liquidação ou substituição `[PENDENTE]`. | — | ADR_078, ADR_098 |
| CP-33 | `[CONFLITO]` | Precisa de decisão do time | `PlanoCreditos` | `[CONFLITO]` a aba "Cópia de Modelo Padrão" define uma segunda classe `Plano`, com `creditos_por_ciclo` e `GerarCreditos()`, diferente do `Plano` de Assinatura. Aqui aparece como `PlanoCreditos` só para não colidir. | CL-029 `PlanoCreditos`, CL-018 `Plano` | — |
| CP-34 | `[CONFLITO]` | Precisa de decisão do time | `Controle.plano: Plano` | `[CONFLITO]` não dá para saber qual dos dois `Plano`. Por isso o campo não tem seta. | CL-032 `Controle`, CL-018 `Plano` | — |
| CP-35 | `[A CONFERIR]` | Conferir na planilha | `Credito` | `status`, `totalDeCreditos`, `qtdCreditosRestantes` e `custoAtualDeCreditos` sem tipo `[A CONFERIR]`. | CL-028 `Credito` | — |

### §5 Coletor

| CP | Situação | O que falta | Ponto | Descrição | Elementos | ADRs |
|---|---|---|---|---|---|---|
| CP-36 | `[PENDENTE]` | Detalhe em aberto | Ingestão OTLP | ADR_108/119: OTLP HTTP (4318) e gRPC (4317), só os caminhos padrão `/v1/logs` e `/v1/traces`. Produto e tenant vêm do token Bearer, sem `productId` na URL. ADR_118: `GET /health` (200 ou 503) e `grpc.health.v1.Health`, sem token; `/ping` removido. Token inválido ou revogado → 401. Sobrecarga → 429/503 com `Retry-After: 120` (ADR_120). Nenhuma classe da planilha cobre esses pontos `[PENDENTE]`. | — | ADR_108, ADR_118, ADR_119, ADR_120 |
| CP-37 | `[PENDENTE]` | Detalhe em aberto | `Produtor`, `TokenApi` | ADR_113/115/122 e DER v9. O `producerId` nasce com o token; um Produto tem vários produtores, cada um com seu token. O token é cifrado com AES-256-GCM (chave no KMS) e pode ser copiado a qualquer momento; o hash SHA-256 é o índice de busca do Coletor. Não expira e pode ser revogado (ADR_106). Para trocar, cria-se outro e revoga-se o antigo (ADR_107). Só administradores criam ou revogam (ADR_109). O serviço que guarda as duas coleções não está escrito `[PENDENTE]`. | CL-041 `Produtor`, CL-042 `TokenApi` | ADR_106, ADR_107, ADR_109, ADR_113, ADR_115, ADR_122 |
| CP-38 | `[PENDENTE]` | Detalhe em aberto | Nome do token | ADR_106: "o usuário dá um nome e recebe o token". Nenhuma fonte diz em que campo fica `[PENDENTE]`. | — | ADR_106 |
| CP-39 | `[PROPOSTO]` | Aguarda aprovação de ADR | `CredencialIngestao` (tabela) | `[CONFLITO]` a pauta ING-02 ligava a tabela ao Tenant; a ADR_111 a mantinha; a ADR_122 (marcado `[INFERIDO]` na ADR) e o DER v9 a dão como substituída por `TokenApi`. `[PROPOSTO]` ADR_155: fica só como substituída pelo `TokenApi`; a ligação com o Tenant sai. Campos do DER v9. É diferente da classe `CredencialIngestao` do SDK (módulo 13). | CL-043 `CredencialIngestao`, CL-042 `TokenApi` | ADR_111, ADR_122, ADR_155 |
| CP-40 | `[PROPOSTO]` | Aguarda aprovação de ADR | `GerenciadorRequisicao.Token` | A planilha tipa como `Credito`, e a ADR_117 diz que esse tipo está errado. `[PROPOSTO]` ADR_155: o tipo passa a ser `TokenApi`, e o Coletor busca o produtor pelo hash SHA-256 do Bearer (ADR_113). Isso liga o grupo `Produtor`/`TokenApi` às classes da ingestão. | CL-034 `GerenciadorRequisicao`, CL-028 `Credito`, CL-042 `TokenApi`, CL-041 `Produtor` | ADR_113, ADR_117, ADR_155 |
| CP-41 | `[PENDENTE]` | Detalhe em aberto | `Arquivo.status` | ADR_099: `PROCESSANDO`, `CONCLUIDO` e `FALHA` (na tela: Processando, Concluído, Falha). Nome do enum `[PENDENTE]`. | CL-039 `Arquivo` | ADR_099 |
| CP-42 | `[PENDENTE]` | Detalhe em aberto | `Arquivo.origem` | ADR_100: uma lista só, com a coluna de origem `MANUAL` ou `AUTOMATICO`; "Arquivo/Lote precisam guardar a origem". Nome do enum `[PENDENTE]`. Como o Arquivo aponta para o lote não está escrito `[PENDENTE]`. | CL-039 `Arquivo` | ADR_100 |
| CP-43 | `[CONFLITO]` | Precisa de decisão do time | `Arquivo 1 -- 1..* Trace` | `[CONFLITO]` o diagrama de classes v2 (Varredura e Finder) usa 1..*; o DER v9 usa 0..* (pauta ING-05, sem decisão sobre este ponto). O Mermaid usa o modelo de classes. Quem cria o `Trace` na ingestão não está escrito `[PENDENTE]`. | CL-039 `Arquivo`, CL-040 `Trace` | — |
| CP-44 | `[PENDENTE]` | Detalhe em aberto | `owner_id`, `company_id` | A planilha não foi atualizada. A ADR_121 diz que todo documento leva `tenantId`. A relação entre esses campos e o `tenantId` só aparece no DER v9 como pendência 11, marcada `[INFERIDO]` `[PENDENTE]`. | — | ADR_121 |
| CP-45 | `[PENDENTE]` | Detalhe em aberto | Detalhe da falha | ADR_103: motivo (malware ou prompt injection, erro de leitura, falha após a DLQ), número de tentativas e erro da última tentativa. Onde fica (Arquivo, histórico ou DLQ) `[PENDENTE]` na própria ADR. | — | ADR_103 |
| CP-46 | `[PENDENTE]` | Detalhe em aberto | Proteção e upload manual | ADR_042: o Coletor recebe todos os arquivos, checa binário/executável e prompt injection e manda o manual para uma seção paralela que enfileira no fim da `FilaOrdenada` (ADR_041). ADR_043: `.txt`, `.json`, `.csv`, `.log` (lista extensível), até 100 MB. ADR_045: vários arquivos numa requisição viram um lote. ADR_048: só o arquivo reprovado é bloqueado. ADR_053: 202 Accepted. ADR_075: o Coletor pede o `execId` `M<uuid>` à API da Varredura antes de enfileirar o lote. Nenhuma classe da planilha cobre a proteção, a seção manual nem o lote manual `[PENDENTE]`. | CL-050 `FilaOrdenada` | ADR_041, ADR_042, ADR_043, ADR_045, ADR_048, ADR_053, ADR_075 |
| CP-47 | `[A CONFERIR]` | Conferir na planilha | Classes de lote | `GerenciadorLote`, `LoteAgrupador` e `EnfileiradorLogs` não aparecem em nenhuma ADR. `GerenciadorLote.TamanhoMaximoByte: Log` `[A CONFERIR]` (o tipo `Log` não existe). A planilha não liga o `EnfileiradorLogs` à `FilaDesordenada`. | CL-036 `GerenciadorLote`, CL-037 `LoteAgrupador`, CL-038 `EnfileiradorLogs`, CL-049 `FilaDesordenada` | — |

### §6 Varredura

| CP | Situação | O que falta | Ponto | Descrição | Elementos | ADRs |
|---|---|---|---|---|---|---|
| CP-48 | `[CONFLITO]` | Atualizar DER ou planilha | Por Produto | ADR_057: toda Varredura é de um Produto, com uma `FilaDesordenada` por Produto. O gatilho por tamanho é opcional, habilitado pelo cliente, com padrão de 500 arquivos; o agendamento (cron) continua. A planilha ainda diz que `limite_disparo` é interno e não exposto ao cliente (ADR_010) `[CONFLITO]`. Onde o cliente configura `[PENDENTE]`. A pauta VAR-01 ficou "pendente de cálculo"; a ADR_057 é posterior. | CL-049 `FilaDesordenada` | ADR_010, ADR_057 |
| CP-49 | `[CONFLITO]` | Atualizar DER ou planilha | `TravaVarredura` | `[CONFLITO]` está na planilha v2 e no DER v9. A pauta VAR-03 decidiu "coleção TravaVarredura, escopo global". Depois, a ADR_068 decidiu que não existe trava por Produto, e as ADR_058/069/072 trocaram a trava por chaves lock por arquivo numa coleção chave-valor do MongoDB: `lock:{tenantProduto}:{execId}:{loteId}:{arquivoId}`, valor de 1 caractere, TTL = estimativa + 10%. As chaves são liberadas no fechamento da execução (ADR_070). A coleção nova não tem nome em nenhuma fonte; a classe da planilha fica até o time decidir. | CL-051 `TravaVarredura` | ADR_058, ADR_068, ADR_069, ADR_070, ADR_072 |
| CP-50 | `[PENDENTE]` | Detalhe em aberto | `execId` | ADR_069/075: `V<uuid>` para varredura automática, gerado no `startVarredura()`, e `M<uuid>` para upload manual, pedido pelo Coletor à API da Varredura. Idempotência `arquivoId + execId` (ADR_070). Nenhuma fonte diz em que campo o `execId` fica `[PENDENTE]`. | — | ADR_069, ADR_070, ADR_075 |
| CP-51 | `[PENDENTE]` | Detalhe em aberto | Fim da execução | ADR_061/070: o Finder chama uma API da Varredura a cada arquivo ("arquivo X da execução Y finalizado") e recebe true/false. Com true, a Varredura faz `finishVarredura()` (`COMPLETED` ou `COMPLETED_WITH_ERROR`), libera as chaves lock e emite "varredura finalizada" ao Core. Rota e contrato `[PENDENTE]`. A planilha marca "quem chama `finishVarredura()`" como `[INFERIDO]`; a ADR_061 resolveu. | — | ADR_061, ADR_070 |
| CP-52 | `[PENDENTE]` | Detalhe em aberto | API de Estimativa | ADR_072: calcula o tempo esperado por arquivo para o TTL. Entradas e cálculo `[PENDENTE]`. Não tem classe. | — | ADR_072 |
| CP-53 | `[PENDENTE]` | Detalhe em aberto | `HistoricoVarredura` | ADR_060: cada execução é registrada (varreduraId, Produto, gatilho, arquivos/lotes, resultado). O nome é provisório na própria ADR e a estrutura `[PENDENTE]`. Os campos são as palavras da ADR, sem tipo. Retenção de 3 meses (ADR_071); a ADR_147 põe um índice TTL de cerca de 90 dias no MongoDB. | CL-052 `HistoricoVarredura` | ADR_060, ADR_071, ADR_147 |
| CP-54 | `[PENDENTE]` | Detalhe em aberto | `ArquivoScanStatus` e tentativas | Pauta FIN-01: status final `ERROR` depois de 3 tentativas. ADR_046/059: DLQ com até 3 tentativas, cada uma no fim da `FilaOrdenada`; erro de leitura/parsing é crítico, sem retry (ADR_049). ADR_073: depois de 3 falhas o usuário só pode enviar um novo arquivo. A planilha deixa `max_attempts` `[PENDENTE]`; as fontes dão 3. | ES-16 `ArquivoScanStatus`, CL-050 `FilaOrdenada` | ADR_046, ADR_049, ADR_059, ADR_073 |
| CP-55 | `[CONFLITO]` | Atualizar DER ou planilha | `ArquivoVarredura.status` × `Arquivo.status` | `[CONFLITO]` a ADR_099 resolveu o conflito "planilha (Arquivo Varredura) × DER × USID_007" com `PROCESSANDO`, `CONCLUIDO`, `FALHA` como status do Arquivo. A planilha (`ArquivoScanStatus`) e a pauta FIN-01 (`ERROR`) continuam com os valores em inglês. As fontes não dizem se os dois status convivem. | CL-046 `ArquivoVarredura`, CL-039 `Arquivo`, ES-16 `ArquivoScanStatus` | ADR_099 |
| CP-56 | `[CONFLITO]` | Atualizar DER ou planilha | `VarreduraStatus` | Planilha. Bate com a ADR_061 (`COMPLETED`, `COMPLETED_WITH_ERROR`). `[CONFLITO]` o DER v9 usa `PENDING` e não tem `SCHEDULED` nem `FAILED`. | ES-14 `VarreduraStatus` | ADR_061 |
| CP-57 | `[CONFLITO]` | Precisa de decisão do time | `AgendamentoVarreduraStatus` | Planilha. O DER tem `ativo` (Boolean) e `status`; pauta VAR-07 sem decisão `[CONFLITO]`. | ES-17 `AgendamentoVarreduraStatus` | — |
| CP-58 | `[CONFLITO]` | Atualizar DER ou planilha | `DLQ`, `requeue()` | A DLQ das ADR_046/059 não tem classe `[PENDENTE]`. A ADR_073 tirou a devolução do arquivo à `FilaDesordenada`; o `requeue()` da planilha ainda existe `[CONFLITO]`. | CL-049 `FilaDesordenada` | ADR_046, ADR_059, ADR_073 |
| CP-59 | `[A CONFERIR]` | Conferir na planilha | `getResume()` | A planilha escreve `VarreduraResume` no retorno e `VarreduraResumo` no tipo `[A CONFERIR]`. | CL-045 `VarreduraResumo` | — |
| CP-60 | `[CONFLITO]` | Atualizar DER ou planilha | Filas em Redis Streams | ADR_143: o broker das filas é o Redis Streams (`FilaDesordenada` e `FilaOrdenada` por Produto, DLQ, fila da Sugestão manual e eventos de notificação). ADR_146: nomes `lhamalog:AMBIENTE:PAPEL` com hash tag por `tenantId` e `produtoId`; envelope obrigatório (`eventId`, `type`, `version`, `timestamp`, `tenantId`, `produtoId`, `execId`, `tentativa`, `payload`); até 3 tentativas com reenvio no fim da mesma stream, depois DLQ por stream; erro crítico sem retry; idempotência `arquivoId + execId` nas filas do Finder. ADR_145: a classe base de consumidor é copiada em cada repositório, sem biblioteca comum. Nenhuma classe da planilha representa a stream, o envelope ou o consumidor base (a ADR não dá nome à classe) `[PENDENTE]`. `FilaDesordenada.requeue()` × reenvio no fim da mesma stream `[CONFLITO]`. | CL-049 `FilaDesordenada`, CL-050 `FilaOrdenada` | ADR_143, ADR_145, ADR_146 |
| CP-61 | `[CONFLITO]` | Atualizar DER ou planilha | Agendador | ADR_147: Spring `@Scheduled` + ShedLock, com o lock no MongoDB. Um tick global lê a coleção `varredura_schedules` (cron e próxima execução por Produto) e publica as execuções vencidas no Redis Streams; o gatilho por tamanho (500) publica na mesma stream; os workers da Varredura consomem. Se `varredura_schedules` é a coleção do `AgendamentoVarredura` (que tem `cron_expression` e `next_executor_at` por Produto) não está escrito `[PENDENTE]`. `[CONFLITO]` `AgendamentoVarredura.dispatch(): Varredura` (marcado `[INFERIDO]` na planilha) cria a Varredura, e pela ADR_147 o tick só publica na stream. | CL-047 `AgendamentoVarredura` | ADR_147 |

### §7 Finder

| CP | Situação | O que falta | Ponto | Descrição | Elementos | ADRs |
|---|---|---|---|---|---|---|
| CP-62 | `[PROPOSTO]` | Aguarda aprovação de ADR | `Finder.Ocorrencia` e `processar()` | A planilha tinha o campo `Ocorrencia` e `processar(): Ocorrencia`, e a ADR_062 diz que o Finder não conhece Ocorrência. `[PROPOSTO]` ADR_161: o campo sai e `processar()` devolve `ResumoAnalise`. | CL-053 `Finder`, CL-066 `Ocorrencia`, CL-061 `ResumoAnalise` | ADR_062, ADR_161 |
| CP-63 | `[CONFLITO]` | Atualizar DER ou planilha | `AchadoAnalise` | DTO sem coleção (ADR_040). Campos da aba original + adições v2 (planilha). `tipo`: ADR_040/062. `recorrente`: ADR_063 ("atributo booleano") e pauta FIN-05. `[CONFLITO]` o DER v9 ainda tem `AchadoAnalise` como entidade, com `gravidade`, `chaveAchado` e `vetorRef`. | CL-060 `AchadoAnalise` | ADR_040, ADR_062, ADR_063 |
| CP-64 | `[CONFLITO]` | Precisa de decisão do time | Gravidade | `[CONFLITO]` a pauta FIN-07 decidiu que a `ClassificadorAnalise` registra a gravidade, num atributo chamado `gravidade`, que é o padrão gravado na Ocorrência. Depois, a ADR_062 decidiu que o Finder não sabe nada de criticidade e que a gravidade é definida pelo Módulo Ocorrência. O Mermaid segue a ADR_062: a gravidade só aparece na `Ocorrencia` (módulo 8). | CL-062 `ClassificadorAnalise`, CL-066 `Ocorrencia` | ADR_062 |
| CP-65 | `[CONFLITO]` | Precisa de decisão do time | `AchadoAnalise → Trace` | Pauta ING-05: um Trace pode ter 0 ou mais `AchadoAnalise`, e o `AchadoAnalise` precisa sempre de 1 Trace. `[CONFLITO]` o DER v9 tem `Trace \|o--o{ AchadoAnalise` e a aba "AchadoAnalise (adições v2)" diz "`traceId` null se o log não tiver trace". | CL-060 `AchadoAnalise`, CL-040 `Trace` | — |
| CP-66 | `[PENDENTE]` | Detalhe em aberto | Recorrência | ADR_063/074 e pauta FIN-05: `recorrente` é atributo booleano. `MotorAnalise.verificarRecorrencia()` consulta o `BancoVetorial`, isolado por Produto, na janela dos achados dos últimos 500 arquivos. Critério de semelhança `[PENDENTE]`. | CL-056 `MotorAnalise`, CL-058 `BancoVetorial` | ADR_063, ADR_074 |
| CP-67 | `[CONFLITO]` | Atualizar DER ou planilha | `RecorrenciaLog` | `[CONFLITO]` está na planilha (que a marca `[INFERIDO]`) e no DER v9 e implementa a regra "3 ou 4 arquivos seguidos" da ADR_013. A ADR_063 trocou essa regra pela janela de 500 arquivos no `BancoVetorial`, mas não remove a classe pelo nome. | CL-059 `RecorrenciaLog`, CL-058 `BancoVetorial` | ADR_013, ADR_063 |
| CP-68 | `[CONFLITO]` | Atualizar DER ou planilha | `BancoVetorial` | Planilha v2. Pauta FIN-06: estrutura baseada nas tratativas de um RAG comum. `[CONFLITO]` `searchSimilar(..., owner_id)` × isolamento por Produto (ADR_074) e `store(..., ocorrencia_id)` × Finder sem Ocorrência (ADR_062). | CL-058 `BancoVetorial` | ADR_062, ADR_074 |
| CP-69 | `[PENDENTE]` | Detalhe em aberto | `MotorAnalise.timeoutMs` | Pauta FIN-02: cálculo determinístico do timeout com base no tamanho do arquivo. A fórmula não está escrita `[PENDENTE]`. | CL-056 `MotorAnalise` | — |
| CP-70 | `[CONFLITO]` | Atualizar DER ou planilha | `validarSeguranca()` | `[CONFLITO]` a planilha diz `void`. A ADR_064 diz que a função troca emails, remove as linhas com senha, token ou secret (com marcador, ex.: "log com senha omitido") e retorna "as linhas mascaradas (+ total para `dadosSensiveisIdentificados`)". O tipo de retorno não está escrito. A lista de regex `[PENDENTE]`. | — | ADR_064 |
| CP-71 | `[PENDENTE]` | Detalhe em aberto | Workers e idempotência | ADR_065/068/070: muitos workers independentes, em qualquer fila de Produto. A chave `arquivoId + execId` é reservada antes de processar. A coleção de idempotência não tem classe `[PENDENTE]`. | — | ADR_065, ADR_068, ADR_070 |

### §8 Ocorrência

| CP | Situação | O que falta | Ponto | Descrição | Elementos | ADRs |
|---|---|---|---|---|---|---|
| CP-72 | `[PROPOSTO]` | Aguarda aprovação de ADR | Resumo × Ocorrência | A aba `Ocorrencia` (e `Ocorrencia v2`) da planilha é o resumo por Arquivo da ADR_020. As ADR_035/040 criaram a Ocorrência concreta e mantiveram o resumo como agrupador ("1 resumo por Arquivo : 0..N Ocorrências", ADR_035). `[PROPOSTO]` ADR_160: o resumo se chama `ResumoArquivo` (opção da ADR_035; pauta OCO-02 sem decisão). | CL-066 `Ocorrencia`, CL-065 `ResumoArquivo` | ADR_020, ADR_035, ADR_040, ADR_160 |
| CP-73 | `[PROPOSTO]` | Aguarda aprovação de ADR | Campos do `ResumoArquivo` | Aba `Ocorrencia v2`. `spamIdentificados` substitui `informacaoIdentificados`, como no DER v9 (ADR_019). `[PROPOSTO]` ADR_160: `achados: List<AchadoAnalise>` vira `ocorrenciaIds: List<uuid>`, porque a ADR_040 diz que o resumo "guarda os contadores e as referências às Ocorrências criadas" e os achados vão no `ResumoAnalise` (ADR_062). A planilha marca `dadosSensiveisIdentificados` e `recorrentesIdentificados` `[INFERIDO]`; `recorrentesIdentificados` tinha "`[PENDENTE]` se RECORRENTE virar atributo", o que a ADR_063 fez. `StatusProcessamento` `[A CONFERIR]` (pauta OCO-03). | CL-065 `ResumoArquivo`, CL-066 `Ocorrencia`, CL-061 `ResumoAnalise` | ADR_019, ADR_040, ADR_062, ADR_063, ADR_160 |
| CP-74 | `[PENDENTE]` | Detalhe em aberto | `chaveIdempotencia` | Na planilha, `= arquivoId` (ADR_014/020). A ADR_070 usa `arquivoId + execId` no envio do `ResumoAnalise`. A chave da Ocorrência concreta continua `[PENDENTE]` (ADR_035/040, pauta OCO-01). | CL-061 `ResumoAnalise` | ADR_014, ADR_020, ADR_035, ADR_040, ADR_070 |
| CP-75 | `[CONFLITO]` | Atualizar DER ou planilha | Ocorrência concreta | Sem aba. Campos do mapeamento da ADR_040, mais `id`, `arquivoId` e `status` (ADR_040) e `tenantId` (ADR_121). Tipos não escritos. "Referência ao resumo", "produto" e "data de criação" não têm nome de campo `[PENDENTE]`; a data é `descobertaEm` no DER e "data de criação" na ADR_040 `[CONFLITO]`. | — | ADR_040, ADR_121 |
| CP-76 | `[PENDENTE]` | Detalhe em aberto | `Ocorrencia.status` | ADR_082: `ABERTA`, `EM_ANALISE` (quando uma Sugestão fica `AGUARDANDO_REVISAO`, ADR_089/091/096) e `FECHADA`. Transições: `ABERTA` → `EM_ANALISE` ou `FECHADA`; `EM_ANALISE` → `FECHADA`; `FECHADA` → `ABERTA`. Só fecha com todas as Sugestões que não falharam `FECHADA` (ADR_089/090). Rota da mudança manual `[PENDENTE]`. | CL-066 `Ocorrencia` | ADR_082, ADR_089, ADR_090, ADR_091, ADR_096 |
| CP-77 | `[CONFLITO]` | Precisa de decisão do time | `Ocorrencia.gravidade` | ADR_062: definida pelo Módulo Ocorrência (criticidade do módulo × tipo do achado). Matriz e valores `[PENDENTE]`. `[CONFLITO]` pauta FIN-07 (`ClassificadorAnalise`). | CL-066 `Ocorrencia`, CL-062 `ClassificadorAnalise` | ADR_062 |
| CP-78 | `[PROPOSTO]` | Aguarda aprovação de ADR | `ModuloOcorrencia` | Planilha v2 (marcada `[INFERIDO]` na própria planilha), com `registrar()` e `existsByChave()`. `[PROPOSTO]` ADR_161: ganha `receberResumo(ResumoAnalise)` (ADR_062: recebe o resumo, define a gravidade e cria as Ocorrências) e `dispararSugestaoAutomatica(Ocorrencia)` (ADR_036: consulta o plano, chama o módulo de Sugestão (`ModuloSugestao`), espera e envia Ocorrência + Sugestão à Notificação). A pauta OCO-06 propunha "ModuloOcorrencia com os métodos novos". Ela não monta prompt nem reserva créditos (ADR_038/039). | CL-064 `ModuloOcorrencia`, CL-075 `ModuloSugestao` | ADR_036, ADR_038, ADR_039, ADR_062, ADR_161 |
| CP-79 | `[PROPOSTO]` | Aguarda aprovação de ADR | `Mapper` | Pauta FIN-09 ("uma classe Mapper que converte para a classe concreta"). `[PROPOSTO]` ADR_161: fica no módulo Ocorrência e é chamado pela `ModuloOcorrencia` ao receber o `ResumoAnalise` (ADR_062 diz que quem cria as Ocorrências é o Módulo Ocorrência). Método `converter()`. | CL-067 `Mapper`, CL-064 `ModuloOcorrencia`, CL-061 `ResumoAnalise` | ADR_062, ADR_161 |
| CP-80 | `[PENDENTE]` | Detalhe em aberto | Consultas | ADR_101: Ocorrências por Produto, por lote e por arquivo. Rotas `[PENDENTE]`. | — | ADR_101 |
| CP-81 | `[PENDENTE]` | Detalhe em aberto | Retenção | ADR_104: por plano, padrão 3 meses. Expurgo `[PENDENTE]`. | — | ADR_104 |

### §9 Sugestão

| CP | Situação | O que falta | Ponto | Descrição | Elementos | ADRs |
|---|---|---|---|---|---|---|
| CP-82 | `[PROPOSTO]` | Aguarda aprovação de ADR | `AvaliacaoSugestao` | DER v9 (`id`, `nota`, `comentario`, `criadaEm`) e ADR_088: 1 a 5 estrelas e comentário; qualquer membro com acesso pode avaliar; uma avaliação por pessoa por Sugestão. A ADR pede o autor (`usuarioId`) e a unicidade `sugestaoId + usuarioId`. `[PROPOSTO]` ADR_159: o autor é o `Membro` (`membroId`), já que o `Usuario` foi substituído pelo `Membro` (DER v9); unicidade `sugestaoId + membroId`. | CL-069 `AvaliacaoSugestao`, CL-002 `Membro`, CL-010 `Usuario` | ADR_088, ADR_159 |
| CP-83 | `[CONFLITO]` | Atualizar DER ou planilha | `Sugestao.avaliacao` e `avaliar()` | `[CONFLITO]` a planilha guarda uma nota; a ADR_088 e o DER usam várias avaliações em `AvaliacaoSugestao`. | CL-068 `Sugestao`, CL-069 `AvaliacaoSugestao` | ADR_088 |
| CP-84 | `[PENDENTE]` | Detalhe em aberto | Contexto | ADR_087: últimas 5 Sugestões da mesma Ocorrência, com avaliações. Nenhum campo da `ContextoSugestao` guarda isso `[PENDENTE]`. Mascaramento igual ao do Finder (ADR_079). | CL-070 `ContextoSugestao` | ADR_079, ADR_087 |
| CP-85 | `[PENDENTE]` | Detalhe em aberto | `GatewayLLMSugestao` | ADR_039: nome novo da interface `GatewayLLM` do módulo Sugestão (pauta SUG-16). `GatewayLLMPadrao` implementa a interface ("implements" na aba). Provedor `[PENDENTE]` (ADR_080). | CL-071 `GatewayLLMSugestao`, CL-072 `GatewayLLMPadrao` | ADR_039, ADR_080 |
| CP-86 | `[PENDENTE]` | Detalhe em aberto | `ChaveLLMTenant` | ADR_128 e DER v9: chave BYOK numa coleção do módulo Sugestão, cifrada com AES-256-GCM e ligada ao `tenantId`. ADR_080: "a `GatewayLLMSugestao` precisa escolher a credencial (LhamaLog ou do cliente)". Rota da API de BYOK `[PENDENTE]`. | CL-074 `ChaveLLMTenant`, CL-071 `GatewayLLMSugestao` | ADR_080, ADR_128 |
| CP-87 | `[PROPOSTO]` | Aguarda aprovação de ADR | `SaldoTokens` | Removida `[PROPOSTO]` ADR_157: a ADR_117 diz que o nome é Créditos e manda atualizar os documentos da Sugestão; a ADR_038 recomendava unificar. A Sugestão usa o `Saldo` do módulo 4. | CL-030 `Saldo` | ADR_038, ADR_117, ADR_157 |
| CP-88 | `[PROPOSTO]` | Aguarda aprovação de ADR | Orquestração | `[PROPOSTO]` ADR_156: as ADRs falam de um "módulo de Sugestão" sem dar nome de classe. Ele virou a `ModuloSugestao` (nome no padrão da `ModuloOcorrencia`). Pelas ADRs, é ele que cria a `Sugestao` (ADR_036: no manual, com status `PROCESSANDO`), monta o prompt com o `ContextoSugestao` (ADR_039), faz a prévia e a reserva no `Saldo` depois do `montarPrompt()` (ADR_038/078/098) e chama a `GatewayLLMSugestao` (ADR_039). A `ModuloOcorrencia` só o chama no fluxo automático (ADR_036). A manual é consumida de uma fila Redis Streams (ADR_143/146) por um worker; o worker e a rota do pedido manual não têm classe própria `[PENDENTE]`. Métodos da `ModuloSugestao` `[PENDENTE]`. Uma fila com prioridade ou duas continua `[PENDENTE]` (pauta SUG-05). | CL-075 `ModuloSugestao`, CL-064 `ModuloOcorrencia`, CL-068 `Sugestao`, CL-070 `ContextoSugestao`, CL-030 `Saldo`, CL-071 `GatewayLLMSugestao` | ADR_036, ADR_038, ADR_039, ADR_078, ADR_098, ADR_143, ADR_146, ADR_156 |

### §10 Notificação

| CP | Situação | O que falta | Ponto | Descrição | Elementos | ADRs |
|---|---|---|---|---|---|---|
| CP-89 | `[CONFLITO]` | Precisa de decisão do time | `Notificacao.tipo` | ADR_081: dois tipos, `OCORRENCIA` e `OCORRENCIA_COM_SUGESTAO`; o segundo leva o `sugestaoId` opcional ou "o campo de erro" quando a Sugestão falhou. Sem IA no plano ou no Produto, vai `OCORRENCIA`. `[CONFLITO]` a pauta NOT-02 decidiu três valores, com `FALHA_SUGESTAO` para a falha da Sugestão manual "só para quem pediu, por PUSH e WEB". Depois, a ADR_081 deixou o tipo da falha manual `[PENDENTE]` e a ADR_086 mandou esse aviso só por WebSocket e histórico, sem push nem email. Nome do enum `[PENDENTE]`. O nome do "campo de erro" não está escrito `[PENDENTE]`. | CL-076 `Notificacao` | ADR_081, ADR_086 |
| CP-90 | `[CONFLITO]` | Precisa de decisão do time | Construtor com `sugestao_id` | Pauta NOT-01: incluir `sugestao_id` opcional no construtor e no DER, preenchido só quando a notificação tem Sugestão. A posição do parâmetro não está escrita: no Mermaid ele aparece no fim, num segundo construtor, só para mostrar a decisão ao lado do construtor original da planilha. O DER v9 ainda não tem `sugestaoId` `[CONFLITO]`. | — | — |
| CP-91 | `[PENDENTE]` | Detalhe em aberto | Templates | Pauta NOT-03: um template por tipo. `OCORRENCIA` mostra os dados da Ocorrência; `OCORRENCIA_COM_SUGESTAO` mostra a Ocorrência e o texto da Sugestão, ou "Não foi possível criar uma sugestão"; `FALHA_SUGESTAO` mostra "Não foi possível criar a sugestão solicitada". A ADR_077 diz que, no automático, o motivo da falha não vai no push nem no email. Nenhuma classe da planilha representa os templates `[PENDENTE]`. | — | ADR_077 |
| CP-92 | `[PROPOSTO]` | Aguarda aprovação de ADR | `Membro -- Notificacao` | DER v9 (`Membro \|\|--o{ Notificacao : recebe por papel`). `[PROPOSTO]` ADR_159: `usuario_id` da planilha vira `membroId` em `Notificacao`, `PreferenciaNotificacao`, `DispositivoPush` e nos métodos dos enviadores, porque o `Usuario` foi substituído pelo `Membro` (DER v9). | CL-002 `Membro`, CL-076 `Notificacao`, CL-077 `PreferenciaNotificacao`, CL-083 `DispositivoPush`, CL-010 `Usuario` | ADR_159 |
| CP-93 | `[PENDENTE]` | Detalhe em aberto | Destinatários | ADR_130/134/136: por papel de notificação (módulo 2), com filtro de gravidade, tipo e Produto. A "consulta de agregação" não tem classe `[PENDENTE]`. | — | ADR_130, ADR_134, ADR_136 |
| CP-94 | `[CONFLITO]` | Precisa de decisão do time | `EnviadorWeb` × WebSocket | `[CONFLITO]` o `EnviadorWeb` publica por WebSocket, mas a ADR_141 deixa a Notificação só de saída e o WebSocket no Core. A ADR registra como `[PENDENTE]` a proposta de a Notificação devolver ao Core o que vai por WebSocket. | CL-082 `EnviadorWeb` | ADR_141 |
| CP-95 | `[PENDENTE]` | Detalhe em aberto | Eventos | ADR_143: os eventos de notificação passam pelo Redis Streams, no padrão da ADR_146. Nenhuma classe da planilha representa esse consumo `[PENDENTE]`. | — | ADR_143, ADR_146 |
| CP-96 | `[PROPOSTO]` | Aguarda aprovação de ADR | `PreferenciaNotificacao` | Ligada ao `Membro` por `membroId` `[PROPOSTO]` ADR_159. A seta para `CanalNotificacao` vem dos métodos dela. | CL-077 `PreferenciaNotificacao`, CL-002 `Membro`, ES-22 `CanalNotificacao` | ADR_159 |
| CP-97 | `[CONFLITO]` | Atualizar DER ou planilha | `PreferenciaNotificacao` × matriz | `[CONFLITO]` o DER v9 tem `severidadeMinima` na preferência, e a matriz de papéis também filtra por gravidade (ADR_134). A classe da planilha não tem `severidadeMinima` (pauta NOT-15, sem decisão). | CL-077 `PreferenciaNotificacao` | ADR_134 |
| CP-98 | `[CONFLITO]` | Precisa de decisão do time | Retorno de `enviar()` | `[CONFLITO]` a interface devolve `TentativaEntrega`; os três enviadores devolvem `StatusEnvioNotificacao` (pauta NOT-09, sem decisão). | CL-084 `TentativaEntrega`, ES-24 `StatusEnvioNotificacao` | — |
| CP-99 | `[CONFLITO]` | Precisa de decisão do time | `Notificacao.tentativaEntrega` × 1:N | `[CONFLITO]` a classe guarda uma tentativa; o DER liga `Notificacao 1:0..*` `TentativaEntrega`. O Mermaid usa o DER. | CL-076 `Notificacao`, CL-084 `TentativaEntrega` | — |
| CP-100 | `[PENDENTE]` | Detalhe em aberto | `StatusEnvioNotificacao.PENDENTE` | Valor de enum, sem relação com a marcação `[PENDENTE]`. | ES-24 `StatusEnvioNotificacao` | — |

### §11 Dashboard

| CP | Situação | O que falta | Ponto | Descrição | Elementos | ADRs |
|---|---|---|---|---|---|---|
| CP-101 | `[A CONFERIR]` | Conferir na planilha | `DashboardProduto` | Tem uma linha "Privado" sem nome nem tipo na aba `[A CONFERIR]`. | CL-088 `DashboardProduto` | — |
| CP-102 | `[A CONFERIR]` | Conferir na planilha | `Periodo.timezone: DateTime` | `[A CONFERIR]` fuso horário tipado como data. | CL-086 `Periodo` | — |
| CP-103 | `[PROPOSTO]` | Aguarda aprovação de ADR | `FiltroOcorrenciaEmpresarial` | O enum `tipoOcorrencia` não tem nome na aba `[A CONFERIR]`. `[PROPOSTO]` ADR_162: `..> Ocorrencia : consulta` (Guia das Classes: "consultar ocorrências de vários Produtos"). De onde vêm as outras métricas (`Metrica`, `Agregacao`) continua `[PENDENTE]`. | CL-090 `FiltroOcorrenciaEmpresarial`, CL-085 `Metrica`, CL-092 `Agregacao` | ADR_162 |
| CP-104 | `[PENDENTE]` | Detalhe em aberto | `Agregacao.formula` | `[PENDENTE]` na própria aba. | CL-092 `Agregacao` | — |
| CP-105 | `[PENDENTE]` | Detalhe em aberto | Serviço | Nenhuma ADR diz em qual serviço fica o Dashboard `[PENDENTE]`. | — | — |
| CP-106 | `[PENDENTE]` | Detalhe em aberto | De onde vêm as métricas | Nenhuma classe liga as métricas aos dados de Ocorrência/Varredura `[PENDENTE]`. | — | — |
| CP-107 | `[PROPOSTO]` | Aguarda aprovação de ADR | `Empresa` | `DashboardEmpresarial.empresa` aponta para a `Empresa`, que é o cadastro do Tenant `[PROPOSTO]` ADR_158. | CL-008 `Empresa`, CL-089 `DashboardEmpresarial` | ADR_158 |

### §12 Relatório

| CP | Situação | O que falta | Ponto | Descrição | Elementos | ADRs |
|---|---|---|---|---|---|---|
| CP-108 | `[PENDENTE]` | Detalhe em aberto | `GeradorArquivo` | Interface sem implementação e sem quem a use na planilha `[PENDENTE]`. | CL-098 `GeradorArquivo` | — |
| CP-109 | `[PENDENTE]` | Detalhe em aberto | `GeracaoRelatorioAgendada.frequencia` e `timezone` | `[PENDENTE]` na própria aba. | CL-097 `GeracaoRelatorioAgendada` | — |
| CP-110 | `[PENDENTE]` | Detalhe em aberto | `ExportacaoRelatorio.status` | Valores não definidos `[PENDENTE]`. | CL-096 `ExportacaoRelatorio` | — |
| CP-111 | `[PROPOSTO]` | Aguarda aprovação de ADR | `RelatorioEmpresarial.empresa` | Aponta para a `Empresa`, que é o cadastro do Tenant `[PROPOSTO]` ADR_158. | CL-094 `RelatorioEmpresarial`, CL-008 `Empresa` | ADR_158 |
| CP-112 | `[PENDENTE]` | Detalhe em aberto | Serviço | Nenhuma ADR diz em qual serviço fica o Relatório `[PENDENTE]`. | — | — |

### §13 Legado

| CP | Situação | O que falta | Ponto | Descrição | Elementos | ADRs |
|---|---|---|---|---|---|---|
| CP-113 | `[CONFLITO]` | Precisa de decisão do time | `Executavel` `<<substituida>>` | Pauta ING-06: a substituição de `Executavel` por `FonteTelemetria` e de `ExternalToken` por `CredencialIngestao` ficou "Alinhado", com a remoção do legado no DER. O DER v9 ainda traz `Executavel` e `ExternalToken` como `MOD_LEGADO` e a ligação com `FonteTelemetria` marcada `[INFERIDO]` `[CONFLITO]`. `FonteTelemetria` só existe no DER (campos do DER v9). | CL-113 `Executavel`, CL-114 `FonteTelemetria`, CL-101 `CredencialIngestao (SDK)` | — |

### DER v9 × ADRs

| CP | Situação | O que falta | Ponto | Descrição | Elementos | ADRs |
|---|---|---|---|---|---|---|
| CP-114 | `[CONFLITO]` | Atualizar DER ou planilha | `Ocorrencia` = resumo por Arquivo, com os contadores | DER v9: `Ocorrencia` = resumo por Arquivo, com os contadores. ADRs: Ocorrência concreta por erro/warning; o resumo é um agrupador à parte. | CL-066 `Ocorrencia` | ADR_035, ADR_040, ADR_062 |
| CP-115 | `[CONFLITO]` | Atualizar DER ou planilha | `AchadoAnalise` como entidade, com `gravidade`, `chaveAchado`, `vetorRef` | DER v9: `AchadoAnalise` como entidade, com `gravidade`, `chaveAchado`, `vetorRef`. ADRs: DTO sem coleção; gravidade no Módulo Ocorrência. | CL-060 `AchadoAnalise` | ADR_040, ADR_062 |
| CP-116 | `[CONFLITO]` | Atualizar DER ou planilha | `chaveIdempotencia = arquivoId` | DER v9: `chaveIdempotencia = arquivoId`. ADRs: `arquivoId + execId` no envio do `ResumoAnalise`. | CL-061 `ResumoAnalise` | ADR_065, ADR_070 |
| CP-117 | `[CONFLITO]` | Atualizar DER ou planilha | `RecorrenciaLog` (3 ou 4 arquivos seguidos) | DER v9: `RecorrenciaLog` (3 ou 4 arquivos seguidos). ADRs: flag `recorrente`; janela de 500 arquivos por Produto. | CL-059 `RecorrenciaLog` | ADR_063, ADR_074 |
| CP-118 | `[CONFLITO]` | Atualizar DER ou planilha | `TravaVarredura` | DER v9: `TravaVarredura`. ADRs: sem trava por Produto; chaves lock por arquivo com TTL. | CL-051 `TravaVarredura` | ADR_058, ADR_068, ADR_069, ADR_072 |
| CP-119 | `[CONFLITO]` | Atualizar DER ou planilha | Arquivo só com spam gera Ocorrência-resumo com achados vazios | DER v9: Arquivo só com spam gera Ocorrência-resumo com achados vazios. ADRs: spam não é armazenado nem vira Ocorrência. | — | ADR_066 |
| CP-120 | `[CONFLITO]` | Atualizar DER ou planilha | `Varredura.status`/`ArquivoVarredura.status` com `PENDING` | DER v9: `Varredura.status`/`ArquivoVarredura.status` com `PENDING`. ADRs: status do Arquivo = `PROCESSANDO`, `CONCLUIDO`, `FALHA`. | CL-044 `Varredura`, CL-046 `ArquivoVarredura` | ADR_099 |
| CP-121 | `[CONFLITO]` | Atualizar DER ou planilha | `Arquivo` sem `status` nem origem | DER v9: `Arquivo` sem `status` nem origem. ADRs: status (ADR_099) e origem (ADR_100). | CL-039 `Arquivo` | ADR_099, ADR_100 |
| CP-122 | `[CONFLITO]` | Atualizar DER ou planilha | `Sugestao` sem `motivoFalha`; `status` String | DER v9: `Sugestao` sem `motivoFalha`; `status` String. ADRs: `motivoFalha`; `PROCESSANDO`, `AGUARDANDO_REVISAO`, `FECHADA`, `FALHA`. | CL-068 `Sugestao` | ADR_077, ADR_096 |
| CP-123 | `[CONFLITO]` | Atualizar DER ou planilha | `Notificacao` sem `tipo` nem `sugestaoId` | DER v9: `Notificacao` sem `tipo` nem `sugestaoId`. ADRs: `tipo` e `sugestaoId` opcional. | CL-076 `Notificacao` | ADR_081 |
| CP-124 | `[CONFLITO]` | Atualizar DER ou planilha | `Plano.recursoIA` Boolean | DER v9: `Plano.recursoIA` Boolean. ADRs: `ProdutoRecursoIA` (`planoTemIA`, `produtoAtivouIA`). | CL-018 `Plano`, CL-021 `ProdutoRecursoIA` | ADR_076 |
| CP-125 | `[CONFLITO]` | Atualizar DER ou planilha | Bloco `EventoGateway` com `resultado`/`motivoFalha` | DER v9: Bloco `EventoGateway` com `resultado`/`motivoFalha`. ADRs: `EXECUTADO`/`FALHA` e erro (o texto do próprio DER v9 já diz isso). | CL-027 `EventoGateway` | ADR_125 |
| CP-126 | `[CONFLITO]` | Atualizar DER ou planilha | `PreferenciaNotificacao.severidadeMinima` | DER v9: `PreferenciaNotificacao.severidadeMinima`. ADRs: gravidade filtrada pela matriz de papéis. | CL-077 `PreferenciaNotificacao` | ADR_134, ADR_136 |
| CP-127 | `[CONFLITO]` | Atualizar DER ou planilha | Sem `ResumoAnalise`, `HistoricoVarredura`, coleção de lock, `ProdutoRecursoIA` | DER v9: Sem `ResumoAnalise`, `HistoricoVarredura`, coleção de lock, `ProdutoRecursoIA`. ADRs: as quatro existem nas ADRs. | CL-061 `ResumoAnalise`, CL-052 `HistoricoVarredura`, CL-021 `ProdutoRecursoIA` | ADR_058, ADR_060, ADR_062, ADR_076 |

### Pauta 03/10 × ADRs

| CP | Situação | O que falta | Ponto | Descrição | Elementos | ADRs |
|---|---|---|---|---|---|---|
| CP-128 | `[PROPOSTO]` | Aguarda aprovação de ADR | ING-02 | Pauta: `CredencialIngestao` do Coletor ligada à tabela de Tenant. ADR posterior: ADR_111 mantém a tabela; ADR_122 a representa por `Produtor` + `TokenApi` (marcado `[INFERIDO]` na ADR). No diagrama: `[PROPOSTO]` ADR_155: só a substituição por `TokenApi`. | CL-043 `CredencialIngestao`, CL-042 `TokenApi`, CL-041 `Produtor` | ADR_111, ADR_122, ADR_155 |
| CP-129 | `[CONFLITO]` | Atualizar DER ou planilha | VAR-03 | Pauta: coleção `TravaVarredura`, escopo global. ADR posterior: ADR_058/068/069: sem trava por Produto, chaves lock por arquivo. No diagrama: `TravaVarredura` da planilha, marcada `[CONFLITO]`. | CL-051 `TravaVarredura` | ADR_058, ADR_068, ADR_069 |
| CP-130 | `[CONFLITO]` | Atualizar DER ou planilha | FIN-07 | Pauta: `ClassificadorAnalise` registra a `gravidade`. ADR posterior: ADR_062: gravidade no Módulo Ocorrência; o Finder não sabe de criticidade. No diagrama: ADR_062 (gravidade só na `Ocorrencia`). | CL-062 `ClassificadorAnalise`, CL-066 `Ocorrencia` | ADR_062 |
| CP-131 | `[CONFLITO]` | Atualizar DER ou planilha | SUG-04 | Pauta: item `SUGESTAO` no enum `RecursosAnaliseIA`. ADR posterior: ADR_076: `ProdutoRecursoIA` com `planoTemIA`. No diagrama: os dois. | ES-03 `RecursosAnaliseIA`, CL-021 `ProdutoRecursoIA` | ADR_076 |
| CP-132 | `[PENDENTE]` | Detalhe em aberto | NOT-02 | Pauta: `tipo` com `FALHA_SUGESTAO`, enviado por PUSH e WEB. ADR posterior: ADR_081: dois tipos, falha manual `[PENDENTE]`; ADR_086: falha manual só por WebSocket. No diagrama: valores da ADR_081. | — | ADR_081, ADR_086 |
| CP-133 | `[CONFLITO]` | Atualizar DER ou planilha | ING-05 | Pauta: `AchadoAnalise` sempre com 1 Trace. ADR posterior: (nenhuma ADR) — o DER v9 e a planilha aceitam `traceId` nulo. No diagrama: pauta. | CL-060 `AchadoAnalise` | — |

### ADR nova (17/10)

| CP | Situação | O que falta | Ponto | Descrição | Elementos | ADRs |
|---|---|---|---|---|---|---|
| CP-134 | `[PROPOSTO]` | Aguarda aprovação de ADR | ADR_149 — Asaas como gateway de pagamento (proposta, LLT-89) | Proposta criada em 17/10, ainda não aplicada ao diagrama. Afeta o módulo 3: `GatewayPagamento` ganha `alterarAssinatura`, `cancelarAssinatura` e `configurarNotaFiscal`; `ApiPagamento.webhookSecret`; `Pagamento.chaveIdempotencia` (externalReference); `Assinatura.diasCarencia` = 15 e status ATIVA, PENDENTE, INADIMPLENTE, SUSPENSA, CANCELAMENTO_AGENDADO e CANCELADA; `TipoOperacaoGateway` sem RENOVACAO, RECUSA, CHARGEBACK e NOTA_FISCAL `[PENDENTE]`. O número 149 também foi usado para "Log padrão de inicialização". | CL-023 `GatewayPagamento`, CL-024 `ApiPagamento`, CL-025 `Pagamento`, CL-020 `Assinatura`, ES-06 `StatusAssinatura`, ES-09 `TipoOperacaoGateway`, CL-027 `EventoGateway`, CL-017 `GerenciadorAssinatura` | ADR_149 |

## 7. Matriz de classes

| ID | Classe | Tipo | § | Base | Responsabilidade | Requisitos | ADRs | Situação | Pendências | Isolamento | Impacto |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CL-001 | `Tenant` | classe | §1 | ADR_121/122; DER v9 | Empresa cliente; espelha a Organization da Clerk (`clerkOrgId`). Todo dado leva `tenantId`. | SSID_017, SSID_002 (inferido), SSID_010 (inferido), USID_040 (inferido) | ADR_030, ADR_105, ADR_121, ADR_122, ADR_123, ADR_137, ADR_158 | `[PROPOSTO]` | CP-01 [PENDENTE], CP-06 [PROPOSTO], CP-15 [PROPOSTO] | tenantId próprio (ADR_121) | Alto (8 rel.) |
| CL-002 | `Membro` | classe | §1 | ADR_122/123; DER v9 | Pessoa de um Tenant, com papel DONO, ADMIN ou MEMBRO; a identidade fica na Clerk. | USID_029, USID_048, USID_049 (inferido), USID_050 (inferido), USID_051 (inferido), SSID_017 | ADR_122, ADR_123, ADR_132, ADR_135, ADR_159 | `[PROPOSTO]` | CP-01 [PENDENTE], CP-02 [PENDENTE], CP-07 [PROPOSTO], CP-09 [PENDENTE], CP-11 [PENDENTE], CP-82 [PROPOSTO], CP-92 [PROPOSTO], CP-96 [PROPOSTO] | tenantId próprio (ADR_121) | Alto (11 rel.) |
| CL-003 | `AcessoProduto` | classe | §1 | ADR_122; DER v9 | Quais Produtos um MEMBRO vê (DONO e ADMIN veem todos). | USID_030 | ADR_032, ADR_122, ADR_126 | `[CONFIRMADO]` | CP-07 [PROPOSTO], CP-09 [PENDENTE], CP-12 [PENDENTE] | via Produto | Médio (2 rel.) |
| CL-004 | `Produto` | classe | §1 | aba Produto | Cadastro dos sistemas (Produtos) de cada empresa. | USID_024, USID_015, USID_016, USID_023 | ADR_030, ADR_122, ADR_129 | `[PENDENTE]` | CP-03 [PENDENTE], CP-04 [PROPOSTO], CP-06 [PROPOSTO] | tenantId próprio (ADR_121) | Alto (21 rel.) |
| CL-005 | `ContextoProduto` | classe | §1 | aba ContextoProduto | Informações descritivas de cada Produto, combinadas com o contexto da empresa. | USID_023, SSID_015 | ADR_039 | `[CONFIRMADO]` | — | via Produto | Médio (3 rel.) |
| CL-006 | `ConfiguracaoProduto` | classe | §1 | aba ConfiguracaoProduto | Parâmetros (chave/valor) que definem se o Produto pode ser ativado. | USID_024, USID_027 (inferido) | ADR_122 | `[CONFIRMADO]` | — | via Produto | Baixo (1 rel.) |
| CL-007 | `ContextoEmpresa` | classe | §1 | aba Contexto Empresa | Contexto empresarial enviado à IA. | USID_022, SSID_015 | ADR_039, ADR_158 | `[PROPOSTO]` | CP-04 [PROPOSTO], CP-06 [PROPOSTO] | — | Alto (6 rel.) |
| CL-008 | `Empresa` | classe | §1 | aba Empresa; ADR_158 (proposta) | Cadastro da empresa cliente (CNPJ, razão social etc.), 1:1 com o Tenant. | USID_021 | ADR_121, ADR_158 | `[CONFLITO]` | CP-04 [PROPOSTO], CP-05 [CONFLITO], CP-06 [PROPOSTO], CP-15 [PROPOSTO], CP-107 [PROPOSTO], CP-111 [PROPOSTO] | via Tenant | Alto (6 rel.) |
| CL-009 | `Endereco` | classe | §1 | aba Endereco | Endereços da empresa (sede, filiais, cobrança) para o faturamento. | USID_021 (inferido) | — | `[CONFLITO]` | CP-05 [CONFLITO], CP-06 [PROPOSTO] | — | Alto (2 rel.) |
| CL-010 | `Usuario` | substituída | §1 | DER v9 (substituída) | Substituída pelo `Membro` (identidade na Clerk). | USID_048, USID_049, USID_051, SSID_017 | ADR_021, ADR_022, ADR_030, ADR_122, ADR_123, ADR_159 | `[SUBSTITUÍDA]` | CP-04 [PROPOSTO], CP-07 [PROPOSTO], CP-82 [PROPOSTO], CP-92 [PROPOSTO] | via Membro | Baixo (1 rel.) |
| CL-011 | `Gestor` | substituída | §1 | aba Gestor (substituída) | Substituída pelo `Membro`. | USID_029, USID_030 | ADR_003, ADR_021, ADR_030, ADR_122, ADR_123, ADR_159 | `[SUBSTITUÍDA]` | CP-07 [PROPOSTO] | via Membro | Baixo (1 rel.) |
| CL-012 | `Vinculo` | substituída | §1 | aba Vinculo (substituída) | Substituída pelo `Membro`. | USID_029, USID_030 | ADR_003, ADR_021, ADR_122, ADR_123, ADR_159 | `[SUBSTITUÍDA]` | CP-07 [PROPOSTO] | via Membro | Baixo (1 rel.) |
| CL-013 | `Acesso` | substituída | §1 | aba Acesso (substituída) | Substituída pelo `Membro` e pela Clerk. | USID_030, USID_049 | ADR_021, ADR_030, ADR_122, ADR_123, ADR_159 | `[SUBSTITUÍDA]` | CP-07 [PROPOSTO] | via Membro | Baixo (1 rel.) |
| CL-014 | `PapelNotificacao` | classe | §2 | ADR_130, 134, 136 a 140, 142; DER v9 | Papel de notificação do Tenant: define quem recebe quais alertas. | USID_012 (inferido), SSID_009 (inferido), SSID_019 (inferido) | ADR_130, ADR_131, ADR_132, ADR_133, ADR_134, ADR_135, ADR_136, ADR_137, ADR_138, ADR_139, ADR_140, ADR_141, ADR_142 | `[CONFIRMADO]` | — | tenantId próprio (ADR_121) | Médio (4 rel.) |
| CL-015 | `PapelSeveridade` | classe | §2 | ADR_134/142; DER v9 | Gravidades que um papel de notificação recebe. | USID_012 (inferido), SSID_009 (inferido) | ADR_134, ADR_142 | `[CONFIRMADO]` | — | tenantId próprio (ADR_121) | Baixo (1 rel.) |
| CL-016 | `PapelTipoAlerta` | classe | §2 | ADR_134/142; DER v9 | Tipos de alerta que um papel de notificação recebe. | USID_012 (inferido), SSID_009 (inferido) | ADR_134, ADR_142 | `[CONFIRMADO]` | — | tenantId próprio (ADR_121) | Baixo (1 rel.) |
| CL-017 | `GerenciadorAssinatura` | classe | §3 | aba Gerenciador Assinatura | Orquestra contratação, alteração, cancelamento, reembolso e inadimplência. | USID_039, USID_040, USID_041, USID_042, USID_043, SSID_016 | ADR_030, ADR_149 | `[CONFIRMADO]` | CP-134 [PROPOSTO] | — | Alto (7 rel.) |
| CL-018 | `Plano` | classe | §3 | aba Plano | Catálogo de planos: nome, armazenamento, retenção, recursos de IA, dashboard e preço. | USID_039, USID_040, USID_041, USID_008, USID_044 (inferido) | ADR_030, ADR_036 | `[CONFLITO]` | CP-20 [A CONFERIR], CP-23 [PENDENTE], CP-33 [CONFLITO], CP-34 [CONFLITO], CP-124 [CONFLITO] | — | Alto (7 rel.) |
| CL-019 | `TabelaPrecificacao` | classe | §3 | ADR_127/131 | Preços e limites de cada plano. | USID_039 | ADR_127, ADR_131 | `[PENDENTE]` | CP-22 [PENDENTE], CP-23 [PENDENTE] | via Produto | Médio (1 rel.) |
| CL-020 | `Assinatura` | classe | §3 | aba Assinatura | Assinatura contratada por uma empresa: plano, status, vigência e carência. | USID_040, USID_041, USID_042, USID_043, SSID_016, SSID_018 | ADR_030, ADR_104, ADR_122, ADR_124, ADR_149 | `[PROPOSTO]` | CP-09 [PENDENTE], CP-16 [PENDENTE], CP-134 [PROPOSTO] | tenantId próprio (ADR_121) | Alto (6 rel.) |
| CL-021 | `ProdutoRecursoIA` | classe | §3 | ADR_076 | Liga plano e Produto ao recurso de IA (`planoTemIA`, `produtoAtivouIA`). | USID_044 (inferido), USID_039 (inferido) | ADR_076 | `[CONFLITO]` | CP-19 [CONFLITO], CP-21 [CONFLITO], CP-124 [CONFLITO], CP-127 [CONFLITO], CP-131 [CONFLITO] | via Produto | Alto (3 rel.) |
| CL-022 | `ProcessamentoPagamento` | classe | §3 | aba Processamento Pagamento | Orquestra o processamento das cobranças e atualiza a assinatura conforme o resultado. | SSID_016, SSID_018, USID_040 | — | `[CONFIRMADO]` | — | — | Médio (4 rel.) |
| CL-023 | `GatewayPagamento` | interface | §3 | aba Gateway Pagamento | Contrato de integração com o gateway de pagamento externo. | SSID_018, USID_039 | ADR_149 | `[PROPOSTO]` | CP-134 [PROPOSTO] | — | Médio (2 rel.) |
| CL-024 | `ApiPagamento` | classe | §3 | aba Api Pagamento | Integrador com o gateway externo (cobranças, transações, autenticidade). | SSID_018 | ADR_149 | `[PROPOSTO]` | CP-134 [PROPOSTO] | — | Médio (2 rel.) |
| CL-025 | `Pagamento` | classe | §3 | aba Pagamento | Histórico de cada cobrança processada. | SSID_018, USID_040, USID_043 | ADR_149 | `[PROPOSTO]` | CP-134 [PROPOSTO] | — | Médio (4 rel.) |
| CL-026 | `Reembolso` | classe | §3 | aba Reembolso | Solicitações de reembolso. | USID_043 | — | `[A CONFERIR]` | CP-28 [A CONFERIR] | — | Médio (4 rel.) |
| CL-027 | `EventoGateway` | classe | §3 | aba Evento Gateway | Evento bruto do gateway, traduzido para as regras internas. | SSID_016, SSID_018 | ADR_125, ADR_149 | `[CONFLITO]` | CP-25 [CONFLITO], CP-26 [A CONFERIR], CP-125 [CONFLITO], CP-134 [PROPOSTO] | via Tenant | Alto (8 rel.) |
| CL-028 | `Credito` | classe | §4 | aba Credito | Créditos (tokens) usados pela empresa. | USID_044 (inferido), SSID_020 | ADR_038 | `[A CONFERIR]` | CP-35 [A CONFERIR], CP-40 [PROPOSTO] | via Produto | Alto (5 rel.) |
| CL-029 | `PlanoCreditos` | classe | §4 | aba Cópia de Modelo Padrão (classe "Plano") | Plano de créditos: valor, periodicidade e créditos concedidos a cada ciclo. | — | — | `[CONFLITO]` | CP-33 [CONFLITO] | — | Médio (1 rel.) |
| CL-030 | `Saldo` | classe | §4 | aba Saldo | Consolida os créditos disponíveis do cliente; recebe a reserva e a liquidação da Sugestão. | USID_044 (inferido), SSID_020 | ADR_038, ADR_078, ADR_098, ADR_117, ADR_157 | `[CONFIRMADO]` | CP-30 [PROPOSTO], CP-87 [PROPOSTO], CP-88 [PROPOSTO] | — | Médio (3 rel.) |
| CL-031 | `Transacao` | classe | §4 | aba Transação | Extrato auditável das movimentações de créditos. | SSID_020 | ADR_038 | `[CONFIRMADO]` | — | via Produto | Alto (7 rel.) |
| CL-032 | `Controle` | classe | §4 | aba Controle | Controle do gasto de tokens e da assinatura do plano contratado. | SSID_020 | ADR_038 | `[CONFLITO]` | CP-34 [CONFLITO] | via Produto | Alto (5 rel.) |
| CL-033 | `Coletor` | classe | §5 | aba Coletor | Recebe a ingestão e coordena validação, lote e envio à fila. | SSID_001, SSID_002, SSID_003, USID_006 (inferido) | ADR_007, ADR_015 | `[CONFIRMADO]` | — | — | Alto (6 rel.) |
| CL-034 | `GerenciadorRequisicao` | classe | §5 | aba GerenciadorRequisicao | A requisição que chega ao Coletor, com o token Bearer do Produtor (`TokenApi`). | SSID_001, SSID_014, USID_016 | ADR_113, ADR_117, ADR_155 | `[PROPOSTO]` | CP-40 [PROPOSTO] | via Produto | Médio (3 rel.) |
| CL-035 | `LogRecebido` | classe | §5 | aba LogRecebido | Log que já passou pela entrada do Coletor. | SSID_002 | ADR_116, ADR_121 | `[CONFIRMADO]` | — | via Produto | Médio (3 rel.) |
| CL-036 | `GerenciadorLote` | classe | §5 | aba GerenciadorLote | Regras de formação dos lotes. | SSID_002 | — | `[CONFIRMADO]` | CP-47 [A CONFERIR] | — | Médio (3 rel.) |
| CL-037 | `LoteAgrupador` | classe | §5 | aba LoteAgrupador | Conjunto de logs agrupados para persistência e processamento. | SSID_002 | — | `[CONFIRMADO]` | CP-47 [A CONFERIR] | via Produto | Médio (2 rel.) |
| CL-038 | `EnfileiradorLogs` | classe | §5 | aba EnfileiradorLogs | Envia os trabalhos à fila. | SSID_003 | — | `[CONFIRMADO]` | CP-47 [A CONFERIR] | — | Médio (2 rel.) |
| CL-039 | `Arquivo` | classe | §5 | aba Arquivo v2 | Pacote de traces e logs gravado pelo Coletor; unidade da fila (também o arquivo do upload manual). | USID_006, USID_007, USID_008 (inferido), SSID_003, SSID_004, SSID_013 | ADR_007, ADR_014, ADR_015, ADR_035, ADR_044, ADR_099, ADR_100 | `[CONFLITO]` | CP-41 [PENDENTE], CP-42 [PENDENTE], CP-43 [CONFLITO], CP-55 [CONFLITO], CP-121 [CONFLITO] | via Produto | Alto (9 rel.) |
| CL-040 | `Trace` | classe | §5 | aba Trace (v2) | Trace OpenTelemetry de um Arquivo: módulos por onde passou e prioridade efetiva. | — | ADR_009, ADR_013, ADR_014, ADR_015 | `[CONFIRMADO]` | CP-43 [CONFLITO], CP-65 [CONFLITO] | — | Médio (4 rel.) |
| CL-041 | `Produtor` | classe | §5 | ADR_122; DER v9 | Máquina de um Produto que envia telemetria ao Coletor. | USID_016, SSID_014, SSID_001 | ADR_106, ADR_107, ADR_109, ADR_113, ADR_115, ADR_122 | `[PENDENTE]` | CP-37 [PENDENTE], CP-40 [PROPOSTO], CP-128 [PROPOSTO] | tenantId próprio (ADR_121) | Médio (3 rel.) |
| CL-042 | `TokenApi` | classe | §5 | ADR_106/113/122; DER v9 | Token Bearer do Produtor: cifrado (AES-256-GCM), com índice SHA-256 para a busca. | USID_016, SSID_014, SSID_001 | ADR_106, ADR_107, ADR_109, ADR_113, ADR_115, ADR_122, ADR_155 | `[PROPOSTO]` | CP-37 [PENDENTE], CP-39 [PROPOSTO], CP-40 [PROPOSTO], CP-128 [PROPOSTO] | — | Médio (3 rel.) |
| CL-043 | `CredencialIngestao` | substituída | §5 | DER v9 (substituída) | Tabela de credencial do servidor; substituída pelo `TokenApi`. | USID_016, SSID_014 | ADR_025, ADR_028, ADR_111, ADR_122, ADR_155 | `[SUBSTITUÍDA]` | CP-39 [PROPOSTO], CP-128 [PROPOSTO] | — | Médio (1 rel.) |
| CL-044 | `Varredura` | classe | §6 | aba Varredura v2 | Uma execução de varredura: corte da fila desordenada, priorização e publicação da fila ordenada. | SSID_005, SSID_006, USID_025, SSID_004 (inferido) | ADR_004, ADR_007, ADR_010 | `[CONFLITO]` | CP-120 [CONFLITO] | via Produto | Alto (12 rel.) |
| CL-045 | `VarreduraResumo` | record | §6 | aba Varredura v2 (tipo de retorno) | Retorno de `getResume()` com os contadores da Varredura. | — | — | `[CONFIRMADO]` | CP-59 [A CONFERIR] | — | Médio (2 rel.) |
| CL-046 | `ArquivoVarredura` | classe | §6 | aba ArquivoVarredura v2 | Controle de um Arquivo dentro de uma Varredura (ordem, status, tentativas, erro). | SSID_004, USID_007 | ADR_014, ADR_099 | `[CONFLITO]` | CP-55 [CONFLITO], CP-120 [CONFLITO] | — | Alto (6 rel.) |
| CL-047 | `AgendamentoVarredura` | classe | §6 | aba AgendamentoVarredura v2 | Agendamento por expressão cron que dispara uma nova Varredura a cada execução. | USID_026, SSID_006, SSID_012 | ADR_006, ADR_010 | `[CONFIRMADO]` | CP-61 [CONFLITO] | via Produto | Médio (3 rel.) |
| CL-048 | `Modulo` | classe | §6 | aba Modulo (v2) | Serviço do cliente identificado pelo service.name, com prioridade configurável. | — | ADR_008, ADR_009 | `[CONFIRMADO]` | — | via Produto | Médio (4 rel.) |
| CL-049 | `FilaDesordenada` | classe | §6 | aba FilaDesordenada (v2) | Fila onde o Coletor grava os Arquivos pendentes. | SSID_003 | ADR_007, ADR_010, ADR_014 | `[CONFIRMADO]` | CP-47 [A CONFERIR], CP-48 [CONFLITO], CP-58 [CONFLITO], CP-60 [CONFLITO] | via Produto | Médio (3 rel.) |
| CL-050 | `FilaOrdenada` | classe | §6 | aba FilaOrdenada (v2) | Fila priorizada publicada pela Varredura e consumida pelo Finder. | — | ADR_007, ADR_011 | `[CONFIRMADO]` | CP-46 [PENDENTE], CP-54 [PENDENTE], CP-60 [CONFLITO] | — | Médio (3 rel.) |
| CL-051 | `TravaVarredura` | classe | §6 | aba TravaVarredura (v2) | Trava que impede duas varreduras ao mesmo tempo. | USID_025 | ADR_010, ADR_058, ADR_068, ADR_069, ADR_070, ADR_072 | `[CONFLITO]` | CP-49 [CONFLITO], CP-118 [CONFLITO], CP-129 [CONFLITO] | via Produto | Médio (1 rel.) |
| CL-052 | `HistoricoVarredura` | classe | §6 | ADR_060; DER v9 | Histórico das execuções de varredura. | SSID_006 (inferido), USID_026 (inferido) | ADR_060, ADR_071, ADR_147 | `[CONFLITO]` | CP-53 [PENDENTE], CP-127 [CONFLITO] | via Produto | Médio (1 rel.) |
| CL-053 | `Finder` | classe | §7 | aba Finder v2 | Orquestra a análise de cada Arquivo e envia o `ResumoAnalise` ao Módulo Ocorrência. | SSID_007, SSID_008 (inferido), SSID_013 | ADR_062, ADR_161 | `[PROPOSTO]` | CP-62 [PROPOSTO] | — | Alto (9 rel.) |
| CL-054 | `ContextoAnalise` | classe | §7 | aba ContextoAnalise | Contexto da análise: empresa, produto, arquivo, varredura e varredura avançada. | SSID_008, USID_027 | ADR_011 | `[CONFIRMADO]` | — | via Produto | Médio (2 rel.) |
| CL-055 | `LogNormalizado` | classe | §7 | aba LogNormalizado | Formato universal dos logs para o Finder (TXT, LOG, JSON, CSV). | SSID_007, USID_006 (inferido) | ADR_016 | `[CONFIRMADO]` | — | — | Médio (2 rel.) |
| CL-056 | `MotorAnalise` | classe | §7 | aba MotorAnalise v2 | Analisa o LogNormalizado com a LLM do Finder e verifica recorrência. | SSID_007, SSID_020 | ADR_011, ADR_016, ADR_017, ADR_018 | `[PENDENTE]` | CP-66 [PENDENTE], CP-69 [PENDENTE] | — | Alto (7 rel.) |
| CL-057 | `GatewayLLMFinder` | interface | §7 | aba GatewayLLM (Interface), renomeada pela ADR_067 | Contrato da LLM usada pelo Finder. | SSID_007, SSID_020 | ADR_018, ADR_067, ADR_080 | `[CONFIRMADO]` | — | — | Baixo (1 rel.) |
| CL-058 | `BancoVetorial` | interface | §7 | aba BancoVetorial (v2) | Contrato do banco vetorial para saber se um erro/alerta já existiu. | — | ADR_062, ADR_074, ADR_152 | `[CONFLITO]` | CP-66 [PENDENTE], CP-67 [CONFLITO], CP-68 [CONFLITO] | — | Médio (1 rel.) |
| CL-059 | `RecorrenciaLog` | classe | §7 | aba RecorrenciaLog (v2) | Controle da regra de recorrência: mesmo log, mesma máquina, Arquivos seguidos. | — | ADR_013, ADR_063 | `[CONFLITO]` | CP-67 [CONFLITO], CP-117 [CONFLITO] | — | Médio (1 rel.) |
| CL-060 | `AchadoAnalise` | DTO | §7 | aba AchadoAnalise + adições v2; ADR_040 | DTO do que o MotorAnalise encontrou; vira Ocorrência concreta. | SSID_007 | ADR_017, ADR_020, ADR_040, ADR_062, ADR_063 | `[CONFLITO]` | CP-63 [CONFLITO], CP-65 [CONFLITO], CP-115 [CONFLITO], CP-133 [CONFLITO] | — | Alto (7 rel.) |
| CL-061 | `ResumoAnalise` | classe | §7 | ADR_062 | Saída do Finder por Arquivo: contadores e achados, enviada ao Módulo Ocorrência. | SSID_007, SSID_009 | ADR_062, ADR_070, ADR_102 | `[CONFLITO]` | CP-62 [PROPOSTO], CP-73 [PROPOSTO], CP-74 [PENDENTE], CP-79 [PROPOSTO], CP-116 [CONFLITO], CP-127 [CONFLITO] | — | Alto (3 rel.) |
| CL-062 | `ClassificadorAnalise` | classe | §7 | aba ClassificadorAnalise v2 | Aplica as regras de negócio e classifica cada achado com o enum Tipo. | SSID_007 | ADR_012, ADR_017, ADR_019 | `[CONFLITO]` | CP-64 [CONFLITO], CP-77 [CONFLITO], CP-130 [CONFLITO] | — | Alto (4 rel.) |
| CL-063 | `ScannerSeguranca` | classe | §7 | aba ScannerSegurança | Varredura avançada: detecta dados sensíveis e aplica máscara antes da LLM. | SSID_008, USID_027 | ADR_016 | `[CONFIRMADO]` | — | — | Médio (2 rel.) |
| CL-064 | `ModuloOcorrencia` | classe | §8 | aba ModuloOcorrencia (v2); ADR_036/062 | Recebe o `ResumoAnalise`, define a gravidade, cria as Ocorrências e dispara a Sugestão automática. | SSID_009, SSID_010, USID_044 (inferido) | ADR_036, ADR_038, ADR_039, ADR_040, ADR_062, ADR_161 | `[PROPOSTO]` | CP-78 [PROPOSTO], CP-79 [PROPOSTO], CP-88 [PROPOSTO] | — | Alto (9 rel.) |
| CL-065 | `ResumoArquivo` | classe | §8 | aba Ocorrencia v2, renomeada pela ADR_160 (proposta); ADR_035/040 | Resumo por Arquivo: contadores e ids das Ocorrências do Arquivo. | USID_007, SSID_004 | ADR_019, ADR_035, ADR_040, ADR_062, ADR_063, ADR_160 | `[PROPOSTO]` | CP-72 [PROPOSTO], CP-73 [PROPOSTO] | via registro pai | Médio (3 rel.) |
| CL-066 | `Ocorrencia` | classe | §8 | ADR_035/040 (as abas Ocorrencia e Ocorrencia v2 descrevem o resumo) | Ocorrência concreta: um erro ou warning de um Arquivo. | USID_001, USID_002, USID_003, USID_004, USID_005, USID_037, SSID_007, SSID_009, SSID_010 | ADR_035, ADR_040, ADR_062, ADR_082, ADR_089, ADR_090, ADR_091, ADR_096 | `[CONFLITO]` | CP-62 [PROPOSTO], CP-64 [CONFLITO], CP-72 [PROPOSTO], CP-73 [PROPOSTO], CP-76 [PENDENTE], CP-77 [CONFLITO], CP-114 [CONFLITO], CP-130 [CONFLITO] | tenantId próprio (ADR_121) | Alto (9 rel.) |
| CL-067 | `Mapper` | classe | §8 | pauta FIN-09; ADR_040/062 | Converte cada `AchadoAnalise` em `Ocorrencia`. | SSID_010 | ADR_040, ADR_062, ADR_161 | `[PROPOSTO]` | CP-79 [PROPOSTO] | — | Médio (3 rel.) |
| CL-068 | `Sugestao` | classe | §9 | aba Sugestão; ADR_036/037 | Sugestão de correção gerada pela IA para uma Ocorrência. | USID_044, USID_045, USID_046, USID_047, USID_028 | ADR_035, ADR_036, ADR_037, ADR_038, ADR_039, ADR_040, ADR_088 | `[CONFLITO]` | CP-83 [CONFLITO], CP-88 [PROPOSTO], CP-122 [CONFLITO] | via registro pai | Alto (7 rel.) |
| CL-069 | `AvaliacaoSugestao` | classe | §9 | ADR_039/088; DER v9 | Avaliação de 1 a 5 estrelas, com comentário, feita por um Membro. | USID_046 | ADR_039, ADR_088, ADR_159 | `[PROPOSTO]` | CP-07 [PROPOSTO], CP-82 [PROPOSTO], CP-83 [CONFLITO] | via Membro | Médio (2 rel.) |
| CL-070 | `ContextoSugestao` | classe | §9 | aba ContextoSugestao | Monta o prompt da Sugestão com o contexto da empresa e do produto. | SSID_015, USID_044 | ADR_039 | `[CONFIRMADO]` | CP-84 [PENDENTE], CP-88 [PROPOSTO] | via Produto | Médio (4 rel.) |
| CL-071 | `GatewayLLMSugestao` | interface | §9 | aba GatewayLLM (Interface), renomeada pela ADR_039 | Contrato de comunicação com o provedor de LLM da Sugestão. | SSID_020 | ADR_018, ADR_039, ADR_080 | `[PENDENTE]` | CP-85 [PENDENTE], CP-86 [PENDENTE], CP-88 [PROPOSTO] | — | Médio (4 rel.) |
| CL-072 | `GatewayLLMPadrao` | classe | §9 | aba GatewayLLMPadrao | Implementa a chamada ao provedor de LLM configurado. | SSID_020 | ADR_039 | `[CONFIRMADO]` | CP-85 [PENDENTE] | — | Médio (2 rel.) |
| CL-073 | `RespostaLLM` | classe | §9 | aba RespostaLLM | Retorno bruto da LLM: texto gerado e tokens consumidos. | SSID_020 | ADR_038 | `[CONFIRMADO]` | — | — | Médio (2 rel.) |
| CL-074 | `ChaveLLMTenant` | classe | §9 | DER v9 | Chave de LLM do próprio cliente (BYOK). | SSID_020 | ADR_080, ADR_128 | `[PENDENTE]` | CP-86 [PENDENTE] | tenantId próprio (ADR_121) | Médio (2 rel.) |
| CL-075 | `ModuloSugestao` | classe | §9 | ADR_156 (proposta); ADR_036/038/039 | Orquestra a Sugestão: monta o prompt, reserva os créditos e chama a LLM. | USID_044, SSID_015, SSID_020 | ADR_036, ADR_038, ADR_039, ADR_156 | `[PROPOSTO]` | CP-30 [PROPOSTO], CP-78 [PROPOSTO], CP-88 [PROPOSTO] | — | Alto (5 rel.) |
| CL-076 | `Notificacao` | classe | §10 | aba Notificação | Notificação individual enviada a um usuário por um canal, com leitura. | USID_009, USID_010, USID_011, USID_013, USID_014, SSID_019, SSID_009 | ADR_036, ADR_037, ADR_081, ADR_086 | `[CONFLITO]` | CP-89 [CONFLITO], CP-92 [PROPOSTO], CP-99 [CONFLITO], CP-123 [CONFLITO] | via Membro | Alto (10 rel.) |
| CL-077 | `PreferenciaNotificacao` | classe | §10 | aba PreferenciaNotificacao | Canais habilitados por usuário e dados de contato. | USID_012, USID_009, USID_010, USID_011 | ADR_134, ADR_159 | `[CONFLITO]` | CP-92 [PROPOSTO], CP-96 [PROPOSTO], CP-97 [CONFLITO], CP-126 [CONFLITO] | via Membro | Alto (2 rel.) |
| CL-078 | `GatewayNotificacao` | interface | §10 | aba GatewayNotificacao (Interface) | Contrato único de envio que todo canal implementa. | SSID_019 | — | `[CONFIRMADO]` | — | — | Alto (6 rel.) |
| CL-079 | `GatewayNotificacaoFactory` | classe | §10 | aba GatewayNotificacaoFactory | Devolve o enviador certo pelo canal da Notificação. | SSID_019 | — | `[CONFIRMADO]` | — | — | Médio (2 rel.) |
| CL-080 | `EnviadorEmail` | classe | §10 | aba EnviadorEmail | Envio por e-mail. | USID_009 | — | `[CONFIRMADO]` | — | — | Médio (3 rel.) |
| CL-081 | `EnviadorPush` | classe | §10 | aba EnviadorPush | Envio push pelo token do dispositivo. | USID_010, USID_014 | ADR_025 | `[CONFIRMADO]` | — | — | Médio (4 rel.) |
| CL-082 | `EnviadorWeb` | classe | §10 | aba EnviadorWeb | Envio web em tempo real (WebSocket). | USID_011, USID_013 | ADR_141 | `[CONFLITO]` | CP-94 [CONFLITO] | — | Alto (3 rel.) |
| CL-083 | `DispositivoPush` | classe | §10 | aba DispositivoPush | Token de push e plataforma do dispositivo do usuário. | USID_010 | ADR_025 | `[CONFIRMADO]` | CP-92 [PROPOSTO] | via Membro | Médio (3 rel.) |
| CL-084 | `TentativaEntrega` | classe | §10 | aba TentativaEntrega | Uma tentativa de entrega da notificação (status, data, motivo da falha). | USID_009, USID_010, USID_011, SSID_009 (inferido) | — | `[CONFIRMADO]` | CP-98 [CONFLITO], CP-99 [CONFLITO] | — | Médio (3 rel.) |
| CL-085 | `Metrica` | classe | §11 | aba Métrica | Resultado de uma métrica dos dashboards. | USID_031, USID_034 | — | `[CONFIRMADO]` | CP-103 [PROPOSTO] | — | Alto (8 rel.) |
| CL-086 | `Periodo` | classe | §11 | aba Período | Intervalo de tempo de consultas, filtros e consolidações. | USID_032, USID_036, SSID_011 | — | `[A CONFERIR]` | CP-102 [A CONFERIR] | — | Alto (8 rel.) |
| CL-087 | `FiltroDashboard` | classe | §11 | aba FiltroDashboard | Critérios para limitar dados e métricas do Dashboard. | USID_032, USID_036 | — | `[CONFIRMADO]` | — | via Produto | Alto (6 rel.) |
| CL-088 | `DashboardProduto` | classe | §11 | aba DashboardProduto | Visão de dados e métricas de um Produto. | USID_031, USID_032 | — | `[A CONFERIR]` | CP-101 [A CONFERIR] | via Produto | Alto (5 rel.) |
| CL-089 | `DashboardEmpresarial` | classe | §11 | aba DashboardEmpresarial | Visão consolidada dos Produtos autorizados da empresa. | USID_034, USID_036 | — | `[CONFIRMADO]` | CP-06 [PROPOSTO], CP-107 [PROPOSTO] | via Produto | Alto (6 rel.) |
| CL-090 | `FiltroOcorrenciaEmpresarial` | classe | §11 | aba FiltroOcorrenciaEmpresarial | Critérios para consultar ocorrências de vários Produtos. | USID_037 | ADR_162 | `[PROPOSTO]` | CP-103 [PROPOSTO] | via Produto | Médio (3 rel.) |
| CL-091 | `ResumoDashboardMobile` | classe | §11 | aba ResumoDashboardMobile | Resumo do Dashboard para dispositivos móveis. | USID_038 | ADR_025 | `[CONFIRMADO]` | — | via Produto | Médio (3 rel.) |
| CL-092 | `Agregacao` | classe | §11 | aba Agregação | Consolida resultados de métricas para dashboards e relatórios. | USID_034, SSID_011 | — | `[PENDENTE]` | CP-103 [PROPOSTO], CP-104 [PENDENTE] | — | Médio (3 rel.) |
| CL-093 | `RelatorioDashboard` | classe | §12 | aba RelatorioDashboard | Dados do Dashboard preparados para um relatório exportável. | USID_033 | — | `[CONFIRMADO]` | — | via Produto | Alto (6 rel.) |
| CL-094 | `RelatorioEmpresarial` | classe | §12 | aba RelatorioEmpresarial | Dados consolidados do relatório empresarial. | USID_035 | ADR_158 | `[PROPOSTO]` | CP-06 [PROPOSTO], CP-111 [PROPOSTO] | via Produto | Alto (7 rel.) |
| CL-095 | `RelatorioConsolidado` | classe | §12 | aba RelatorioConsolidado | Resultado consolidado de métricas e agregações de um período. | SSID_011 | — | `[CONFIRMADO]` | — | via Produto | Alto (5 rel.) |
| CL-096 | `ExportacaoRelatorio` | classe | §12 | aba ExportacaoRelatorio | Registro de uma exportação de relatório. | USID_033, USID_035 | — | `[PENDENTE]` | CP-110 [PENDENTE] | — | Médio (3 rel.) |
| CL-097 | `GeracaoRelatorioAgendada` | classe | §12 | aba GeraçãoRelatorioAgendada | Geração programada dos dados consolidados. | SSID_011 | — | `[PENDENTE]` | CP-109 [PENDENTE] | — | Médio (2 rel.) |
| CL-098 | `GeradorArquivo` | interface | §12 | aba GeradorArquivo | Contrato para gerar o arquivo entregue numa exportação. | USID_033, USID_035 | — | `[PENDENTE]` | CP-108 [PENDENTE] | — | Médio (3 rel.) |
| CL-099 | `LogSDK` | classe | §13 | aba LogSDK | Fachada pública da SDK Java. | USID_015, USID_017 | ADR_007 | `[LEGADO]` | — | — | Alto (7 rel.) |
| CL-100 | `ConfiguracaoSdk` | classe | §13 | aba ConfiguracaoSdk | Configurações para inicializar a SDK em um Produto. | USID_015 | ADR_007 | `[LEGADO]` | — | via Produto | Médio (4 rel.) |
| CL-101 | `CredencialIngestao (SDK)` | classe | §13 | aba CredencialIngestao | Token usado pela SDK para autenticar o Produto. | USID_016, SSID_001 | ADR_007 | `[LEGADO]` | CP-113 [CONFLITO] | — | Baixo (1 rel.) |
| CL-102 | `IdentificadorProduto` | classe | §13 | aba IdentificadorProduto | Objeto de valor que identifica o Produto monitorado na SDK. | USID_015 | ADR_007 | `[LEGADO]` | — | via Produto | Médio (3 rel.) |
| CL-103 | `EventoLog` | classe | §13 | aba EventoLog | Log bruto capturado no código do Produto. | SSID_001 | ADR_007 | `[LEGADO]` | — | — | Médio (3 rel.) |
| CL-104 | `EnvelopeIngestao` | classe | §13 | aba EnvelopeIngestao | EventoLog com os metadados mínimos para a transmissão. | SSID_001 | ADR_007 | `[LEGADO]` | — | via Produto | Médio (3 rel.) |
| CL-105 | `ClienteColetor` | interface | §13 | aba ClienteColetor | Contrato da SDK para transmitir logs e testar a conexão com o Coletor. | SSID_001, USID_015 | ADR_007 | `[LEGADO]` | — | — | Médio (4 rel.) |
| CL-106 | `SerializadorIngestao` | interface | §13 | aba SerializadorIngestao | Converte o envelope para o formato aceito pelo Coletor. | SSID_001 | ADR_007 | `[LEGADO]` | — | — | Baixo (1 rel.) |
| CL-107 | `ValidadorEventoLog` | classe | §13 | aba ValidadorEventoLog | Valida a consistência mínima do log antes da transmissão. | SSID_001 | ADR_007 | `[LEGADO]` | — | — | Médio (2 rel.) |
| CL-108 | `ResultadoValidacao` | classe | §13 | aba ResultadoValidacao | Resultado das validações antes da transmissão. | SSID_001 | ADR_007 | `[LEGADO]` | — | — | Médio (2 rel.) |
| CL-109 | `RedatorDadosSensiveis` | interface | §13 | aba RedatorDadosSensiveis | Ponto de extensão para mascarar dados sensíveis na SDK. | — | ADR_007 | `[LEGADO]` | — | — | Médio (2 rel.) |
| CL-110 | `RespostaColetor` | classe | §13 | aba RespostaColetor | Retorno seguro do Coletor para a SDK. | SSID_001 | ADR_007 | `[LEGADO]` | — | — | Baixo (1 rel.) |
| CL-111 | `ResultadoEnvio` | classe | §13 | aba ResultadoEnvio | Resultado entregue ao Produto depois de uma tentativa de envio. | SSID_001 | ADR_007 | `[LEGADO]` | — | — | Baixo (1 rel.) |
| CL-112 | `ResultadoConexao` | classe | §13 | aba ResultadoConexao | Resultado do teste de conectividade e autenticação da SDK. | SSID_001 | ADR_007 | `[LEGADO]` | — | — | Médio (2 rel.) |
| CL-113 | `Executavel` | substituída | §13 | aba Executavel | Agente instalado que monitora uma pasta e envia arquivos (modelo antigo). | USID_018, USID_019, USID_020 | ADR_007, ADR_111 | `[SUBSTITUÍDA]` | CP-113 [CONFLITO] | via Produto | Médio (4 rel.) |
| CL-114 | `FonteTelemetria` | classe | §13 | DER v9; pauta ING-06 | Fonte de telemetria OpenTelemetry que substitui o Executável. | USID_015 (inferido), USID_016 (inferido) | — | `[LEGADO]` | CP-113 [CONFLITO] | — | Baixo (1 rel.) |

## 8. Matriz de enums

| ID | Enum | § | Valores | Usado por | Requisitos | Situação | Pendências |
|---|---|---|---|---|---|---|---|
| ES-01 | `TipoEndereco` | §1 | SEDE, FILIAL, COBRANCA | CL-009 `Endereco` | USID_021 (inferido) | `[CONFIRMADO]` | — |
| ES-02 | `TipoPlano` | §3 | FREE, STARTER, PRO, BUSINESS, ENTERPRISE | CL-018 `Plano` | USID_039 | `[CONFIRMADO]` | — |
| ES-03 | `RecursosAnaliseIA` | §3 | NENHUMA, DETECCAO_ANOMALIAS, INVESTIGACAO_AUTOMATICA, RASTREIO_USUARIO, SUGESTAO | CL-018 `Plano` | USID_039, USID_044 (inferido) | `[CONFLITO]` | CP-19 [CONFLITO], CP-20 [A CONFERIR], CP-131 [CONFLITO] |
| ES-04 | `TipoDashboard` | §3 | BASICO, PADRAO, PERSONALIZADO | CL-018 `Plano` | USID_039 | `[CONFIRMADO]` | — |
| ES-05 | `Periodicidade` | §3 | MENSAL, ANUAL | CL-018 `Plano` | USID_039 | `[CONFIRMADO]` | — |
| ES-06 | `StatusAssinatura` | §3 | (sem valores na fonte) | CL-017 `GerenciadorAssinatura`, CL-020 `Assinatura` | USID_042, SSID_016 | `[PENDENTE]` | CP-18 [PENDENTE], CP-134 [PROPOSTO] |
| ES-07 | `StatusPagamento` | §3 | PENDENTE, PAGO, RECUSADO, ESTORNADO | CL-022 `ProcessamentoPagamento`, CL-023 `GatewayPagamento`, CL-024 `ApiPagamento`, CL-025 `Pagamento` | SSID_018 | `[CONFIRMADO]` | — |
| ES-08 | `StatusReembolso` | §3 | SOLICITADO, APROVADO, NEGADO, CONCLUIDO | CL-026 `Reembolso` | USID_043 | `[CONFIRMADO]` | — |
| ES-09 | `TipoOperacaoGateway` | §3 | PRIMEIRA_COMPRA, ATRASO, CANCELAMENTO, UPGRADE_DOWNGRADE | CL-017 `GerenciadorAssinatura`, CL-027 `EventoGateway` | SSID_016 | `[PROPOSTO]` | CP-25 [CONFLITO], CP-134 [PROPOSTO] |
| ES-10 | `ResultadoEventoGateway` | §3 | SUCESSO, FALHA | CL-027 `EventoGateway` | SSID_016, SSID_018 | `[CONFIRMADO]` | — |
| ES-11 | `TipoTransacao` | §4 | CONSUMO, RECARGA, ESTORNO, EXPIRACAO | CL-031 `Transacao` | SSID_020 (inferido) | `[CONFIRMADO]` | — |
| ES-12 | `StatusTransacao` | §4 | SUCESSO, FALHA | CL-031 `Transacao` | SSID_020 (inferido) | `[CONFIRMADO]` | — |
| ES-13 | `StatusOperacao` | §4 | PENDENTE, AUTORIZADA, NEGADA, CONCLUIDA, REVERTIDA | CL-032 `Controle` | SSID_020 (inferido) | `[CONFIRMADO]` | — |
| ES-14 | `VarreduraStatus` | §6 | SCHEDULED, PROCESSING, COMPLETED, COMPLETED_WITH_ERROR, FAILED | CL-044 `Varredura`, CL-045 `VarreduraResumo` | — | `[CONFLITO]` | CP-56 [CONFLITO] |
| ES-15 | `VarreduraTrigger` | §6 | SCHEDULED, QUEUE_SIZE, FORCED | CL-044 `Varredura` | USID_025, SSID_005, SSID_006 | `[CONFIRMADO]` | — |
| ES-16 | `ArquivoScanStatus` | §6 | PENDING, PROCESSING, COMPLETED, ERROR, FAILED | CL-046 `ArquivoVarredura` | USID_007, SSID_004 | `[PENDENTE]` | CP-54 [PENDENTE], CP-55 [CONFLITO] |
| ES-17 | `AgendamentoVarreduraStatus` | §6 | ACTIVE, PAUSE, DISABLE | CL-047 `AgendamentoVarredura` | USID_026 | `[CONFLITO]` | CP-57 [CONFLITO] |
| ES-18 | `NivelPrioridade` | §6 | VERY_HIGH, HIGH, MEDIUM, LOW, VERY_LOW | CL-040 `Trace`, CL-046 `ArquivoVarredura`, CL-048 `Modulo` | — | `[CONFIRMADO]` | — |
| ES-19 | `Tipo` | §7 | ERRO, WARNING, SPAM | CL-060 `AchadoAnalise`, CL-062 `ClassificadorAnalise` | SSID_007, SSID_009 | `[CONFIRMADO]` | — |
| ES-20 | `Nivel` | §7 | BASICO, MEDIO, AVANCADO | CL-063 `ScannerSeguranca` | USID_027, SSID_008 | `[CONFIRMADO]` | — |
| ES-21 | `StatusSugestao` | §9 | PROCESSANDO, AGUARDANDO_REVISAO, FECHADA, FALHA | CL-068 `Sugestao` | USID_045, USID_046, USID_047 | `[CONFIRMADO]` | — |
| ES-22 | `CanalNotificacao` | §10 | EMAIL, PUSH, WEB | CL-076 `Notificacao`, CL-077 `PreferenciaNotificacao`, CL-079 `GatewayNotificacaoFactory` | USID_009, USID_010, USID_011, USID_012 | `[CONFIRMADO]` | CP-96 [PROPOSTO] |
| ES-23 | `PlataformaDispositivo` | §10 | IOS, ANDROID | CL-083 `DispositivoPush` | USID_010 | `[CONFIRMADO]` | — |
| ES-24 | `StatusEnvioNotificacao` | §10 | PENDENTE, ENVIADA, FALHA | CL-080 `EnviadorEmail`, CL-081 `EnviadorPush`, CL-082 `EnviadorWeb`, CL-084 `TentativaEntrega` | USID_009, USID_010, USID_011 | `[PENDENTE]` | CP-98 [CONFLITO], CP-100 [PENDENTE] |
| ES-25 | `FormatoArquivo` | §12 | PDF, CSV | CL-096 `ExportacaoRelatorio`, CL-098 `GeradorArquivo` | USID_033, USID_035 | `[CONFIRMADO]` | — |
| ES-26 | `SistemaOperacional` | §13 | WINDOWS, LINUX, MACOS | CL-113 `Executavel` | USID_018 | `[LEGADO]` | — |
| ES-27 | `StatusExecutavel` | §13 | PENDENTE_CONFIGURACAO, ATIVO, PARADO, DESCONECTADO | CL-113 `Executavel` | USID_019, USID_020 | `[LEGADO]` | — |

## 9. Matriz de relações

| ID | § | Origem | Tipo | Destino | Rótulo | Alcance | Base | Requisitos | Situação | Pendências |
|---|---|---|---|---|---|---|---|---|---|---|
| RE-001 | §1 | CL-001 `Tenant` | associação `--` | CL-008 `Empresa` | cadastro | no módulo | ADR_158 (proposta) | — | `[PROPOSTO]` | CP-06, CP-15 |
| RE-002 | §1 | CL-001 `Tenant` | associação `--` | CL-002 `Membro` | membros | no módulo | multiplicidade da fonte (DER v9 / ADR) | SSID_017 | `[PENDENTE]` | CP-01 |
| RE-003 | §1 | CL-001 `Tenant` | associação `--` | CL-004 `Produto` | produtos | no módulo | multiplicidade da fonte (DER v9 / ADR) | — | `[CONFIRMADO]` | CP-06 |
| RE-004 | §1 | CL-002 `Membro` | associação `--` | CL-003 `AcessoProduto` | recebe | no módulo | multiplicidade da fonte (DER v9 / ADR) | — | `[CONFIRMADO]` | CP-07, CP-09 |
| RE-005 | §1 | CL-004 `Produto` | associação `--` | CL-003 `AcessoProduto` | libera | no módulo | multiplicidade da fonte (DER v9 / ADR) | — | `[CONFIRMADO]` | — |
| RE-006 | §1 | CL-004 `Produto` | associação `--` | CL-006 `ConfiguracaoProduto` | configura | no módulo | campo `ConfiguracaoProduto configuracao_produto` | USID_024 | `[CONFIRMADO]` | — |
| RE-007 | §1 | CL-004 `Produto` | associação `--` | CL-005 `ContextoProduto` | — | no módulo | campo `ContextoProduto contexto_produto` | USID_023 | `[CONFIRMADO]` | — |
| RE-008 | §1 | CL-004 `Produto` | associação dirigida `-->` | CL-008 `Empresa` | empresa | no módulo | campo `Empresa empresa` | — | `[PROPOSTO]` | CP-04, CP-06 |
| RE-009 | §1 | CL-005 `ContextoProduto` | dependência `..>` | CL-007 `ContextoEmpresa` | CombinarComContextoEmpresa | no módulo | método `CombinarComContextoEmpresa(ContextoEmpresa contexto) string` | SSID_015 | `[CONFIRMADO]` | — |
| RE-010 | §1 | CL-008 `Empresa` | associação `--` | CL-007 `ContextoEmpresa` | — | no módulo | campo `ContextoEmpresa contexto_empresa` | — | `[PROPOSTO]` | CP-04, CP-06 |
| RE-011 | §1 | CL-008 `Empresa` | associação `--` | CL-009 `Endereco` | possui | no módulo | campo `Endereco endereco` | USID_021 | `[CONFLITO]` | CP-05, CP-06 |
| RE-012 | §1 | CL-009 `Endereco` | associação dirigida `-->` | ES-01 `TipoEndereco` | — | no módulo | campo `TipoEndereco tipo` | USID_021 | `[CONFIRMADO]` | — |
| RE-013 | §1 | CL-010 `Usuario` | dependência `..>` | CL-002 `Membro` | substituida por | no módulo | substituição (DER v9 / ADR) | SSID_017, USID_048, USID_049, USID_051 | `[SUBSTITUÍDA]` | CP-07, CP-82, CP-92 |
| RE-014 | §1 | CL-011 `Gestor` | dependência `..>` | CL-002 `Membro` | substituida por | no módulo | substituição (DER v9 / ADR) | USID_029 | `[SUBSTITUÍDA]` | CP-07 |
| RE-015 | §1 | CL-012 `Vinculo` | dependência `..>` | CL-002 `Membro` | substituida por | no módulo | substituição (DER v9 / ADR) | USID_029 | `[SUBSTITUÍDA]` | CP-07 |
| RE-016 | §1 | CL-013 `Acesso` | dependência `..>` | CL-002 `Membro` | substituida por | no módulo | substituição (DER v9 / ADR) | USID_049 | `[SUBSTITUÍDA]` | CP-07 |
| RE-017 | §2 | CL-001 `Tenant` | associação `--` | CL-014 `PapelNotificacao` | define | entre módulos (§1 → §2) | multiplicidade da fonte (DER v9 / ADR) | — | `[CONFIRMADO]` | — |
| RE-018 | §2 | CL-002 `Membro` | associação `--` | CL-014 `PapelNotificacao` | participa | entre módulos (§1 → §2) | multiplicidade da fonte (DER v9 / ADR) | — | `[CONFIRMADO]` | — |
| RE-019 | §2 | CL-014 `PapelNotificacao` | associação `--` | CL-015 `PapelSeveridade` | gravidades | no módulo | multiplicidade da fonte (DER v9 / ADR) | SSID_009, USID_012 | `[CONFIRMADO]` | — |
| RE-020 | §2 | CL-014 `PapelNotificacao` | associação `--` | CL-016 `PapelTipoAlerta` | tipos de alerta | no módulo | multiplicidade da fonte (DER v9 / ADR) | SSID_009, USID_012 | `[CONFIRMADO]` | — |
| RE-021 | §3 | CL-001 `Tenant` | associação `--` | CL-020 `Assinatura` | possui | entre módulos (§1 → §3) | multiplicidade da fonte (DER v9 / ADR) | USID_040 | `[CONFIRMADO]` | — |
| RE-022 | §3 | CL-001 `Tenant` | associação `--` | CL-027 `EventoGateway` | eventos | entre módulos (§1 → §3) | multiplicidade da fonte (DER v9 / ADR) | — | `[CONFIRMADO]` | — |
| RE-023 | §3 | CL-017 `GerenciadorAssinatura` | dependência `..>` | CL-020 `Assinatura` | contrata / altera / cancela | no módulo | método `contratarPlano(UUID empresa_id, Plano plano) Assinatura` | SSID_016, USID_040, USID_041, USID_042, USID_043 | `[PROPOSTO]` | CP-134 |
| RE-024 | §3 | CL-017 `GerenciadorAssinatura` | dependência `..>` | CL-027 `EventoGateway` | aplicarEventoDeAssinatura | no módulo | método `aplicarEventoDeAssinatura(String assinaturaId, TipoOperacaoGateway tipoOperacao, EventoGateway evento) void` | SSID_016 | `[CONFIRMADO]` | CP-134 |
| RE-025 | §3 | CL-017 `GerenciadorAssinatura` | dependência `..>` | CL-018 `Plano` | listarPlanosDisponiveis | no módulo | método `listarPlanosDisponiveis() List<Plano>` | USID_039, USID_040, USID_041 | `[CONFIRMADO]` | — |
| RE-026 | §3 | CL-017 `GerenciadorAssinatura` | associação dirigida `-->` | CL-022 `ProcessamentoPagamento` | orquestra | no módulo | tabela do §3 | SSID_016, USID_040 | `[CONFIRMADO]` | — |
| RE-027 | §3 | CL-017 `GerenciadorAssinatura` | dependência `..>` | CL-026 `Reembolso` | solicitarReembolso | no módulo | método `solicitarReembolso(String pagamentoId, String motivo) Reembolso` | USID_043 | `[CONFIRMADO]` | — |
| RE-028 | §3 | CL-017 `GerenciadorAssinatura` | dependência `..>` | ES-06 `StatusAssinatura` | validarTransicaoDeStatus | no módulo | método `validarTransicaoDeStatus(StatusAssinatura atual, StatusAssinatura novo) Boolean` | SSID_016, USID_042 | `[CONFIRMADO]` | CP-134 |
| RE-029 | §3 | CL-017 `GerenciadorAssinatura` | dependência `..>` | ES-09 `TipoOperacaoGateway` | aplicarEventoDeAssinatura | no módulo | método `aplicarEventoDeAssinatura(String assinaturaId, TipoOperacaoGateway tipoOperacao, EventoGateway evento) void` | SSID_016 | `[PROPOSTO]` | CP-134 |
| RE-030 | §3 | CL-018 `Plano` | associação `--` | CL-020 `Assinatura` | plano | no módulo | multiplicidade da fonte (DER v9 / ADR) | USID_040, USID_041 | `[CONFIRMADO]` | — |
| RE-031 | §3 | CL-018 `Plano` | associação dirigida `-->` | ES-05 `Periodicidade` | — | no módulo | campo `Periodicidade periodicidade` | USID_039 | `[CONFIRMADO]` | — |
| RE-032 | §3 | CL-018 `Plano` | associação dirigida `-->` | ES-03 `RecursosAnaliseIA` | — | no módulo | tabela do §3 | USID_039, USID_044 | `[A CONFERIR]` | CP-20 |
| RE-033 | §3 | CL-018 `Plano` | associação dirigida `-->` | ES-04 `TipoDashboard` | — | no módulo | campo `TipoDashboard dashboard` | USID_039 | `[CONFIRMADO]` | — |
| RE-034 | §3 | CL-018 `Plano` | associação dirigida `-->` | ES-02 `TipoPlano` | — | no módulo | campo `TipoPlano nome` | USID_039 | `[CONFIRMADO]` | — |
| RE-035 | §3 | CL-019 `TabelaPrecificacao` | associação `--` | CL-020 `Assinatura` | preco | no módulo | multiplicidade da fonte (DER v9 / ADR) | — | `[CONFIRMADO]` | — |
| RE-036 | §3 | CL-020 `Assinatura` | associação `--` | CL-025 `Pagamento` | cobrancas | no módulo | multiplicidade da fonte (DER v9 / ADR) | SSID_018, USID_040, USID_043 | `[PROPOSTO]` | CP-134 |
| RE-037 | §3 | CL-020 `Assinatura` | associação dirigida `-->` | ES-06 `StatusAssinatura` | — | no módulo | campo `StatusAssinatura status` | SSID_016, USID_042 | `[PROPOSTO]` | CP-134 |
| RE-038 | §3 | CL-021 `ProdutoRecursoIA` | associação `--` | CL-018 `Plano` | relaciona | no módulo | tabela do §3 | USID_039, USID_044 | `[CONFLITO]` | CP-124 |
| RE-039 | §3 | CL-021 `ProdutoRecursoIA` | associação `--` | CL-004 `Produto` | relaciona | entre módulos (§3 → §1) | tabela do §3 | — | `[CONFIRMADO]` | — |
| RE-040 | §3 | CL-022 `ProcessamentoPagamento` | dependência `..>` | CL-027 `EventoGateway` | receberEventoGateway | no módulo | método `receberEventoGateway(EventoGateway evento) void` | SSID_016, SSID_018 | `[CONFIRMADO]` | — |
| RE-041 | §3 | CL-022 `ProcessamentoPagamento` | dependência `..>` | CL-025 `Pagamento` | processarPagamento | no módulo | método `processarPagamento(String assinaturaId, Decimal valor) Pagamento` | SSID_018, USID_040 | `[CONFIRMADO]` | — |
| RE-042 | §3 | CL-022 `ProcessamentoPagamento` | dependência `..>` | ES-07 `StatusPagamento` | reprocessarPagamentoFalho | no módulo | método `reprocessarPagamentoFalho(String pagamentoId) StatusPagamento` | SSID_018 | `[CONFIRMADO]` | — |
| RE-043 | §3 | CL-023 `GatewayPagamento` | dependência `..>` | CL-027 `EventoGateway` | — | no módulo | método `enviarCobranca(Object dados) EventoGateway` | SSID_018 | `[PROPOSTO]` | CP-134 |
| RE-044 | §3 | CL-023 `GatewayPagamento` | dependência `..>` | ES-07 `StatusPagamento` | consultarStatus | no módulo | método `consultarStatus(String referenciaExterna) StatusPagamento` | SSID_018 | `[CONFIRMADO]` | — |
| RE-045 | §3 | CL-024 `ApiPagamento` | dependência `..>` | CL-027 `EventoGateway` | enviarCobranca / solicitarReembolsoExterno / validarAutenticidade | no módulo | método `enviarCobranca(Object dados) EventoGateway` | SSID_018 | `[PROPOSTO]` | CP-134 |
| RE-046 | §3 | CL-024 `ApiPagamento` | dependência `..>` | ES-07 `StatusPagamento` | consultarStatus | no módulo | método `consultarStatus(String referenciaExterna) StatusPagamento` | SSID_018 | `[CONFIRMADO]` | — |
| RE-047 | §3 | CL-025 `Pagamento` | associação `--` | CL-026 `Reembolso` | reembolso | no módulo | multiplicidade da fonte (DER v9 / ADR) | USID_043 | `[CONFIRMADO]` | — |
| RE-048 | §3 | CL-025 `Pagamento` | associação dirigida `-->` | ES-07 `StatusPagamento` | — | no módulo | campo `StatusPagamento status` | SSID_018 | `[CONFIRMADO]` | — |
| RE-049 | §3 | CL-026 `Reembolso` | associação `--` | CL-027 `EventoGateway` | eventos | no módulo | multiplicidade da fonte (DER v9 / ADR) | — | `[CONFIRMADO]` | — |
| RE-050 | §3 | CL-026 `Reembolso` | associação dirigida `-->` | ES-08 `StatusReembolso` | — | no módulo | campo `StatusReembolso status` | USID_043 | `[CONFIRMADO]` | — |
| RE-051 | §3 | CL-027 `EventoGateway` | associação dirigida `-->` | ES-10 `ResultadoEventoGateway` | — | no módulo | campo `ResultadoEventoGateway resultado` | SSID_016, SSID_018 | `[CONFIRMADO]` | — |
| RE-052 | §3 | CL-027 `EventoGateway` | associação dirigida `-->` | ES-09 `TipoOperacaoGateway` | — | no módulo | campo `TipoOperacaoGateway tipoOperacao` | SSID_016 | `[CONFLITO]` | CP-25, CP-134 |
| RE-053 | §4 | CL-028 `Credito` | associação dirigida `-->` | CL-007 `ContextoEmpresa` | — | entre módulos (§4 → §1) | campo `ContextoEmpresa contexto` | — | `[CONFIRMADO]` | — |
| RE-054 | §4 | CL-028 `Credito` | associação dirigida `-->` | CL-004 `Produto` | — | entre módulos (§4 → §1) | campo `Produto produto` | — | `[CONFIRMADO]` | — |
| RE-055 | §4 | CL-029 `PlanoCreditos` | dependência `..>` | CL-028 `Credito` | GerarCreditos | no módulo | método `GerarCreditos(datetime data_referencia) Credito` | — | `[CONFIRMADO]` | — |
| RE-056 | §4 | CL-030 `Saldo` | agregação `o--` | CL-028 `Credito` | creditos | no módulo | campo `List<Credito> creditos` | SSID_020, USID_044 | `[CONFIRMADO]` | — |
| RE-057 | §4 | CL-031 `Transacao` | associação dirigida `-->` | CL-007 `ContextoEmpresa` | — | entre módulos (§4 → §1) | campo `ContextoEmpresa contexto` | — | `[CONFIRMADO]` | — |
| RE-058 | §4 | CL-031 `Transacao` | associação dirigida `-->` | CL-028 `Credito` | credito | no módulo | campo `Credito credito` | SSID_020 | `[CONFIRMADO]` | — |
| RE-059 | §4 | CL-031 `Transacao` | associação dirigida `-->` | CL-004 `Produto` | — | entre módulos (§4 → §1) | campo `Produto produto` | — | `[CONFIRMADO]` | — |
| RE-060 | §4 | CL-031 `Transacao` | associação dirigida `-->` | ES-12 `StatusTransacao` | — | no módulo | campo `StatusTransacao status` | SSID_020 | `[CONFIRMADO]` | — |
| RE-061 | §4 | CL-031 `Transacao` | associação dirigida `-->` | ES-11 `TipoTransacao` | — | no módulo | campo `TipoTransacao tipo` | SSID_020 | `[CONFIRMADO]` | — |
| RE-062 | §4 | CL-031 `Transacao` | associação dirigida `-->` | CL-031 `Transacao` | transacao_origem_id | no módulo | método `GerarEstorno() Transacao` | SSID_020 | `[CONFIRMADO]` | — |
| RE-063 | §4 | CL-032 `Controle` | associação dirigida `-->` | CL-007 `ContextoEmpresa` | — | entre módulos (§4 → §1) | campo `ContextoEmpresa contexto` | — | `[CONFIRMADO]` | — |
| RE-064 | §4 | CL-032 `Controle` | associação dirigida `-->` | CL-004 `Produto` | — | entre módulos (§4 → §1) | campo `Produto produto` | — | `[CONFIRMADO]` | — |
| RE-065 | §4 | CL-032 `Controle` | associação dirigida `-->` | CL-030 `Saldo` | saldo | no módulo | campo `Saldo saldo` | SSID_020 | `[CONFIRMADO]` | — |
| RE-066 | §4 | CL-032 `Controle` | associação dirigida `-->` | ES-13 `StatusOperacao` | — | no módulo | campo `StatusOperacao status_operacao` | SSID_020 | `[CONFIRMADO]` | — |
| RE-067 | §4 | CL-032 `Controle` | dependência `..>` | CL-031 `Transacao` | ExecutarConsumo / ReverterOperacao | no módulo | método `ExecutarConsumo() Transacao` | SSID_020 | `[CONFIRMADO]` | — |
| RE-068 | §4 | CL-075 `ModuloSugestao` | dependência `..>` | CL-030 `Saldo` | reserva e liquida (Sugestao) | entre módulos (§9 → §4) | ADR_157 (proposta) | SSID_020, USID_044 | `[PROPOSTO]` | CP-30, CP-88 |
| RE-069 | §5 | CL-004 `Produto` | associação `--` | CL-041 `Produtor` | produtores | entre módulos (§1 → §5) | multiplicidade da fonte (DER v9 / ADR) | USID_016 | `[CONFIRMADO]` | — |
| RE-070 | §5 | CL-033 `Coletor` | dependência `..>` | CL-039 `Arquivo` | EnviarLote / EnviarArquivo | no módulo | método `EnviarLote() List<Arquivo>` | SSID_003, USID_006 | `[CONFIRMADO]` | — |
| RE-071 | §5 | CL-033 `Coletor` | associação dirigida `-->` | CL-038 `EnfileiradorLogs` | — | no módulo | campo `EnfileiradorLogs EnfilerarLog` | SSID_003 | `[CONFIRMADO]` | — |
| RE-072 | §5 | CL-033 `Coletor` | associação dirigida `-->` | CL-036 `GerenciadorLote` | — | no módulo | campo `GerenciadorLote GerenciadorLote` | SSID_002 | `[CONFIRMADO]` | — |
| RE-073 | §5 | CL-033 `Coletor` | associação dirigida `-->` | CL-034 `GerenciadorRequisicao` | ReceberLog | no módulo | campo `GerenciadorRequisicao GerenciadorRequisicao` | SSID_001 | `[CONFIRMADO]` | — |
| RE-074 | §5 | CL-033 `Coletor` | associação dirigida `-->` | CL-044 `Varredura` | — | entre módulos (§5 → §6) | campo `Varredura Varredura` | — | `[CONFIRMADO]` | — |
| RE-075 | §5 | CL-034 `GerenciadorRequisicao` | associação dirigida `-->` | CL-035 `LogRecebido` | — | no módulo | campo `LogRecebido LogRecebido` | — | `[CONFIRMADO]` | — |
| RE-076 | §5 | CL-034 `GerenciadorRequisicao` | dependência `..>` | CL-042 `TokenApi` | busca pelo hash SHA-256 | no módulo | ADR_155 (proposta) | SSID_001, SSID_014, USID_016 | `[PROPOSTO]` | CP-40 |
| RE-077 | §5 | CL-035 `LogRecebido` | associação dirigida `-->` | CL-039 `Arquivo` | — | no módulo | campo `Arquivo Arquivo` | — | `[CONFIRMADO]` | — |
| RE-078 | §5 | CL-036 `GerenciadorLote` | associação dirigida `-->` | CL-037 `LoteAgrupador` | — | no módulo | campo `LoteAgrupador LoteAgrupador` | SSID_002 | `[CONFIRMADO]` | CP-47 |
| RE-079 | §5 | CL-037 `LoteAgrupador` | associação `--` | CL-035 `LogRecebido` | agrupa | no módulo | campo `List<LogRecebido> Logs` | SSID_002 | `[CONFIRMADO]` | — |
| RE-080 | §5 | CL-038 `EnfileiradorLogs` | associação dirigida `-->` | CL-036 `GerenciadorLote` | — | no módulo | campo `GerenciadorLote GerenciadorLote` | — | `[CONFIRMADO]` | CP-47 |
| RE-081 | §5 | CL-039 `Arquivo` | associação `--` | CL-040 `Trace` | agrupa | no módulo | método `getTraces() Trace[]` | — | `[CONFLITO]` | CP-43 |
| RE-082 | §5 | CL-040 `Trace` | associação `--` | CL-048 `Modulo` | passa por | entre módulos (§5 → §6) | método `resolvePrioridade(Modulo[] modulos) NivelPrioridade` | — | `[CONFIRMADO]` | — |
| RE-083 | §5 | CL-041 `Produtor` | associação dirigida `-->` | CL-001 `Tenant` | tenantId | entre módulos (§5 → §1) | tabela do §5 | — | `[CONFIRMADO]` | — |
| RE-084 | §5 | CL-041 `Produtor` | associação `--` | CL-042 `TokenApi` | tokens | no módulo | multiplicidade da fonte (DER v9 / ADR) | SSID_001, SSID_014, USID_016 | `[PROPOSTO]` | CP-37, CP-40, CP-128 |
| RE-085 | §5 | CL-043 `CredencialIngestao` | dependência `..>` | CL-042 `TokenApi` | substituida por | no módulo | substituição (DER v9 / ADR) | SSID_014, USID_016 | `[SUBSTITUÍDA]` | CP-39, CP-128 |
| RE-086 | §6 | CL-004 `Produto` | associação `--` | CL-049 `FilaDesordenada` | uma fila por Produto | entre módulos (§1 → §6) | multiplicidade da fonte (DER v9 / ADR) | — | `[CONFIRMADO]` | — |
| RE-087 | §6 | CL-040 `Trace` | associação `--` | CL-048 `Modulo` | service.name | entre módulos (§5 → §6) | método `resolvePrioridade(Modulo[] modulos) NivelPrioridade` | — | `[CONFIRMADO]` | — |
| RE-088 | §6 | CL-040 `Trace` | associação dirigida `-->` | ES-18 `NivelPrioridade` | — | entre módulos (§5 → §6) | campo `NivelPrioridade prioridade` | — | `[CONFIRMADO]` | — |
| RE-089 | §6 | CL-044 `Varredura` | dependência `..>` | CL-039 `Arquivo` | takeSnapshot / prioritizeArquivos | entre módulos (§6 → §5) | método `takeSnapshot(timestamp snapshot_at) Arquivo[]` | SSID_004 | `[CONFIRMADO]` | — |
| RE-090 | §6 | CL-044 `Varredura` | associação `--` | CL-046 `ArquivoVarredura` | processa | no módulo | multiplicidade da fonte (DER v9 / ADR) | SSID_004 | `[CONFLITO]` | CP-120 |
| RE-091 | §6 | CL-044 `Varredura` | dependência `..>` | CL-049 `FilaDesordenada` | takeSnapshot | no módulo | tabela do §6 | — | `[CONFIRMADO]` | — |
| RE-092 | §6 | CL-044 `Varredura` | dependência `..>` | CL-050 `FilaOrdenada` | publishFilaOrdenada | no módulo | método `publishFilaOrdenada() FilaOrdenada` | — | `[CONFIRMADO]` | — |
| RE-093 | §6 | CL-044 `Varredura` | dependência `..>` | CL-052 `HistoricoVarredura` | registra cada execucao | no módulo | tabela do §6 | SSID_006 | `[CONFIRMADO]` | — |
| RE-094 | §6 | CL-044 `Varredura` | dependência `..>` | CL-051 `TravaVarredura` | acquire / release | no módulo | tabela do §6 | USID_025 | `[CONFIRMADO]` | — |
| RE-095 | §6 | CL-044 `Varredura` | dependência `..>` | CL-045 `VarreduraResumo` | getResume | no módulo | método `getResume() VarreduraResumo` | — | `[CONFIRMADO]` | — |
| RE-096 | §6 | CL-044 `Varredura` | associação dirigida `-->` | ES-14 `VarreduraStatus` | — | no módulo | campo `VarreduraStatus status` | — | `[CONFIRMADO]` | — |
| RE-097 | §6 | CL-044 `Varredura` | associação dirigida `-->` | ES-15 `VarreduraTrigger` | — | no módulo | campo `VarreduraTrigger trigger` | SSID_005, SSID_006, USID_025 | `[CONFIRMADO]` | — |
| RE-098 | §6 | CL-045 `VarreduraResumo` | associação dirigida `-->` | ES-14 `VarreduraStatus` | — | no módulo | campo `VarreduraStatus status` | — | `[CONFIRMADO]` | — |
| RE-099 | §6 | CL-046 `ArquivoVarredura` | associação dirigida `-->` | CL-039 `Arquivo` | arquivo_id | entre módulos (§6 → §5) | tabela do §6 | SSID_004, USID_007 | `[CONFLITO]` | CP-55 |
| RE-100 | §6 | CL-046 `ArquivoVarredura` | associação dirigida `-->` | ES-16 `ArquivoScanStatus` | — | no módulo | campo `ArquivoScanStatus status` | SSID_004, USID_007 | `[CONFLITO]` | CP-55 |
| RE-101 | §6 | CL-046 `ArquivoVarredura` | associação dirigida `-->` | ES-18 `NivelPrioridade` | — | no módulo | campo `NivelPrioridade prioridade` | — | `[CONFIRMADO]` | — |
| RE-102 | §6 | CL-047 `AgendamentoVarredura` | associação dirigida `-->` | ES-17 `AgendamentoVarreduraStatus` | — | no módulo | campo `AgendamentoVarreduraStatus status` | USID_026 | `[CONFIRMADO]` | — |
| RE-103 | §6 | CL-047 `AgendamentoVarredura` | associação `--` | CL-044 `Varredura` | dispara | no módulo | método `dispatch() Varredura` | SSID_006 | `[CONFIRMADO]` | — |
| RE-104 | §6 | CL-047 `AgendamentoVarredura` | dependência `..>` | CL-044 `Varredura` | dispatch | no módulo | método `dispatch() Varredura` | SSID_006 | `[CONFIRMADO]` | — |
| RE-105 | §6 | CL-048 `Modulo` | associação dirigida `-->` | ES-18 `NivelPrioridade` | — | no módulo | campo `NivelPrioridade prioridade` | — | `[CONFIRMADO]` | — |
| RE-106 | §6 | CL-048 `Modulo` | associação dirigida `-->` | CL-004 `Produto` | product_id | entre módulos (§6 → §1) | tabela do §6 | — | `[CONFIRMADO]` | — |
| RE-107 | §6 | CL-049 `FilaDesordenada` | agregação `o--` | CL-039 `Arquivo` | pendentes | entre módulos (§6 → §5) | método `snapshot(timestamp snapshot_at) Arquivo[]` | SSID_003 | `[CONFIRMADO]` | — |
| RE-108 | §6 | CL-050 `FilaOrdenada` | agregação `o--` | CL-046 `ArquivoVarredura` | — | no módulo | método `publish(ArquivoVarredura[] arquivos)` | — | `[CONFIRMADO]` | — |
| RE-109 | §7 | CL-048 `Modulo` | associação `--` | CL-060 `AchadoAnalise` | afeta | entre módulos (§6 → §7) | multiplicidade da fonte (DER v9 / ADR) | — | `[CONFIRMADO]` | — |
| RE-110 | §7 | CL-053 `Finder` | associação dirigida `-->` | CL-039 `Arquivo` | — | entre módulos (§7 → §5) | campo `Arquivo Arquivo` | SSID_013 | `[CONFIRMADO]` | — |
| RE-111 | §7 | CL-053 `Finder` | associação dirigida `-->` | CL-046 `ArquivoVarredura` | — | entre módulos (§7 → §6) | campo `ArquivoVarredura ArquivoVarredura` | — | `[CONFIRMADO]` | — |
| RE-112 | §7 | CL-053 `Finder` | associação dirigida `-->` | CL-062 `ClassificadorAnalise` | — | no módulo | campo `ClassificadorAnalise ClassificadorAnalise` | SSID_007 | `[CONFIRMADO]` | — |
| RE-113 | §7 | CL-053 `Finder` | dependência `..>` | CL-054 `ContextoAnalise` | montarContexto | no módulo | método `montarContexto() ContextoAnalise` | SSID_008 | `[CONFIRMADO]` | — |
| RE-114 | §7 | CL-053 `Finder` | associação dirigida `-->` | CL-050 `FilaOrdenada` | — | entre módulos (§7 → §6) | campo `FilaOrdenada FilaOrdenada` | — | `[CONFIRMADO]` | — |
| RE-115 | §7 | CL-053 `Finder` | dependência `..>` | CL-064 `ModuloOcorrencia` | envia o ResumoAnalise | entre módulos (§7 → §8) | tabela do §7 | — | `[CONFIRMADO]` | — |
| RE-116 | §7 | CL-053 `Finder` | associação dirigida `-->` | CL-056 `MotorAnalise` | — | no módulo | campo `MotorAnalise MotorAnalise` | SSID_007 | `[CONFIRMADO]` | — |
| RE-117 | §7 | CL-053 `Finder` | dependência `..>` | CL-061 `ResumoAnalise` | agrupa os AchadoAnalise | no módulo | método `processar() ResumoAnalise` | SSID_007 | `[PROPOSTO]` | CP-62 |
| RE-118 | §7 | CL-053 `Finder` | associação dirigida `-->` | CL-063 `ScannerSeguranca` | — | no módulo | campo `ScannerSeguranca ScannerSeguranca` | SSID_008 | `[CONFIRMADO]` | — |
| RE-119 | §7 | CL-055 `LogNormalizado` | associação dirigida `-->` | CL-054 `ContextoAnalise` | — | no módulo | campo `ContextoAnalise contextoAnalise` | — | `[CONFIRMADO]` | — |
| RE-120 | §7 | CL-056 `MotorAnalise` | dependência `..>` | CL-060 `AchadoAnalise` | Analisar | no módulo | método `Analisar() List<AchadoAnalise>` | SSID_007 | `[CONFIRMADO]` | — |
| RE-121 | §7 | CL-056 `MotorAnalise` | associação dirigida `-->` | CL-058 `BancoVetorial` | verificarRecorrencia | no módulo | campo `BancoVetorial bancoVetorial` | — | `[CONFIRMADO]` | CP-66 |
| RE-122 | §7 | CL-056 `MotorAnalise` | dependência `..>` | CL-062 `ClassificadorAnalise` | interpretarResposta | no módulo | método `interpretarResposta() ClassificadorAnalise` | SSID_007 | `[CONFIRMADO]` | — |
| RE-123 | §7 | CL-056 `MotorAnalise` | associação dirigida `-->` | CL-057 `GatewayLLMFinder` | executarAI | no módulo | campo `GatewayLLMFinder gatewayLLM` | SSID_007, SSID_020 | `[CONFIRMADO]` | — |
| RE-124 | §7 | CL-056 `MotorAnalise` | associação dirigida `-->` | CL-055 `LogNormalizado` | — | no módulo | campo `LogNormalizado logNormalizado` | SSID_007 | `[CONFIRMADO]` | — |
| RE-125 | §7 | CL-056 `MotorAnalise` | dependência `..>` | CL-059 `RecorrenciaLog` | verificarRecorrencia | no módulo | tabela do §7 | — | `[CONFIRMADO]` | — |
| RE-126 | §7 | CL-060 `AchadoAnalise` | associação dirigida `-->` | ES-19 `Tipo` | — | no módulo | campo `Tipo tipo` | SSID_007 | `[CONFIRMADO]` | — |
| RE-127 | §7 | CL-060 `AchadoAnalise` | associação dirigida `-->` | CL-040 `Trace` | traceId | entre módulos (§7 → §5) | multiplicidade da fonte (DER v9 / ADR) | — | `[CONFLITO]` | CP-65 |
| RE-128 | §7 | CL-061 `ResumoAnalise` | agregação `o--` | CL-060 `AchadoAnalise` | — | no módulo | campo `List<AchadoAnalise>` | SSID_007 | `[CONFIRMADO]` | — |
| RE-129 | §7 | CL-062 `ClassificadorAnalise` | associação dirigida `-->` | CL-060 `AchadoAnalise` | — | no módulo | campo `AchadoAnalise achadoAnalise` | SSID_007 | `[CONFIRMADO]` | — |
| RE-130 | §7 | CL-062 `ClassificadorAnalise` | associação dirigida `-->` | ES-19 `Tipo` | classificado | no módulo | campo `Tipo classificado` | SSID_007 | `[CONFIRMADO]` | — |
| RE-131 | §7 | CL-063 `ScannerSeguranca` | associação dirigida `-->` | ES-20 `Nivel` | — | no módulo | campo `Nivel nivel` | SSID_008, USID_027 | `[CONFIRMADO]` | — |
| RE-132 | §8 | CL-039 `Arquivo` | associação `--` | CL-065 `ResumoArquivo` | resumo | entre módulos (§5 → §8) | multiplicidade da fonte (DER v9 / ADR) | SSID_004, USID_007 | `[CONFIRMADO]` | — |
| RE-133 | §8 | CL-064 `ModuloOcorrencia` | associação dirigida `-->` | CL-067 `Mapper` | converte os achados | no módulo | ADR_161 (proposta) | SSID_010 | `[PROPOSTO]` | CP-79 |
| RE-134 | §8 | CL-064 `ModuloOcorrencia` | dependência `..>` | CL-075 `ModuloSugestao` | dispararSugestaoAutomatica | entre módulos (§8 → §9) | ADR_156 (proposta) | USID_044 | `[PROPOSTO]` | CP-78, CP-88 |
| RE-135 | §8 | CL-064 `ModuloOcorrencia` | dependência `..>` | CL-076 `Notificacao` | envia Ocorrencia e Sugestao | entre módulos (§8 → §10) | tabela do §8 | SSID_009 | `[CONFIRMADO]` | — |
| RE-136 | §8 | CL-064 `ModuloOcorrencia` | dependência `..>` | CL-066 `Ocorrencia` | registrar | no módulo | método `registrar(Ocorrencia ocorrencia) bool` | SSID_009, SSID_010 | `[CONFIRMADO]` | — |
| RE-137 | §8 | CL-064 `ModuloOcorrencia` | dependência `..>` | CL-021 `ProdutoRecursoIA` | consulta o plano | entre módulos (§8 → §3) | tabela do §8 | USID_044 | `[CONFIRMADO]` | — |
| RE-138 | §8 | CL-064 `ModuloOcorrencia` | dependência `..>` | CL-061 `ResumoAnalise` | receberResumo | entre módulos (§8 → §7) | ADR_161 (proposta) | SSID_009 | `[PROPOSTO]` | CP-79 |
| RE-139 | §8 | CL-064 `ModuloOcorrencia` | dependência `..>` | CL-065 `ResumoArquivo` | grava | no módulo | tabela do §8 | — | `[CONFIRMADO]` | — |
| RE-140 | §8 | CL-064 `ModuloOcorrencia` | dependência `..>` | CL-068 `Sugestao` | recebe a gerada (ADR_036) | entre módulos (§8 → §9) | ADR_161 (proposta) | USID_044 | `[PROPOSTO]` | CP-88 |
| RE-141 | §8 | CL-065 `ResumoArquivo` | associação `--` | CL-066 `Ocorrencia` | ocorrenciaIds | no módulo | ADR_160 (proposta) | — | `[PROPOSTO]` | CP-72, CP-73 |
| RE-142 | §8 | CL-066 `Ocorrencia` | associação dirigida `-->` | CL-039 `Arquivo` | arquivoId | entre módulos (§8 → §5) | tabela do §8 | — | `[CONFIRMADO]` | — |
| RE-143 | §8 | CL-066 `Ocorrencia` | associação `--` | CL-068 `Sugestao` | — | entre módulos (§8 → §9) | multiplicidade da fonte (DER v9 / ADR) | — | `[CONFIRMADO]` | — |
| RE-144 | §8 | CL-067 `Mapper` | dependência `..>` | CL-060 `AchadoAnalise` | converter | entre módulos (§8 → §7) | pauta FIN-09; ADR_040 | — | `[CONFIRMADO]` | — |
| RE-145 | §8 | CL-067 `Mapper` | dependência `..>` | CL-066 `Ocorrencia` | cria | no módulo | pauta FIN-09; ADR_040 | SSID_010 | `[CONFIRMADO]` | — |
| RE-146 | §9 | CL-001 `Tenant` | associação `--` | CL-074 `ChaveLLMTenant` | byok | entre módulos (§1 → §9) | multiplicidade da fonte (DER v9 / ADR) | — | `[CONFIRMADO]` | — |
| RE-147 | §9 | CL-068 `Sugestao` | associação `--` | CL-069 `AvaliacaoSugestao` | avaliacoes | no módulo | multiplicidade da fonte (DER v9 / ADR) | USID_046 | `[CONFLITO]` | CP-83 |
| RE-148 | §9 | CL-068 `Sugestao` | associação dirigida `-->` | CL-066 `Ocorrencia` | ocorrencia_id | entre módulos (§9 → §8) | multiplicidade da fonte (DER v9 / ADR) | — | `[CONFIRMADO]` | — |
| RE-149 | §9 | CL-068 `Sugestao` | associação dirigida `-->` | ES-21 `StatusSugestao` | — | no módulo | campo `StatusSugestao status` | USID_045, USID_046, USID_047 | `[CONFIRMADO]` | — |
| RE-150 | §9 | CL-069 `AvaliacaoSugestao` | associação dirigida `-->` | CL-002 `Membro` | membroId | entre módulos (§9 → §1) | ADR_159 (proposta) | — | `[PROPOSTO]` | CP-07, CP-82 |
| RE-151 | §9 | CL-070 `ContextoSugestao` | associação dirigida `-->` | CL-007 `ContextoEmpresa` | contextoEmpresarial | entre módulos (§9 → §1) | campo `ContextoEmpresa contextoEmpresarial` | SSID_015 | `[CONFIRMADO]` | — |
| RE-152 | §9 | CL-070 `ContextoSugestao` | associação dirigida `-->` | CL-005 `ContextoProduto` | — | entre módulos (§9 → §1) | campo `ContextoProduto contextoProduto` | SSID_015 | `[CONFIRMADO]` | — |
| RE-153 | §9 | CL-070 `ContextoSugestao` | associação dirigida `-->` | CL-066 `Ocorrencia` | ocorrencia_id | entre módulos (§9 → §8) | tabela do §9 | — | `[CONFIRMADO]` | — |
| RE-154 | §9 | CL-071 `GatewayLLMSugestao` | dependência `..>` | CL-074 `ChaveLLMTenant` | escolhe a credencial | no módulo | tabela do §9 | SSID_020 | `[PENDENTE]` | CP-86 |
| RE-155 | §9 | CL-071 `GatewayLLMSugestao` | dependência `..>` | CL-073 `RespostaLLM` | — | no módulo | método `solicitar(String prompt) RespostaLLM` | SSID_020 | `[CONFIRMADO]` | — |
| RE-156 | §9 | CL-072 `GatewayLLMPadrao` | realização `..|>` | CL-071 `GatewayLLMSugestao` | — | no módulo | implementação da interface | SSID_020 | `[PENDENTE]` | CP-85 |
| RE-157 | §9 | CL-072 `GatewayLLMPadrao` | dependência `..>` | CL-073 `RespostaLLM` | solicitar | no módulo | método `solicitar(String prompt) RespostaLLM` | SSID_020 | `[CONFIRMADO]` | — |
| RE-158 | §9 | CL-075 `ModuloSugestao` | dependência `..>` | CL-070 `ContextoSugestao` | montarPrompt | no módulo | ADR_156 (proposta) | SSID_015, USID_044 | `[PROPOSTO]` | CP-88 |
| RE-159 | §9 | CL-075 `ModuloSugestao` | dependência `..>` | CL-071 `GatewayLLMSugestao` | solicitar | no módulo | ADR_156 (proposta) | SSID_020 | `[PROPOSTO]` | CP-88 |
| RE-160 | §9 | CL-075 `ModuloSugestao` | dependência `..>` | CL-030 `Saldo` | reserva e liquida | entre módulos (§9 → §4) | ADR_157 (proposta) | SSID_020, USID_044 | `[PROPOSTO]` | CP-30, CP-88 |
| RE-161 | §9 | CL-075 `ModuloSugestao` | dependência `..>` | CL-068 `Sugestao` | cria (automatica e manual) | no módulo | ADR_156 (proposta) | USID_044 | `[PROPOSTO]` | CP-88 |
| RE-162 | §10 | CL-002 `Membro` | associação `--` | CL-076 `Notificacao` | recebe por papel | entre módulos (§1 → §10) | multiplicidade da fonte (DER v9 / ADR) | — | `[PROPOSTO]` | CP-92 |
| RE-163 | §10 | CL-076 `Notificacao` | associação dirigida `-->` | ES-22 `CanalNotificacao` | — | no módulo | campo `CanalNotificacao canal` | USID_009, USID_010, USID_011 | `[CONFIRMADO]` | — |
| RE-164 | §10 | CL-076 `Notificacao` | associação dirigida `-->` | CL-066 `Ocorrencia` | ocorrencia_id | entre módulos (§10 → §8) | tabela do §10 | SSID_009 | `[CONFIRMADO]` | — |
| RE-165 | §10 | CL-076 `Notificacao` | associação dirigida `-->` | CL-068 `Sugestao` | sugestao_id | entre módulos (§10 → §9) | multiplicidade da fonte (DER v9 / ADR) | — | `[CONFIRMADO]` | — |
| RE-166 | §10 | CL-076 `Notificacao` | associação `--` | CL-084 `TentativaEntrega` | entregas | no módulo | campo `TentativaEntrega tentativaEntrega` | SSID_009, USID_009, USID_010, USID_011 | `[CONFLITO]` | CP-99 |
| RE-167 | §10 | CL-077 `PreferenciaNotificacao` | dependência `..>` | ES-22 `CanalNotificacao` | habilitarCanal / desabilitarCanal / possuiCanalHabilitado | no módulo | método `habilitarCanal(CanalNotificacao canal) void` | USID_009, USID_010, USID_011, USID_012 | `[PROPOSTO]` | CP-96 |
| RE-168 | §10 | CL-077 `PreferenciaNotificacao` | associação dirigida `-->` | CL-002 `Membro` | membroId | entre módulos (§10 → §1) | ADR_159 (proposta) | — | `[PROPOSTO]` | CP-92, CP-96 |
| RE-169 | §10 | CL-078 `GatewayNotificacao` | dependência `..>` | CL-076 `Notificacao` | enviar | no módulo | método `enviar(Notificacao notificacao) TentativaEntrega` | SSID_019 | `[CONFIRMADO]` | — |
| RE-170 | §10 | CL-078 `GatewayNotificacao` | dependência `..>` | CL-084 `TentativaEntrega` | enviar | no módulo | método `enviar(Notificacao notificacao) TentativaEntrega` | — | `[CONFIRMADO]` | — |
| RE-171 | §10 | CL-079 `GatewayNotificacaoFactory` | dependência `..>` | ES-22 `CanalNotificacao` | obterGateway | no módulo | método `obterGateway(CanalNotificacao canal) GatewayNotificacao` | — | `[CONFIRMADO]` | — |
| RE-172 | §10 | CL-079 `GatewayNotificacaoFactory` | dependência `..>` | CL-078 `GatewayNotificacao` | obterGateway | no módulo | método `obterGateway(CanalNotificacao canal) GatewayNotificacao` | SSID_019 | `[CONFIRMADO]` | — |
| RE-173 | §10 | CL-080 `EnviadorEmail` | realização `..|>` | CL-078 `GatewayNotificacao` | — | no módulo | implementação da interface | — | `[CONFIRMADO]` | — |
| RE-174 | §10 | CL-080 `EnviadorEmail` | dependência `..>` | CL-076 `Notificacao` | enviar | no módulo | método `enviar(Notificacao notificacao) StatusEnvioNotificacao` | USID_009 | `[CONFIRMADO]` | — |
| RE-175 | §10 | CL-080 `EnviadorEmail` | dependência `..>` | ES-24 `StatusEnvioNotificacao` | — | no módulo | método `enviar(Notificacao notificacao) StatusEnvioNotificacao` | USID_009 | `[CONFIRMADO]` | — |
| RE-176 | §10 | CL-081 `EnviadorPush` | dependência `..>` | CL-083 `DispositivoPush` | obterDispositivos | no módulo | método `obterDispositivos(UUID membroId) List<DispositivoPush>` | USID_010 | `[CONFIRMADO]` | — |
| RE-177 | §10 | CL-081 `EnviadorPush` | realização `..|>` | CL-078 `GatewayNotificacao` | — | no módulo | implementação da interface | — | `[CONFIRMADO]` | — |
| RE-178 | §10 | CL-081 `EnviadorPush` | dependência `..>` | CL-076 `Notificacao` | enviar | no módulo | método `enviar(Notificacao notificacao) StatusEnvioNotificacao` | USID_010, USID_014 | `[CONFIRMADO]` | — |
| RE-179 | §10 | CL-081 `EnviadorPush` | dependência `..>` | ES-24 `StatusEnvioNotificacao` | — | no módulo | método `enviar(Notificacao notificacao) StatusEnvioNotificacao` | USID_010 | `[CONFIRMADO]` | — |
| RE-180 | §10 | CL-082 `EnviadorWeb` | realização `..|>` | CL-078 `GatewayNotificacao` | — | no módulo | implementação da interface | — | `[CONFIRMADO]` | — |
| RE-181 | §10 | CL-082 `EnviadorWeb` | dependência `..>` | CL-076 `Notificacao` | enviar | no módulo | método `enviar(Notificacao notificacao) StatusEnvioNotificacao` | USID_011, USID_013 | `[CONFIRMADO]` | — |
| RE-182 | §10 | CL-082 `EnviadorWeb` | dependência `..>` | ES-24 `StatusEnvioNotificacao` | — | no módulo | método `enviar(Notificacao notificacao) StatusEnvioNotificacao` | USID_011 | `[CONFIRMADO]` | — |
| RE-183 | §10 | CL-083 `DispositivoPush` | associação dirigida `-->` | CL-002 `Membro` | membroId | entre módulos (§10 → §1) | ADR_159 (proposta) | — | `[PROPOSTO]` | CP-92 |
| RE-184 | §10 | CL-083 `DispositivoPush` | associação dirigida `-->` | ES-23 `PlataformaDispositivo` | — | no módulo | campo `PlataformaDispositivo plataforma` | USID_010 | `[CONFIRMADO]` | — |
| RE-185 | §10 | CL-084 `TentativaEntrega` | associação dirigida `-->` | ES-24 `StatusEnvioNotificacao` | — | no módulo | campo `StatusEnvioNotificacao status_envio` | USID_009, USID_010, USID_011 | `[CONFIRMADO]` | CP-98 |
| RE-186 | §11 | CL-087 `FiltroDashboard` | agregação `o--` | CL-085 `Metrica` | metricasSelecionadas | no módulo | campo `List<Metrica> metricasSelecionadas` | — | `[CONFIRMADO]` | — |
| RE-187 | §11 | CL-087 `FiltroDashboard` | associação dirigida `-->` | CL-086 `Periodo` | — | no módulo | campo `Periodo periodo` | USID_032, USID_036 | `[CONFIRMADO]` | — |
| RE-188 | §11 | CL-087 `FiltroDashboard` | associação dirigida `-->` | CL-004 `Produto` | — | entre módulos (§11 → §1) | campo `Produto produto` | — | `[CONFIRMADO]` | — |
| RE-189 | §11 | CL-088 `DashboardProduto` | associação dirigida `-->` | CL-087 `FiltroDashboard` | filtro | no módulo | campo `FiltroDashboard filtro` | USID_032 | `[CONFIRMADO]` | — |
| RE-190 | §11 | CL-088 `DashboardProduto` | dependência `..>` | CL-085 `Metrica` | obterMetricas | no módulo | método `obterMetricas() List<Metrica>` | USID_031 | `[CONFIRMADO]` | — |
| RE-191 | §11 | CL-088 `DashboardProduto` | associação dirigida `-->` | CL-004 `Produto` | — | entre módulos (§11 → §1) | campo `Produto produto` | — | `[CONFIRMADO]` | — |
| RE-192 | §11 | CL-089 `DashboardEmpresarial` | dependência `..>` | CL-088 `DashboardProduto` | selecionarProduto | no módulo | método `selecionarProduto(Produto produto) DashboardProduto` | — | `[CONFIRMADO]` | — |
| RE-193 | §11 | CL-089 `DashboardEmpresarial` | associação dirigida `-->` | CL-008 `Empresa` | — | entre módulos (§11 → §1) | campo `Empresa empresa` | — | `[PROPOSTO]` | CP-06, CP-107 |
| RE-194 | §11 | CL-089 `DashboardEmpresarial` | associação dirigida `-->` | CL-087 `FiltroDashboard` | filtro | no módulo | campo `FiltroDashboard filtro` | USID_036 | `[CONFIRMADO]` | — |
| RE-195 | §11 | CL-089 `DashboardEmpresarial` | agregação `o--` | CL-085 `Metrica` | metricasAgregadas | no módulo | campo `List<Metrica> metricasAgregadas` | USID_034 | `[CONFIRMADO]` | — |
| RE-196 | §11 | CL-089 `DashboardEmpresarial` | associação dirigida `-->` | CL-004 `Produto` | produtosAutorizados | entre módulos (§11 → §1) | campo `List<Produto> produtosAutorizados` | — | `[CONFIRMADO]` | CP-06 |
| RE-197 | §11 | CL-090 `FiltroOcorrenciaEmpresarial` | dependência `..>` | CL-066 `Ocorrencia` | consulta | entre módulos (§11 → §8) | ADR_162 (proposta) | USID_037 | `[PROPOSTO]` | — |
| RE-198 | §11 | CL-090 `FiltroOcorrenciaEmpresarial` | associação dirigida `-->` | CL-086 `Periodo` | — | no módulo | campo `Periodo periodo` | — | `[CONFIRMADO]` | — |
| RE-199 | §11 | CL-090 `FiltroOcorrenciaEmpresarial` | associação dirigida `-->` | CL-004 `Produto` | produtos | entre módulos (§11 → §1) | campo `List<Produto> produtos` | — | `[CONFIRMADO]` | — |
| RE-200 | §11 | CL-091 `ResumoDashboardMobile` | agregação `o--` | CL-085 `Metrica` | metricasPrincipais | no módulo | campo `List<Metrica> metricasPrincipais` | — | `[CONFIRMADO]` | — |
| RE-201 | §11 | CL-091 `ResumoDashboardMobile` | associação dirigida `-->` | CL-086 `Periodo` | — | no módulo | campo `Periodo periodo` | — | `[CONFIRMADO]` | — |
| RE-202 | §11 | CL-091 `ResumoDashboardMobile` | associação dirigida `-->` | CL-004 `Produto` | — | entre módulos (§11 → §1) | campo `Produto produto` | — | `[CONFIRMADO]` | — |
| RE-203 | §11 | CL-092 `Agregacao` | agregação `o--` | CL-085 `Metrica` | metricas | no módulo | campo `List<Metrica> metricas` | USID_034 | `[CONFIRMADO]` | CP-103 |
| RE-204 | §11 | CL-092 `Agregacao` | associação dirigida `-->` | CL-086 `Periodo` | — | no módulo | campo `Periodo periodo` | SSID_011 | `[CONFIRMADO]` | — |
| RE-205 | §12 | CL-093 `RelatorioDashboard` | associação dirigida `-->` | CL-088 `DashboardProduto` | dashboard | entre módulos (§12 → §11) | campo `DashboardProduto dashboard` | — | `[CONFIRMADO]` | — |
| RE-206 | §12 | CL-093 `RelatorioDashboard` | associação dirigida `-->` | CL-087 `FiltroDashboard` | filtroAplicado | entre módulos (§12 → §11) | campo `FiltroDashboard filtroAplicado` | — | `[CONFIRMADO]` | — |
| RE-207 | §12 | CL-093 `RelatorioDashboard` | agregação `o--` | CL-085 `Metrica` | — | entre módulos (§12 → §11) | campo `List<Metrica> metricas` | — | `[CONFIRMADO]` | — |
| RE-208 | §12 | CL-093 `RelatorioDashboard` | associação dirigida `-->` | CL-086 `Periodo` | — | entre módulos (§12 → §11) | campo `Periodo periodo` | — | `[CONFIRMADO]` | — |
| RE-209 | §12 | CL-094 `RelatorioEmpresarial` | associação dirigida `-->` | CL-089 `DashboardEmpresarial` | dashboard | entre módulos (§12 → §11) | campo `DashboardEmpresarial dashboard` | — | `[CONFIRMADO]` | CP-06 |
| RE-210 | §12 | CL-094 `RelatorioEmpresarial` | associação dirigida `-->` | CL-008 `Empresa` | — | entre módulos (§12 → §1) | campo `Empresa empresa` | — | `[PROPOSTO]` | CP-06, CP-111 |
| RE-211 | §12 | CL-094 `RelatorioEmpresarial` | agregação `o--` | CL-085 `Metrica` | — | entre módulos (§12 → §11) | campo `List<Metrica> metricasAgregadas` | — | `[CONFIRMADO]` | — |
| RE-212 | §12 | CL-094 `RelatorioEmpresarial` | associação dirigida `-->` | CL-086 `Periodo` | — | entre módulos (§12 → §11) | campo `Periodo periodo` | — | `[CONFIRMADO]` | — |
| RE-213 | §12 | CL-094 `RelatorioEmpresarial` | associação dirigida `-->` | CL-004 `Produto` | produtosAutorizados | entre módulos (§12 → §1) | campo `List<Produto> produtosAutorizados` | — | `[CONFIRMADO]` | CP-06 |
| RE-214 | §12 | CL-095 `RelatorioConsolidado` | agregação `o--` | CL-092 `Agregacao` | — | entre módulos (§12 → §11) | campo `List<Agregacao> agregacoes` | SSID_011 | `[CONFIRMADO]` | — |
| RE-215 | §12 | CL-095 `RelatorioConsolidado` | agregação `o--` | CL-085 `Metrica` | — | entre módulos (§12 → §11) | campo `List<Metrica> metricas` | — | `[CONFIRMADO]` | — |
| RE-216 | §12 | CL-095 `RelatorioConsolidado` | associação dirigida `-->` | CL-086 `Periodo` | — | entre módulos (§12 → §11) | campo `Periodo periodo` | SSID_011 | `[CONFIRMADO]` | — |
| RE-217 | §12 | CL-095 `RelatorioConsolidado` | associação dirigida `-->` | CL-004 `Produto` | — | entre módulos (§12 → §1) | campo `Produto produto` | — | `[CONFIRMADO]` | — |
| RE-218 | §12 | CL-096 `ExportacaoRelatorio` | associação dirigida `-->` | ES-25 `FormatoArquivo` | — | no módulo | campo `FormatoArquivo formato` | USID_033, USID_035 | `[CONFIRMADO]` | — |
| RE-219 | §12 | CL-096 `ExportacaoRelatorio` | dependência `..>` | CL-093 `RelatorioDashboard` | exportar | no módulo | método `exportar(RelatorioDashboard relatorio) void` | USID_033 | `[CONFIRMADO]` | — |
| RE-220 | §12 | CL-096 `ExportacaoRelatorio` | dependência `..>` | CL-094 `RelatorioEmpresarial` | exportarEmpresarial | no módulo | método `exportarEmpresarial(RelatorioEmpresarial relatorio) void` | USID_035 | `[CONFIRMADO]` | — |
| RE-221 | §12 | CL-097 `GeracaoRelatorioAgendada` | associação dirigida `-->` | CL-086 `Periodo` | — | entre módulos (§12 → §11) | campo `Periodo periodo` | SSID_011 | `[CONFIRMADO]` | — |
| RE-222 | §12 | CL-097 `GeracaoRelatorioAgendada` | associação dirigida `-->` | CL-095 `RelatorioConsolidado` | relatorio | no módulo | campo `RelatorioConsolidado relatorio` | SSID_011 | `[CONFIRMADO]` | — |
| RE-223 | §12 | CL-098 `GeradorArquivo` | dependência `..>` | ES-25 `FormatoArquivo` | — | no módulo | método `gerar(RelatorioDashboard relatorio, FormatoArquivo formato) String` | USID_033, USID_035 | `[CONFIRMADO]` | — |
| RE-224 | §12 | CL-098 `GeradorArquivo` | dependência `..>` | CL-093 `RelatorioDashboard` | — | no módulo | método `gerar(RelatorioDashboard relatorio, FormatoArquivo formato) String` | USID_033 | `[CONFIRMADO]` | — |
| RE-225 | §12 | CL-098 `GeradorArquivo` | dependência `..>` | CL-094 `RelatorioEmpresarial` | — | no módulo | método `gerarEmpresarial(RelatorioEmpresarial relatorio, FormatoArquivo formato) String` | USID_035 | `[CONFIRMADO]` | — |
| RE-226 | §13 | CL-099 `LogSDK` | associação dirigida `-->` | CL-105 `ClienteColetor` | — | no módulo | campo `ClienteColetor cliente_coletor` | USID_015 | `[LEGADO]` | — |
| RE-227 | §13 | CL-099 `LogSDK` | associação dirigida `-->` | CL-100 `ConfiguracaoSdk` | — | no módulo | campo `ConfiguracaoSdk configuracao` | USID_015 | `[LEGADO]` | — |
| RE-228 | §13 | CL-099 `LogSDK` | dependência `..>` | CL-103 `EventoLog` | registrarEvento | no módulo | tabela do §13 | — | `[LEGADO]` | — |
| RE-229 | §13 | CL-099 `LogSDK` | associação dirigida `-->` | CL-109 `RedatorDadosSensiveis` | — | no módulo | campo `RedatorDadosSensiveis redator` | — | `[LEGADO]` | — |
| RE-230 | §13 | CL-099 `LogSDK` | dependência `..>` | CL-112 `ResultadoConexao` | — | no módulo | método `testarConexao() ResultadoConexao` | — | `[LEGADO]` | — |
| RE-231 | §13 | CL-099 `LogSDK` | dependência `..>` | CL-111 `ResultadoEnvio` | — | no módulo | método `registrarEvento() ResultadoEnvio` | — | `[LEGADO]` | — |
| RE-232 | §13 | CL-099 `LogSDK` | associação dirigida `-->` | CL-107 `ValidadorEventoLog` | — | no módulo | campo `ValidadorEventoLog validador` | — | `[LEGADO]` | — |
| RE-233 | §13 | CL-100 `ConfiguracaoSdk` | associação dirigida `-->` | CL-101 `CredencialIngestao (SDK)` | credencial | no módulo | campo `CredencialIngestao credencial` | — | `[LEGADO]` | — |
| RE-234 | §13 | CL-100 `ConfiguracaoSdk` | associação dirigida `-->` | CL-102 `IdentificadorProduto` | produto_id | no módulo | campo `IdentificadorProduto produto_id` | USID_015 | `[LEGADO]` | — |
| RE-235 | §13 | CL-100 `ConfiguracaoSdk` | dependência `..>` | CL-108 `ResultadoValidacao` | — | no módulo | método `validar() ResultadoValidacao` | — | `[LEGADO]` | — |
| RE-236 | §13 | CL-102 `IdentificadorProduto` | dependência `..>` | CL-004 `Produto` | — | entre módulos (§13 → §1) | tabela do §13 | USID_015 | `[CONFIRMADO]` | — |
| RE-237 | §13 | CL-104 `EnvelopeIngestao` | associação dirigida `-->` | CL-103 `EventoLog` | — | no módulo | campo `EventoLog evento` | SSID_001 | `[LEGADO]` | — |
| RE-238 | §13 | CL-104 `EnvelopeIngestao` | associação dirigida `-->` | CL-102 `IdentificadorProduto` | — | no módulo | campo `IdentificadorProduto produto_id` | — | `[LEGADO]` | — |
| RE-239 | §13 | CL-105 `ClienteColetor` | dependência `..>` | CL-033 `Coletor` | transmite | entre módulos (§13 → §5) | tabela do §13 | SSID_001 | `[CONFIRMADO]` | — |
| RE-240 | §13 | CL-105 `ClienteColetor` | dependência `..>` | CL-110 `RespostaColetor` | — | no módulo | método `transmitir() RespostaColetor` | SSID_001 | `[LEGADO]` | — |
| RE-241 | §13 | CL-105 `ClienteColetor` | dependência `..>` | CL-112 `ResultadoConexao` | — | no módulo | método `testarConexao() ResultadoConexao` | SSID_001 | `[LEGADO]` | — |
| RE-242 | §13 | CL-106 `SerializadorIngestao` | dependência `..>` | CL-104 `EnvelopeIngestao` | serializa | no módulo | tabela do §13 | SSID_001 | `[LEGADO]` | — |
| RE-243 | §13 | CL-107 `ValidadorEventoLog` | dependência `..>` | CL-108 `ResultadoValidacao` | — | no módulo | método `validar() ResultadoValidacao` | SSID_001 | `[LEGADO]` | — |
| RE-244 | §13 | CL-109 `RedatorDadosSensiveis` | dependência `..>` | CL-103 `EventoLog` | redigir | no módulo | método `redigir(EventoLog evento) EventoLog` | — | `[LEGADO]` | — |
| RE-245 | §13 | CL-113 `Executavel` | dependência `..>` | CL-114 `FonteTelemetria` | substituida por | no módulo | substituição (DER v9 / ADR) | — | `[SUBSTITUÍDA]` | CP-113 |
| RE-246 | §13 | CL-113 `Executavel` | associação dirigida `-->` | CL-004 `Produto` | produto_id | entre módulos (§13 → §1) | tabela do §13 | — | `[CONFIRMADO]` | — |
| RE-247 | §13 | CL-113 `Executavel` | associação dirigida `-->` | ES-26 `SistemaOperacional` | — | no módulo | campo `SistemaOperacional sistema_operacional` | USID_018 | `[LEGADO]` | — |
| RE-248 | §13 | CL-113 `Executavel` | associação dirigida `-->` | ES-27 `StatusExecutavel` | — | no módulo | campo `StatusExecutavel status` | USID_019, USID_020 | `[LEGADO]` | — |

## 10. Matriz de cardinalidades

| ID | Relação | Origem | Mult. origem | Mult. destino | Destino | Rótulo | Situação |
|---|---|---|---|---|---|---|---|
| CA-01 | RE-001 | `Tenant` | 1 | 1 | `Empresa` | cadastro | `[PROPOSTO]` |
| CA-02 | RE-002 | `Tenant` | 1 | 0..* | `Membro` | membros | `[PENDENTE]` |
| CA-03 | RE-003 | `Tenant` | 1 | 0..* | `Produto` | produtos | `[CONFIRMADO]` |
| CA-04 | RE-004 | `Membro` | 1 | 0..* | `AcessoProduto` | recebe | `[CONFIRMADO]` |
| CA-05 | RE-005 | `Produto` | 1 | 0..* | `AcessoProduto` | libera | `[CONFIRMADO]` |
| CA-06 | RE-006 | `Produto` | 1 | 0..* | `ConfiguracaoProduto` | configura | `[CONFIRMADO]` |
| CA-07 | RE-011 | `Empresa` | 1 | 0..* | `Endereco` | possui | `[CONFLITO]` |
| CA-08 | RE-017 | `Tenant` | 1 | 0..* | `PapelNotificacao` | define | `[CONFIRMADO]` |
| CA-09 | RE-018 | `Membro` | 0..* | 0..* | `PapelNotificacao` | participa | `[CONFIRMADO]` |
| CA-10 | RE-019 | `PapelNotificacao` | 1 | 1..* | `PapelSeveridade` | gravidades | `[CONFIRMADO]` |
| CA-11 | RE-020 | `PapelNotificacao` | 1 | 1..* | `PapelTipoAlerta` | tipos de alerta | `[CONFIRMADO]` |
| CA-12 | RE-021 | `Tenant` | 1 | 1 | `Assinatura` | possui | `[CONFIRMADO]` |
| CA-13 | RE-022 | `Tenant` | 1 | 0..* | `EventoGateway` | eventos | `[CONFIRMADO]` |
| CA-14 | RE-030 | `Plano` | 1 | 0..* | `Assinatura` | plano | `[CONFIRMADO]` |
| CA-15 | RE-035 | `TabelaPrecificacao` | 1 | 0..* | `Assinatura` | preco | `[CONFIRMADO]` |
| CA-16 | RE-036 | `Assinatura` | 1 | 0..* | `Pagamento` | cobrancas | `[PROPOSTO]` |
| CA-17 | RE-047 | `Pagamento` | 1 | 0..* | `Reembolso` | reembolso | `[CONFIRMADO]` |
| CA-18 | RE-049 | `Reembolso` | 0..1 | 0..* | `EventoGateway` | eventos | `[CONFIRMADO]` |
| CA-19 | RE-056 | `Saldo` | — | 0..* | `Credito` | creditos | `[CONFIRMADO]` |
| CA-20 | RE-069 | `Produto` | 1 | 0..* | `Produtor` | produtores | `[CONFIRMADO]` |
| CA-21 | RE-079 | `LoteAgrupador` | 1 | 1..* | `LogRecebido` | agrupa | `[CONFIRMADO]` |
| CA-22 | RE-081 | `Arquivo` | 1 | 1..* | `Trace` | agrupa | `[CONFLITO]` |
| CA-23 | RE-082 | `Trace` | 0..* | 1..* | `Modulo` | passa por | `[CONFIRMADO]` |
| CA-24 | RE-084 | `Produtor` | 1 | 0..* | `TokenApi` | tokens | `[PROPOSTO]` |
| CA-25 | RE-086 | `Produto` | 1 | 1 | `FilaDesordenada` | uma fila por Produto | `[CONFIRMADO]` |
| CA-26 | RE-087 | `Trace` | 0..* | 1..* | `Modulo` | service.name | `[CONFIRMADO]` |
| CA-27 | RE-090 | `Varredura` | 1 | 0..* | `ArquivoVarredura` | processa | `[CONFLITO]` |
| CA-28 | RE-103 | `AgendamentoVarredura` | 0..1 | 0..* | `Varredura` | dispara | `[CONFIRMADO]` |
| CA-29 | RE-109 | `Modulo` | 0..1 | 0..* | `AchadoAnalise` | afeta | `[CONFIRMADO]` |
| CA-30 | RE-127 | `AchadoAnalise` | 0..* | 1 | `Trace` | traceId | `[CONFLITO]` |
| CA-31 | RE-132 | `Arquivo` | 1 | 0..1 | `ResumoArquivo` | resumo | `[CONFIRMADO]` |
| CA-32 | RE-141 | `ResumoArquivo` | 1 | 0..* | `Ocorrencia` | ocorrenciaIds | `[PROPOSTO]` |
| CA-33 | RE-143 | `Ocorrencia` | 1 | 0..* | `Sugestao` | — | `[CONFIRMADO]` |
| CA-34 | RE-146 | `Tenant` | 1 | 0..* | `ChaveLLMTenant` | byok | `[CONFIRMADO]` |
| CA-35 | RE-147 | `Sugestao` | 1 | 0..* | `AvaliacaoSugestao` | avaliacoes | `[CONFLITO]` |
| CA-36 | RE-148 | `Sugestao` | 0..* | 1 | `Ocorrencia` | ocorrencia_id | `[CONFIRMADO]` |
| CA-37 | RE-150 | `AvaliacaoSugestao` | 0..* | 1 | `Membro` | membroId | `[PROPOSTO]` |
| CA-38 | RE-162 | `Membro` | 1 | 0..* | `Notificacao` | recebe por papel | `[PROPOSTO]` |
| CA-39 | RE-165 | `Notificacao` | — | 0..1 | `Sugestao` | sugestao_id | `[CONFIRMADO]` |
| CA-40 | RE-166 | `Notificacao` | 1 | 0..* | `TentativaEntrega` | entregas | `[CONFLITO]` |
| CA-41 | RE-196 | `DashboardEmpresarial` | — | 0..* | `Produto` | produtosAutorizados | `[CONFIRMADO]` |
| CA-42 | RE-199 | `FiltroOcorrenciaEmpresarial` | — | 0..* | `Produto` | produtos | `[CONFIRMADO]` |
| CA-43 | RE-213 | `RelatorioEmpresarial` | — | 0..* | `Produto` | produtosAutorizados | `[CONFIRMADO]` |

## 11. Matriz de operações

| ID | Classe | § | Assinatura | Visibilidade | Requisitos (pela classe) | Situação | Pendências |
|---|---|---|---|---|---|---|---|
| OP-001 | CL-004 `Produto` | §1 | `ativar() void` | público | USID_024, USID_015, USID_016, USID_023 | `[CONFIRMADO]` | — |
| OP-002 | CL-004 `Produto` | §1 | `suspender() void` | público | USID_024, USID_015, USID_016, USID_023 | `[CONFIRMADO]` | — |
| OP-003 | CL-004 `Produto` | §1 | `estaConfigurado() boolean` | público | USID_024, USID_015, USID_016, USID_023 | `[CONFIRMADO]` | — |
| OP-004 | CL-005 `ContextoProduto` | §1 | `EstaCompleto() bool` | público | USID_023, SSID_015 | `[CONFIRMADO]` | — |
| OP-005 | CL-005 `ContextoProduto` | §1 | `CombinarComContextoEmpresa(ContextoEmpresa contexto) string` | público | USID_023, SSID_015 | `[CONFIRMADO]` | — |
| OP-006 | CL-005 `ContextoProduto` | §1 | `AtualizarContexto() void` | público | USID_023, SSID_015 | `[CONFIRMADO]` | — |
| OP-007 | CL-006 `ConfiguracaoProduto` | §1 | `EstaPreenchida() bool` | público | USID_024, USID_027 (inferido) | `[CONFIRMADO]` | — |
| OP-008 | CL-006 `ConfiguracaoProduto` | §1 | `ValidarValor() bool` | público | USID_024, USID_027 (inferido) | `[CONFIRMADO]` | — |
| OP-009 | CL-006 `ConfiguracaoProduto` | §1 | `AtualizarValor(string novo_valor) bool` | público | USID_024, USID_027 (inferido) | `[CONFIRMADO]` | — |
| OP-010 | CL-006 `ConfiguracaoProduto` | §1 | `ObterValorExibicao() string` | público | USID_024, USID_027 (inferido) | `[CONFIRMADO]` | — |
| OP-011 | CL-007 `ContextoEmpresa` | §1 | `gerarPrompt() string` | público | USID_022, SSID_015 | `[CONFIRMADO]` | — |
| OP-012 | CL-007 `ContextoEmpresa` | §1 | `toJson() string` | privado | USID_022, SSID_015 | `[CONFIRMADO]` | — |
| OP-013 | CL-007 `ContextoEmpresa` | §1 | `fromJson(string json)` | privado | USID_022, SSID_015 | `[CONFIRMADO]` | — |
| OP-014 | CL-007 `ContextoEmpresa` | §1 | `estaCompleto() boolean` | privado | USID_022, SSID_015 | `[CONFIRMADO]` | — |
| OP-015 | CL-008 `Empresa` | §1 | `FormatarCnpj()` | privado | USID_021 | `[CONFIRMADO]` | — |
| OP-016 | CL-008 `Empresa` | §1 | `CadastrarEmpresa()` | público | USID_021 | `[CONFIRMADO]` | — |
| OP-017 | CL-009 `Endereco` | §1 | `FormatarEnderecoCompleto() string` | público | USID_021 (inferido) | `[CONFIRMADO]` | — |
| OP-018 | CL-009 `Endereco` | §1 | `ValidarEndereco() bool` | público | USID_021 (inferido) | `[CONFIRMADO]` | — |
| OP-019 | CL-009 `Endereco` | §1 | `DefinirComoPrincipal() void` | público | USID_021 (inferido) | `[CONFIRMADO]` | — |
| OP-020 | CL-009 `Endereco` | §1 | `EhInternacional() bool` | público | USID_021 (inferido) | `[CONFIRMADO]` | — |
| OP-021 | CL-017 `GerenciadorAssinatura` | §3 | `listarPlanosDisponiveis() List<Plano>` | público | USID_039, USID_040, USID_041, USID_042, USID_043, SSID_016 | `[CONFIRMADO]` | — |
| OP-022 | CL-017 `GerenciadorAssinatura` | §3 | `contratarPlano(UUID empresa_id, Plano plano) Assinatura` | público | USID_039, USID_040, USID_041, USID_042, USID_043, SSID_016 | `[CONFIRMADO]` | — |
| OP-023 | CL-017 `GerenciadorAssinatura` | §3 | `contratarPlano(String tenantId, Plano plano) Assinatura` | público | USID_039, USID_040, USID_041, USID_042, USID_043, SSID_016 | `[CONFIRMADO]` | — |
| OP-024 | CL-017 `GerenciadorAssinatura` | §3 | `alterarAssinatura(String assinaturaId, Plano novoPlano) Assinatura` | público | USID_039, USID_040, USID_041, USID_042, USID_043, SSID_016 | `[PROPOSTO]` | CP-134 |
| OP-025 | CL-017 `GerenciadorAssinatura` | §3 | `cancelarAssinatura(String assinaturaId, Boolean imediato) void` | público | USID_039, USID_040, USID_041, USID_042, USID_043, SSID_016 | `[PROPOSTO]` | CP-134 |
| OP-026 | CL-017 `GerenciadorAssinatura` | §3 | `solicitarReembolso(String pagamentoId, String motivo) Reembolso` | público | USID_039, USID_040, USID_041, USID_042, USID_043, SSID_016 | `[CONFIRMADO]` | — |
| OP-027 | CL-017 `GerenciadorAssinatura` | §3 | `aplicarEventoDeAssinatura(String assinaturaId, TipoOperacaoGateway tipoOperacao, EventoGateway evento) void` | público | USID_039, USID_040, USID_041, USID_042, USID_043, SSID_016 | `[CONFIRMADO]` | — |
| OP-028 | CL-017 `GerenciadorAssinatura` | §3 | `verificarInadimplencia(UUID empresa_id) Boolean` | público | USID_039, USID_040, USID_041, USID_042, USID_043, SSID_016 | `[CONFIRMADO]` | — |
| OP-029 | CL-017 `GerenciadorAssinatura` | §3 | `verificarInadimplencia(String tenantId) Boolean` | público | USID_039, USID_040, USID_041, USID_042, USID_043, SSID_016 | `[CONFIRMADO]` | — |
| OP-030 | CL-017 `GerenciadorAssinatura` | §3 | `calcularValorProporcional(UUID empresa_id) Decimal` | privado | USID_039, USID_040, USID_041, USID_042, USID_043, SSID_016 | `[CONFIRMADO]` | — |
| OP-031 | CL-017 `GerenciadorAssinatura` | §3 | `calcularValorProporcional(String tenantId) Decimal` | privado | USID_039, USID_040, USID_041, USID_042, USID_043, SSID_016 | `[CONFIRMADO]` | — |
| OP-032 | CL-017 `GerenciadorAssinatura` | §3 | `validarTransicaoDeStatus(StatusAssinatura atual, StatusAssinatura novo) Boolean` | privado | USID_039, USID_040, USID_041, USID_042, USID_043, SSID_016 | `[CONFIRMADO]` | — |
| OP-033 | CL-022 `ProcessamentoPagamento` | §3 | `processarPagamento(String assinaturaId, Decimal valor) Pagamento` | público | SSID_016, SSID_018, USID_040 | `[CONFIRMADO]` | — |
| OP-034 | CL-022 `ProcessamentoPagamento` | §3 | `receberEventoGateway(EventoGateway evento) void` | público | SSID_016, SSID_018, USID_040 | `[CONFIRMADO]` | — |
| OP-035 | CL-022 `ProcessamentoPagamento` | §3 | `validarDadosEvento(EventoGateway evento) Boolean` | público | SSID_016, SSID_018, USID_040 | `[CONFIRMADO]` | — |
| OP-036 | CL-022 `ProcessamentoPagamento` | §3 | `reprocessarPagamentoFalho(String pagamentoId) StatusPagamento` | público | SSID_016, SSID_018, USID_040 | `[CONFIRMADO]` | — |
| OP-037 | CL-022 `ProcessamentoPagamento` | §3 | `validarAutenticidadeEvento(EventoGateway evento) Boolean` | privado | SSID_016, SSID_018, USID_040 | `[CONFIRMADO]` | — |
| OP-038 | CL-023 `GatewayPagamento` | §3 | `enviarCobranca(Object dados) EventoGateway` | público | SSID_018, USID_039 | `[CONFIRMADO]` | — |
| OP-039 | CL-023 `GatewayPagamento` | §3 | `consultarStatus(String referenciaExterna) StatusPagamento` | público | SSID_018, USID_039 | `[CONFIRMADO]` | — |
| OP-040 | CL-023 `GatewayPagamento` | §3 | `solicitarReembolsoExterno(String referenciaExterna, Decimal valor) EventoGateway` | público | SSID_018, USID_039 | `[CONFIRMADO]` | — |
| OP-041 | CL-023 `GatewayPagamento` | §3 | `validarAutenticidade(EventoGateway evento) Boolean` | público | SSID_018, USID_039 | `[CONFIRMADO]` | — |
| OP-042 | CL-024 `ApiPagamento` | §3 | `enviarCobranca(Object dados) EventoGateway` | público | SSID_018 | `[CONFIRMADO]` | — |
| OP-043 | CL-024 `ApiPagamento` | §3 | `consultarStatus(String referenciaExterna) StatusPagamento` | público | SSID_018 | `[CONFIRMADO]` | — |
| OP-044 | CL-024 `ApiPagamento` | §3 | `solicitarReembolsoExterno(String referenciaExterna, Decimal valor) EventoGateway` | público | SSID_018 | `[CONFIRMADO]` | — |
| OP-045 | CL-024 `ApiPagamento` | §3 | `validarAutenticidade(EventoGateway evento) Boolean` | público | SSID_018 | `[CONFIRMADO]` | — |
| OP-046 | CL-028 `Credito` | §4 | `foiBemSucedida() boolean` | público | USID_044 (inferido), SSID_020 | `[CONFIRMADO]` | — |
| OP-047 | CL-029 `PlanoCreditos` | §4 | `EhAtivo() bool` | privado | — | `[CONFIRMADO]` | — |
| OP-048 | CL-029 `PlanoCreditos` | §4 | `AtivarPlano() void` | público | — | `[CONFIRMADO]` | — |
| OP-049 | CL-029 `PlanoCreditos` | §4 | `DesativarPlano() void` | privado | — | `[CONFIRMADO]` | — |
| OP-050 | CL-029 `PlanoCreditos` | §4 | `GerarCreditos(datetime data_referencia) Credito` | público | — | `[CONFLITO]` | CP-33 |
| OP-051 | CL-030 `Saldo` | §4 | `ConsultarSaldo() integer` | público | USID_044 (inferido), SSID_020 | `[CONFIRMADO]` | — |
| OP-052 | CL-030 `Saldo` | §4 | `AdicionarCredito(Credito credito) void` | público | USID_044 (inferido), SSID_020 | `[CONFIRMADO]` | — |
| OP-053 | CL-030 `Saldo` | §4 | `SelecionarCreditosParaConsumo(integer quantidade) List<Credito>` | público | USID_044 (inferido), SSID_020 | `[CONFIRMADO]` | — |
| OP-054 | CL-030 `Saldo` | §4 | `AtualizarSaldo() void` | público | USID_044 (inferido), SSID_020 | `[CONFIRMADO]` | — |
| OP-055 | CL-031 `Transacao` | §4 | `FoiBemSucedida() bool` | público | SSID_020 | `[CONFIRMADO]` | — |
| OP-056 | CL-031 `Transacao` | §4 | `Registrar() bool` | público | SSID_020 | `[CONFIRMADO]` | — |
| OP-057 | CL-031 `Transacao` | §4 | `EhEstorno() bool` | público | SSID_020 | `[CONFIRMADO]` | — |
| OP-058 | CL-031 `Transacao` | §4 | `GerarEstorno() Transacao` | público | SSID_020 | `[CONFIRMADO]` | — |
| OP-059 | CL-032 `Controle` | §4 | `ColetarDados(Produto produto, integer quantidade) void` | público | SSID_020 | `[CONFIRMADO]` | — |
| OP-060 | CL-032 `Controle` | §4 | `AutorizarConsumo() bool` | público | SSID_020 | `[CONFIRMADO]` | — |
| OP-061 | CL-032 `Controle` | §4 | `ExecutarConsumo() Transacao` | público | SSID_020 | `[CONFIRMADO]` | — |
| OP-062 | CL-032 `Controle` | §4 | `ReverterOperacao(Transacao transacao) Transacao` | público | SSID_020 | `[CONFIRMADO]` | — |
| OP-063 | CL-033 `Coletor` | §5 | `ReceberLog() GerenciadorRequisicao` | público | SSID_001, SSID_002, SSID_003, USID_006 (inferido) | `[CONFIRMADO]` | — |
| OP-064 | CL-033 `Coletor` | §5 | `EnviarLote() List<Arquivo>` | público | SSID_001, SSID_002, SSID_003, USID_006 (inferido) | `[CONFIRMADO]` | — |
| OP-065 | CL-033 `Coletor` | §5 | `EnviarArquivo() Arquivo` | público | SSID_001, SSID_002, SSID_003, USID_006 (inferido) | `[CONFIRMADO]` | — |
| OP-066 | CL-034 `GerenciadorRequisicao` | §5 | `PersistirLog() void` | público | SSID_001, SSID_014, USID_016 | `[CONFIRMADO]` | — |
| OP-067 | CL-034 `GerenciadorRequisicao` | §5 | `ValidarContexto() boolean` | privado | SSID_001, SSID_014, USID_016 | `[CONFIRMADO]` | — |
| OP-068 | CL-034 `GerenciadorRequisicao` | §5 | `ValidarOrigem() boolean` | privado | SSID_001, SSID_014, USID_016 | `[CONFIRMADO]` | — |
| OP-069 | CL-034 `GerenciadorRequisicao` | §5 | `LocalizarLog() LogRecebido` | público | SSID_001, SSID_014, USID_016 | `[CONFIRMADO]` | — |
| OP-070 | CL-035 `LogRecebido` | §5 | `AssociarLogLote() void` | público | SSID_002 | `[CONFIRMADO]` | — |
| OP-071 | CL-036 `GerenciadorLote` | §5 | `CriarLotes() List<LoteAgrupador>` | público | SSID_002 | `[CONFIRMADO]` | — |
| OP-072 | CL-036 `GerenciadorLote` | §5 | `CriarLoteUnico() LoteAgrupador` | público | SSID_002 | `[CONFIRMADO]` | — |
| OP-073 | CL-036 `GerenciadorLote` | §5 | `ValidarLote() boolean` | público | SSID_002 | `[CONFIRMADO]` | — |
| OP-074 | CL-037 `LoteAgrupador` | §5 | `AdicionarLog() void` | público | SSID_002 | `[CONFIRMADO]` | — |
| OP-075 | CL-038 `EnfileiradorLogs` | §5 | `EnfilerarLote() void` | público | SSID_003 | `[CONFIRMADO]` | — |
| OP-076 | CL-039 `Arquivo` | §5 | `loadLines() Stream<String>` | público | USID_006, USID_007, USID_008 (inferido), SSID_003, SSID_004, SSID_013 | `[CONFIRMADO]` | — |
| OP-077 | CL-039 `Arquivo` | §5 | `destroy()` | público | USID_006, USID_007, USID_008 (inferido), SSID_003, SSID_004, SSID_013 | `[CONFIRMADO]` | — |
| OP-078 | CL-039 `Arquivo` | §5 | `getTraces() Trace[]` | público | USID_006, USID_007, USID_008 (inferido), SSID_003, SSID_004, SSID_013 | `[CONFIRMADO]` | — |
| OP-079 | CL-040 `Trace` | §5 | `resolvePrioridade(Modulo[] modulos) NivelPrioridade` | público | — | `[CONFIRMADO]` | — |
| OP-080 | CL-044 `Varredura` | §6 | `enqueueArquivos(String[] arquivos)` | público | SSID_005, SSID_006, USID_025, SSID_004 (inferido) | `[CONFIRMADO]` | — |
| OP-081 | CL-044 `Varredura` | §6 | `startVarredura()` | público | SSID_005, SSID_006, USID_025, SSID_004 (inferido) | `[CONFIRMADO]` | — |
| OP-082 | CL-044 `Varredura` | §6 | `finishVarredura()` | público | SSID_005, SSID_006, USID_025, SSID_004 (inferido) | `[CONFIRMADO]` | — |
| OP-083 | CL-044 `Varredura` | §6 | `getResume() VarreduraResumo` | público | SSID_005, SSID_006, USID_025, SSID_004 (inferido) | `[CONFIRMADO]` | — |
| OP-084 | CL-044 `Varredura` | §6 | `takeSnapshot(timestamp snapshot_at) Arquivo[]` | público | SSID_005, SSID_006, USID_025, SSID_004 (inferido) | `[CONFIRMADO]` | — |
| OP-085 | CL-044 `Varredura` | §6 | `prioritizeArquivos(Arquivo[] arquivos) Arquivo[]` | público | SSID_005, SSID_006, USID_025, SSID_004 (inferido) | `[CONFIRMADO]` | — |
| OP-086 | CL-044 `Varredura` | §6 | `publishFilaOrdenada() FilaOrdenada` | público | SSID_005, SSID_006, USID_025, SSID_004 (inferido) | `[CONFIRMADO]` | — |
| OP-087 | CL-046 `ArquivoVarredura` | §6 | `startScan()` | público | SSID_004, USID_007 | `[CONFIRMADO]` | — |
| OP-088 | CL-046 `ArquivoVarredura` | §6 | `retryScan(String error)` | público | SSID_004, USID_007 | `[CONFIRMADO]` | — |
| OP-089 | CL-046 `ArquivoVarredura` | §6 | `finishScan()` | público | SSID_004, USID_007 | `[CONFIRMADO]` | — |
| OP-090 | CL-047 `AgendamentoVarredura` | §6 | `create(String cron) AgendamentoVarredura` | público | USID_026, SSID_006, SSID_012 | `[CONFIRMADO]` | — |
| OP-091 | CL-047 `AgendamentoVarredura` | §6 | `pause()` | público | USID_026, SSID_006, SSID_012 | `[CONFIRMADO]` | — |
| OP-092 | CL-047 `AgendamentoVarredura` | §6 | `resume()` | público | USID_026, SSID_006, SSID_012 | `[CONFIRMADO]` | — |
| OP-093 | CL-047 `AgendamentoVarredura` | §6 | `cancel()` | público | USID_026, SSID_006, SSID_012 | `[CONFIRMADO]` | — |
| OP-094 | CL-047 `AgendamentoVarredura` | §6 | `dispatch() Varredura` | público | USID_026, SSID_006, SSID_012 | `[CONFLITO]` | CP-61 |
| OP-095 | CL-048 `Modulo` | §6 | `registerFromServiceName(String service_name) Modulo` | público | — | `[CONFIRMADO]` | — |
| OP-096 | CL-048 `Modulo` | §6 | `rename(String nome)` | público | — | `[CONFIRMADO]` | — |
| OP-097 | CL-048 `Modulo` | §6 | `changePrioridade(NivelPrioridade prioridade)` | público | — | `[CONFIRMADO]` | — |
| OP-098 | CL-049 `FilaDesordenada` | §6 | `enqueue(uuid arquivo_id)` | público | SSID_003 | `[CONFIRMADO]` | — |
| OP-099 | CL-049 `FilaDesordenada` | §6 | `size() int` | público | SSID_003 | `[CONFIRMADO]` | — |
| OP-100 | CL-049 `FilaDesordenada` | §6 | `snapshot(timestamp snapshot_at) Arquivo[]` | público | SSID_003 | `[CONFIRMADO]` | — |
| OP-101 | CL-049 `FilaDesordenada` | §6 | `requeue(uuid arquivo_id)` | público | SSID_003 | `[CONFLITO]` | CP-58, CP-60 |
| OP-102 | CL-050 `FilaOrdenada` | §6 | `publish(ArquivoVarredura[] arquivos)` | público | — | `[CONFIRMADO]` | — |
| OP-103 | CL-050 `FilaOrdenada` | §6 | `next() ArquivoVarredura` | público | — | `[CONFIRMADO]` | — |
| OP-104 | CL-050 `FilaOrdenada` | §6 | `isEmpty() bool` | público | — | `[CONFIRMADO]` | — |
| OP-105 | CL-051 `TravaVarredura` | §6 | `acquire(uuid varredura_id) bool` | público | USID_025 | `[CONFIRMADO]` | — |
| OP-106 | CL-051 `TravaVarredura` | §6 | `release()` | público | USID_025 | `[CONFIRMADO]` | — |
| OP-107 | CL-053 `Finder` | §7 | `processar() ResumoAnalise` | público | SSID_007, SSID_008 (inferido), SSID_013 | `[PROPOSTO]` | CP-62 |
| OP-108 | CL-053 `Finder` | §7 | `montarContexto() ContextoAnalise` | privado | SSID_007, SSID_008 (inferido), SSID_013 | `[CONFIRMADO]` | — |
| OP-109 | CL-053 `Finder` | §7 | `analisarRegistro() List<ClassificadorAnalise>` | privado | SSID_007, SSID_008 (inferido), SSID_013 | `[CONFIRMADO]` | — |
| OP-110 | CL-053 `Finder` | §7 | `removerLinhasDuplicadas(List<String> linhas) List<String>` | privado | SSID_007, SSID_008 (inferido), SSID_013 | `[CONFIRMADO]` | — |
| OP-111 | CL-053 `Finder` | §7 | `recarregarPorCorrelationId(String correlationId) List<String>` | privado | SSID_007, SSID_008 (inferido), SSID_013 | `[CONFIRMADO]` | — |
| OP-112 | CL-054 `ContextoAnalise` | §7 | `permiteVarreduraAvancada() Boolean` | público | SSID_008, USID_027 | `[CONFIRMADO]` | — |
| OP-113 | CL-054 `ContextoAnalise` | §7 | `pertenceAoProduto() Boolean` | público | SSID_008, USID_027 | `[CONFIRMADO]` | — |
| OP-114 | CL-054 `ContextoAnalise` | §7 | `pertenceAEmpresa() Boolean` | público | SSID_008, USID_027 | `[CONFIRMADO]` | — |
| OP-115 | CL-055 `LogNormalizado` | §7 | `obterCampo() Object` | público | SSID_007, USID_006 (inferido) | `[CONFIRMADO]` | — |
| OP-116 | CL-055 `LogNormalizado` | §7 | `adicionarCampo() void` | público | SSID_007, USID_006 (inferido) | `[CONFIRMADO]` | — |
| OP-117 | CL-056 `MotorAnalise` | §7 | `Analisar() List<AchadoAnalise>` | público | SSID_007, SSID_020 | `[CONFIRMADO]` | — |
| OP-118 | CL-056 `MotorAnalise` | §7 | `interpretarResposta() ClassificadorAnalise` | público | SSID_007, SSID_020 | `[CONFIRMADO]` | — |
| OP-119 | CL-056 `MotorAnalise` | §7 | `executarAI() void` | público | SSID_007, SSID_020 | `[CONFIRMADO]` | — |
| OP-120 | CL-056 `MotorAnalise` | §7 | `verificarRecorrencia(AchadoAnalise achado) Boolean` | público | SSID_007, SSID_020 | `[PENDENTE]` | CP-66 |
| OP-121 | CL-057 `GatewayLLMFinder` | §7 | `executarAI()` | público | SSID_007, SSID_020 | `[CONFIRMADO]` | — |
| OP-122 | CL-058 `BancoVetorial` | §7 | `searchSimilar(String log, uuid owner_id) List<uuid>` | público | — | `[CONFLITO]` | CP-68 |
| OP-123 | CL-058 `BancoVetorial` | §7 | `store(String log, uuid owner_id, uuid ocorrencia_id)` | público | — | `[CONFLITO]` | CP-68 |
| OP-124 | CL-059 `RecorrenciaLog` | §7 | `register(uuid arquivo_id) int` | público | — | `[CONFIRMADO]` | — |
| OP-125 | CL-059 `RecorrenciaLog` | §7 | `isRecorrente(int limite) bool` | público | — | `[CONFIRMADO]` | — |
| OP-126 | CL-062 `ClassificadorAnalise` | §7 | `classificarAnalise() void` | público | SSID_007 | `[CONFIRMADO]` | — |
| OP-127 | CL-062 `ClassificadorAnalise` | §7 | `geraOcorrencia() Boolean` | público | SSID_007 | `[CONFIRMADO]` | — |
| OP-128 | CL-063 `ScannerSeguranca` | §7 | `validarSeguranca() void` | público | SSID_008, USID_027 | `[CONFIRMADO]` | — |
| OP-129 | CL-064 `ModuloOcorrencia` | §8 | `registrar(Ocorrencia ocorrencia) bool` | público | SSID_009, SSID_010, USID_044 (inferido) | `[PROPOSTO]` | CP-78 |
| OP-130 | CL-064 `ModuloOcorrencia` | §8 | `existsByChave(String chave_idempotencia) bool` | público | SSID_009, SSID_010, USID_044 (inferido) | `[PROPOSTO]` | CP-78 |
| OP-131 | CL-064 `ModuloOcorrencia` | §8 | `receberResumo(ResumoAnalise resumo) bool` | público | SSID_009, SSID_010, USID_044 (inferido) | `[PROPOSTO]` | CP-78 |
| OP-132 | CL-064 `ModuloOcorrencia` | §8 | `dispararSugestaoAutomatica(Ocorrencia ocorrencia) Sugestao` | público | SSID_009, SSID_010, USID_044 (inferido) | `[PROPOSTO]` | CP-78 |
| OP-133 | CL-067 `Mapper` | §8 | `converter(AchadoAnalise achado) Ocorrencia` | público | SSID_010 | `[PROPOSTO]` | CP-79 |
| OP-134 | CL-068 `Sugestao` | §9 | `Sugestao(UUID ocorrencia_id, String conteudo, Integer tokens_consumidos)` | público | USID_044, USID_045, USID_046, USID_047, USID_028 | `[PROPOSTO]` | CP-88, CP-122 |
| OP-135 | CL-068 `Sugestao` | §9 | `avaliar(Integer nota) void` | público | USID_044, USID_045, USID_046, USID_047, USID_028 | `[CONFLITO]` | CP-83 |
| OP-136 | CL-068 `Sugestao` | §9 | `fechar() void` | público | USID_044, USID_045, USID_046, USID_047, USID_028 | `[CONFIRMADO]` | — |
| OP-137 | CL-070 `ContextoSugestao` | §9 | `ContextoSugestao(UUID ocorrencia_id, ContextoEmpresa contextoEmpresarial, ContextoProduto contextoProduto)` | público | SSID_015, USID_044 | `[PENDENTE]` | CP-84, CP-88 |
| OP-138 | CL-070 `ContextoSugestao` | §9 | `montarPrompt() String` | público | SSID_015, USID_044 | `[PROPOSTO]` | CP-88 |
| OP-139 | CL-071 `GatewayLLMSugestao` | §9 | `solicitar(String prompt) RespostaLLM` | público | SSID_020 | `[CONFIRMADO]` | — |
| OP-140 | CL-072 `GatewayLLMPadrao` | §9 | `solicitar(String prompt) RespostaLLM` | público | SSID_020 | `[CONFIRMADO]` | — |
| OP-141 | CL-073 `RespostaLLM` | §9 | `RespostaLLM(String conteudo, Integer tokens_consumidos)` | público | SSID_020 | `[CONFIRMADO]` | — |
| OP-142 | CL-076 `Notificacao` | §10 | `Notificacao(ocorrencia_id, membroId, canal, conteudo)` | público | USID_009, USID_010, USID_011, USID_013, USID_014, SSID_019, SSID_009 | `[PROPOSTO]` | CP-92, CP-123 |
| OP-143 | CL-076 `Notificacao` | §10 | `Notificacao(ocorrencia_id, membroId, canal, conteudo, sugestao_id)` | público | USID_009, USID_010, USID_011, USID_013, USID_014, SSID_019, SSID_009 | `[PROPOSTO]` | CP-92, CP-123 |
| OP-144 | CL-076 `Notificacao` | §10 | `marcarComoLida() void` | público | USID_009, USID_010, USID_011, USID_013, USID_014, SSID_019, SSID_009 | `[CONFIRMADO]` | — |
| OP-145 | CL-076 `Notificacao` | §10 | `arquivar() void` | público | USID_009, USID_010, USID_011, USID_013, USID_014, SSID_019, SSID_009 | `[CONFIRMADO]` | — |
| OP-146 | CL-077 `PreferenciaNotificacao` | §10 | `habilitarCanal(CanalNotificacao canal) void` | público | USID_012, USID_009, USID_010, USID_011 | `[CONFIRMADO]` | — |
| OP-147 | CL-077 `PreferenciaNotificacao` | §10 | `desabilitarCanal(CanalNotificacao canal) void` | público | USID_012, USID_009, USID_010, USID_011 | `[CONFIRMADO]` | — |
| OP-148 | CL-077 `PreferenciaNotificacao` | §10 | `possuiCanalHabilitado(CanalNotificacao canal) Boolean` | público | USID_012, USID_009, USID_010, USID_011 | `[CONFIRMADO]` | — |
| OP-149 | CL-078 `GatewayNotificacao` | §10 | `enviar(Notificacao notificacao) TentativaEntrega` | público | SSID_019 | `[CONFIRMADO]` | — |
| OP-150 | CL-079 `GatewayNotificacaoFactory` | §10 | `obterGateway(CanalNotificacao canal) GatewayNotificacao` | público | SSID_019 | `[CONFIRMADO]` | — |
| OP-151 | CL-080 `EnviadorEmail` | §10 | `enviar(Notificacao notificacao) StatusEnvioNotificacao` | público | USID_009 | `[CONFIRMADO]` | — |
| OP-152 | CL-080 `EnviadorEmail` | §10 | `formatarCorpoEmail(String conteudo) String` | privado | USID_009 | `[CONFIRMADO]` | — |
| OP-153 | CL-081 `EnviadorPush` | §10 | `enviar(Notificacao notificacao) StatusEnvioNotificacao` | público | USID_010, USID_014 | `[CONFIRMADO]` | — |
| OP-154 | CL-081 `EnviadorPush` | §10 | `obterDispositivos(UUID membroId) List<DispositivoPush>` | privado | USID_010, USID_014 | `[CONFIRMADO]` | — |
| OP-155 | CL-082 `EnviadorWeb` | §10 | `enviar(Notificacao notificacao) StatusEnvioNotificacao` | público | USID_011, USID_013 | `[CONFIRMADO]` | — |
| OP-156 | CL-082 `EnviadorWeb` | §10 | `publicarViaWebSocket(UUID membroId, String conteudo) void` | privado | USID_011, USID_013 | `[CONFIRMADO]` | — |
| OP-157 | CL-083 `DispositivoPush` | §10 | `atualizarToken(String novo_token) void` | público | USID_010 | `[CONFIRMADO]` | — |
| OP-158 | CL-084 `TentativaEntrega` | §10 | `TentativaEntrega(UUID notificacao_id)` | público | USID_009, USID_010, USID_011, SSID_009 (inferido) | `[CONFLITO]` | CP-98, CP-99 |
| OP-159 | CL-084 `TentativaEntrega` | §10 | `marcarComoEnviada() void` | público | USID_009, USID_010, USID_011, SSID_009 (inferido) | `[CONFIRMADO]` | — |
| OP-160 | CL-084 `TentativaEntrega` | §10 | `marcarComoFalha(String motivo) void` | público | USID_009, USID_010, USID_011, SSID_009 (inferido) | `[CONFIRMADO]` | — |
| OP-161 | CL-085 `Metrica` | §11 | `atualizarValor(Number valor) void` | público | USID_031, USID_034 | `[CONFIRMADO]` | — |
| OP-162 | CL-085 `Metrica` | §11 | `zerar() void` | público | USID_031, USID_034 | `[CONFIRMADO]` | — |
| OP-163 | CL-086 `Periodo` | §11 | `estaValido() boolean` | público | USID_032, USID_036, SSID_011 | `[CONFIRMADO]` | — |
| OP-164 | CL-086 `Periodo` | §11 | `contem(DateTime data) boolean` | público | USID_032, USID_036, SSID_011 | `[CONFIRMADO]` | — |
| OP-165 | CL-087 `FiltroDashboard` | §11 | `validar() boolean` | público | USID_032, USID_036 | `[CONFIRMADO]` | — |
| OP-166 | CL-087 `FiltroDashboard` | §11 | `aplicar() void` | público | USID_032, USID_036 | `[CONFIRMADO]` | — |
| OP-167 | CL-087 `FiltroDashboard` | §11 | `limpar() void` | público | USID_032, USID_036 | `[CONFIRMADO]` | — |
| OP-168 | CL-088 `DashboardProduto` | §11 | `carregarMetricas() void` | público | USID_031, USID_032 | `[CONFIRMADO]` | — |
| OP-169 | CL-088 `DashboardProduto` | §11 | `aplicarFiltro(FiltroDashboard filtro) void` | público | USID_031, USID_032 | `[CONFIRMADO]` | — |
| OP-170 | CL-088 `DashboardProduto` | §11 | `atualizar() void` | público | USID_031, USID_032 | `[CONFIRMADO]` | — |
| OP-171 | CL-088 `DashboardProduto` | §11 | `obterMetricas() List<Metrica>` | público | USID_031, USID_032 | `[CONFIRMADO]` | — |
| OP-172 | CL-089 `DashboardEmpresarial` | §11 | `carregarDados() void` | público | USID_034, USID_036 | `[CONFIRMADO]` | — |
| OP-173 | CL-089 `DashboardEmpresarial` | §11 | `aplicarFiltro(FiltroDashboard filtro) void` | público | USID_034, USID_036 | `[CONFIRMADO]` | — |
| OP-174 | CL-089 `DashboardEmpresarial` | §11 | `atualizar() void` | público | USID_034, USID_036 | `[CONFIRMADO]` | — |
| OP-175 | CL-089 `DashboardEmpresarial` | §11 | `obterMetricasAgregadas() List<Metrica>` | público | USID_034, USID_036 | `[CONFIRMADO]` | — |
| OP-176 | CL-089 `DashboardEmpresarial` | §11 | `selecionarProduto(Produto produto) DashboardProduto` | público | USID_034, USID_036 | `[CONFIRMADO]` | — |
| OP-177 | CL-090 `FiltroOcorrenciaEmpresarial` | §11 | `validar() boolean` | público | USID_037 | `[CONFIRMADO]` | — |
| OP-178 | CL-090 `FiltroOcorrenciaEmpresarial` | §11 | `aplicar() void` | público | USID_037 | `[CONFIRMADO]` | — |
| OP-179 | CL-090 `FiltroOcorrenciaEmpresarial` | §11 | `limpar() void` | público | USID_037 | `[CONFIRMADO]` | — |
| OP-180 | CL-090 `FiltroOcorrenciaEmpresarial` | §11 | `adicionarProduto(Produto produto) void` | público | USID_037 | `[CONFIRMADO]` | — |
| OP-181 | CL-090 `FiltroOcorrenciaEmpresarial` | §11 | `removerProduto(Produto produto) void` | público | USID_037 | `[CONFIRMADO]` | — |
| OP-182 | CL-091 `ResumoDashboardMobile` | §11 | `carregarResumo() void` | público | USID_038 | `[CONFIRMADO]` | — |
| OP-183 | CL-091 `ResumoDashboardMobile` | §11 | `atualizar() void` | público | USID_038 | `[CONFIRMADO]` | — |
| OP-184 | CL-091 `ResumoDashboardMobile` | §11 | `obterMetricasPrincipais() List<Metrica>` | público | USID_038 | `[CONFIRMADO]` | — |
| OP-185 | CL-092 `Agregacao` | §11 | `calcular() Number` | público | USID_034, SSID_011 | `[CONFIRMADO]` | — |
| OP-186 | CL-092 `Agregacao` | §11 | `adicionarMetrica(Metrica metrica) void` | público | USID_034, SSID_011 | `[CONFIRMADO]` | — |
| OP-187 | CL-092 `Agregacao` | §11 | `removerMetrica(Metrica metrica) void` | público | USID_034, SSID_011 | `[CONFIRMADO]` | — |
| OP-188 | CL-092 `Agregacao` | §11 | `zerar() void` | público | USID_034, SSID_011 | `[CONFIRMADO]` | — |
| OP-189 | CL-093 `RelatorioDashboard` | §12 | `gerar() void` | público | USID_033 | `[CONFIRMADO]` | — |
| OP-190 | CL-093 `RelatorioDashboard` | §12 | `carregarDados() void` | público | USID_033 | `[CONFIRMADO]` | — |
| OP-191 | CL-093 `RelatorioDashboard` | §12 | `obterMetricas() List<Metrica>` | público | USID_033 | `[CONFIRMADO]` | — |
| OP-192 | CL-093 `RelatorioDashboard` | §12 | `atualizarDados() void` | público | USID_033 | `[CONFIRMADO]` | — |
| OP-193 | CL-094 `RelatorioEmpresarial` | §12 | `gerar() void` | público | USID_035 | `[CONFIRMADO]` | — |
| OP-194 | CL-094 `RelatorioEmpresarial` | §12 | `carregarDados() void` | público | USID_035 | `[CONFIRMADO]` | — |
| OP-195 | CL-094 `RelatorioEmpresarial` | §12 | `obterMetricasAgregadas() List<Metrica>` | público | USID_035 | `[CONFIRMADO]` | — |
| OP-196 | CL-094 `RelatorioEmpresarial` | §12 | `atualizarDados() void` | público | USID_035 | `[CONFIRMADO]` | — |
| OP-197 | CL-095 `RelatorioConsolidado` | §12 | `consolidar() void` | público | SSID_011 | `[CONFIRMADO]` | — |
| OP-198 | CL-095 `RelatorioConsolidado` | §12 | `adicionarMetrica(Metrica metrica) void` | público | SSID_011 | `[CONFIRMADO]` | — |
| OP-199 | CL-095 `RelatorioConsolidado` | §12 | `adicionarAgregacao(Agregacao agregacao) void` | público | SSID_011 | `[CONFIRMADO]` | — |
| OP-200 | CL-095 `RelatorioConsolidado` | §12 | `obterMetricas() List<Metrica>` | público | SSID_011 | `[CONFIRMADO]` | — |
| OP-201 | CL-095 `RelatorioConsolidado` | §12 | `marcarProcessado() void` | público | SSID_011 | `[CONFIRMADO]` | — |
| OP-202 | CL-095 `RelatorioConsolidado` | §12 | `zerarResultados() void` | público | SSID_011 | `[CONFIRMADO]` | — |
| OP-203 | CL-096 `ExportacaoRelatorio` | §12 | `exportar(RelatorioDashboard relatorio) void` | público | USID_033, USID_035 | `[CONFIRMADO]` | — |
| OP-204 | CL-096 `ExportacaoRelatorio` | §12 | `exportarEmpresarial(RelatorioEmpresarial relatorio) void` | público | USID_033, USID_035 | `[CONFIRMADO]` | — |
| OP-205 | CL-096 `ExportacaoRelatorio` | §12 | `cancelar() void` | público | USID_033, USID_035 | `[CONFIRMADO]` | — |
| OP-206 | CL-096 `ExportacaoRelatorio` | §12 | `registrarExportacao() void` | público | USID_033, USID_035 | `[CONFIRMADO]` | — |
| OP-207 | CL-096 `ExportacaoRelatorio` | §12 | `concluir(String arquivo) void` | público | USID_033, USID_035 | `[CONFIRMADO]` | — |
| OP-208 | CL-097 `GeracaoRelatorioAgendada` | §12 | `executar() RelatorioConsolidado` | público | SSID_011 | `[CONFIRMADO]` | — |
| OP-209 | CL-097 `GeracaoRelatorioAgendada` | §12 | `reagendar() void` | público | SSID_011 | `[CONFIRMADO]` | — |
| OP-210 | CL-097 `GeracaoRelatorioAgendada` | §12 | `ativar() void` | público | SSID_011 | `[CONFIRMADO]` | — |
| OP-211 | CL-097 `GeracaoRelatorioAgendada` | §12 | `desativar() void` | público | SSID_011 | `[CONFIRMADO]` | — |
| OP-212 | CL-097 `GeracaoRelatorioAgendada` | §12 | `registrarFalha() void` | público | SSID_011 | `[CONFIRMADO]` | — |
| OP-213 | CL-098 `GeradorArquivo` | §12 | `gerar(RelatorioDashboard relatorio, FormatoArquivo formato) String` | público | USID_033, USID_035 | `[CONFIRMADO]` | — |
| OP-214 | CL-098 `GeradorArquivo` | §12 | `gerarEmpresarial(RelatorioEmpresarial relatorio, FormatoArquivo formato) String` | público | USID_033, USID_035 | `[CONFIRMADO]` | — |
| OP-215 | CL-099 `LogSDK` | §13 | `criarConfiguracao() ConfiguracaoSdk` | público | USID_015, USID_017 | `[LEGADO]` | — |
| OP-216 | CL-099 `LogSDK` | §13 | `registrarEvento() ResultadoEnvio` | público | USID_015, USID_017 | `[LEGADO]` | — |
| OP-217 | CL-099 `LogSDK` | §13 | `registrarTodos() List<ResultadoEnvio>` | público | USID_015, USID_017 | `[LEGADO]` | — |
| OP-218 | CL-099 `LogSDK` | §13 | `testarConexao() ResultadoConexao` | público | USID_015, USID_017 | `[LEGADO]` | — |
| OP-219 | CL-099 `LogSDK` | §13 | `fechar() void` | público | USID_015, USID_017 | `[LEGADO]` | — |
| OP-220 | CL-100 `ConfiguracaoSdk` | §13 | `builder() ConfiguracaoSdk.Builder` | público | USID_015 | `[LEGADO]` | — |
| OP-221 | CL-100 `ConfiguracaoSdk` | §13 | `validar() ResultadoValidacao` | público | USID_015 | `[LEGADO]` | — |
| OP-222 | CL-100 `ConfiguracaoSdk` | §13 | `cofigMetadado() ConfiguracaoSdk` | público | USID_015 | `[LEGADO]` | — |
| OP-223 | CL-101 `CredencialIngestao (SDK)` | §13 | `estaPresente() boolean` | público | USID_016, SSID_001 | `[LEGADO]` | — |
| OP-224 | CL-101 `CredencialIngestao (SDK)` | §13 | `copiaSegura() String` | público | USID_016, SSID_001 | `[LEGADO]` | — |
| OP-225 | CL-101 `CredencialIngestao (SDK)` | §13 | `limpar() void` | público | USID_016, SSID_001 | `[LEGADO]` | — |
| OP-226 | CL-102 `IdentificadorProduto` | §13 | `identificarProduito() IdentificadorProduto` | público | USID_015 | `[LEGADO]` | — |
| OP-227 | CL-102 `IdentificadorProduto` | §13 | `estaValido() boolean` | público | USID_015 | `[LEGADO]` | — |
| OP-228 | CL-103 `EventoLog` | §13 | `criarEvento() EventoLog` | público | SSID_001 | `[LEGADO]` | — |
| OP-229 | CL-103 `EventoLog` | §13 | `builder() EventoLog` | público | SSID_001 | `[LEGADO]` | — |
| OP-230 | CL-103 `EventoLog` | §13 | `adicionarAtributo() EventoLog` | público | SSID_001 | `[LEGADO]` | — |
| OP-231 | CL-103 `EventoLog` | §13 | `comCorrelacao() EventoLog` | público | SSID_001 | `[LEGADO]` | — |
| OP-232 | CL-104 `EnvelopeIngestao` | §13 | `criar() EnvelopeIngestao` | público | SSID_001 | `[LEGADO]` | — |
| OP-233 | CL-104 `EnvelopeIngestao` | §13 | `calcularChecksum() String` | público | SSID_001 | `[LEGADO]` | — |
| OP-234 | CL-105 `ClienteColetor` | §13 | `transmitir() RespostaColetor` | público | SSID_001, USID_015 | `[LEGADO]` | — |
| OP-235 | CL-105 `ClienteColetor` | §13 | `testarConexao() ResultadoConexao` | público | SSID_001, USID_015 | `[LEGADO]` | — |
| OP-236 | CL-105 `ClienteColetor` | §13 | `fechar() void` | público | SSID_001, USID_015 | `[LEGADO]` | — |
| OP-237 | CL-106 `SerializadorIngestao` | §13 | `serializar() byte[]` | público | SSID_001 | `[LEGADO]` | — |
| OP-238 | CL-106 `SerializadorIngestao` | §13 | `tipoConteudo() String` | público | SSID_001 | `[LEGADO]` | — |
| OP-239 | CL-106 `SerializadorIngestao` | §13 | `versaoFormato() String` | público | SSID_001 | `[LEGADO]` | — |
| OP-240 | CL-107 `ValidadorEventoLog` | §13 | `validar() ResultadoValidacao` | público | SSID_001 | `[LEGADO]` | — |
| OP-241 | CL-107 `ValidadorEventoLog` | §13 | `validarAtributos() ResultadoValidacao` | público | SSID_001 | `[LEGADO]` | — |
| OP-242 | CL-108 `ResultadoValidacao` | §13 | `sucesso() ResultadoValidacao` | público | SSID_001 | `[LEGADO]` | — |
| OP-243 | CL-108 `ResultadoValidacao` | §13 | `falha() ResultadoValidacao` | público | SSID_001 | `[LEGADO]` | — |
| OP-244 | CL-108 `ResultadoValidacao` | §13 | `estaValido() boolean` | público | SSID_001 | `[LEGADO]` | — |
| OP-245 | CL-109 `RedatorDadosSensiveis` | §13 | `redigir(EventoLog evento) EventoLog` | público | — | `[LEGADO]` | — |
| OP-246 | CL-109 `RedatorDadosSensiveis` | §13 | `redigirValor(String chave, Object valor) Object` | público | — | `[LEGADO]` | — |
| OP-247 | CL-110 `RespostaColetor` | §13 | `foiAceita() boolean` | público | SSID_001 | `[LEGADO]` | — |
| OP-248 | CL-110 `RespostaColetor` | §13 | `podeSerReenviada() boolean` | público | SSID_001 | `[LEGADO]` | — |
| OP-249 | CL-111 `ResultadoEnvio` | §13 | `sucesso() boolean` | público | SSID_001 | `[LEGADO]` | — |
| OP-250 | CL-111 `ResultadoEnvio` | §13 | `falhaTemporaria() boolean` | público | SSID_001 | `[LEGADO]` | — |
| OP-251 | CL-111 `ResultadoEnvio` | §13 | `falhaDefinitiva() boolean` | público | SSID_001 | `[LEGADO]` | — |
| OP-252 | CL-112 `ResultadoConexao` | §13 | `estaPronto() boolean` | público | SSID_001 | `[LEGADO]` | — |
| OP-253 | CL-113 `Executavel` | §13 | `Executavel(produto_id, token_id, pasta_monitorada, periodicidade_cron, nome_amigavel)` | público | USID_018, USID_019, USID_020 | `[CONFLITO]` | CP-113 |
| OP-254 | CL-113 `Executavel` | §13 | `iniciarVarredura() void` | público | USID_018, USID_019, USID_020 | `[LEGADO]` | — |
| OP-255 | CL-113 `Executavel` | §13 | `pararVarredura() void` | público | USID_018, USID_019, USID_020 | `[LEGADO]` | — |
| OP-256 | CL-113 `Executavel` | §13 | `estaConectado() Boolean` | público | USID_018, USID_019, USID_020 | `[LEGADO]` | — |

## 12. Removidos e substituídos

Do DC-10 v7 (seção "Classes e elementos removidos ou substituídos"). Esses elementos não têm ID na matriz; o requisito que eles atendiam passa para a classe que os substitui.

| Elemento da planilha | Situação | Fonte |
|---|---|---|
| `Empresa` | deixou de ser substituída: cadastro 1:1 do `Tenant` | `[PROPOSTO]` ADR_158 (DER v9 dizia substituída) |
| `TokenMetadata` | removida | ADR_154 `[PROPOSTO]` |
| `SaldoTokens` | removida; a Sugestão usa o `Saldo` | ADR_117, `[PROPOSTO]` ADR_157 |
| `Finder.Ocorrencia`, `processar(): Ocorrencia` | campo sai; retorno vira `ResumoAnalise` | ADR_062, `[PROPOSTO]` ADR_161 |
| `Ocorrencia` (resumo) `achados` | vira `ResumoArquivo.ocorrenciaIds` | ADR_035/040, `[PROPOSTO]` ADR_160 |
| `usuario_id` (Notificação, Avaliação) | vira `membroId` | DER v9, `[PROPOSTO]` ADR_159 |
| `Usuario`, `Gestor`, `Vinculo`, `Acesso` | substituídas por `Membro` (no diagrama) | DER v9, ADR_122 |
| `Executavel` | substituída por `FonteTelemetria` (no diagrama) | pauta ING-06 |
| `CredencialIngestao` (tabela do DER) | substituída por `TokenApi` (no diagrama) | DER v9, `[PROPOSTO]` ADR_155 |
| `Autorizador` (+ enum `TenantRoles`), `API - Token`, `ExternalToken`, `Autorizador - SDK` | removidas | ADR_111 |
| `GatewayLLM` (Finder) | renomeada para `GatewayLLMFinder` | ADR_067 |
| `GatewayLLM` (Sugestão) | renomeada para `GatewayLLMSugestao` | ADR_039 |
| `Finder.enviarOcorrencia()` | removido | ADR_062 |
| `Finder.devolverParaFila()` | removido (vira DLQ) | ADR_059 |
| `Tipo.INFO`, `Tipo.RECORRENTE` | removidos (`recorrente` vira atributo) | ADR_019, ADR_063 |
| `StatusSugestao.DISPONIVEL`, `AVALIADA` | removidos; entram `AGUARDANDO_REVISAO` e `FALHA` | ADR_096 |
| `Ocorrencia.informacaoIdentificados` | vira `spamIdentificados` | DER v9 (ADR_019) |
| `GerenciadorRequisicao.Token: Credito` | o tipo sai | ADR_117 |

## 13. Sugestões ainda em aberto

Sugestões do DC-10 v7 que não foram aplicadas. Elas não estão no diagrama nem na matriz; ficam aqui para quem for fechar as pendências.

| # | Onde falta | Fonte do pedido | Sugestão |
|---|---|---|---|
| S1 | Enums sem nome: `Membro.papel`, `Membro.status`, `Arquivo.status`, `Arquivo.origem`, `Ocorrencia.status`, `Notificacao.tipo`, `EventoGateway.status` | ADR_099, 100, 082, 081, 125; DER v9 | `PapelMembro`, `StatusMembro`, `StatusArquivo`, `OrigemArquivo`, `StatusOcorrencia`, `TipoNotificacao`, `StatusEventoGateway`. |
| S2 | Coleção das chaves lock | ADR_058, 069, 072 | Classe `ChaveLock` (`chave`, `valor`, `expiraEm`) no módulo Varredura, substituindo a `TravaVarredura`. |
| S3 | Onde fica o `execId` | ADR_069, 070, 075 | Campo `execId` na `Varredura` e decidir se o upload manual também gera uma `Varredura` (com um `trigger` próprio). |
| S4 | Contadores do `ResumoAnalise` | ADR_062, 102 | `registrosProcessados`, `errosIdentificados`, `warningsIdentificados`, `spamIdentificados`, `dadosSensiveisIdentificados` + `List<AchadoAnalise> achados`, reaproveitando os nomes do resumo. |
| S6 | Campos sem nome da Ocorrência concreta | ADR_040 | `resumoId`, `produtoId` e um nome único para a data (`descobertaEm` do DER ou `criadaEm`), mais a chave de idempotência (pauta OCO-01 cita `arquivoId + traceId/correlationId + linha`). |
| S8 | Retorno de `validarSeguranca()` | ADR_064 | Um retorno com as linhas mascaradas e o total (ex.: `List<String>` + contador, ou um objeto próprio). |
| S9 | Onde fica o nome do token | ADR_106 | Campo `nome` no `TokenApi`. |
| S10 | Campo de erro da Notificação | ADR_081 | Campo `erro` (String) na `Notificacao`. |
| S11 | Campos de ligação do `ProdutoRecursoIA` | ADR_076 | `produtoId` e `planoId`. |
| S12 | `origem` e `tentativas` da Sugestão | pauta SUG-14; ADR_036, 094 | Confirmar os dois (`AUTOMATICA`/`MANUAL`) e registrar numa ADR. |
| S13 | Implementação do gateway de pagamento | planilha (Guia) | Declarar `ApiPagamento implements GatewayPagamento` e a ligação `ProcessamentoPagamento → GatewayPagamento`. |
| S14 | Estrutura de `Assinatura.limites` | ADR_122 | Objeto com `ia`, `retencaoDias` e `creditos`, alinhado à `TabelaPrecificacao`. |
| S16 | `RecorrenciaLog` e `TravaVarredura` | ADR_063, 068 | Retirar as duas da planilha e do DER, já que as regras que elas implementavam foram trocadas. |
| S19 | Comportamentos sem classe | ADR_042, 046, 059, 065, 072, 121, 130, 036 | **Aplicada só a orquestração da Sugestão (`ModuloSugestao`, ADR_156, proposta).** Classes para: proteção e seção manual do Coletor, DLQ, coleção de idempotência, API de Estimativa, camada de filtro por tenant, consulta de agregação dos destinatários e orquestração da Sugestão automática no Módulo Ocorrência (os métodos novos da `ModuloOcorrencia`, pauta OCO-06). |
| S21 | Serviço de Créditos, Dashboard e Relatório | ADR_054, 141 | Registrar numa ADR em qual dos seis serviços cada um fica. |
| S22 | Streams, envelope, consumidor base e agendamento | ADR_143, 145, 146, 147 | Classe do envelope padrão (`eventId`, `type`, `version`, `timestamp`, `tenantId`, `produtoId`, `execId`, `tentativa`, `payload`) e a classe base de consumidor; decidir se `varredura_schedules` é a coleção do `AgendamentoVarredura` e trocar `dispatch()` por "publica a execução na stream". |

## 14. Artefatos

| Arquivo | Conteúdo |
|---|---|
| `rastreabilidade.md` | Este documento. |
| `rastreabilidade.xlsx` | As mesmas tabelas em abas, com cores por módulo e por situação, e o mapa Requisitos × Módulos. Abre no Google Sheets. |
| `rastreabilidade.csv` | A matriz requisito → classes (separador vírgula, UTF-8): uma linha por classe, agrupada por requisito. Abre direto no Google Sheets. |
| `DC-10-diagrama-de-classes.md` | Diagrama de classes v8, a base desta matriz. |
| `ADR_154` a `ADR_162` | ADRs propostas para as decisões de fechamento do diagrama (publicadas na pasta de ADRs do Drive em 17/10, status Proposto). |
| `decisoes-tomadas.md` | Justificativa das decisões (itens 47 a 51). |
