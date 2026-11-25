# Renovação, atraso e recusa (diagrama 6) — Assinatura e Pagamento com o Asaas (LhamaLog)

**LLT-90 (v4, 26/10/2026).** Caso de uso: SSID_016, SSID_018. Gateway: Asaas (ADR_163). Imagem: `evento_gateway_externo.png` (nesta pasta).
Arquivo completo com os 7 diagramas: `LLT-90 - sequencia-assinatura-pagamento-asaas.md` (pasta v4).
## 6. Renovação, atraso e recusa (SSID_016 + SSID_018)

15 dias de carência com acesso mantido; depois 30 dias de suspensão e então cancelamento (decisões de 17/10).
Vale para qualquer periodicidade. No cartão o Asaas cobra sozinho; no Pix o Dono recebe a cobrança de cada ciclo e paga.

```mermaid
sequenceDiagram
  participant Asaas
  participant Proc as ProcessamentoPagamento (Core)
  participant Ger as GerenciadorAssinatura
  participant Mongo as MongoDB
  participant Agenda as Agendamento do Core [PROPOSTO]
  actor Dono

  Note over Asaas,Proc: cobranca do ciclo (semana, mes ou semestre) gerada com antecedencia pelo Asaas
  alt renovacao paga
    Asaas->>Proc: webhook PAYMENT_CONFIRMED (cartao) ou PAYMENT_RECEIVED (Pix) -- diagrama 0
    Proc->>Ger: aplicarEventoDeAssinatura(RENOVACAO)
    Ger->>Mongo: vigenciaAte avanca um ciclo -- ATIVA
    Note over Asaas,Proc: NFS-e emitida pelo Asaas -- evento NOTA_FISCAL
  else pagamento recusado ou em atraso
    alt cartao recusado (depois das 5 tentativas do Asaas)
      Asaas->>Proc: webhook PAYMENT_CREDIT_CARD_CAPTURE_REFUSED
      Proc->>Ger: aplicarEventoDeAssinatura(RECUSA)
    else Pix nao pago no vencimento
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

Tentativas no cartão (Blog Asaas, atualizado em 04/05/2026): 3 no dia do vencimento (8h, 14h e 20h) e mais 2 a
cada 24h; a carência de 15 dias começa depois disso. O excedente de GB e o armazenamento extra são cobrados
numa cobrança avulsa mensal (LLT-234 e LLT-235); o atraso dela segue a mesma regra de carência e suspensão.
