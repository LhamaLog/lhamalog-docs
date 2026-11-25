# LLT-234 — Acompanhar o consumo de logs do mês — Desenho

Versão: v2 Status: para aprovação Autor: André Felipe Data: 27/10/2026 Base: documento de Requisitos da LLT-234 (v2) Mudanças da v2: no plano semanal o fechamento é semanal e o excedente da semana vai somado à próxima cobrança semanal.

Este documento diz **como** a tarefa será construída. O **o quê** está no documento de Requisitos.

## 1. Partes envolvidas

| **Parte**                            | **O que faz nesta tarefa**                                                                               |
|--------------------------------------|----------------------------------------------------------------------------------------------------------|
| Front                                | Mostra o consumo e o teto (fora desta tarefa; usa a API daqui)                                           |
| Core (lhamalog-core)                 | Soma o consumo, calcula percentuais e excedente, guarda o teto, manda os avisos e fecha o período de uso |
| Coletor (lhamalog-collector)         | Mede o GB bruto por produto, publica o uso e recusa logs quando a conta está pausada                     |
| Notification (lhamalog-notification) | Envia os avisos por e-mail                                                                               |
| Asaas                                | Recebe a cobrança do excedente (por meio da interface do gateway, LLT-235)                               |
| MongoDB, Redis Streams               | Guardam o consumo e levam as mensagens entre os serviços                                                 |

## 2. Fluxos

### 2.1 Medir o consumo

1.  O Coletor soma o tamanho bruto dos logs recebidos por produto e, a cada hora, publica um evento de uso no Redis Streams (tenantId, produtoId, GB da hora, volume retido do dia).

2.  O Core consome o evento, soma no documento consumo_mensal do período de uso atual (dedupe pelo id do evento) e recalcula o percentual da franquia.

### 2.2 Avisos e pausa

1.  Depois de cada soma, o Core compara o consumo com a franquia e com o teto de gasto.

2.  Cruzou 80% ou 100% da franquia: grava o aviso (uma vez por período de uso) e pede ao Notification o e-mail para o Dono e os Administradores; a plataforma mostra o aviso.

3.  **Free** chegou a 100%: o Core marca a conta como PAUSADA_FRANQUIA.

4.  **Plano pago** passou da franquia: continua e acumula o excedente. Cruzou 80% ou 100% do teto: aviso; chegou a 100%: PAUSADA_TETO.

5.  O estado da conta fica num lugar que o Coletor lê (um documento por conta, cacheado por 1 minuto). Pausada, o Coletor recusa os logs com a resposta "franquia ou teto atingido".

6.  A pausa termina quando o período de uso vira, o Dono aumenta o teto ou a conta faz upgrade (a LLT-232 avisa o Core, que recalcula).

### 2.3 Fechar o período de uso

1.  Um job do Core (@Scheduled com ShedLock) roda todo dia e fecha os períodos de uso que terminaram naquele dia (mês de uso nos planos mensal e semestral; semana de uso no semanal).

2.  Calcula: excedente de ingestão = GB acima da franquia × preço por GB; armazenamento extra = (média diária do volume retido − franquia) × preço por GB-mês, só se positivo. Os preços são os do Planos Ajustado da forma de pagamento da assinatura (LLT-230).

3.  Se o total for zero, só fecha o período. Se houver valor, chama GatewayPagamento.registrarExcedente:

    - **Plano mensal:** soma o valor à cobrança do próximo ciclo já gerada (PUT /v3/payments/{id} com novo value e description). Se a cobrança já estiver paga ou ainda não existir, cria uma cobrança avulsa à parte.

    - **Plano semanal:** soma o excedente da semana à próxima cobrança semanal pendente (o Asaas já gera até 4 de uma vez); o armazenamento extra, que segue o mês de uso, é somado na primeira cobrança semanal depois que o mês fecha.

    - **Plano semestral:** cria uma cobrança avulsa (POST /v3/payments) com o detalhamento na descrição, uma vez por mês.

4.  Grava o fechamento (fechamento_consumo) com os números e o id da cobrança, zera o contador, abre o novo período de uso e levanta qualquer pausa por franquia ou teto.

## 3. Contrato da API

Todas exigem login; as de leitura valem para Dono e Administrador, e a de alterar o teto só para o Dono.

**GET /api/v1/consumo**

Resposta 200:

{

"periodoDeUso": { "tipo": "MES", "inicio": "2026-10-26", "fim": "2026-11-25" },

"atualizadoEm": "2026-10-27T15:00:00-03:00",

"franquiaGb": 10,

"consumoGbTotal": 8.4,

"percentualFranquia": 84,

"excedenteGb": 0,

"excedenteEstimadoCentavos": 0,

"armazenamentoExtraEstimadoCentavos": 0,

"teto": { "centavos": 8099, "usadoCentavos": 0, "padrao": true },

"estado": "NORMAL",

"produtos": \[

{ "produtoId": "pr_01H...", "nome": "api-pagamentos", "consumoGb": 5.1 },

{ "produtoId": "pr_02H...", "nome": "web-app", "consumoGb": 3.3 }

\]

}

periodoDeUso.tipo é MES (mensal e semestral) ou SEMANA (semanal). estado é NORMAL, PAUSADA_FRANQUIA ou PAUSADA_TETO.

**PUT /api/v1/consumo/teto** (Dono): corpo { "tetoCentavos": 20000 }. Resposta 200 com o teto novo; se a conta estava pausada pelo teto e o novo teto cobre o gasto, a pausa termina.

**GET /api/v1/consumo/avisos**: avisos do período de uso e dos anteriores.

Erros: 401 (sem login), 403 (membro comum, ou não-Dono ao mudar o teto), 400 (teto negativo ou abaixo do que já foi usado de excedente).

## 4. Dados

**consumo_mensal**: tenantId, produtoId, inicioDoPeriodo, gbBruto (soma), volumeRetidoMedioGb, ultimoEventoId, atualizadoEm.

**estado_ingestao**: tenantId, estado (NORMAL, PAUSADA_FRANQUIA, PAUSADA_TETO), desde, motivo. Lido pelo Coletor.

**aviso_consumo**: tenantId, tipo (FRANQUIA_80, FRANQUIA_100, TETO_80, TETO_100), periodoDeUso, enviadoEm, destinatarios.

**fechamento_consumo**: tenantId, periodoDeUso, gbBruto, excedenteGb, armazenamentoExtraGb, valorCentavos, idCobrancaAsaas, status.

**assinatura** (já existe): ganha tetoExcedenteCentavos (vazio = usa o padrão, a mensalidade do plano) e diaDoMesDeUso (dia do primeiro pagamento).

## 5. Organização do código (arquitetura hexagonal leve)

- **Entrada:** ConsumoController (consumo, teto, avisos) e o consumidor do stream de uso (UsoConsumer).

- **Regra de negócio:** GerenciadorConsumo (soma, percentuais, avisos, pausa) e FechamentoDeUso (calcula e cobra). O preço vem da tabela da LLT-230.

- **Porta do gateway:** GatewayPagamento.registrarExcedente (LLT-235).

- **Portas de dados e de mensagens:** repositórios de consumo, estado, avisos e fechamento (MongoDB); publicador de pedido de e-mail para o Notification.

- **Agendador:** fechamento diário dos períodos de uso e verificação de pausas.

## 6. Segurança e idempotência

- O Core nunca confia no consumo que a tela mostra: calcula sempre pelo que o Coletor mediu.

- O evento de uso tem id; evento repetido não soma duas vezes.

- Fechamento idempotente: um período de uso fecha uma vez; antes de criar a cobrança, o Core confere se já existe um fechamento com cobrança.

- Só Dono e Administrador leem; só Dono muda o teto, e a mudança fica registrada.

- Chaves do Asaas só em variáveis de ambiente.

## 7. Estados

Conta: NORMAL → PAUSADA_FRANQUIA (Free, 100%) → NORMAL (período vira ou upgrade). Conta: NORMAL → PAUSADA_TETO (plano pago, 100% do teto) → NORMAL (período vira ou teto aumentado). Período de uso: aberto → fechado (com ou sem cobrança de excedente).

## 8. Verificações no sandbox

Confirmadas em 26 e 27/10/2026 (viraram regra):

| **Verificação**                                                           | **Resultado**                                                                                                                                                                                                                                                                                     |
|---------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Somar o excedente à cobrança pendente do próximo ciclo (mensal e semanal) | **Funciona**: PUT /v3/payments/{id} com novo value e description (20,23 + 3 GB × R\$ 6,00 = 38,23, em cobrança semanal pendente).                                                                                                                                                                 |
| Cobrança avulsa para o excedente (semestral)                              | **Funciona**: POST /v3/payments com billingType PIX ou UNDEFINED (o cliente escolhe na fatura), valor e descrição com o detalhamento. Cobrança avulsa de R\$ 18,00 teve netValue 17,01: paga a taxa fixa do Asaas (R\$ 0,99 no sandbox, R\$ 1,99 no Pix padrão), como a planilha do Michel avisa. |

Ainda a conferir durante a implementação (com plano B):

| **Verificação**                                                                     | **Se der certo**         | **Se não der**                                                                           |
|-------------------------------------------------------------------------------------|--------------------------|------------------------------------------------------------------------------------------|
| POST /v3/payments avulsa já na forma de pagamento da assinatura com cartão guardado | A cobrança sai no cartão | A cobrança sai sem forma definida (UNDEFINED) e o cliente escolhe na fatura (já testado) |
| Medir o volume retido por dia no Coletor                                            | Média diária calculada   | Usa o volume do último dia do mês até a medição diária existir                           |

## 9. Testes (make test)

| **Teste**                                                                                                 | **O que garante**                  |
|-----------------------------------------------------------------------------------------------------------|------------------------------------|
| Membro comum recebe 403 em consumo, avisos e teto                                                         | Regra R3                           |
| Consumo por produto e total soma os eventos de uso do período de uso                                      | Regra R1                           |
| Evento de uso repetido não soma duas vezes                                                                | Seção 6                            |
| O mês de uso começa no dia do primeiro pagamento e usa o último dia do mês quando o dia não existe        | Seção 4 dos Requisitos             |
| Aviso de 80% e de 100% da franquia sai uma vez por período de uso                                         | Regra R4                           |
| Free chega a 1 GB: estado PAUSADA_FRANQUIA, sem cobrança, volta no mês seguinte                           | Regra R5                           |
| Plano pago passa da franquia: continua e calcula o excedente com o preço do plano e da forma de pagamento | Regra R6                           |
| Teto padrão = mensalidade do plano; o Dono altera e a mudança é registrada                                | Regra R7                           |
| Aviso de 80% e 100% do teto; 100% do teto pausa a ingestão                                                | Regra R8                           |
| Excedente e armazenamento extra entram na conta do teto                                                   | Regra R9                           |
| Armazenamento extra usa a média diária do mês, só na parte acima da franquia                              | Regra R10                          |
| Fechamento mensal: plano mensal soma o valor à próxima cobrança                                           | Regra R11                          |
| Fechamento semanal soma o excedente da semana à próxima cobrança semanal                                  | Regra R11                          |
| Fechamento mensal: semestral cria cobrança avulsa                                                         | Regra R11                          |
| Franquia semanal usa o mesmo número de GB do mensal e zera a cada semana de uso                           | Regra R11 e seção 4 dos Requisitos |
| Fechamento sem excedente não cria cobrança                                                                | Regra R11                          |
| Fechamento repetido não cria duas cobranças                                                               | Seção 6                            |
| No teste de 14 dias, passar da franquia pausa sem cobrar                                                  | Regra R12                          |
| Coletor recusa logs com a conta pausada; volta ao normal quando a pausa termina                           | Regra R13                          |
| Upgrade vale na hora para a franquia; downgrade só no próximo ciclo                                       | Regra R15                          |

## 10. Git

- Branch pelo card do Jira no lhamalog-core, com a chave LLT-234.

- Commits começam com LLT-234.

- PR com a chave no título, template preenchido e pelo menos um revisor.

## 11. Pendências

Nenhuma.

## 12. Ações decorrentes

- Quem cuida do Coletor: evento de uso por hora, leitura do estado de ingestão e recusa com resposta clara.

- Design: tela de consumo.

- Michel e Pedro: registrar no diagrama de classes consumo_mensal, estado_ingestao, aviso_consumo, fechamento_consumo e os campos novos da assinatura.

- O código começa quando o repositório lhamalog-core receber o template do Michel (LLT-80).
