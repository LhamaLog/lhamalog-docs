# LLT-234 — Acompanhar o consumo de logs do mês — Requisitos

Versão: v2 Status: para aprovação Autor: André Felipe Data: 27/10/2026 Épico: Assinatura e cobrança (LLT-109) · Sprint 6 Mudanças da v2: no plano semanal a franquia é semanal (mesmo número de GB do mensal, por semana) e o excedente da semana vem junto com a cobrança semanal (decisão de 27/10/2026). Relacionadas: LLT-230 (planos e preços), LLT-231 (contratar), LLT-232 (alterar ou cancelar), LLT-235 (interface do gateway)

## 1. Objetivo

Mostrar ao Dono e aos Administradores quantos GB de logs a conta já usou no mês, avisar quando a franquia chegar perto do limite e aplicar a regra de excedente do plano (cobrar o que passou, respeitando o teto de gasto, ou pausar a ingestão).

## 2. Quem usa

- **Dono e Administrador da conta:** veem o consumo, recebem os avisos e (só o Dono) definem o teto de gasto.

- Membros comuns não veem o consumo (decisão de 27/10/2026).

## 3. O pedido no Jira

> Como administrador, quero ver quantos logs já usei da franquia.

Critérios de aceite do card:

1.  Mostra consumo atual por produto e total, na unidade de cobrança decidida.

2.  Avisos ao atingir 80% e 100%.

3.  Comportamento ao exceder segue a decisão (bloquear, cobrar excedente ou reduzir).

## 4. Como o uso é cobrado (contexto)

- **Unidade:** GB **bruto** (o tamanho do log recebido, e não do pacote de transmissão) — decisão de 22/10/2026. A forma exata de medir o tamanho no Coletor combina-se com quem cuida do Coletor.

- **Franquia por plano** (Plano de Monetização v4, aba Planos Base): Free 1 GB, Starter 10 GB, Pro 100 GB, Business 500 GB, Enterprise 1.000 GB **por mês**. No plano **semanal** o mesmo número vale **por semana** (Starter 10 GB por semana, e assim por diante).

- **Excedente** (preço por GB do Planos Ajustado, por forma de pagamento, tabela da LLT-230): Starter R\$ 6,00, Pro R\$ 4,50, Business R\$ 3,50 e Enterprise R\$ 2,80 no Pix e no boleto (cartão: R\$ 6,19, R\$ 4,64, R\$ 3,61 e R\$ 2,89; débito: R\$ 6,12, R\$ 4,59, R\$ 3,57 e R\$ 2,86).

- **Armazenamento extra:** R\$ 0,10 por GB-mês retido acima da franquia no Pix e no boleto (R\$ 0,11 no cartão e no débito).

- **Período de uso:** é o **mês de uso** nos planos mensal e semestral e a **semana de uso** no plano semanal. O **mês de uso** conta **a partir do dia da contratação** (decisão de 27/10/2026). Começa no dia do primeiro pagamento (com teste grátis, no 15º dia) e se repete no mesmo dia dos meses seguintes; se o dia não existir no mês, usa o último dia do mês. A **semana de uso** começa no dia do primeiro pagamento e se repete a cada 7 dias.

## 5. Regras

| **\#** | **Regra**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| R1     | A tela mostra o consumo do mês de uso atual: total e por produto, em GB bruto, a franquia do plano, o percentual usado, o excedente em GB e o valor estimado do excedente.                                                                                                                                                                                                                                                                                                                                 |
| R2     | O consumo é **atualizado a cada hora** (decisão de 27/10/2026). A tela mostra a hora da última atualização.                                                                                                                                                                                                                                                                                                                                                                                                |
| R3     | **Só Dono e Administrador** veem o consumo e recebem os avisos.                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| R4     | **Avisos da franquia:** ao atingir **80%** e **100%** da franquia do período de uso, o Dono e os Administradores recebem um aviso por e-mail e na plataforma. Cada aviso sai uma vez por mês de uso.                                                                                                                                                                                                                                                                                                       |
| R5     | **Plano Free:** ao chegar em 1 GB, a ingestão **pausa** até o mês de uso virar ou a conta fazer upgrade. Nada é cobrado.                                                                                                                                                                                                                                                                                                                                                                                   |
| R6     | **Planos pagos:** ao passar da franquia, a ingestão **continua** e o excedente é cobrado por GB, ao preço do plano e da forma de pagamento da assinatura.                                                                                                                                                                                                                                                                                                                                                  |
| R7     | **Teto de gasto:** valor máximo de excedente (em reais) que a conta aceita pagar no mês. Só o Dono define e altera. **Padrão: igual à mensalidade do plano** (preço mensal do Planos Ajustado na forma de pagamento da assinatura; ex.: Starter no Pix, R\$ 80,99).                                                                                                                                                                                                                                        |
| R8     | **Avisos do teto:** ao atingir **80%** e **100%** do teto, o Dono e os Administradores recebem aviso. Ao atingir 100% do teto, a ingestão **pausa** até o mês de uso virar ou o Dono aumentar o teto.                                                                                                                                                                                                                                                                                                      |
| R9     | O excedente de ingestão e o armazenamento extra entram na conta do teto.                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| R10    | **Armazenamento extra:** mede-se o volume retido todo dia, e cobra-se pela **média diária do mês de uso**, na parte que passa da franquia, vezes o preço por GB-mês.                                                                                                                                                                                                                                                                                                                                       |
| R11    | **Cobrança do excedente:** quando o período de uso fecha, o sistema calcula o excedente de ingestão e o armazenamento extra e cobra: no plano **mensal**, somado à próxima fatura da mensalidade; no **semanal**, o excedente da semana é somado à próxima cobrança semanal (e o armazenamento extra, que segue o mês de uso, na primeira cobrança semanal depois que o mês fecha); no **semestral**, numa cobrança separada, uma vez por mês. O cliente recebe o detalhamento (GB, preço por GB e total). |
| R12    | **Durante o teste de 14 dias**, ao chegar na franquia a ingestão pausa e nada é cobrado (regra R15 da LLT-231).                                                                                                                                                                                                                                                                                                                                                                                            |
| R13    | **Pausa de ingestão:** o Coletor recusa novos logs da conta com uma resposta clara de "franquia ou teto atingido". A pausa termina sozinha quando o mês de uso vira, o Dono aumenta o teto ou a conta faz upgrade. Logs recusados durante a pausa não são guardados.                                                                                                                                                                                                                                       |
| R14    | **Assinatura suspensa por atraso** tem o bloqueio próprio da ADR_163 (ingestão parada), independente desta regra.                                                                                                                                                                                                                                                                                                                                                                                          |
| R15    | Após upgrade, a franquia e o preço do plano novo valem na hora para o resto do mês de uso; após downgrade, só no próximo ciclo.                                                                                                                                                                                                                                                                                                                                                                            |

## 6. Fora do escopo desta tarefa

- Contratar, alterar ou cancelar (LLT-231 e 232), reembolso (LLT-233) e a interface do gateway (LLT-235).

- Dashboard de análise de logs (épico de dashboards).

- Tela do front (épico do front web). Esta tarefa entrega a API e as regras.

- Limites de membros, produtos e chamadas de IA (valem nos módulos correspondentes).

## 7. Critérios de aceite

1.  A API devolve o consumo do mês de uso por produto e total, em GB bruto, atualizado a cada hora.

2.  Só Dono e Administrador acessam; membros comuns recebem 403.

3.  Aviso de 80% e de 100% da franquia chega uma vez por mês de uso, por e-mail e na plataforma.

4.  No Free, ao chegar em 1 GB a ingestão pausa e volta quando o mês vira ou há upgrade.

5.  Nos planos pagos, o excedente é calculado com o preço do plano e da forma de pagamento.

6.  O teto de gasto, definido pelo Dono, pausa a ingestão ao chegar em 100% e avisa em 80% e 100%.

7.  O armazenamento extra é calculado pela média diária do mês de uso.

8.  Ao fechar o período de uso, o excedente é cobrado do jeito certo para cada periodicidade.

## 8. Decisões tomadas

Do André, em 22/10/2026:

- Modelo por uso: mensalidade base + franquia + preço por GB a mais (valores configuráveis).

- Passou da franquia: cobra por GB até o teto de gasto definido pelo Dono; depois pausa; avisos em 80% e 100%.

- GB bruto como unidade.

- Free: 1 GB; ao chegar, pausa, sem cobrança.

Do André, em 27/10/2026:

- Só Dono e Administrador veem o consumo.

- Atualização a cada hora.

- Armazenamento extra: média diária do mês de uso.

- Teto de gasto padrão igual à mensalidade do plano.

- O mês de uso conta a partir do dia da contratação.

- Plano semanal: franquia semanal (mesmo número do mensal) e excedente da semana junto com a cobrança semanal (conversado com o Michel).

## 9. Pendências

Nenhuma.

## 10. Ações decorrentes

- Quem cuida do Coletor: combinar como medir o GB bruto e como expor o volume retido por dia.

- Design: tela de consumo (barra de uso, aviso de teto, hora da última atualização).

- Felipe (Termos de Uso): incluir o teto de gasto e a pausa da ingestão.

- Michel e Pedro: registrar no diagrama de classes o consumo mensal, os avisos e o teto de gasto na assinatura.

- O código desta tarefa começa quando o repositório lhamalog-core receber o template do Michel (LLT-80).
