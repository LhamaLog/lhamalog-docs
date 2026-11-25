# Renovação, atraso e recusa (diagrama 6) — Assinatura e Pagamento com o Asaas (LhamaLog)

**LLT-90.** Caso de uso: SSID_016 + SSID_018. Gateway: Asaas (ADR_163). Imagem: `evento_gateway_externo.png` (nesta pasta).
Arquivo completo com os 7 diagramas: `LLT-90 - sequencia-assinatura-pagamento-asaas.md` (pasta v3).

15 dias de carência (Assinatura.diasCarencia) com acesso mantido; depois 30 dias SUSPENSA e então CANCELADA (regra da
ADR_163, mantida em 21/10/2026). Revisão de 21/10: ciclo mensal ou anual; recusa de cartão vira RECUSA (não ATRASO);
no cartão o Asaas faz 5 tentativas antes de marcar a cobrança como vencida; 30 dias para exportar (Termos de Uso).

```mermaid
sequenceDiagram
  participant Asaas
  participant Proc as ProcessamentoPagamento (Core)
  participant Ger as GerenciadorAssinatura
  participant Mongo as MongoDB
  participant Agenda as Agendamento do Core [PROPOSTO]
  actor Dono

  Note over Asaas,Proc: cobranca do ciclo (mes ou ano) gerada 40 dias antes do vencimento
  alt renovacao paga
    Asaas->>Proc: webhook PAYMENT_CONFIRMED (cartao) ou PAYMENT_RECEIVED (Pix e boleto) -- diagrama 0
    Proc->>Ger: aplicarEventoDeAssinatura(RENOVACAO)
    Ger->>Mongo: vigenciaAte avanca um ciclo (mes ou ano) -- ATIVA
    Note over Asaas,Proc: NFS-e emitida pelo Asaas -- evento NOTA_FISCAL
  else pagamento recusado ou em atraso
    alt cartao recusado (depois das 5 tentativas do Asaas)
      Asaas->>Proc: webhook PAYMENT_CREDIT_CARD_CAPTURE_REFUSED
      Proc->>Ger: aplicarEventoDeAssinatura(RECUSA)
    else Pix ou boleto nao pago no vencimento
      Asaas->>Proc: webhook PAYMENT_OVERDUE
      Proc->>Ger: aplicarEventoDeAssinatura(ATRASO)
    end
    Ger->>Mongo: Assinatura INADIMPLENTE -- acesso mantido (fecha ASS-05)
    Ger->>Dono: aviso por e-mail e na plataforma com o link de pagamento
    Ger->>Agenda: verificar em Assinatura.diasCarencia (15 dias)
    alt paga dentro dos 15 dias
      Asaas->>Proc: webhook PAYMENT_RECEIVED ou PAYMENT_CONFIRMED
      Ger->>Mongo: Assinatura ATIVA
    else 15 dias sem pagamento
      Agenda->>Ger: prazo vencido
      Ger->>Mongo: Assinatura SUSPENSA -- Coletor recusa ingestao e Sugestao por IA bloqueada
      Ger->>Dono: aviso de suspensao (avisos de cobranca continuam)
      Ger->>Agenda: verificar em 30 dias
      alt paga durante a suspensao
        Asaas->>Proc: webhook PAYMENT_RECEIVED ou PAYMENT_CONFIRMED
        Ger->>Mongo: Assinatura ATIVA -- ingestao e IA liberadas
      else 30 dias suspensa sem pagamento
        Agenda->>Ger: prazo vencido
        Ger->>Mongo: Assinatura CANCELADA -- Produtos desativados e TokenApi revogados
        Ger->>Dono: aviso de cancelamento -- 30 dias para exportar os relatorios (Termos de Uso)
      end
    end
  end

  alt FA-07: evento sem assinatura identificada
    Proc->>Proc: EventoGateway FALHA -- estado mantido
  else FA-05/FA-08: Asaas indisponivel na reconsulta
    Proc->>Proc: EventoGateway FALHA -- ultimo estado valido mantido, reprocessa depois
  end
```

Tentativas no cartão (Blog Asaas, atualizado em 04/05/2026): 3 no dia do vencimento (8h, 14h e 20h) e mais 2 a cada
24h; a carência de 15 dias começa depois disso.
