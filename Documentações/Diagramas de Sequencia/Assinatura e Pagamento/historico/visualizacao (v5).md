# Visualização dos planos (diagrama 1) — Assinatura e Pagamento com o Asaas (LhamaLog)

**LLT-90 (v5, 26/10/2026).** Caso de uso: USID_039. Gateway: Asaas (ADR_163). Imagem: `visualizacao.png` (nesta pasta).
Arquivo completo com os 7 diagramas: `LLT-90 - sequencia-assinatura-pagamento-asaas.md` (pasta v5).
## 1. Visualização dos planos (USID_039)

Só mostra os planos e leva o usuário à contratação. Cada plano pago tem um preço para cada periodicidade
(semanal, mensal, semestral) e forma de pagamento (Pix, cartão de crédito), já com a taxa do Asaas (aba Planos Ajustado do Plano de
Monetização v4). Detalhe da tela e da API na LLT-230.

```mermaid
sequenceDiagram
  actor Usuario
  participant Front
  participant Ger as GerenciadorAssinatura (Core)
  participant Mongo as MongoDB (planos, tabela_precificacao)

  Usuario->>Front: acessa a pagina de planos
  Front->>Ger: GET /api/v1/planos (LLT-230)
  Ger->>Mongo: le os planos e os precos publicos (Planos Ajustado do v4) de cada periodicidade e forma de pagamento
  Ger-->>Front: planos (precos, franquia, excedente, limites, recursos)<br/>e o plano atual, se houver login
  Usuario->>Front: escolhe o plano, a periodicidade (semanal, mensal ou semestral)<br/>e a forma de pagamento (cartao ou Pix) e clica em assinar
  alt plano FREE (decisao de 17/10)
    Front->>Ger: POST assinatura FREE
    Ger-->>Front: segue para a criacao do tenant sem gateway (diagrama 2, opt FREE)
  else plano pago
    Front->>Front: pede os dados do comprador: CPF ou CNPJ, nome, e-mail,<br/>telefone e endereco completo (CEP, rua, numero, bairro)
    Front-->>Usuario: segue para a contratacao (diagrama 2)
  end

  alt FA-01: nenhum plano disponivel
    Ger-->>Front: "nao ha planos disponiveis no momento"
  else FA-02: falha ao carregar planos
    Ger-->>Front: "falha ao carregar, tente novamente"
  end
  Note over Ger,Front: Asaas indisponivel ao iniciar a contratacao: tratado no diagrama 2 (FA-04)
```
