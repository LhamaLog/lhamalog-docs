# LLT-231 — Contratar plano pelo gateway de pagamento — Desenho

Versão: v5 Status: para aprovação Autor: André Felipe Data: 27/10/2026 Base: documento de Requisitos da LLT-231 (v5) Mudanças da v5: caminhos de débito e boleto (assinatura direta, pagos pela fatura do Asaas), formas DEBITO e BOLETO na API. Mudanças da v4: achados do sandbox de 26/10/2026 aplicados: ligação do pagamento no cartão pelo código do checkout e preenchimento posterior da descrição e da referência; teste de 14 dias, ciclos semanal e semestral e acerto do vencimento confirmados; Pix semanal com 4 cobranças; nomes com até 30 caracteres. Mudanças da v3: o valor vem da tabela_precificacao (preço público do Planos Ajustado, LLT-230), sem CalculadoraPreco. Mudanças da v2: dois caminhos no Asaas (cartão pela página hospedada, Pix direto como assinatura); sem anual; periodicidade semanal, mensal e semestral; cliente com telefone e endereço completo; preço da tabela da LLT-230; achados do sandbox na seção 9.

Este documento diz **como** a tarefa será construída. O **o quê** está no documento de Requisitos.

## 1. Partes envolvidas

| **Parte**            | **O que faz nesta tarefa**                                                                                                                           |
|----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|
| Front                | Coleta os dados, mostra o resultado e leva o comprador à página do Asaas, ao QR Code Pix, à fatura ou ao boleto (fora desta tarefa; usa a API daqui) |
| Core (lhamalog-core) | Cria a contratação, fala com o Asaas, recebe os avisos e ativa a conta                                                                               |
| Clerk                | Confirma o login e cria a Organization da conta                                                                                                      |
| Asaas                | Cobra, hospeda a página de pagamento do cartão e a fatura, e avisa o resultado                                                                       |
| MongoDB              | Guarda pré-cadastro, aceite, uso do teste, assinatura e pagamentos                                                                                   |

## 2. Fluxo principal

1.  O comprador escolhe plano, periodicidade e forma de pagamento (LLT-230) e preenche os dados.

2.  O front chama POST /api/v1/contratacoes com o login.

3.  O Core confere o login na Clerk, os dados e as regras (plano pago ativo, sem assinatura paga, combinação válida).

4.  O Core lê o valor na tabela_precificacao (LLT-230) e grava o **pré-cadastro** (status AGUARDANDO_PAGAMENTO) e o **aceite** dos Termos.

5.  O Core cria ou atualiza o cliente no Asaas (POST /v3/customers), com CPF/CNPJ, nome, e-mail, telefone e endereço completo. O pré-cadastro vai como externalReference.

6.  Daqui o caminho depende da forma de pagamento:

    - **Cartão:** POST /v3/checkouts com chargeTypes = RECURRENT, billingTypes = CREDIT_CARD, o ciclo (WEEKLY, MONTHLY ou SEMIANNUALLY) e o valor. O nome do item tem no máximo 30 caracteres ("Plano Starter (mensal)"). O Asaas devolve o link da página de pagamento.

    - **Pix:** POST /v3/subscriptions com billingType = PIX, o ciclo, o valor, a descrição ("LhamaLog - Plano Starter (mensal)"), o externalReference e o vencimento da primeira cobrança em 3 dias. O Asaas gera a primeira cobrança na hora (no semanal, 4 de uma vez); o Core busca o QR Code dela (GET /v3/payments/{id}/pixQrCode).

    - **Débito:** POST /v3/subscriptions com billingType = UNDEFINED (o Asaas não aceita débito na assinatura), o ciclo, o valor do **débito**, a descrição, o externalReference e o vencimento em 3 dias. A cobrança nasce PENDING; o Core devolve o invoiceUrl e o cliente escolhe débito na fatura.

    - **Boleto:** POST /v3/subscriptions com billingType = BOLETO, o ciclo, o valor do Pix, a descrição e o vencimento em 3 dias; o Core devolve o link do boleto (bankSlipUrl).

7.  O Core devolve ao front o link (cartão), o QR Code Pix, ou o link da fatura (débito) ou do boleto. No cartão, o Core guarda o código do checkout (idCheckoutAsaas, devolvido na criação) no pré-cadastro. A pessoa paga.

8.  Ao voltar da página do cartão, o front mostra "pagamento em processamento": voltar **não** ativa nada.

9.  O Asaas avisa o Core (webhook). O Core confere o aviso, consulta o pagamento direto na API do Asaas e só então ativa.

10. **Ativação:** no cartão, o Core liga o aviso ao pré-cadastro pelo checkoutSession e preenche a descrição e a referência na assinatura (PUT /v3/subscriptions/{id} com description e externalReference); cria a Organization na Clerk, o Tenant, a Assinatura (ATIVA), o Membro Dono e os papéis padrão; grava o pagamento; configura a nota fiscal; e avisa o front pelo WebSocket.

11. **Acerto do ciclo (Pix, débito e boleto):** como o ciclo começa no dia do primeiro pagamento (R11), o Core atualiza a data do próximo vencimento da assinatura (PUT /v3/subscriptions/{id} com nextDueDate) para um ciclo depois do pagamento.

12. O pré-cadastro passa para CONCLUIDO.

## 3. Variações

**Com teste de 14 dias (Starter ou Pro, mensal, cartão)** No passo 6, o checkout recorrente recebe o vencimento da primeira cobrança 14 dias à frente. O cartão fica registrado na página do Asaas, e a primeira cobrança só acontece no 15º dia.

- **Ativação:** o aviso que ativa a conta é a **criação da assinatura**, conferida na API do Asaas (assinatura ativa com cartão registrado). A assinatura recebe testeAte (hoje + 14 dias).

- **Dia 15:** o Asaas cobra o cartão. Pagou: segue o ciclo normal. Falhou: regra de atraso (15 dias de carência, 30 dias suspensa, depois cancelada).

- **Cancelar no teste:** o Core apaga a assinatura no Asaas e volta a conta ao Free, sem cobrança.

- **Uma vez por documento:** antes de criar o checkout, o Core confere o registro de uso do teste. Se o CPF/CNPJ já usou, responde 409.

**Cartão recusado** A página do Asaas mostra "Pagamento não autorizado" e deixa o comprador tentar de novo; nenhuma cobrança nem assinatura nasce, e não chega nenhum aviso. Enquanto não houver pagamento confirmado, o pré-cadastro continua AGUARDANDO_PAGAMENTO e nada é ativado. Se o pré-cadastro vencer (seção 8), vira EXPIRADO.

**Conta Free que contrata** Os passos 3 a 9 são iguais, mas o pré-cadastro guarda o tenantId da conta existente. No passo 10, em vez de criar conta, o Core **troca o plano** da Assinatura Free e a vigência passa a valer.

**Conta que já tem plano pago ativo** No passo 3, o Core responde 409 com o código JA_TEM_PLANO_PAGO, e o front leva a pessoa para a tela de alteração (LLT-232).

## 4. Contrato da API

**POST /api/v1/contratacoes** (exige login)

Corpo:

{

"codigoPlano": "PRO",

"periodicidade": "MENSAL",

"formaPagamento": "CARTAO",

"comTeste": true,

"cliente": {

"documento": "12345678000199",

"nome": "Empresa Exemplo Ltda",

"emailCobranca": "financeiro@exemplo.com",

"telefone": "47999999999",

"endereco": { "cep": "89201001", "logradouro": "...", "numero": "100", "bairro": "..." }

},

"aceite": { "versaoTermos": "0.2", "versaoPrivacidade": "0.2" }

}

Valores aceitos: periodicidade = SEMANAL, MENSAL ou SEMESTRAL; formaPagamento = CARTAO, PIX, DEBITO ou BOLETO (o teste de 14 dias só vale com CARTAO). O front não manda valor: o Core lê a tabela de preços. A cidade e a UF vêm do CEP.

Cabeçalho Idempotency-Key: o front manda o mesmo valor se repetir a chamada, e o Core devolve a mesma contratação em vez de criar outra.

Resposta 201 (cartão):

{

"contratacaoId": "c_01H...",

"status": "AGUARDANDO_PAGAMENTO",

"valorCentavos": 41181,

"expiraEm": "2026-10-29T20:00:00-03:00",

"pagamento": { "tipo": "CHECKOUT", "url": "https://..." }

}

Resposta 201 (débito e boleto): pagamento traz tipo: "FATURA" (débito) ou tipo: "BOLETO", a url da fatura ou do boleto e o vencimento.

Resposta 201 (Pix): pagamento traz tipo: "PIX", o qrCodePix (imagem), o codigoCopiaECola e o vencimento.

**GET /api/v1/contratacoes/{id}** (exige login, só do dono da contratação): devolve o status (AGUARDANDO_PAGAMENTO, CONCLUIDO, EXPIRADO, FALHA_ATIVACAO) para o front consultar. O resultado também chega pelo WebSocket.

Erros:

| **Código** | **Quando**                                                                                                                                     |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------|
| 400        | Dados inválidos (documento, e-mail, telefone, endereço, plano, combinação que não existe, como teste fora de Starter ou Pro mensal com cartão) |
| 401        | Sem login                                                                                                                                      |
| 409        | JA_TEM_PLANO_PAGO ou TESTE_JA_USADO                                                                                                            |
| 503        | Asaas fora do ar ao iniciar                                                                                                                    |

## 5. Dados

**pre_cadastro**

| **Campo**                                            | **Observação**                                                                                                                   |
|------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------|
| id                                                   | identificador da contratação (é a referência enviada ao Asaas)                                                                   |
| clerkUserId                                          | quem está contratando                                                                                                            |
| tenantId                                             | vazio para comprador novo; preenchido na conta Free                                                                              |
| cliente                                              | documento, nome, e-mail de cobrança, telefone e endereço                                                                         |
| codigoPlano, periodicidade, formaPagamento, comTeste | o que foi escolhido                                                                                                              |
| valorCentavos                                        | valor lido da tabela de preços na hora da contratação                                                                            |
| status                                               | AGUARDANDO_PAGAMENTO, CONCLUIDO, EXPIRADO, FALHA_ATIVACAO                                                                        |
| expiraEm                                             | criação + 3 dias (Pix, débito e boleto); no cartão, o prazo da página de pagamento                                               |
| idClienteAsaas, idCheckoutAsaas, idAssinaturaAsaas   | ligação com o Asaas; no cartão, o idCheckoutAsaas é a chave para achar o pré-cadastro (a página do Asaas não grava a referência) |
| chaveIdempotencia                                    | evita duas contratações iguais                                                                                                   |

**aceite_legal**: usuário, pré-cadastro, versão dos Termos, versão da Política, data e hora.

**uso_teste**: documento (CPF/CNPJ), data de início. Chave única no documento.

**assinatura** (já existe): ganha periodicidade, formaPagamento e testeAte (vazio fora do teste). O status continua sendo os já existentes; o teste é identificado por testeAte.

## 6. Organização do código (arquitetura hexagonal leve)

- **Entrada:** ContratacaoController (cria e consulta) e a rota do webhook, que é da LLT-235.

- **Regra de negócio:** GerenciadorAssinatura.contratarPlano faz as conferências, lê o valor na tabela_precificacao, grava o pré-cadastro e chama o gateway. ProcessamentoPagamento ativa a conta quando o pagamento é confirmado.

- **Porta do gateway:** GatewayPagamento (criada na LLT-235) com enviarCobranca, consultarStatus e configurarNotaFiscal. A 231 usa essas operações. O adaptador escolhe sozinho entre checkout (cartão) e assinatura direta (Pix, débito e boleto).

- **Adaptador do Asaas:** ApiPagamento (gatewayAtivo = ASAAS).

- **Agendador:** um job do Core (@Scheduled com ShedLock) marca como EXPIRADO os pré-cadastros vencidos e, no Pix, no débito e no boleto, apaga a assinatura no Asaas.

- **Portas de dados:** repositórios de pré-cadastro, aceite, uso do teste, assinatura e pagamento, com adaptadores MongoDB.

## 7. Segurança e idempotência

- Chaves e tokens do Asaas ficam só em variáveis de ambiente (.env), nunca no Git.

- Webhook: confere o token (asaas-access-token), o IP de origem e a consulta à API; o aviso repetido é descartado pelo id do evento (EventoGateway). O Asaas entrega "pelo menos uma vez", então repetição é esperada.

- Toda criação no Asaas leva o id do pré-cadastro como externalReference (o Asaas não tem Idempotency-Key). Antes de repetir uma chamada que deu tempo esgotado, o Core pergunta se o recurso já existe.

- O front nunca decide valor nem plano: o Core lê os dados de planos e os preços.

- A criação de contratação tem limite de tentativas por usuário.

- Dados de cartão não existem no LhamaLog: a página de pagamento é do Asaas.

- Telefone e endereço são dados pessoais: ficam só no pré-cadastro e no cliente do Asaas, e seguem a Política de Privacidade.

## 8. Estados do pré-cadastro

AGUARDANDO_PAGAMENTO → CONCLUIDO (pagamento confirmado e conta ativada) AGUARDANDO_PAGAMENTO → EXPIRADO (3 dias sem pagamento) AGUARDANDO_PAGAMENTO → FALHA_ATIVACAO (pagamento confirmado, mas a criação da conta falhou; a equipe reprocessa)

## 9. Verificações no sandbox

Confirmadas em 24, 25, 26 e 27/10/2026, com os preços do Planos Ajustado (viraram regra):

| **Verificação**                                                                 | **Resultado**                                                                                                                                                                                                                                                    |
|---------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| A página recorrente aceita Pix junto com cartão?                                | **Não.** Só CREDIT_CARD. O Pix recorrente exige assinatura criada direto (e uma chave Pix cadastrada na conta).                                                                                                                                                  |
| A página com cliente já cadastrado funciona sem telefone e endereço?            | **Não.** Exige telefone, endereço, número, CEP, bairro e cidade (R3).                                                                                                                                                                                            |
| O que a página devolve?                                                         | O link pronto para o comprador.                                                                                                                                                                                                                                  |
| A criação da assinatura gera a primeira cobrança?                               | **Sim**, na hora.                                                                                                                                                                                                                                                |
| O cartão só é cobrado no primeiro vencimento (14 dias à frente)?                | **Sim.** O cartão fica guardado e a cobrança fica PENDING até 09/11 (teste de 14 dias confirmado; R17 não precisa de plano B).                                                                                                                                   |
| PUT /v3/subscriptions com nextDueDate move o vencimento depois do primeiro Pix? | **Sim** (29/11 virou 26/11). O ciclo conta do dia do pagamento (R11).                                                                                                                                                                                            |
| Os ciclos WEEKLY e SEMIANNUALLY são aceitos?                                    | **Sim**, na assinatura direta (Pix), com os valores 20,23 e 475,99. O semanal gera 4 cobranças de uma vez.                                                                                                                                                       |
| O débito funciona na assinatura?                                                | **Só pela fatura.** DEBIT_CARD na assinatura dá erro 400; com UNDEFINED a fatura oferece boleto, Pix, crédito e débito, e o pagamento no débito (R\$ 80,88) foi confirmado com netValue 79,01. A API também recusa trocar a cobrança para débito.                |
| O boleto funciona na assinatura?                                                | **Sim**, criado direto com BOLETO (teste de 24/10), pago pelo QR Code ou pelo código de barras.                                                                                                                                                                  |
| A página do cartão grava descrição e referência na assinatura?                  | **Não.** O PUT depois da confirmação grava (R23).                                                                                                                                                                                                                |
| O nome do item da página aceita texto longo?                                    | **Não.** No máximo 30 caracteres (R24).                                                                                                                                                                                                                          |
| Cartão recusado cria cobrança?                                                  | **Não.** Mensagem "Pagamento não autorizado" e nada é criado (R21).                                                                                                                                                                                              |
| O valor cobrado bate com o líquido da planilha?                                 | Pix: netValue = valor − taxa do Pix (no sandbox a taxa é R\$ 0,99, promocional; a planilha usa R\$ 1,99). Cartão: netValue 79,83 sobre 81,95 (taxa promocional de 1,99% + R\$ 0,49; a planilha usa 2,99%). Débito: netValue 79,01 sobre 80,88, igual à planilha. |

Ainda a conferir durante a implementação (cada uma já tem plano B):

| **Verificação**                                                                                | **Se der certo**         | **Se não der**                                                                 |
|------------------------------------------------------------------------------------------------|--------------------------|--------------------------------------------------------------------------------|
| Qual aviso chega quando a assinatura com teste é criada (túnel de aviso necessário)            | Esse aviso ativa a conta | A ativação passa a consultar a assinatura na API logo após o retorno da página |
| O aviso do Asaas repetido (mesmo id) é descartado pelo EventoGateway                           | Regra R7 como descrita   | Ajustar a deduplicação                                                         |
| Se o Asaas permite restringir as formas de pagamento da fatura do débito (pergunta ao suporte) | O débito fica travado    | O risco de pagamento em outra forma fica registrado e acompanhado              |

## 10. Testes (make test)

| **Teste**                                                                                                                  | **O que garante** |
|----------------------------------------------------------------------------------------------------------------------------|-------------------|
| Contratação válida grava pré-cadastro e aceite e devolve o link (cartão), o QR Code (Pix) ou o link da fatura ou do boleto | Regras R3, R4     |
| O valor gravado e enviado ao Asaas é o da tabela_precificacao para plano, periodicidade e forma                            | Critério 8        |
| Cliente sem telefone ou sem endereço completo recebe 400                                                                   | Regra R3          |
| Nenhum campo de cartão é recebido nem gravado                                                                              | Regra R5          |
| Voltar da página sem aviso do Asaas não cria conta                                                                         | Regra R6          |
| Aviso confirmado cria Organization, Tenant, Assinatura e Dono                                                              | Regra R6          |
| Aviso repetido não cria nada em dobro                                                                                      | Regra R7          |
| Aviso com token ou IP inválido é recusado e não grava                                                                      | Regra R7          |
| Estado vem da API do Asaas, não do corpo do aviso                                                                          | Regra R7          |
| Pix, débito ou boleto não pago em 3 dias vira EXPIRADO e não cria conta                                                    | Regra R8          |
| Débito cria assinatura UNDEFINED com o preço de débito e devolve o link da fatura                                          | Regra R25         |
| Boleto cria assinatura BOLETO com o preço do Pix e devolve o link do boleto                                                | Regra R26         |
| Teste de 14 dias recusado para Pix, débito e boleto                                                                        | Regra R13         |
| Cobrança de débito paga em outra forma é registrada com a forma real                                                       | Regra R25         |
| Conta Free que paga troca o plano e não cria conta nova                                                                    | Regra R9          |
| Conta com plano pago ativo recebe 409 JA_TEM_PLANO_PAGO                                                                    | Regra R10         |
| O ciclo conta a partir do primeiro pagamento (Pix acerta o vencimento)                                                     | Regra R11         |
| Semestral cria uma cobrança de 6 meses; semanal e mensal criam o ciclo certo                                               | Regras R11, R12   |
| Teste aceito só em Starter e Pro, mensal, cartão de crédito                                                                | Regra R13         |
| Segundo teste com o mesmo CPF/CNPJ recebe 409 TESTE_JA_USADO                                                               | Regra R14         |
| Cancelar no teste volta ao Free e apaga a assinatura no Asaas                                                              | Regra R16         |
| Cartão recusado não cria conta e permite nova tentativa; nenhum pré-cadastro é concluído                                   | Regra R21         |
| No cartão, o aviso do Asaas é ligado ao pré-cadastro pelo checkoutSession                                                  | Regra R23         |
| Depois da confirmação no cartão, o Core grava descrição e referência na assinatura                                         | Regra R23         |
| Nome do item do checkout com mais de 30 caracteres nunca é enviado                                                         | Regra R24         |
| No Pix semanal, só a cobrança já vencida gera atraso (as futuras pendentes não)                                            | Regra R22         |
| Falha ao criar conta depois do pagamento vira FALHA_ATIVACAO e pode ser reprocessada                                       | Regra R19         |
| Asaas fora do ar ao iniciar devolve 503 e não grava cobrança                                                               | Regra R19         |
| Mesma Idempotency-Key devolve a mesma contratação                                                                          | Seção 7           |
| Dados (aceite, uso do teste) ficam com data, hora e versão                                                                 | Regras R4, R14    |

## 11. Git

- Branch pelo card do Jira no lhamalog-core, com a chave LLT-231.

- Commits começam com LLT-231.

- PR com a chave no título, template preenchido e pelo menos um revisor.

## 12. Pendências

Nenhuma.

## 13. Ações decorrentes

- Felipe: ajustar os Termos de Uso (profissional autônomo e teste de 14 dias).

- Design: ajustar o protótipo da tela de pagamento.

- André: perguntar ao suporte do Asaas se dá para restringir as formas de pagamento da fatura de uma assinatura.

- Michel e Pedro: registrar no diagrama de classes pre_cadastro, aceite_legal, uso_teste e os campos novos da assinatura.

- O código começa quando o repositório lhamalog-core receber o template do Michel (LLT-80).
