# LLT-235 — Criar a interface genérica do gateway de pagamento — Desenho

Versão: v1 Status: para aprovação Autor: André Felipe Data: 27/10/2026 Base: documento de Requisitos da LLT-235 (v1)

Este documento diz **como** a tarefa será construída. O **o quê** está no documento de Requisitos.

## 1. Partes envolvidas

| **Parte**            | **O que faz nesta tarefa**                                                                 |
|----------------------|--------------------------------------------------------------------------------------------|
| Core (lhamalog-core) | Tem a porta GatewayPagamento, o adaptador ApiPagamento, a rota de avisos e o processamento |
| Asaas                | Recebe as chamadas e envia os avisos                                                       |
| Notification         | Envia o e-mail para a equipe quando um aviso falha                                         |
| MongoDB              | Guarda o registro dos avisos (evento_gateway)                                              |
| Equipe LhamaLog      | Reprocessa avisos com falha por rota interna                                               |

## 2. A porta e o adaptador

GatewayPagamento é uma interface de domínio. ApiPagamento é o adaptador do Asaas (gatewayAtivo = ASAAS). Quem usa a porta não importa nada do Asaas.

| **Operação da porta**                  | **Chamada do Asaas (testada no sandbox)**                                                                    | **Usada por**  |
|----------------------------------------|--------------------------------------------------------------------------------------------------------------|----------------|
| enviarCobranca (assinatura com cartão) | POST /v3/customers + POST /v3/checkouts (RECURRENT, CREDIT_CARD)                                             | LLT-231        |
| enviarCobranca (assinatura com Pix)    | POST /v3/customers + POST /v3/subscriptions (PIX) + GET /v3/payments/{id}/pixQrCode                          | LLT-231        |
| enviarCobranca (diferença do upgrade)  | POST /v3/checkouts (DETACHED, CREDIT_CARD e PIX)                                                             | LLT-232        |
| consultarStatus                        | GET /v3/payments/{id} e GET /v3/subscriptions/{id}                                                           | todas          |
| alterarAssinatura                      | PUT /v3/subscriptions/{id} (valor, ciclo, nextDueDate, updatePendingPayments)                                | LLT-231, 232   |
| gravarDescricaoReferencia              | PUT /v3/subscriptions/{id} (description, externalReference)                                                  | LLT-231        |
| cancelarAssinatura                     | PUT /v3/subscriptions/{id} (endDate), DELETE /v3/payments/{id} (cada futura) e DELETE /v3/subscriptions/{id} | LLT-232, 233   |
| solicitarReembolsoExterno              | POST /v3/payments/{id}/refund                                                                                | LLT-233        |
| registrarExcedente                     | PUT /v3/payments/{id} (soma à cobrança pendente) ou POST /v3/payments (avulsa)                               | LLT-234        |
| configurarNotaFiscal                   | POST /v3/subscriptions/{id}/invoiceSettings                                                                  | LLT-231        |
| validarAutenticidade                   | token + IP + reconsulta (sem chamada própria)                                                                | rota de avisos |

A porta trabalha com tipos do domínio (CobrancaGateway, AssinaturaGateway, ResultadoReembolso...). O adaptador converte para o JSON do Asaas e de volta, e é o único lugar que conhece URLs, cabeçalhos (access_token, User-Agent) e nomes de campo do Asaas.

## 3. Recebimento dos avisos (webhook)

1.  O Asaas chama POST /webhooks/asaas (rota pública do Core) com o cabeçalho asaas-access-token.

2.  O Core valida: token igual ao segredo guardado (ApiPagamento.webhookSecret, entre 32 e 255 caracteres) e IP de origem na lista oficial do Asaas. Falhou: responde 401 e **não grava nada**.

3.  O Core procura o id do evento em evento_gateway. Se já existe, responde 200 e **não faz mais nada** (aviso repetido).

4.  Se é novo, grava o evento como RECEBIDO e responde **200 na hora**.

5.  Um processador assíncrono pega o evento, consulta o recurso na API (consultarStatus) e aplica o **estado da API** (não o do corpo do aviso), mapeando o evento para um dos 9 tipos de operação. Chama a regra da tarefa dona do assunto (contratação, alteração, cancelamento, reembolso, atraso...).

6.  Sucesso: o evento vira EXECUTADO. Evento sem tipo mapeado (por exemplo, "checkout visualizado") vira EXECUTADO sem efeito.

7.  Falha: o processador tenta de novo 3 vezes (1, 5 e 30 minutos). Se continuar, o evento vira FALHA, a equipe recebe e-mail pelo Notification e o evento aparece no painel interno.

8.  A ligação do aviso com a contratação ou alteração: no Pix, pela referência (externalReference); no cartão pela página de pagamento, pelo checkoutSession do pagamento.

## 4. Reprocessamento

- GET /internal/eventos-gateway?status=FALHA: lista.

- POST /internal/eventos-gateway/{id}/reprocessar: roda o processamento de novo. É seguro repetir: o resultado de cada tipo de operação é idempotente (por exemplo, "criar o Tenant" confere se o pré-cadastro já está concluído).

- Protegidas por credencial de serviço e IP interno.

## 5. Dados

**evento_gateway**

| **Campo**                                  | **Observação**                                |
|--------------------------------------------|-----------------------------------------------|
| id                                         | id do evento do Asaas (chave de deduplicação) |
| tipoEvento                                 | nome do Asaas (ex.: PAYMENT_CONFIRMED)        |
| tipoOperacao                               | um dos 9 valores, ou vazio                    |
| recursoId                                  | id do pagamento ou da assinatura no Asaas     |
| payload                                    | corpo recebido (sem dados sensíveis)          |
| estado                                     | RECEBIDO, EXECUTADO, FALHA                    |
| tentativas, proximaTentativaEm, ultimoErro | controle das 3 tentativas                     |
| recebidoEm, processadoEm                   | datas                                         |

**Configuração:** gateway ativo, URL base (sandbox ou produção), chave de API, segredo do aviso, lista de IPs: todos em variáveis de ambiente.

## 6. Tratamento de erros nas chamadas ao Asaas

- **4xx** (dado inválido, recurso inexistente): não repete; devolve erro de domínio com a mensagem traduzida (ex.: nome do item maior que 30 caracteres).

- **5xx ou tempo esgotado:** repete até 3 vezes com espera crescente (1, 2 e 4 segundos); depois responde "gateway indisponível" (503) ao chamador.

- **Tempo esgotado em criação:** antes de repetir, consulta pela referência se o recurso já foi criado (R12).

- O adaptador nunca devolve ao chamador uma exceção do cliente HTTP; só erros de domínio.

## 7. Organização do código (arquitetura hexagonal leve)

- **Porta:** GatewayPagamento (interface de domínio) e os tipos do domínio.

- **Adaptador:** ApiPagamento (Asaas), com um cliente REST próprio (o Asaas não tem SDK Java oficial) e o conversor de JSON.

- **Entrada:** WebhookAsaasController (POST /webhooks/asaas) e EventoGatewayInternoController (rotas internas).

- **Regra de negócio:** ProcessamentoPagamento (processa o evento e chama o gerenciador certo) e GerenciadorAssinatura.

- **Agendador** (@Scheduled com ShedLock): pega eventos com tentativa vencida e reprocessa.

- **Portas de dados e de mensagens:** repositório de evento_gateway (MongoDB) e publicador de pedido de e-mail para o Notification.

## 8. Segurança

- O segredo do aviso e a chave de API ficam só em variáveis de ambiente; o .env não vai para o Git.

- Aviso sem token válido ou de IP fora da lista é recusado antes de qualquer gravação.

- O corpo do aviso nunca decide estado: sempre a reconsulta.

- O log mascara CPF/CNPJ e nunca grava cartão nem chave.

- Rotas internas só com credencial de serviço.

## 9. Verificações no sandbox

Confirmadas em 24 a 27/10/2026 (viraram regra): criação de cliente, página de pagamento do cartão (recorrente e avulsa), assinatura direta no Pix com ciclos semanal, mensal e semestral, QR Code do Pix, alterar valor e ciclo, preencher descrição e referência, mover vencimento, apagar cobranças futuras, excedente por PUT e por cobrança avulsa, estorno no cartão e no Pix, cartão recusado e débito pela fatura.

Ainda a conferir durante a implementação (precisa de túnel público para receber os avisos):

| **Verificação**                                                                | **Se der certo**                 | **Se não der**                                                        |
|--------------------------------------------------------------------------------|----------------------------------|-----------------------------------------------------------------------|
| Qual aviso chega quando a assinatura com teste é criada                        | Esse aviso ativa a conta         | A ativação consulta a assinatura na API logo após o retorno da página |
| O mesmo aviso reenviado chega com o mesmo id                                   | A deduplicação por id funciona   | Deduplicar por recurso + tipo + data                                  |
| O aviso PAYMENT_REFUNDED chega no estorno de Pix depois da aprovação no painel | O pedido conclui pelo aviso      | A equipe confere no painel do Asaas e conclui por reprocessamento     |
| Configuração da NFS-e por assinatura no sandbox                                | A nota é configurada na ativação | Fica para a produção, depois da constituição da empresa               |

## 10. Testes (make test)

| **Teste**                                                                   | **O que garante** |
|-----------------------------------------------------------------------------|-------------------|
| Aviso com token errado recebe 401 e não grava                               | Regra R4          |
| Aviso de IP fora da lista recebe 401 e não grava                            | Regra R4          |
| Aviso novo grava RECEBIDO e responde 200 antes de processar                 | Regras R7, R8     |
| Aviso repetido (mesmo id) responde 200 e não reaplica                       | Regra R5          |
| Estado aplicado vem da consulta na API, não do corpo do aviso               | Regra R4          |
| Aviso atrasado (estado mais novo já aplicado) não desfaz nada               | Regra R6          |
| Evento sem tipo mapeado fica EXECUTADO sem efeito                           | Regra R11         |
| Falha ao processar tenta 3 vezes (1, 5 e 30 min) e depois vira FALHA        | Regra R9          |
| FALHA envia e-mail para a equipe e aparece na lista interna                 | Regra R9          |
| Reprocessar um FALHA conclui sem aplicar duas vezes                         | Regra R10         |
| Erro 4xx do Asaas não é repetido e vira erro de domínio                     | Regra R13         |
| Erro 5xx ou tempo esgotado repete 3 vezes e vira 503                        | Regra R13         |
| Tempo esgotado em criação consulta a referência antes de repetir            | Regra R12         |
| Cada operação da porta chama o endpoint certo do Asaas com os campos certos | Seção 2           |
| Nenhum teste nem log grava chave, cartão ou CPF/CNPJ completo               | Regras R14, R15   |
| Trocar o adaptador por um falso não muda nenhuma regra de negócio           | Regra R16         |

## 11. Git

- Branch pelo card do Jira no lhamalog-core, com a chave LLT-235.

- Commits começam com LLT-235.

- PR com a chave no título, template preenchido e pelo menos um revisor.

## 12. Pendências

Nenhuma.

## 13. Ações decorrentes

- Michel: endereço público do Core para os avisos, segredo no ambiente e lista de IPs do Asaas.

- Michel e Pedro: registrar no diagrama de classes as operações novas da porta e evento_gateway com os estados.

- O código começa quando o repositório lhamalog-core receber o template do Michel (LLT-80).
