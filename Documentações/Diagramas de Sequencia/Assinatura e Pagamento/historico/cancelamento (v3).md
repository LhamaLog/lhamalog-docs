# Cancelamento (diagrama 4) — Assinatura e Pagamento com o Asaas (LhamaLog)

**LLT-90.** Caso de uso: USID_042. Gateway: Asaas (ADR_163). Imagem: `cancelamento.png` (nesta pasta).
Arquivo completo com os 7 diagramas: `LLT-90 - sequencia-assinatura-pagamento-asaas.md` (pasta v3).

Fim da vigência controlado pelo Core. O Asaas gera cada cobrança 40 dias antes do vencimento e o DELETE da assinatura apaga as cobranças pendentes (ADR_163).

```mermaid
sequenceDiagram
  actor Dono
  participant Front
  participant Ger as GerenciadorAssinatura (Core)
  participant ApiAsaas
  participant Asaas
  participant Mongo as MongoDB
  participant Agenda as Agendamento do Core [PROPOSTO]

  Dono->>Front: area da assinatura -- cancelar
  Ger-->>Front: condicoes: acesso ate vigenciaAte, sem reembolso do periodo
  Dono->>Front: confirma
  Front->>Ger: POST cancelamento
  Ger->>ApiAsaas: cancelarAssinatura(fimDoPeriodo) [PROPOSTO]
  ApiAsaas->>Asaas: PUT /v3/subscriptions/{id} (endDate = vigenciaAte) -- nao gera novas cobrancas
  ApiAsaas->>Asaas: DELETE /v3/payments/{id} da proxima cobranca ja gerada [A VALIDAR]
  Ger->>Mongo: Assinatura CANCELAMENTO_AGENDADO (mantem vigenciaAte)
  Ger->>Agenda: agenda o encerramento em vigenciaAte
  Ger-->>Front: "assinatura valida ate o termino do periodo contratado"

  Agenda->>Ger: chegou vigenciaAte
  Ger->>ApiAsaas: DELETE /v3/subscriptions/{id}
  Asaas->>Ger: webhook SUBSCRIPTION_DELETED (diagrama 0) -- confirma
  Ger->>Mongo: Assinatura CANCELADA
  Ger->>Ger: desativa Produtos e revoga TokenApi do tenant [dependencia - modulo Produto]

  alt FA-01: desistencia antes de confirmar
    Ger-->>Front: assinatura mantida ativa
  else FA-02: falha ao cancelar no Asaas
    Ger-->>Front: "nao foi possivel concluir, assinatura mantida ativa"
  else FA-03: Asaas indisponivel
    Ger-->>Front: "solicitacao nao pode ser processada agora"
  else FA-04: ja existe cancelamento agendado
    Ger-->>Front: informa a data prevista de encerramento
  else FA-05: falha ao desativar Produtos no fim da vigencia
    Ger->>Mongo: registra a falha para reprocessar [PENDENTE - ASS-06]
  end
```

[A VALIDAR] exclusão da próxima cobrança e se o Asaas encerra a assinatura sozinho na endDate, o que dispensaria o DELETE.
