# Contratação e criação do tenant (diagrama 2) — Assinatura e Pagamento com o Asaas (LhamaLog)

**LLT-90 (v4, 26/10/2026).** Caso de uso: USID_040. Gateway: Asaas (ADR_163). Imagem: `contratacao.png` (nesta pasta).
Arquivo completo com os 7 diagramas: `LLT-90 - sequencia-assinatura-pagamento-asaas.md` (pasta v4).
## 2. Contratação e criação do tenant (USID_040 + tenant_criacao_assinatura)

O Tenant só nasce no webhook de pagamento aprovado (ADR_121, decisão de 17/10). **Cartão:** página de pagamento
hospedada pelo Asaas (checkout recorrente, que só aceita cartão de crédito). **Pix:** assinatura criada direto
(`POST /v3/subscriptions`), porque o Pix recorrente não passa pelo checkout (confirmado no sandbox em 24/10/2026).

```mermaid
sequenceDiagram
  actor Comprador
  participant Front
  participant Clerk
  participant Ger as GerenciadorAssinatura (Core)
  participant ApiAsaas
  participant Asaas
  participant Evt as EventoGateway
  participant Mongo as MongoDB

  Front->>Ger: POST /api/v1/contratacoes (plano, periodicidade, forma de pagamento,<br/>dados do comprador, aceite, session token)
  Ger->>Clerk: valida o session token -- clerkUserId
  Ger->>Ger: confere regras (plano pago, sem plano pago ativo, teste so se permitido)<br/>e calcula o valor (CalculadoraPreco)
  Ger->>Mongo: cria PreCadastro e AceiteLegal (AGUARDANDO_PAGAMENTO, expira em 3 dias) [PROPOSTO]
  Ger->>ApiAsaas: enviarCobranca(preCadastroId)
  ApiAsaas->>Asaas: POST /v3/customers (nome, CPF/CNPJ, e-mail, telefone, endereco,<br/>externalReference = preCadastroId)
  alt cartao de credito (pagina hospedada)
    ApiAsaas->>Asaas: POST /v3/checkouts (RECURRENT, CREDIT_CARD,<br/>cycle WEEKLY, MONTHLY ou SEMIANNUALLY, valor, successUrl, cancelUrl, externalReference)
    Asaas-->>ApiAsaas: link da pagina de pagamento
    Ger-->>Front: devolve o link -- front redireciona ao Asaas
    Comprador->>Asaas: paga com o cartao (o LhamaLog nao ve o cartao)
    Asaas-->>Front: redireciona ao successUrl -- o callback NAO confirma o pagamento
    Front-->>Comprador: "pagamento em processamento"
  else Pix (assinatura direta)
    ApiAsaas->>Asaas: POST /v3/subscriptions (billingType PIX, cycle, valor,<br/>nextDueDate = hoje + 3 dias, externalReference = preCadastroId)
    Asaas-->>ApiAsaas: assinatura e 1a cobranca (gerada na hora)
    ApiAsaas->>Asaas: GET /v3/payments/{id}/pixQrCode
    Asaas-->>ApiAsaas: QR Code e codigo copia e cola
    Ger-->>Front: mostra o QR Code Pix e o vencimento (3 dias)
    Comprador->>Asaas: paga o Pix pelo app do banco
  end
  Asaas->>Ger: webhook PAYMENT_CONFIRMED (cartao) ou PAYMENT_RECEIVED (Pix) -- diagrama 0
  Ger->>ApiAsaas: consultarStatus(pagamento) -- confirmado pela API
  Ger->>Evt: evento PRIMEIRA_COMPRA EXECUTADO (ADR_125)
  Ger->>Clerk: cria a Organization com o comprador como org:admin
  Clerk-->>Ger: clerkOrgId
  Ger->>Mongo: cria Tenant, Assinatura (ATIVA, periodicidade, limites do plano),<br/>Membro DONO e PapelNotificacao padrao (ADR_121/136/137)
  Ger->>Mongo: Pagamento (chaveIdempotencia = externalReference, id do Asaas)
  opt Pix: ciclo comeca no dia do pagamento (decisao de 22/10)
    Ger->>ApiAsaas: alterarAssinatura(nextDueDate = pagamento + 1 ciclo) [A VALIDAR]
    ApiAsaas->>Asaas: PUT /v3/subscriptions/{id}
  end
  Ger->>ApiAsaas: configurarNotaFiscal(assinatura) [PROPOSTO]
  ApiAsaas->>Asaas: POST /v3/subscriptions/{id}/invoiceSettings (ON_PAYMENT_CONFIRMATION)
  Ger-->>Front: assinatura ativa (WebSocket) -- usuario entra na Organization

  opt conta Free que contrata
    Note over Ger,Mongo: nao cria Tenant: troca o plano da Assinatura Free ao confirmar o pagamento
  end

  opt teste de 14 dias (Starter ou Pro, mensal, cartao, 1 vez por CPF/CNPJ)
    Note over ApiAsaas,Asaas: o checkout recebe o 1o vencimento em hoje + 14 dias [A VALIDAR]<br/>a conta ativa com a criacao da assinatura (testeAte = hoje + 14 dias), e<br/>o cartao so e cobrado no 15o dia
  end

  opt plano FREE (sem gateway)
    Ger->>Clerk: cria a Organization
    Ger->>Mongo: cria Tenant, Assinatura FREE, Membro DONO e papeis padrao
  end

  alt FA-01: cartao recusado na pagina do Asaas
    Asaas-->>Comprador: pagamento nao aprovado -- tenta outro cartao, nada e criado
  else FA-02: Pix nao pago em 3 dias
    Ger->>Mongo: PreCadastro EXPIRADO (agendador do Core) -- nenhum tenant criado
    Ger->>ApiAsaas: DELETE /v3/subscriptions/{id} -- para de gerar cobrancas
  else FA-03: comprador fecha a pagina de pagamento
    Asaas-->>Front: redireciona ao cancelUrl -- PreCadastro continua AGUARDANDO_PAGAMENTO
  else FA-04: Asaas indisponivel ao iniciar
    Ger-->>Front: "nao foi possivel iniciar a contratacao, tente depois"
  else FA-05: pagamento aprovado mas falha na Clerk ou no banco
    Ger->>Evt: evento FALHA com o erro (ADR_125)
    Ger-->>Front: "pagamento recebido -- ativacao em processamento"
    Note over Ger,Evt: equipe reprocessa por POST /internal/eventos-gateway/{eventoId}/reprocessar (ADR_133)
  else FA-06: conta ja tem plano pago ativo
    Ger-->>Front: 409 JA_TEM_PLANO_PAGO -- leva a pessoa para alterar o plano (diagrama 3)
  end
```

Achados do sandbox (24 e 25/10/2026): o checkout recorrente aceita só `CREDIT_CARD`; com cliente já cadastrado ele
exige telefone, endereço, número, CEP, bairro e cidade; a resposta já traz o `link`; a criação da assinatura gera a
primeira cobrança na hora. `[A VALIDAR]` na implementação: adiar a primeira cobrança do cartão em 14 dias;
`PUT /v3/subscriptions` com `nextDueDate`; ciclos `WEEKLY` e `SEMIANNUALLY` na página e na assinatura direta.
Pix Automático fica para depois (exige CNPJ ativo há 6 meses, ADR_163).
