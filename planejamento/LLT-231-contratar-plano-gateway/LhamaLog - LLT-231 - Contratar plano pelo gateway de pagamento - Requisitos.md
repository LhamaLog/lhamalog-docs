# LLT-231 — Contratar plano pelo gateway de pagamento — Requisitos

Versão: v5 Status: para aprovação Autor: André Felipe Data: 27/10/2026 Épico: Assinatura e cobrança (LLT-109) · Sprint 6 Relacionadas: LLT-230 (ver planos), LLT-232 (alterar ou cancelar), LLT-233 (reembolso), LLT-234 (consumo), LLT-235 (interface do gateway) Mudanças da v5: cartão de débito e boleto entram no MVP (pagos pela fatura do Asaas, sem débito automático), com os preços da LLT-230 v7. Mudanças da v4: confirmações no sandbox com os preços do Planos Ajustado (26/10/2026): o teste de 14 dias funciona; o Pix semanal gera várias cobranças de uma vez; a página de pagamento do cartão não grava descrição nem referência (o Core preenche depois); nome do item com no máximo 30 caracteres; cartão recusado não cria cobrança. Mudanças da v3: o valor cobrado é o preço público da aba Planos Ajustado do Plano de Monetização v4 (LLT-230), sem fórmula; o excedente no plano mensal vai na mesma fatura da mensalidade. Mudanças da v2: segue o Plano de Monetização v4 e os testes feitos no sandbox do Asaas em 24 e 25/10/2026. Entram a periodicidade semanal e semestral; o Pix passa a ser criado direto como assinatura; o Asaas exige telefone e endereço completo; o preço depende da forma de pagamento.

## 1. Objetivo

Permitir que uma pessoa assine um plano pago com pagamento seguro, e que a assinatura só fique ativa depois que o gateway de pagamento (Asaas) confirmar.

## 2. Quem usa

- **Comprador novo:** cria a conta e contrata um plano pago. Ao ter o pagamento confirmado, vira o **Dono** da conta.

- **Dono de uma conta Free:** já tem conta e decide passar para um plano pago.

## 3. O pedido no Jira

> Como administrador, quero assinar um plano com pagamento seguro.

Critérios de aceite do card:

1.  Pagamento feito no gateway escolhido; o LhamaLog não guarda dados de cartão.

2.  Assinatura só fica ativa após confirmação do gateway.

3.  Eventos do gateway são verificados e idempotentes.

## 4. Como o pagamento funciona (contexto)

- **Formas de pagamento:** cartão de crédito (o Asaas cobra sozinho a cada ciclo), Pix, cartão de débito e boleto (nestes três o cliente paga a cada cobrança; débito e boleto são pagos pela fatura do Asaas, sem débito automático). Pix Automático só depois que o CNPJ da empresa completar 6 meses.

- **Periodicidade:** semanal, mensal ou semestral.

- **Valor cobrado:** o preço público da LLT-230 (aba Planos Ajustado do v4) para o plano, a periodicidade e a forma de pagamento escolhidos, já com a taxa do Asaas. O excedente de GB e o armazenamento extra não fazem parte desta tarefa (LLT-234 e LLT-235): no mensal vão na mesma fatura da mensalidade seguinte; no semanal, o excedente da semana vem junto com a cobrança semanal; no semestral, numa cobrança mensal separada.

- **Três caminhos no Asaas** (confirmado no sandbox): o **cartão de crédito** usa a página de pagamento hospedada pelo Asaas; o **Pix** não pode usar essa página em assinatura recorrente, então o Core cria a assinatura direto e o cliente paga pelo QR Code da cobrança; o **débito** e o **boleto** também são assinaturas criadas direto, e o cliente paga cada cobrança pela fatura do Asaas.

- Até a empresa ter CNPJ, tudo roda no ambiente de testes (sandbox) do Asaas.

## 5. Regras

| **\#** | **Regra**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| R1     | Só se contrata plano pago. O plano Free não passa pelo gateway.                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| R2     | Quem contrata precisa ter login. O plano, o valor e a periodicidade vêm dos dados de planos (LLT-230), nunca digitados pela tela.                                                                                                                                                                                                                                                                                                                                                                         |
| R3     | **Dados pedidos:** CPF ou CNPJ, nome ou razão social, e-mail de cobrança, **telefone** e **endereço completo** (CEP, rua, número, bairro; a cidade vem do CEP). O Asaas exige telefone e endereço para abrir a página de pagamento.                                                                                                                                                                                                                                                                       |
| R4     | **Aceite:** o comprador precisa marcar que aceita os Termos de Uso e a Política de Privacidade. O LhamaLog guarda quem aceitou, quando (data e hora) e qual versão de cada documento.                                                                                                                                                                                                                                                                                                                     |
| R5     | **Cartão:** o pagamento é feito na página do Asaas. O LhamaLog nunca vê nem guarda número de cartão.                                                                                                                                                                                                                                                                                                                                                                                                      |
| R6     | **Ativação só com confirmação do gateway.** Voltar da página de pagamento não ativa nada. A conta é criada (ou o plano trocado) só quando o Asaas confirma o pagamento e o LhamaLog confere esse estado direto na API do Asaas.                                                                                                                                                                                                                                                                           |
| R7     | **Eventos do gateway** são conferidos (token, IP de origem e consulta à API) e tratados uma única vez, mesmo que o Asaas mande o mesmo aviso duas vezes ou fora de ordem.                                                                                                                                                                                                                                                                                                                                 |
| R8     | **Pix, débito e boleto:** o cliente tem **3 dias** para pagar a primeira cobrança. Passado esse prazo, a contratação expira e nenhuma conta é criada.                                                                                                                                                                                                                                                                                                                                                     |
| R9     | **Conta Free que contrata:** não cria conta nova. Ao confirmar o pagamento, o plano da conta passa para o plano pago. Não há cobrança proporcional.                                                                                                                                                                                                                                                                                                                                                       |
| R10    | **Conta que já tem plano pago ativo** não contrata de novo: a pessoa é levada para alterar o plano (LLT-232).                                                                                                                                                                                                                                                                                                                                                                                             |
| R11    | **Ciclo:** começa no dia do primeiro pagamento, e as próximas cobranças vencem no mesmo dia da semana (semanal), do mês (mensal) ou a cada 6 meses (semestral). Com teste, o ciclo pago começa no 15º dia.                                                                                                                                                                                                                                                                                                |
| R12    | **Semestral:** a mensalidade base dos 6 meses é paga numa cobrança só, adiantada.                                                                                                                                                                                                                                                                                                                                                                                                                         |
| R13    | **Teste grátis de 14 dias:** vale só para os planos **Starter e Pro**, só no pagamento **mensal** e só com **cartão de crédito**. Pix, débito e boleto pagam na contratação.                                                                                                                                                                                                                                                                                                                              |
| R14    | **Uma vez por CPF/CNPJ:** o mesmo documento não usa o teste duas vezes.                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| R15    | **Durante o teste** vale a franquia de GB do plano. Ao chegar no limite, a ingestão pausa e nada é cobrado (avisos em 80% e 100%, na LLT-234).                                                                                                                                                                                                                                                                                                                                                            |
| R16    | **Cancelar durante o teste:** a conta volta para o plano Free, sem cobrança. **Falha no pagamento do 15º dia:** segue a regra de atraso (15 dias de carência com acesso, 30 dias suspensa, depois cancelada).                                                                                                                                                                                                                                                                                             |
| R17    | Se o Asaas não permitir adiar a primeira cobrança do cartão (conferido no sandbox), o teste sai do MVP e a contratação cobra na hora. O resto não muda.                                                                                                                                                                                                                                                                                                                                                   |
| R18    | **Nota fiscal:** a NFS-e é emitida pelo Asaas a cada cobrança, configurada depois da ativação. Só vale em produção, depois de a empresa ter CNPJ (no sandbox, com dados fictícios).                                                                                                                                                                                                                                                                                                                       |
| R19    | **Falhas:** se o Asaas estiver fora do ar ao iniciar, a tela diz "não foi possível iniciar a contratação, tente depois". Se o pagamento foi aprovado mas a criação da conta falhou, a tela diz "pagamento recebido, ativação em processamento", e a equipe reprocessa.                                                                                                                                                                                                                                    |
| R20    | O que o comprador vê na confirmação: o plano, o valor, a periodicidade e, no Pix, como pagar (QR Code e código copia e cola) e até quando; no débito e no boleto, o link da fatura do Asaas e até quando.                                                                                                                                                                                                                                                                                                 |
| R21    | **Cartão recusado** na página do Asaas (mensagem "Pagamento não autorizado"): o Asaas **não cria cobrança nem assinatura**, o comprador pode tentar de novo com outro cartão na mesma página, e nenhuma conta é criada.                                                                                                                                                                                                                                                                                   |
| R22    | O Asaas gera a primeira cobrança no momento em que a assinatura é criada. As seguintes são geradas por ele com antecedência. No **plano semanal** ele gera **4 cobranças de uma vez** (a da semana e as 3 seguintes); só a cobrança já vencida conta como atraso.                                                                                                                                                                                                                                         |
| R23    | **Identificação do pagamento no cartão:** a página de pagamento do Asaas não grava a descrição nem a referência do LhamaLog na assinatura. O Core guarda o código do checkout (checkoutSession) no pré-cadastro para ligar o aviso do Asaas à contratação e, depois da confirmação, preenche a descrição e a referência na assinatura. No Pix, os dois campos já vão na criação.                                                                                                                          |
| R24    | **Textos que o cliente vê** (fatura, e-mail, página de pagamento): "LhamaLog - Plano Starter (mensal)", montado pelo Core a partir do plano e da periodicidade. O nome do item da página de pagamento tem no máximo 30 caracteres.                                                                                                                                                                                                                                                                        |
| R25    | **Cartão de débito:** o Asaas não debita sozinho. A assinatura é criada com forma "a escolher" e o cliente paga **cada cobrança** abrindo a fatura (o Asaas avisa por e-mail) e escolhendo débito. O preço é o de débito do Planos Ajustado. Cobrança não paga segue a regra de atraso (15 dias de carência, 30 dias suspensa, depois cancelada). A fatura também mostra Pix, crédito e boleto; se o cliente pagar com outra forma, o valor líquido do LhamaLog pode ser menor, e o fato fica registrado. |
| R26    | **Boleto:** a assinatura é criada direto como boleto, com o preço do Pix (decisão de 27/10/2026). O boleto vence em 3 dias; pago pelo QR Code Pix do boleto, confirma na hora; pelo código de barras, em até 3 dias úteis. A conta só é liberada depois da confirmação.                                                                                                                                                                                                                                   |

## 6. Fora do escopo desta tarefa

- Ver os planos (LLT-230).

- Trocar de plano, de periodicidade ou cancelar depois de ativo (LLT-232).

- Reembolso (LLT-233).

- Consumo de GB e cobrança do excedente (LLT-234).

- A interface do gateway em si e o recebimento genérico de avisos (LLT-235). A 231 usa essa interface, então as duas andam juntas.

- Tela do front (épico do front web). Esta tarefa entrega a API.

- Plano anual, cupom de desconto e Pix Automático.

## 7. Critérios de aceite

1.  O pagamento no cartão é feito na página do Asaas e nenhum dado de cartão passa pelo LhamaLog.

2.  A conta só fica ativa depois de o Asaas confirmar o pagamento, e a confirmação é conferida na API do Asaas.

3.  Um aviso repetido do Asaas não cria conta nem cobrança em dobro.

4.  Pix, débito ou boleto não pagos em 3 dias expiram sem criar conta.

5.  A conta Free que paga troca de plano sem criar outra conta.

6.  Quem já tem plano pago ativo é levado para alterar o plano.

7.  O aceite dos Termos e da Política fica registrado com data, hora e versão.

8.  O valor cobrado é o da LLT-230 para o plano, a periodicidade e a forma de pagamento.

9.  O teste de 14 dias só aparece para Starter e Pro, mensal, com cartão de crédito, e uma vez por CPF/CNPJ.

10. Cancelar no teste volta a conta para o Free sem cobrança.

11. Cartão recusado não cria conta e permite nova tentativa.

12. Falha ao criar a conta depois do pagamento fica registrada e pode ser reprocessada pela equipe.

## 8. Decisões tomadas

Do André, em 22/10/2026:

- Pode contratar quem tem CPF ou CNPJ.

- Prazo da primeira cobrança do Pix: 3 dias.

- Conta Free que paga é uma contratação (esta tarefa), sem criar conta nova.

- O aceite dos Termos e da Política é registrado no Core, com data, hora e versão.

- Teste de 14 dias grátis, só com cartão, uma vez por CPF/CNPJ, só Starter e Pro, só no mensal.

- Durante o teste, passar da franquia pausa a ingestão, sem cobrar.

- Cancelar no teste volta ao Free; falha no 15º dia segue a regra de atraso.

- Se o Asaas não permitir adiar a primeira cobrança, o teste sai do MVP (conferido no sandbox: permite, o plano B não é preciso).

- O ciclo começa no dia do primeiro pagamento.

- O Tenant só nasce com o pagamento confirmado, com os dados guardados antes num pré-cadastro.

- O gateway é o Asaas; Pix Automático só depois de 6 meses de CNPJ.

Do André, em 26/10/2026 (Plano de Monetização v4):

- Periodicidade semanal, mensal e semestral; o anual saiu.

- Preço por forma de pagamento, com a taxa do Asaas somada.

- O valor cobrado é o preço do Planos Ajustado, copiado como dado (sem fórmula no sistema).

Achados do sandbox do Asaas (24 e 25/10/2026), que viraram regra:

- A página de pagamento recorrente só aceita cartão de crédito; o Pix recorrente é criado direto como assinatura.

- A página de pagamento com cliente já cadastrado exige telefone e endereço completo (R3).

- A criação da assinatura gera a primeira cobrança na hora (R22).

- O teste de 14 dias funciona: com o primeiro vencimento em 14 dias, o cartão é guardado e **não é cobrado** até lá (R13, R17 sem plano B).

- O Pix semanal gera 4 cobranças de uma vez (R22); o semestral gera uma só.

- A página de pagamento não grava descrição nem referência (R23); o nome do item aceita no máximo 30 caracteres (R24).

- Cartão recusado não cria nada (R21).

- No cartão, o dinheiro cai na conta do LhamaLog cerca de 30 dias depois; no Pix, na hora.

Do André, em 27/10/2026:

- **Cartão de débito e boleto entram no MVP**, pagos pela fatura do Asaas (sem débito automático). O preço do boleto é igual ao do Pix.

## 9. Pendências

Nenhuma.

## 10. Ações decorrentes

- Felipe (Termos de Uso): incluir que o serviço pode ser contratado por profissional autônomo (CPF) e descrever o teste de 14 dias (planos, cartão de crédito, uma vez por documento).

- Design (protótipo da tela de pagamento): pedir telefone e endereço completo; mostrar seletores de periodicidade (semanal, mensal, semestral) e de forma de pagamento (Pix, cartão, débito, boleto); mostrar o teste só em Starter e Pro, mensal, com cartão; remover o plano anual.

- André: perguntar ao suporte do Asaas se dá para restringir as formas de pagamento da fatura de uma assinatura (para o cliente do débito não pagar com outra forma pelo mesmo preço).

- Michel e Pedro: registrar no diagrama de classes o pré-cadastro, o registro de aceite e o registro de uso do teste, e os campos novos da assinatura.

- Conta Asaas de produção: precisa de uma chave Pix cadastrada para gerar cobranças Pix (no sandbox a chave foi cadastrada nos testes).

- O código desta tarefa começa quando o repositório lhamalog-core receber o template do Michel (LLT-80).
