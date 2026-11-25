# Alteração de plano (diagrama 3) — Assinatura e Pagamento com o Asaas (LhamaLog)

**LLT-90.** Caso de uso: USID_041. Gateway: Asaas (ADR_163). Imagem: `alteracao_upgrade.png` (nesta pasta).
Arquivo completo com os 7 diagramas: `LLT-90 - sequencia-assinatura-pagamento-asaas.md` (pasta v3).

Proration calculada pelo Core. Upgrade vale quando a diferença é paga; downgrade vale no próximo ciclo, sem reembolso
(ADR_124). Revisão de 21/10/2026 (ADR_163): a diferença é cobrada por um checkout avulso (DETACHED), sem depender de
cartão salvo; no plano anual a proporção é sobre os dias que faltam no ano; a troca de mensal para anual (ou o
contrário) vale no ciclo seguinte [PROPOSTO].

```mermaid
sequenceDiagram
  actor Dono
  participant Front
  participant Ger as GerenciadorAssinatura (Core)
  participant ApiAsaas
  participant Asaas
  participant Mongo as MongoDB

  Dono->>Front: area da assinatura -- escolhe o novo plano ou a periodicidade
  Front->>Ger: POST alteracao (novo plano, periodicidade) -- so DONO [INFERIDO]
  alt upgrade (mensal ou anual)
    Ger->>Ger: calcularValorProporcional(planoAtual, planoNovo,<br/>dias restantes do ciclo -- mes ou ano)
    Ger->>ApiAsaas: enviarCobranca(diferenca, externalReference = alteracaoId)
    ApiAsaas->>Asaas: POST /v3/checkouts (DETACHED, CREDIT_CARD e PIX) -- cobranca avulsa da diferenca
    Ger-->>Front: redireciona ao checkout da diferenca
    Dono->>Asaas: paga a diferenca (cartao ou Pix, mesmo quem assina por boleto)
    Asaas->>Ger: webhook PAYMENT_CONFIRMED ou PAYMENT_RECEIVED da diferenca (diagrama 0)
    Ger->>ApiAsaas: alterarAssinatura(novo valor) [PROPOSTO]
    ApiAsaas->>Asaas: PUT /v3/subscriptions/{id} (value do novo plano, updatePendingPayments = true)
    Ger->>Mongo: Assinatura: plano e limites novos (ADR_124/131)
    Ger-->>Front: upgrade aplicado
  else downgrade ou troca de periodicidade
    Ger->>ApiAsaas: alterarAssinatura(novo valor e ciclo, a partir do proximo ciclo)
    ApiAsaas->>Asaas: PUT /v3/subscriptions/{id} (value e cycle novos, updatePendingPayments = true)
    Ger->>Mongo: Assinatura.planoAgendado = novo plano e periodicidade, vale em vigenciaAte [PROPOSTO]
    Ger-->>Front: "a mudanca vale a partir do proximo ciclo"
    Note over Ger,Mongo: na virada do ciclo: Assinatura muda de plano -- excedentes ficam ACESSO_PENDENTE (ADR_129)
  end

  alt FA-01: desistencia antes de confirmar
    Ger-->>Front: assinatura mantida, sem modificacoes
  else FA-02: diferenca recusada ou nao paga
    Asaas->>Ger: webhook PAYMENT_CREDIT_CARD_CAPTURE_REFUSED ou PAYMENT_OVERDUE
    Ger-->>Front: "nao foi possivel realizar o upgrade, assinatura mantida" -- nada a desfazer
  else FA-03: Asaas indisponivel
    Ger-->>Front: "alteracao nao pode ser realizada agora"
  end
```

`updatePendingPayments = true` aplica a mudança também à cobrança já gerada (o Asaas gera cada cobrança 40 dias antes
do vencimento). Alterar o valor de assinatura no cartão exige a tokenização habilitada na conta Asaas.
