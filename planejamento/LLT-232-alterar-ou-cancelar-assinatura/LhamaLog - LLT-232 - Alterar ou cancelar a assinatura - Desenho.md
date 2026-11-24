# LLT-232 — Alterar ou cancelar a assinatura — Desenho

Versão: v2 Status: para aprovação Autor: André Felipe Data: 27/10/2026 Base: documento de Requisitos da LLT-232 (v2) Mudanças da v2: o valor da diferença do upgrade inclui a taxa fixa do Asaas repassada ao cliente.

Este documento diz **como** a tarefa será construída. O **o quê** está no documento de Requisitos.

## 1. Partes envolvidas

| **Parte**            | **O que faz nesta tarefa**                                                                                                     |
|----------------------|--------------------------------------------------------------------------------------------------------------------------------|
| Front                | Mostra a simulação, leva a pessoa à página de pagamento da diferença e mostra o resultado (fora desta tarefa; usa a API daqui) |
| Core (lhamalog-core) | Calcula a diferença, cria a alteração, fala com o Asaas, aplica a mudança e registra o histórico                               |
| Asaas                | Hospeda a página de pagamento da diferença, cobra os ciclos e avisa o resultado                                                |
| MongoDB              | Guarda a assinatura, as alterações e o histórico                                                                               |

## 2. Fluxos

### 2.1 Simular (antes de confirmar)

1.  O Dono escolhe plano e periodicidade novos.

2.  O front chama GET /api/v1/assinatura/alteracoes/simulacao?codigoPlano=PRO&periodicidade=MENSAL.

3.  O Core confere as regras (Dono, assinatura ATIVA, sem cancelamento agendado, não está no teste) e responde o **tipo** (UPGRADE, DOWNGRADE ou SO_PERIODICIDADE), o **valor da diferença** (só no upgrade), **quando vale** e os **bloqueios** (por exemplo, membros acima do limite).

### 2.2 Upgrade (vale na hora, depois de pagar a diferença)

1.  O front chama POST /api/v1/assinatura/alteracoes com o plano e a periodicidade novos.

2.  O Core recalcula a diferença (regra R4, com a taxa fixa da forma de pagamento da assinatura repassada), grava a alteração como AGUARDANDO_PAGAMENTO (expira em 1 hora) e cria no Asaas uma **página de pagamento avulsa**: POST /v3/checkouts com chargeTypes = DETACHED, billingTypes = CREDIT_CARD e PIX e um item "Upgrade Starter para Pro" (até 30 caracteres) com o valor da diferença.

3.  O Core guarda o código do checkout na alteração e devolve o link ao front. A pessoa paga na página do Asaas.

4.  O Asaas avisa o Core (webhook). O Core liga o aviso à alteração pelo checkoutSession (a página não grava a referência), consulta o pagamento na API do Asaas e só então aplica.

5.  **Aplicação:** o Core troca o plano e os limites da assinatura na hora; atualiza a assinatura no Asaas (PUT /v3/subscriptions/{id} com o valor novo, a descrição nova e updatePendingPayments = true, que também corrige a cobrança do próximo ciclo já gerada); e, se a troca incluir periodicidade nova, agenda essa parte para o próximo ciclo (2.3).

6.  A alteração passa a APLICADA, o histórico recebe o registro e o front é avisado pelo WebSocket.

Se a diferença não for paga (cartão recusado, Pix não pago ou página fechada), a alteração vira EXPIRADA e nada muda (regra R16).

### 2.3 Downgrade e troca de periodicidade (valem no próximo ciclo)

1.  O front chama POST /api/v1/assinatura/alteracoes.

2.  O Core confere os limites (regra R8): se o uso passa dos limites do plano novo, responde 409 LIMITES_EXCEDIDOS com o excesso.

3.  Sem bloqueio, o Core grava planoAgendado e periodicidadeAgendada na assinatura, com vigenciaAte como data em que passam a valer, e substitui qualquer agendamento anterior (regra R10).

4.  No Asaas, o Core atualiza a assinatura (PUT /v3/subscriptions/{id} com valor e ciclo novos e updatePendingPayments = true), o que altera a cobrança do próximo ciclo já gerada. Como a assinatura está ATIVA (ciclo atual pago), só essa cobrança muda.

5.  Na virada do ciclo, um job do Core aplica o agendado: troca o plano e os limites, limpa os campos ...Agendado e grava o histórico. Excedentes continuam como na ADR_129.

6.  Antes de a mudança valer, o Dono pode cancelar o agendamento: o Core desfaz o PUT no Asaas (volta valor e ciclo anteriores) e apaga os campos agendados.

### 2.4 Cancelar

1.  O front mostra as condições (acesso até vigenciaAte, sem reembolso do período, 30 dias para exportar) e, confirmado, chama POST /api/v1/assinatura/cancelamento.

2.  **No teste de 14 dias:** o Core apaga a assinatura no Asaas (DELETE /v3/subscriptions/{id}), volta a conta ao plano Free e registra no histórico.

3.  **Plano já pago:** o Core define a data final da assinatura no Asaas (PUT /v3/subscriptions/{id} com endDate = vigenciaAte) e **apaga cada cobrança futura pendente** (DELETE /v3/payments/{id}), porque o endDate sozinho não apaga as já geradas (no semanal são até 4). A assinatura fica CANCELAMENTO_AGENDADO e o acesso continua.

4.  Um job do Core, em vigenciaAte, apaga a assinatura no Asaas (DELETE /v3/subscriptions/{id}). O aviso SUBSCRIPTION_DELETED confirma, a assinatura vira CANCELADA, a ingestão para e os Tokens de Produto são revogados. Começa a contagem de 30 dias para exportar.

## 3. Contrato da API

Todas exigem login e o papel de Dono.

**GET /api/v1/assinatura/alteracoes/simulacao**

Resposta 200:

{

"tipo": "UPGRADE",

"planoAtual": "STARTER",

"planoNovo": "PRO",

"periodicidadeAtual": "MENSAL",

"periodicidadeNova": "MENSAL",

"diferencaCentavos": 16199,

"taxaRepassadaCentavos": 199,

"valeEm": "NA_HORA",

"bloqueios": \[\]

}

Exemplo: Starter para Pro mensal no Pix, com metade do ciclo restante: (40099 − 8099) × 0,5 + 199 = 16199 (R\$ 161,99). taxaRepassadaCentavos mostra a parte da taxa para a tela.

Em DOWNGRADE ou SO_PERIODICIDADE, diferencaCentavos vem null e valeEm traz a data (vigenciaAte). Em caso de bloqueio, bloqueios lista o motivo (por exemplo { "codigo": "MEMBROS_ACIMA_DO_LIMITE", "uso": 10, "limite": 3 }).

**POST /api/v1/assinatura/alteracoes**

Corpo: { "codigoPlano": "PRO", "periodicidade": "MENSAL" }. Cabeçalho Idempotency-Key opcional.

Resposta 201 (upgrade): { "alteracaoId": "a_01H...", "status": "AGUARDANDO_PAGAMENTO", "diferencaCentavos": 16199, "expiraEm": "...", "pagamento": { "tipo": "CHECKOUT", "url": "https://..." } }.

Resposta 200 (downgrade ou periodicidade): { "alteracaoId": "a_01H...", "status": "AGENDADA", "valeEm": "2026-11-26" }.

**DELETE /api/v1/assinatura/alteracoes/agendada**: cancela o agendamento antes de valer. Resposta 204.

**GET /api/v1/assinatura/alteracoes/{id}**: devolve o status da alteração (AGUARDANDO_PAGAMENTO, APLICADA, AGENDADA, EXPIRADA, CANCELADA).

**POST /api/v1/assinatura/cancelamento**: corpo opcional { "motivo": "..." }. Resposta 200: { "status": "CANCELAMENTO_AGENDADO", "acessoAte": "2026-11-26" }; no teste, { "status": "FREE" }.

**GET /api/v1/assinatura/historico**: lista das mudanças, da mais nova para a mais antiga.

Erros:

| **Código** | **Quando**                                                               |
|------------|--------------------------------------------------------------------------|
| 400        | Combinação inválida (plano igual ao atual, plano inexistente, Free)      |
| 401        | Sem login                                                                |
| 403        | Quem pede não é o Dono                                                   |
| 409        | ASSINATURA_NAO_ATIVA, CANCELAMENTO_AGENDADO, EM_TESTE, LIMITES_EXCEDIDOS |
| 503        | Asaas fora do ar                                                         |

## 4. Dados

**alteracao_assinatura**

| **Campo**                                                          | **Observação**                                                         |
|--------------------------------------------------------------------|------------------------------------------------------------------------|
| id                                                                 | identificador da alteração                                             |
| tenantId, solicitanteId                                            | conta e Dono que pediu                                                 |
| tipo                                                               | UPGRADE, DOWNGRADE, SO_PERIODICIDADE                                   |
| planoAnterior, planoNovo, periodicidadeAnterior, periodicidadeNova | o que mudou                                                            |
| diferencaCentavos                                                  | só no upgrade (inclui a taxa fixa repassada)                           |
| status                                                             | AGUARDANDO_PAGAMENTO, APLICADA, AGENDADA, EXPIRADA, CANCELADA          |
| valeEm                                                             | data em que passa a valer                                              |
| idCheckoutAsaas                                                    | ligação com o Asaas no upgrade (chave para achar a alteração no aviso) |
| expiraEm                                                           | criação + 1 hora (upgrade)                                             |
| chaveIdempotencia                                                  | evita duas alterações iguais                                           |

**assinatura** (já existe): ganha planoAgendado, periodicidadeAgendada, vigenciaAte e canceladaEm.

**historico_assinatura**: tenantId, quem, quando, tipo da mudança, antes e depois (plano e periodicidade), valor da diferença, resultado e data em que passa a valer. Só se inclui; nunca se altera nem apaga.

## 5. Organização do código (arquitetura hexagonal leve)

- **Entrada:** AlteracaoAssinaturaController (simular, alterar, cancelar agendamento, histórico) e CancelamentoController. O webhook é da LLT-235.

- **Regra de negócio:** GerenciadorAssinatura.alterarPlano, calcularValorProporcional (já existe no diagrama de classes) e cancelarAssinatura. ProcessamentoPagamento aplica o upgrade quando o pagamento da diferença é confirmado.

- **Porta do gateway:** GatewayPagamento (LLT-235) com enviarCobranca (página avulsa), alterarAssinatura (valor, ciclo e descrição), cancelarAssinatura (data final, apagar cobranças futuras e apagar a assinatura) e consultarStatus.

- **Adaptador do Asaas:** ApiPagamento.

- **Agendadores** (@Scheduled com ShedLock): aplicar as mudanças agendadas na virada do ciclo, expirar alterações não pagas e encerrar as assinaturas em vigenciaAte.

- **Portas de dados:** repositórios de alteração, assinatura e histórico, com adaptadores MongoDB.

## 6. Segurança e idempotência

- Só o papel Dono passa; o Core confere o papel pela Clerk em cada chamada.

- O valor e o plano nunca vêm da tela: o Core lê a tabela de preços (LLT-230) e calcula a diferença.

- Avisos do Asaas: token, IP e reconsulta; aviso repetido é descartado pelo id do evento.

- Cada alteração e cada cancelamento tem chave de idempotência; antes de repetir uma chamada ao Asaas que deu tempo esgotado, o Core pergunta se o recurso já existe.

- Chaves do Asaas ficam só em variáveis de ambiente.

- Limite de tentativas por usuário nas chamadas de alteração.

## 7. Estados

Alteração: AGUARDANDO_PAGAMENTO → APLICADA (diferença paga) ou EXPIRADA (não paga em 1 hora). Alteração agendada: AGENDADA → APLICADA (na virada) ou CANCELADA (o Dono desfez). Assinatura: ATIVA → CANCELAMENTO_AGENDADO → CANCELADA (em vigenciaAte); no teste, ATIVA → Free na hora.

## 8. Verificações no sandbox

Confirmadas em 26 e 27/10/2026 (viraram regra):

| **Verificação**                                                      | **Resultado**                                                                                                                                                                                        |
|----------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| A página avulsa aceita Pix e cartão e cobra só a diferença?          | **Sim.** DETACHED com CREDIT_CARD e PIX; pago no cartão: cobrança CONFIRMED sem assinatura, ligada só pelo checkoutSession. A cobrança avulsa paga a taxa do Asaas (R\$ 160,00 renderam R\$ 156,33). |
| Trocar valor e ciclo da assinatura muda a cobrança do próximo ciclo? | **Sim**, com updatePendingPayments = true.                                                                                                                                                           |
| O endDate apaga cobranças futuras?                                   | **Não.** É preciso DELETE /v3/payments/{id} em cada uma (confirmado, deleted: true).                                                                                                                 |
| Cancelar no teste sem cobrança?                                      | O teste de 14 dias mantém a cobrança PENDING até o dia 15; apagar a assinatura antes não cobra nada.                                                                                                 |
| As renovações herdam descrição e referência da assinatura?           | **Sim.**                                                                                                                                                                                             |

Ainda a conferir durante a implementação (com plano B):

| **Verificação**                                                                   | **Se der certo**                       | **Se não der**                                                         |
|-----------------------------------------------------------------------------------|----------------------------------------|------------------------------------------------------------------------|
| Depois de trocar o ciclo para semestral, o vencimento seguinte é recalculado      | A cobrança seguinte vem 6 meses depois | O Core ajusta o vencimento com nextDueDate na virada do ciclo          |
| Desfazer o agendamento com um novo PUT volta o valor da cobrança do próximo ciclo | Agendamento cancelável                 | O Core apaga a cobrança do próximo ciclo e deixa o Asaas gerar de novo |

## 9. Testes (make test)

| **Teste**                                                                                                                                                                                             | **O que garante**      |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------|
| Quem não é Dono recebe 403 em alterar e cancelar                                                                                                                                                      | Regra R1               |
| Assinatura em atraso ou suspensa recebe 409 ASSINATURA_NAO_ATIVA                                                                                                                                      | Regra R2               |
| Diferença do upgrade = (preço novo − atual) × dias restantes ÷ dias do ciclo + taxa fixa da forma (Pix e boleto R\$ 1,99; crédito R\$ 0,49 ÷ 0,9701; débito R\$ 0,35 ÷ 0,9811), arredondada para cima | Regra R4               |
| Upgrade só aplica o plano novo depois do aviso de pagamento confirmado e da consulta na API                                                                                                           | Regra R3               |
| Upgrade não pago expira e a assinatura fica como estava                                                                                                                                               | Regra R16              |
| Aviso do upgrade é ligado à alteração pelo checkoutSession                                                                                                                                            | Seção 2.2              |
| Depois do upgrade, o valor da assinatura e da próxima cobrança no Asaas é o do plano novo                                                                                                             | Regra R5               |
| Downgrade só vale na virada do ciclo; até lá os limites antigos continuam                                                                                                                             | Regra R6               |
| Troca de periodicidade junto com upgrade: plano na hora e periodicidade no próximo ciclo                                                                                                              | Regra R7               |
| Downgrade com membros ou produtos acima do limite recebe 409 LIMITES_EXCEDIDOS                                                                                                                        | Regra R8               |
| Novo agendamento substitui o anterior; o Dono consegue cancelar o agendamento                                                                                                                         | Regra R10              |
| Durante o teste de 14 dias, trocar de plano recebe 409 EM_TESTE                                                                                                                                       | Regra R11              |
| Cancelar no teste apaga a assinatura no Asaas e volta ao Free sem cobrança                                                                                                                            | Regra R11              |
| Cancelar um plano pago define a data final e apaga todas as cobranças futuras pendentes (semanal: até 4)                                                                                              | Regras R12, critério 9 |
| Na data final a assinatura vira CANCELADA, a ingestão para e os tokens são revogados                                                                                                                  | Regra R12              |
| Com cancelamento agendado, trocar de plano recebe 409 CANCELAMENTO_AGENDADO                                                                                                                           | Regra R15              |
| Cada mudança grava um registro no histórico, e o histórico não pode ser alterado                                                                                                                      | Regra R17              |
| Aviso repetido do Asaas não aplica o upgrade duas vezes                                                                                                                                               | Seção 6                |
| Asaas fora do ar devolve 503 e não altera nada                                                                                                                                                        | Seção 3                |

## 10. Git

- Branch pelo card do Jira no lhamalog-core, com a chave LLT-232.

- Commits começam com LLT-232.

- PR com a chave no título, template preenchido e pelo menos um revisor.

## 11. Pendências

Nenhuma.

## 12. Ações decorrentes

- Design: protótipo da área da assinatura (simulação do upgrade, aviso de excesso, fim do acesso, histórico).

- Michel e Pedro: registrar no diagrama de classes alteracao_assinatura, historico_assinatura e os campos novos da assinatura.

- O código começa quando o repositório lhamalog-core receber o template do Michel (LLT-80).
