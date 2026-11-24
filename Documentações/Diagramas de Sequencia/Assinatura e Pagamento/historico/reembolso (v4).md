# Reembolso (diagrama 5) — Assinatura e Pagamento com o Asaas (LhamaLog)

**LLT-90 (v4, 26/10/2026).** Caso de uso: USID_043. Gateway: Asaas (ADR_163). Imagem: `reembolso.png` (nesta pasta).
Arquivo completo com os 7 diagramas: `LLT-90 - sequencia-assinatura-pagamento-asaas.md` (pasta v4).
## 5. Reembolso (USID_043)

Regras dos Termos de Uso (alinhadas em 21/10/2026): integral em até 7 dias da primeira contratação; a diferença
em até 7 dias de um upgrade; cobrança duplicada ou indevida a qualquer tempo. A equipe LhamaLog aprova.
**Reembolso de Pix (sandbox, 25/10/2026):** o Asaas só estorna se a conta tiver saldo e pede uma segunda aprovação
(evento crítico), que a equipe confirma no painel do Asaas (no sandbox, com o código `000000`). Reembolso no cartão
não passa por essa etapa.

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
  alt pagamento no cartao
    Asaas->>Ger: webhook PAYMENT_REFUND_IN_PROGRESS e depois PAYMENT_REFUNDED<br/>ou PAYMENT_PARTIALLY_REFUNDED (diagrama 0)
  else pagamento por Pix
    alt conta do Asaas sem saldo
      Asaas-->>ApiAsaas: 400 "Saldo insuficiente"
      Ger->>Mongo: Reembolso continua APROVADO -- aguardando saldo
      Ger->>Equipe: aviso: faltou saldo no Asaas para estornar o Pix
      Note over Equipe,Asaas: a equipe deposita saldo na conta do Asaas e a chamada e repetida
    else com saldo
      Asaas-->>ApiAsaas: estorno pendente de aprovacao (evento critico)
      Equipe->>Asaas: aprova o estorno no painel do Asaas (codigo de confirmacao)
      Asaas->>Ger: webhook PAYMENT_REFUND_IN_PROGRESS e depois PAYMENT_REFUNDED (diagrama 0)
    end
  end
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
