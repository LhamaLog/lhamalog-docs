# LLT-233 — Solicitar reembolso — Desenho

Versão: v2 Status: para aprovação Autor: André Felipe Data: 27/10/2026 Base: documento de Requisitos da LLT-233 (v2) Mudanças da v2: estorno de débito e boleto na lista de verificações a conferir.

Este documento diz **como** a tarefa será construída. O **o quê** está no documento de Requisitos.

## 1. Partes envolvidas

| **Parte**            | **O que faz nesta tarefa**                                                                      |
|----------------------|-------------------------------------------------------------------------------------------------|
| Front                | Mostra os pagamentos elegíveis, recebe o pedido e o status (fora desta tarefa; usa a API daqui) |
| Core (lhamalog-core) | Confere a elegibilidade, guarda o pedido, fala com o Asaas e atualiza a assinatura              |
| Equipe LhamaLog      | Aprova ou nega por uma rota interna, e aprova o evento crítico do Pix no painel do Asaas        |
| Asaas                | Faz o estorno e avisa o resultado                                                               |
| MongoDB              | Guarda pagamentos, pedidos de reembolso e histórico                                             |

## 2. Fluxo

### 2.1 Pedido

1.  O Dono abre a lista de pagamentos: GET /api/v1/reembolsos/elegiveis devolve só os pagamentos que se encaixam na política (R2), com o valor máximo a devolver.

2.  Ele escolhe um pagamento, o motivo e o texto, e o front chama POST /api/v1/reembolsos.

3.  O Core confere o papel de Dono, a hipótese (a, b ou c), a janela de 7 dias, que não há pedido aberto nem reembolso anterior para o pagamento, e calcula o valor (R4).

4.  O Core grava o pedido como SOLICITADO, avisa o Dono ("recebemos seu pedido, resposta em até 7 dias corridos") e avisa a equipe.

### 2.2 Decisão da equipe

1.  A equipe usa a rota interna: POST /internal/reembolsos/{id}/aprovar ou /negar (com o motivo). Pedidos com mais de 7 dias sem decisão aparecem como atrasados em GET /internal/reembolsos?status=SOLICITADO&atrasados=true.

2.  **Negado:** o pedido vira NEGADO, e o Dono recebe o motivo por e-mail e na plataforma.

3.  **Aprovado:** o pedido vira APROVADO e o Core chama o Asaas: POST /v3/payments/{id}/refund com description (e value quando for parcial, no caso do upgrade).

### 2.3 Resposta do Asaas

- **Cartão:** o estorno é imediato (status REFUNDED, valor integral). O Core confere pelo aviso e pela consulta (GET /v3/payments/{id}) e marca CONCLUIDO.

- **Pix com saldo:** o Asaas deixa o estorno em AWAITING_CRITICAL_ACTION_AUTHORIZATION. O pedido passa a EM_PROCESSAMENTO, e a equipe aprova no painel do Asaas (botão "Enviar código"). Só com o aviso REFUNDED conferido na API o pedido vira CONCLUIDO.

- **Pix sem saldo:** o Asaas responde 400 "Saldo insuficiente". O pedido fica APROVADO com a marca AGUARDANDO_SALDO, a equipe é avisada por e-mail e, quando houver saldo, repete a aprovação (POST /internal/reembolsos/{id}/reenviar).

- **Débito e boleto** (pagos pela fatura): o Core chama o mesmo estorno; o resultado só vale com o aviso REFUNDED conferido na API.

### 2.4 Efeito na assinatura (regra R11)

Quando o pedido vira CONCLUIDO:

- **1ª contratação:** a assinatura é encerrada na hora (a mesma rotina do cancelamento no teste, da LLT-232: apaga a assinatura e as cobranças futuras no Asaas) e a conta volta ao plano Free.

- **Upgrade:** a assinatura volta ao plano anterior (atualiza o valor e a descrição no Asaas e os limites no Core).

- **Cobrança duplicada ou indevida:** nada muda na assinatura.

## 3. Contrato da API

**GET /api/v1/reembolsos/elegiveis** (Dono): lista de { "pagamentoId", "descricao", "valorPagoCentavos", "hipotese", "valorMaximoCentavos", "prazoAte" }.

**POST /api/v1/reembolsos** (Dono)

Corpo: { "pagamentoId": "p_01H...", "motivo": "ARREPENDIMENTO_PRIMEIRA_CONTRATACAO", "descricao": "..." }. Cabeçalho Idempotency-Key opcional.

Resposta 201: { "reembolsoId": "r_01H...", "status": "SOLICITADO", "valorCentavos": 8195, "respostaAte": "2026-11-03" }.

**GET /api/v1/reembolsos** e **GET /api/v1/reembolsos/{id}** (Dono): os pedidos dele e o status (SOLICITADO, APROVADO, EM_PROCESSAMENTO, CONCLUIDO, NEGADO).

**Rotas internas (equipe):** GET /internal/reembolsos, POST /internal/reembolsos/{id}/aprovar, POST /internal/reembolsos/{id}/negar (corpo { "motivo": "..." }) e POST /internal/reembolsos/{id}/reenviar. Protegidas por credencial de serviço e IP interno.

Erros do pedido:

| **Código** | **Quando**                                                                   |
|------------|------------------------------------------------------------------------------|
| 400        | Dados inválidos (pagamento inexistente, motivo fora da lista)                |
| 401        | Sem login                                                                    |
| 403        | Quem pede não é o Dono                                                       |
| 409        | NAO_ELEGIVEL, PEDIDO_ABERTO ou JA_REEMBOLSADO                                |
| 503        | Asaas fora do ar ao aprovar (o pedido continua aprovado para nova tentativa) |

## 4. Dados

**reembolso**

| **Campo**                              | **Observação**                                            |
|----------------------------------------|-----------------------------------------------------------|
| id                                     | identificador do pedido                                   |
| tenantId, solicitanteId                | conta e Dono                                              |
| pagamentoId, idPagamentoAsaas          | pagamento a devolver                                      |
| hipotese                               | PRIMEIRA_CONTRATACAO, UPGRADE, COBRANCA_INDEVIDA          |
| motivo, descricao                      | o que o Dono informou                                     |
| valorCentavos                          | valor a devolver (R4)                                     |
| status                                 | SOLICITADO, APROVADO, EM_PROCESSAMENTO, CONCLUIDO, NEGADO |
| aguardandoSaldo                        | verdadeiro quando o Pix ficou sem saldo                   |
| decididoPor, decididoEm, motivoDecisao | quem decidiu e por quê                                    |
| respostaAte                            | solicitação + 7 dias corridos                             |
| chaveIdempotencia                      | evita pedidos duplicados                                  |

O histórico da assinatura (LLT-232) recebe um registro quando o pedido é concluído.

## 5. Organização do código (arquitetura hexagonal leve)

- **Entrada:** ReembolsoController (Dono) e ReembolsoInternoController (equipe).

- **Regra de negócio:** GerenciadorAssinatura.solicitarReembolso (já existe no diagrama de classes) e ProcessamentoPagamento (conclui o pedido quando chega o aviso).

- **Porta do gateway:** GatewayPagamento.solicitarReembolsoExterno e consultarStatus (LLT-235).

- **Agendador** (@Scheduled com ShedLock): marca pedidos sem decisão passados de 7 dias como atrasados e lembra a equipe.

- **Portas de dados:** repositórios de reembolso, pagamento e assinatura, com adaptadores MongoDB.

## 6. Segurança e idempotência

- Só o papel Dono pede; as rotas internas exigem credencial de serviço.

- O valor a devolver nunca vem da tela: o Core calcula e confere contra o valor pago.

- Cada pagamento tem no máximo um pedido aberto e um reembolso concluído (verificado antes de chamar o Asaas).

- O estorno no Asaas leva a referência do pedido; antes de repetir uma chamada que deu tempo esgotado, o Core consulta se o estorno já existe.

- Avisos do Asaas: token, IP e reconsulta; aviso repetido é descartado pelo id do evento.

## 7. Estados

SOLICITADO → APROVADO → CONCLUIDO (cartão: direto; Pix: passa por EM_PROCESSAMENTO) SOLICITADO → NEGADO APROVADO (Pix sem saldo) → repete → EM_PROCESSAMENTO → CONCLUIDO

## 8. Verificações no sandbox

Confirmadas em 25 e 26/10/2026 (viraram regra):

| **Verificação**          | **Resultado**                                                         |
|--------------------------|-----------------------------------------------------------------------|
| Estorno no cartão        | **Imediato**: status REFUNDED, valor integral, sem aprovação extra.   |
| Estorno no Pix com saldo | Fica em AWAITING_CRITICAL_ACTION_AUTHORIZATION até aprovar no painel. |
| Estorno no Pix sem saldo | Erro 400 "Saldo insuficiente".                                        |

Ainda a conferir durante a implementação (com plano B):

| **Verificação**                                                | **Se der certo**                                                    | **Se não der**                                                                     |
|----------------------------------------------------------------|---------------------------------------------------------------------|------------------------------------------------------------------------------------|
| No sandbox, aprovar o evento crítico do Pix conclui o estorno  | O aviso REFUNDED chega e o pedido conclui                           | O pedido fica EM_PROCESSAMENTO até o aviso, e a equipe confere no painel do Asaas  |
| A taxa do Asaas volta no estorno                               | O LhamaLog recupera a taxa                                          | O custo da taxa fica por conta do LhamaLog e entra no cálculo de margem            |
| Estorno de pagamento no débito e no boleto (pagos pela fatura) | Estorno como no cartão (débito) ou com os dados do pagador (boleto) | A equipe faz o estorno pelo painel do Asaas e conclui o pedido por reprocessamento |

## 9. Testes (make test)

| **Teste**                                                                        | **O que garante** |
|----------------------------------------------------------------------------------|-------------------|
| Quem não é Dono recebe 403 ao pedir reembolso                                    | Regra R1          |
| Pagamento fora das três hipóteses recebe 409 NAO_ELEGIVEL                        | Regra R2          |
| 1ª contratação com 8 dias não é elegível; com 7 dias é                           | Regra R2          |
| Valor do upgrade é só a diferença paga; da 1ª contratação é o valor pago         | Regra R4          |
| Valor nunca passa do valor pago                                                  | Regra R4          |
| Segundo pedido para o mesmo pagamento recebe 409 PEDIDO_ABERTO ou JA_REEMBOLSADO | Regra R5          |
| Pedido sem decisão por mais de 7 dias aparece como atrasado                      | Regra R6          |
| Negar exige motivo e avisa o Dono                                                | Regra R7          |
| Aprovar no cartão estorna e conclui depois do aviso e da consulta                | Regras R8, R10    |
| Pix sem saldo fica APROVADO aguardando saldo e avisa a equipe                    | Regra R9          |
| Pix com saldo vira EM_PROCESSAMENTO e só conclui com o aviso REFUNDED conferido  | Regras R9, R10    |
| Reembolso da 1ª contratação encerra a assinatura e volta ao Free                 | Regra R11         |
| Reembolso do upgrade volta ao plano anterior                                     | Regra R11         |
| Cobrança indevida não altera a assinatura                                        | Regra R11         |
| Aviso repetido não conclui o pedido duas vezes                                   | Seção 6           |
| Cada pedido e decisão grava registro com quem e quando                           | Regra R12         |
| Asaas fora do ar ao aprovar devolve 503 e o pedido continua aprovado             | Seção 3           |

## 10. Git

- Branch pelo card do Jira no lhamalog-core, com a chave LLT-233.

- Commits começam com LLT-233.

- PR com a chave no título, template preenchido e pelo menos um revisor.

## 11. Pendências

Nenhuma.

## 12. Ações decorrentes

- Design: protótipo da tela de pedido de reembolso.

- Michel e Pedro: registrar no diagrama de classes reembolso e seus status.

- O código começa quando o repositório lhamalog-core receber o template do Michel (LLT-80).
