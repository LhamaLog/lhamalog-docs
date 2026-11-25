# Contratação e criação do tenant (diagrama 2) — Assinatura e Pagamento com o Asaas (LhamaLog)

**LLT-90.** Caso de uso: USID_040 + tenant_criacao_assinatura. Gateway: Asaas (ADR_163). Imagem: `contratacao.png` (nesta pasta).
Arquivo completo com os 7 diagramas: `LLT-90 - sequencia-assinatura-pagamento-asaas.md` (pasta v3).

O Tenant só nasce no webhook de pagamento aprovado (ADR_121). Revisão de 21/10/2026 (ADR_163): mensal ou anual;
cartão e Pix pelo checkout hospedado; boleto fora do checkout (o checkout do Asaas só aceita cartão e Pix), criado
direto como assinatura. Pix Automático fica para depois (exige CNPJ ativo há 6 meses).

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

  Front->>Ger: POST contratacao (plano, periodicidade, forma de pagamento,<br/>dados da empresa, session token)
  Ger->>Clerk: valida o session token -- clerkUserId
  Ger->>Mongo: cria PreCadastro (clerkUserId, CNPJ, plano, periodicidade,<br/>forma de pagamento, AGUARDANDO_PAGAMENTO) [PROPOSTO]
  Ger->>ApiAsaas: enviarCobranca(preCadastroId)
  ApiAsaas->>Asaas: POST /v3/customers (nome, CNPJ, externalReference = preCadastroId)
  alt cartao ou Pix (checkout hospedado)
    ApiAsaas->>Asaas: POST /v3/checkouts (RECURRENT, CREDIT_CARD e PIX,<br/>cycle MONTHLY ou YEARLY, successUrl, cancelUrl, externalReference)
    Asaas-->>ApiAsaas: link do checkout
    Ger-->>Front: redireciona ao checkout hospedado
    Comprador->>Asaas: escolhe cartao ou Pix e paga (o LhamaLog nao ve o cartao)
    Asaas-->>Front: redireciona ao successUrl -- o callback NAO confirma o pagamento
  else boleto (fora do checkout)
    ApiAsaas->>Asaas: POST /v3/subscriptions (billingType BOLETO,<br/>cycle MONTHLY ou YEARLY, externalReference = preCadastroId)
    Asaas-->>ApiAsaas: assinatura e link do boleto com QR Code Pix
    Ger-->>Front: mostra o boleto -- "conta liberada apos a compensacao"
    Comprador->>Asaas: paga pelo QR Code (na hora) ou pelo codigo de barras (ate 3 dias uteis)
  end
  Front-->>Comprador: "pagamento em processamento"
  Asaas->>Ger: webhook PAYMENT_CONFIRMED (cartao) ou PAYMENT_RECEIVED (Pix e boleto) -- diagrama 0
  Ger->>ApiAsaas: consultarStatus(pagamento) -- confirmado pela API
  Ger->>Evt: evento PRIMEIRA_COMPRA EXECUTADO (ADR_125)
  Ger->>Clerk: cria a Organization com o comprador como org:admin
  Clerk-->>Ger: clerkOrgId
  Ger->>Mongo: cria Tenant, Assinatura (ATIVA, periodicidade, limites da TabelaPrecificacao),<br/>Membro DONO e PapelNotificacao padrao (ADR_121/136/137)
  Ger->>Mongo: Pagamento (chaveIdempotencia = externalReference, id do Asaas)
  Ger->>ApiAsaas: configurarNotaFiscal(assinatura) [PROPOSTO]
  ApiAsaas->>Asaas: POST /v3/subscriptions/{id}/invoiceSettings (ON_PAYMENT_CONFIRMATION)
  Ger-->>Front: assinatura ativa (WebSocket) -- usuario entra na Organization

  opt plano FREE (sem gateway)
    Ger->>Clerk: cria a Organization
    Ger->>Mongo: cria Tenant, Assinatura FREE, Membro DONO e papeis padrao
  end

  alt FA-01: cartao recusado no checkout
    Asaas-->>Comprador: pagamento nao aprovado -- tenta outro cartao ou Pix
  else FA-02: Pix ou boleto nao pago ate o vencimento
    Asaas->>Ger: webhook PAYMENT_OVERDUE [A VALIDAR - evento do Pix do checkout]
    Ger->>Mongo: PreCadastro EXPIRADO -- nenhum tenant criado
    Ger->>ApiAsaas: no boleto, DELETE /v3/subscriptions/{id} -- para de gerar cobrancas
  else FA-03: comprador fecha o checkout
    Asaas-->>Front: redireciona ao cancelUrl -- PreCadastro continua AGUARDANDO_PAGAMENTO
  else FA-04: Asaas indisponivel ao iniciar
    Ger-->>Front: "nao foi possivel iniciar a contratacao, tente depois"
  else FA-05: pagamento aprovado mas falha na Clerk ou no banco
    Ger->>Evt: evento FALHA com o erro (ADR_125)
    Ger-->>Front: "pagamento recebido -- ativacao em processamento"
    Note over Ger,Evt: equipe reprocessa por POST /internal/eventos-gateway/{eventoId}/reprocessar (ADR_133)
  end
```

[A VALIDAR] no sandbox: se o checkout `RECURRENT` aceita `PIX` junto com `CREDIT_CARD` (se não aceitar, o Pix segue o
mesmo caminho do boleto, com `billingType PIX`); e qual evento chega quando o Pix do checkout não é pago.
