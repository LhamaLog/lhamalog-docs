# Recebimento de webhook do Asaas (diagrama 0, novo) — Assinatura e Pagamento com o Asaas (LhamaLog)

**LLT-90.** Caso de uso: SSID_016, SSID_018. Gateway: Asaas (ADR_163). Imagem: `webhook_asaas.png` (nesta pasta).
Arquivo completo com os 7 diagramas: `LLT-90 - sequencia-assinatura-pagamento-asaas.md` (pasta v3).

Base de todos os fluxos: valida o token e o IP, deduplica pelo id do evento e aplica o estado consultado na API do Asaas (resolve o ASS-07).

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

A rota POST /webhooks/asaas e [PROPOSTO]. Mapeamento completo de eventos na ADR_163.
