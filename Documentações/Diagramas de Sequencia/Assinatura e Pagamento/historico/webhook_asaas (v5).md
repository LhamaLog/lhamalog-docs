# Recebimento de webhook do Asaas (diagrama 0) — Assinatura e Pagamento com o Asaas (LhamaLog)

**LLT-90 (v5, 26/10/2026).** Caso de uso: SSID_016, SSID_018. Gateway: Asaas (ADR_163). Imagem: `webhook_asaas.png` (nesta pasta).
Arquivo completo com os 7 diagramas: `LLT-90 - sequencia-assinatura-pagamento-asaas.md` (pasta v5).
## 0. Recebimento de webhook do Asaas (base de todos os fluxos)

Resolve ASS-07 (eventos repetidos ou fora de ordem) e a falta de HMAC no Asaas (LLT-89, seção 2, itens 7 a 9).

```mermaid
sequenceDiagram
  participant Asaas
  participant Core as Core (POST /webhooks/asaas) [PROPOSTO - rota]
  participant Evt as EventoGateway
  participant Proc as ProcessamentoPagamento
  participant ApiAsaas
  participant Ger as GerenciadorAssinatura

  Asaas->>Core: POST evento (id, event, payment ou subscription)<br/>header asaas-access-token
  Core->>Core: validarAutenticidade: token == ApiPagamento.webhookSecret<br/>e IP de origem na lista oficial do Asaas
  Core->>Evt: existe evento com este id? (deduplicacao)
  alt evento ja registrado
    Core-->>Asaas: 200 OK -- nada e refeito (entrega "pelo menos uma vez")
  else evento novo
    Core->>Evt: grava evento RECEBIDO (id, tipo, payload)
    Core-->>Asaas: 200 OK imediato -- processamento assincrono
    Proc->>ApiAsaas: consultarStatus(id do recurso)
    ApiAsaas->>Asaas: GET /v3/payments/{id} ou GET /v3/subscriptions/{id}
    Asaas-->>ApiAsaas: estado ATUAL do recurso
    Note over Evt,Ger: o estado aplicado vem da API, nao do corpo do webhook:<br/>prova de autenticidade e resolve evento fora de ordem
    Proc->>Ger: aplicarEventoDeAssinatura(tipoOperacao, estado atual)
    Ger-->>Proc: novo status registrado
    Proc->>Evt: evento EXECUTADO
  end

  alt FA-01: token invalido ou IP fora da lista
    Core-->>Asaas: 401 -- nada e gravado
  else FA-02: falha ao aplicar (Clerk, banco, Asaas indisponivel)
    Proc->>Evt: evento FALHA com o erro -- reprocessamento pela API interna (ADR_133)
  else FA-03: evento sem tipo mapeado (ex.: PAYMENT_CHECKOUT_VIEWED)
    Proc->>Evt: evento EXECUTADO sem efeito -- so registro
  end
```

**Mapeamento de eventos** (`TipoOperacaoGateway` com 9 valores, ADR_163): `PAYMENT_CONFIRMED`/`PAYMENT_RECEIVED` →
PRIMEIRA_COMPRA (1ª cobrança) ou RENOVACAO · `SUBSCRIPTION_UPDATED` → UPGRADE_DOWNGRADE ·
`SUBSCRIPTION_INACTIVATED`/`SUBSCRIPTION_DELETED` → CANCELAMENTO · `PAYMENT_OVERDUE` → ATRASO ·
`PAYMENT_CREDIT_CARD_CAPTURE_REFUSED`/`PAYMENT_REPROVED_BY_RISK_ANALYSIS` → RECUSA ·
`PAYMENT_REFUND_IN_PROGRESS`/`PAYMENT_REFUNDED`/`PAYMENT_PARTIALLY_REFUNDED` → REEMBOLSO ·
`PAYMENT_CHARGEBACK_REQUESTED`/`PAYMENT_CHARGEBACK_DISPUTE`/`PAYMENT_AWAITING_CHARGEBACK_REVERSAL` → CHARGEBACK ·
`INVOICE_AUTHORIZED`/`INVOICE_ERROR`/`INVOICE_CANCELED` → NOTA_FISCAL.

Observação (sandbox): a fila de avisos do Asaas pausa depois de 15 falhas seguidas; por isso o Core responde 200 na hora e processa depois.
