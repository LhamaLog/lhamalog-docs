# Visualização dos planos (diagrama 1) — Assinatura e Pagamento com o Asaas (LhamaLog)

**LLT-90.** Caso de uso: USID_039. Gateway: Asaas (ADR_163). Imagem: `visualizacao.png` (nesta pasta).
Arquivo completo com os 7 diagramas: `LLT-90 - sequencia-assinatura-pagamento-asaas.md` (pasta v3).

Só mostra os planos e leva o usuário à contratação. Revisão de 21/10/2026 (ADR_163): cada plano pago tem preço mensal
e anual (anual com desconto, valor a definir com o PO), e o Dono escolhe a periodicidade e a forma de pagamento
(cartão, Pix ou boleto). Detalhe da tela e da API na LLT-230.

```mermaid
sequenceDiagram
  actor Usuario
  participant Front
  participant Ger as GerenciadorAssinatura (Core)
  participant Mongo as MongoDB (TabelaPrecificacao)
  participant ApiAsaas
  participant Asaas

  Usuario->>Front: acessa a pagina de planos
  Front->>Ger: GET /api/v1/planos (LLT-230)
  Ger->>Mongo: le a TabelaPrecificacao (ADR_131)
  Ger-->>Front: planos (preco mensal e anual em R$, franquia, limites, recursos)<br/>e o plano atual, se houver login
  Usuario->>Front: escolhe o plano e a periodicidade (mensal ou anual) e clica em assinar
  alt plano FREE (decisao de 17/10)
    Front->>Ger: POST assinatura FREE
    Ger-->>Front: segue para a criacao do tenant sem gateway (diagrama 2, opt FREE)
  else plano pago
    Front->>Front: pede os dados da empresa (razao social, CNPJ)<br/>e a forma de pagamento (cartao, Pix ou boleto)
    Front-->>Usuario: segue para a contratacao (diagrama 2)
  end

  alt FA-01: nenhum plano disponivel
    Ger-->>Front: "nao ha planos disponiveis no momento"
  else FA-02: falha ao carregar planos
    Ger-->>Front: "falha ao carregar, tente novamente"
  end
  Note over Ger,Asaas: Asaas indisponivel ao iniciar a contratacao: tratado no diagrama 2 (FA-04)
```

[PENDENTE] valor do desconto do plano anual (PO, Plano de Monetização); até lá, o preço anual vem vazio.
