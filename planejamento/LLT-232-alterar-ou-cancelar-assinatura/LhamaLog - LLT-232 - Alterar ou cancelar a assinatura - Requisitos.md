# LLT-232 — Alterar ou cancelar a assinatura — Requisitos

Versão: v2 Status: para aprovação Autor: André Felipe Data: 27/10/2026 Épico: Assinatura e cobrança (LLT-109) · Sprint 6 Mudanças da v2: a diferença do upgrade passa a repassar ao cliente a taxa fixa do Asaas da cobrança avulsa (decisão de 27/10/2026); formas de pagamento incluem débito e boleto. Relacionadas: LLT-230 (ver planos), LLT-231 (contratar), LLT-233 (reembolso), LLT-234 (consumo), LLT-235 (interface do gateway) Casos de uso: USID_041 (alterar plano) e USID_042 (cancelar)

## 1. Objetivo

Permitir que o Dono da conta mude de plano ou de periodicidade e cancele a assinatura, com regras claras de quando cada mudança vale e com tudo registrado.

## 2. Quem usa

- **Dono da conta:** é o único que altera ou cancela (decisão de 22/10/2026). Administradores e membros veem o plano, mas não mudam.

## 3. O pedido no Jira

> Como administrador, quero mudar de plano ou cancelar.

Critérios de aceite do card:

1.  Upgrade e downgrade aplicam a regra definida (proporcional ou no próximo ciclo).

2.  Cancelamento mantém acesso até o fim do período pago e depois para a ingestão.

3.  Todas as mudanças ficam registradas.

## 4. Como funciona o pagamento nas mudanças (contexto)

- Os preços são os do Planos Ajustado (LLT-230), na **forma de pagamento da contratação** (Pix, cartão de crédito, débito ou boleto), que não muda aqui.

- O Asaas gera a cobrança do ciclo seguinte com antecedência. Por isso "valer no próximo ciclo" significa mudar o valor dessa cobrança já gerada.

- No upgrade, a **diferença** é paga numa página de pagamento avulsa do Asaas, com Pix ou cartão à escolha de quem paga (a página não oferece débito nem boleto).

- No cancelamento, o Asaas não apaga sozinho as cobranças futuras: o sistema apaga uma a uma.

## 5. Regras

| **\#** | **Regra**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| R1     | Só o **Dono** altera ou cancela a assinatura.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| R2     | A mudança de plano ou de periodicidade só é feita com a assinatura **ATIVA** (paga e sem atraso). Em atraso ou suspensa, a pessoa primeiro regulariza o pagamento.                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| R3     | **Upgrade** (plano mais caro): vale **na hora**, depois que a diferença é paga. Até o pagamento ser confirmado, o plano atual continua valendo.                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| R4     | **Diferença do upgrade:** (preço do plano novo − preço do plano atual) × dias que faltam no ciclo ÷ dias do ciclo, com os preços do Planos Ajustado da forma de pagamento e da periodicidade atuais, **mais a taxa fixa do Asaas da cobrança avulsa**, arredondada para cima ao centavo. A taxa fixa repassada é: Pix e boleto R\$ 1,99; cartão de crédito R\$ 0,49 ÷ 0,9701; cartão de débito R\$ 0,35 ÷ 0,9811 (a parte percentual da taxa já está dentro dos preços do Planos Ajustado). O cálculo é feito pelo Core, e a tela mostra o valor total e quanto dele é taxa antes de a pessoa confirmar. |
| R5     | Depois do upgrade, a próxima cobrança do ciclo já vem com o preço do plano novo.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| R6     | **Downgrade** (plano mais barato): vale no **próximo ciclo**, sem reembolso. A cobrança do próximo ciclo passa a ter o preço do plano novo, e o acesso do plano antigo vai até o fim do período já pago.                                                                                                                                                                                                                                                                                                                                                                                                 |
| R7     | **Troca de periodicidade** (semanal, mensal, semestral): vale sempre no **próximo ciclo**, sem reembolso, mesmo quando a troca vem junto com um upgrade (nesse caso, o plano novo vale na hora e a periodicidade nova no próximo ciclo).                                                                                                                                                                                                                                                                                                                                                                 |
| R8     | **Downgrade bloqueado** quando o uso atual passa dos limites do plano novo (membros ou produtos). A tela mostra o excesso ("você tem 10 membros e o plano Starter permite 3") e só aceita depois que o Dono remove o que passa.                                                                                                                                                                                                                                                                                                                                                                          |
| R9     | A **forma de pagamento** (Pix, cartão, débito ou boleto) não muda nesta tarefa.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| R10    | Só existe **uma mudança agendada por vez**. Um novo pedido de downgrade ou de troca de periodicidade substitui o anterior, e a pessoa pode cancelar o agendamento antes de ele valer.                                                                                                                                                                                                                                                                                                                                                                                                                    |
| R11    | **Durante o teste de 14 dias** só é possível cancelar: a conta volta para o plano Free na hora, sem cobrança (regra R16 da LLT-231). Para mudar de plano, a pessoa espera o primeiro pagamento.                                                                                                                                                                                                                                                                                                                                                                                                          |
| R12    | **Cancelar** a assinatura: o acesso continua até o **fim do período já pago**; a assinatura fica CANCELAMENTO_AGENDADO e, na data, passa a CANCELADA, com a ingestão parando e os Tokens de Produto revogados. Os dados ficam disponíveis por 30 dias para exportar (Termos de Uso).                                                                                                                                                                                                                                                                                                                     |
| R13    | O cancelamento **não devolve** o período já pago. Reembolso só nas hipóteses da LLT-233.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| R14    | Quem agendou o cancelamento **não pode desistir**. Para voltar, contrata um plano novo depois do fim do período (nova contratação, sem teste grátis).                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| R15    | Com o cancelamento agendado, a mudança de plano fica bloqueada, e a tela mostra a data em que o acesso acaba.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| R16    | Se a diferença do upgrade não for paga (cartão recusado, Pix não pago em 1 hora, página fechada), **nada muda**: a assinatura fica como estava e a pessoa pode tentar de novo.                                                                                                                                                                                                                                                                                                                                                                                                                           |
| R17    | **Toda mudança fica registrada** em um histórico: quem pediu, quando, plano e periodicidade de antes e de depois, valor da diferença, quando passa a valer e o resultado (aplicada, agendada, expirada, cancelada). O Dono pode consultar.                                                                                                                                                                                                                                                                                                                                                               |
| R18    | O plano Free não troca de plano aqui: quem está no Free contrata pela LLT-231.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |

## 6. Fora do escopo desta tarefa

- Contratar plano (LLT-231) e ver planos (LLT-230).

- Reembolso (LLT-233), inclusive o reembolso do upgrade em até 7 dias.

- Consumo e cobrança do excedente (LLT-234).

- A interface do gateway e o recebimento de avisos (LLT-235).

- Trocar a forma de pagamento (por exemplo, de Pix para cartão).

- Tela do front (épico do front web). Esta tarefa entrega a API.

## 7. Critérios de aceite

1.  O upgrade só vale depois de a diferença ser paga, e o valor da diferença (com a taxa fixa repassada) bate com a fórmula da regra R4.

2.  O downgrade e a troca de periodicidade valem só no próximo ciclo, e o acesso do plano antigo vai até o fim do período pago.

3.  O downgrade com uso acima dos limites do plano novo é bloqueado, com o excesso mostrado.

4.  O cancelamento mantém o acesso até o fim do período pago, e depois a ingestão para.

5.  O cancelamento no teste de 14 dias volta a conta ao Free sem cobrança.

6.  Quem não é Dono não consegue alterar nem cancelar.

7.  Upgrade não pago não altera nada.

8.  Toda mudança aparece no histórico.

9.  Depois do cancelamento, o Asaas não cobra mais nada (cobranças futuras apagadas).

## 8. Decisões tomadas

Do André, em 22/10/2026:

- Só o Dono altera ou cancela.

- Upgrade imediato com cobrança proporcional; downgrade e troca de periodicidade no próximo ciclo, sem reembolso (ADR_124).

- Cancelar no teste de 14 dias volta ao Free.

- Quando o cancelamento chega ao fim: ingestão para, dados por 30 dias (Termos de Uso).

Do André, em 27/10/2026:

- A forma de pagamento da contratação não muda nesta tarefa.

- Troca de plano junto com periodicidade: plano na hora (se for upgrade) e periodicidade no próximo ciclo.

- Quem agendou o cancelamento não pode desistir; só contratando de novo.

- Downgrade com uso acima dos limites é bloqueado até o Dono ajustar.

- **A taxa do Asaas na cobrança da diferença do upgrade é repassada ao cliente** (o v4 não prevê esse caso; o Michel é avisado).

- Também confirmadas: R2 (só com assinatura ATIVA), R10 (uma mudança agendada por vez), R11 (no teste só cancela) e R15 (cancelamento agendado bloqueia a troca de plano).

Achados do sandbox (26 e 27/10/2026) que viraram regra:

- A diferença do upgrade é cobrada por uma página de pagamento avulsa que aceita Pix e cartão (R3).

- Trocar valor e ciclo na assinatura altera também a cobrança do próximo ciclo já gerada (R5, R6, R7).

- A data final (endDate) não apaga cobranças futuras (R12).

## 9. Pendências

Nenhuma.

## 10. Ações decorrentes

- Design (protótipo da área da assinatura): mostrar o valor da diferença (e quanto é taxa) antes de confirmar, o aviso de excesso no downgrade, a data do fim do acesso no cancelamento e o histórico.

- Michel: avisar que a diferença do upgrade repassa a taxa fixa do Asaas (o plano de monetização v4 não prevê esse caso).

- Michel e Pedro: registrar no diagrama de classes alteracao_assinatura, o histórico e os campos novos da assinatura (plano agendado, periodicidade agendada).

- Felipe (Termos de Uso): conferir o texto do cancelamento (acesso até o fim do período, sem reembolso, 30 dias para exportar).

- O código desta tarefa começa quando o repositório lhamalog-core receber o template do Michel (LLT-80).
