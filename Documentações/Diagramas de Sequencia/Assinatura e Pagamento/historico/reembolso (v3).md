# Reembolso (diagrama 5) — Assinatura e Pagamento com o Asaas (LhamaLog)

**LLT-90.** Caso de uso: USID_043. Gateway: Asaas (ADR_163). Imagem: `reembolso.png` (nesta pasta).
Arquivo completo com os 7 diagramas: `LLT-90 - sequencia-assinatura-pagamento-asaas.md` (pasta v3).

Regras alinhadas com os Termos de Uso em 21/10/2026 (ADR_163): (a) integral em até 7 dias da primeira contratação;
(b) em até 7 dias de um upgrade, devolve a diferença; (c) cobrança duplicada ou indevida, a qualquer tempo.
Fora disso, não há reembolso de período já iniciado, inclusive no plano anual. A equipe LhamaLog aprova.

```mermaid
sequenceDiagram
  actor Dono
  participant Front
  participant Ger as GerenciadorAssinatura (Core)
  actor Equipe as Equipe LhamaLog
  participant ApiAsaas
  participant Asaas
  participant Mongo as MongoDB

  Dono->>Front: area da assinatura -- solicitar reembolso (pagamento, motivo)
  Front->>Ger: POST reembolso
  Ger->>Ger: elegivel? (a) 1a contratacao ha no maximo 7 dias -- integral<br/>(b) upgrade ha no maximo 7 dias -- so a diferenca<br/>(c) cobranca duplicada ou indevida -- a qualquer tempo
  Ger->>Mongo: Reembolso SOLICITADO (motivo, hipotese, valor)
  Ger-->>Front: "solicitacao em analise"
  Equipe->>Ger: aprova o reembolso [PENDENTE - rota interna]
  Ger->>ApiAsaas: solicitarReembolsoExterno(pagamento, valor)
  ApiAsaas->>Asaas: POST /v3/payments/{id}/refund (sem value = integral, com value = parcial)
  Asaas->>Ger: webhook PAYMENT_REFUND_IN_PROGRESS e depois<br/>PAYMENT_REFUNDED ou PAYMENT_PARTIALLY_REFUNDED (diagrama 0)
  Ger->>Mongo: Reembolso CONCLUIDO
  alt (a) primeira contratacao
    Ger->>Ger: encerra a assinatura como no diagrama 4, sem esperar vigenciaAte [INFERIDO]
  else (b) upgrade
    Ger->>ApiAsaas: alterarAssinatura(valor do plano anterior)
    Ger->>Mongo: Assinatura volta ao plano anterior [INFERIDO]
  else (c) cobranca duplicada ou indevida
    Note over Ger,Mongo: assinatura sem alteracao
  end
  Ger-->>Front: status do reembolso (WebSocket)

  alt FA-01: desistencia antes de confirmar
    Ger-->>Front: assinatura sem alteracoes
  else FA-02: fora das hipoteses (a), (b) e (c)
    Ger-->>Front: "nao elegivel" + motivo
  else FA-03: equipe nega
    Ger->>Mongo: Reembolso NEGADO (motivo)
    Ger-->>Front: status recusado + motivo
  else FA-04: Asaas indisponivel
    Ger-->>Front: "nao foi possivel encaminhar agora" -- reembolso continua aprovado para nova tentativa
  else FA-05: consulta antes de concluir
    Ger-->>Front: status SOLICITADO ou APROVADO (em analise)
  end
```

[A VALIDAR] no sandbox: como o Asaas devolve um pagamento feito por boleto (se pede dados bancários do Dono).
