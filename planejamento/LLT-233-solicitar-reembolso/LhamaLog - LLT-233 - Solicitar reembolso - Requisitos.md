# LLT-233 — Solicitar reembolso — Requisitos

Versão: v2 Status: para aprovação Autor: André Felipe Data: 27/10/2026 Épico: Assinatura e cobrança (LLT-109) · Sprint 6 Mudanças da v2: débito e boleto (pagos pela fatura) entram nas formas de pagamento estornáveis; o estorno do upgrade devolve a diferença com a taxa repassada. Relacionadas: LLT-231 (contratar), LLT-232 (alterar ou cancelar), LLT-235 (interface do gateway) Caso de uso: USID_043

## 1. Objetivo

Permitir que o Dono peça o dinheiro de volta nas situações que os Termos de Uso permitem, com aprovação da equipe LhamaLog e devolução pelo Asaas.

## 2. Quem usa

- **Dono da conta:** é o único que pede reembolso (decisão de 27/10/2026).

- **Equipe LhamaLog:** analisa o pedido e aprova ou nega, por uma rota interna sem tela no MVP (decisão de 22/10/2026).

## 3. O pedido no Jira

> Como administrador, quero pedir reembolso de cobrança indevida.

Critério de aceite do card:

1.  O fluxo segue a política definida e o recurso do gateway.

## 4. A política de reembolso (Termos de Uso, alinhados em 21/10/2026)

- **Primeira contratação:** reembolso **integral** em até 7 dias.

- **Upgrade:** em até 7 dias, devolve só a **diferença** cobrada.

- **Cobrança duplicada ou indevida:** a **qualquer tempo**, no valor da cobrança.

- Fora disso, **não há reembolso** de período já iniciado, inclusive no semestral.

## 5. Regras

| **\#** | **Regra**                                                                                                                                                                                                                                                       |
|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| R1     | Só o **Dono** pede reembolso.                                                                                                                                                                                                                                   |
| R2     | O pedido só é aceito nas três hipóteses da seção 4: (a) 1ª contratação há no máximo 7 dias, (b) upgrade há no máximo 7 dias, (c) cobrança duplicada ou indevida. Fora delas, a tela diz "não elegível" e explica o motivo.                                      |
| R3     | **Dados do pedido:** o pagamento escolhido, o motivo (lista: arrependimento na 1ª contratação, arrependimento do upgrade, cobrança duplicada, cobrança indevida, outro) e um texto livre.                                                                       |
| R4     | O sistema calcula o **valor a devolver** pela hipótese: (a) o valor pago da contratação, (b) o valor da diferença paga (a taxa repassada na diferença volta junto), (c) o valor da cobrança. Nunca passa do que foi pago.                                       |
| R5     | Cada pagamento tem **no máximo um pedido aberto** e não pode ser reembolsado duas vezes.                                                                                                                                                                        |
| R6     | **A equipe decide em até 7 dias corridos.** A tela avisa o prazo; pedidos passados do prazo aparecem como atrasados para a equipe.                                                                                                                              |
| R7     | A equipe **aprova ou nega**, sempre com um motivo escrito. Quem pediu é avisado por e-mail e na plataforma em cada mudança (pedido recebido, aprovado, concluído, negado).                                                                                      |
| R8     | **Cartão de crédito:** o estorno sai na hora que a equipe aprova (confirmado no sandbox). **Débito e boleto** (pagos pela fatura): seguem o mesmo pedido e a mesma aprovação; o estorno é feito pelo Asaas e só vale como concluído pelo aviso conferido (R10). |
| R9     | **Pix:** o Asaas só estorna com saldo na conta e pede uma segunda aprovação da equipe no painel do Asaas. Sem saldo, o pedido fica APROVADO aguardando saldo, a equipe é avisada e a chamada é repetida depois.                                                 |
| R10    | O reembolso só vale como **concluído** quando o Asaas avisa (REFUNDED) e o sistema confere na API do Asaas. Nunca se assume pelo pedido.                                                                                                                        |
| R11    | **Depois do reembolso da 1ª contratação**, a assinatura é encerrada na hora e a conta volta para o plano Free. **Depois do reembolso de um upgrade**, a assinatura volta ao plano anterior. Cobrança duplicada ou indevida não altera a assinatura.             |
| R12    | Tudo fica registrado: quem pediu, motivo, hipótese, valor, quem decidiu, quando e o resultado. O Dono consulta os pedidos dele.                                                                                                                                 |
| R13    | Chargeback (contestação no banco do cartão) está fora desta tarefa.                                                                                                                                                                                             |

## 6. Fora do escopo desta tarefa

- Contratar (LLT-231), alterar ou cancelar (LLT-232), consumo (LLT-234) e a interface do gateway (LLT-235).

- Tela interna para a equipe aprovar (no MVP é uma rota interna).

- Chargeback.

- Reembolso fora da política (por exemplo, de período já usado).

- Tela do front (épico do front web). Esta tarefa entrega a API.

## 7. Critérios de aceite

1.  Só o Dono consegue pedir reembolso, e só nas três hipóteses da política.

2.  O valor a devolver bate com a hipótese e nunca passa do valor pago.

3.  A equipe aprova ou nega com motivo, em até 7 dias corridos.

4.  Cartão estornado na hora da aprovação; Pix aguardando saldo e aprovação quando preciso.

5.  O reembolso só aparece como concluído depois do aviso do Asaas conferido na API.

6.  Reembolso da 1ª contratação encerra a assinatura e volta ao Free; o do upgrade volta ao plano anterior.

7.  Um pagamento não é reembolsado duas vezes.

8.  Cada pedido e cada decisão ficam registrados.

## 8. Decisões tomadas

Do André, em 21 e 22/10/2026:

- Política de reembolso igual à dos Termos de Uso (7 dias da 1ª contratação, 7 dias do upgrade, cobrança indevida a qualquer tempo).

- Aprovação da equipe, por rota interna sem tela no MVP.

Do André, em 27/10/2026:

- Só o Dono pede reembolso.

- A equipe responde em até 7 dias corridos.

- Reembolso da 1ª contratação encerra a assinatura e volta ao Free; reembolso do upgrade volta ao plano anterior.

- Estorno de Pix: aprovação manual da equipe (sem saldo, fica aguardando).

Achados do sandbox (25 e 26/10/2026) que viraram regra:

- Estorno no cartão é imediato e integral, sem aprovação extra (R8).

- Estorno no Pix fica aguardando aprovação humana no painel do Asaas, e no sandbox a aprovação não concluiu o estorno (R9, R10).

## 9. Pendências

Nenhuma.

## 10. Ações decorrentes

- Felipe (Termos de Uso): conferir que o texto de reembolso coincide com a seção 4.

- Design: protótipo da tela de pedido de reembolso (escolha do pagamento, motivo, prazo da resposta, status).

- Michel e Pedro: registrar no diagrama de classes o pedido de reembolso e seus status.

- O código desta tarefa começa quando o repositório lhamalog-core receber o template do Michel (LLT-80).
