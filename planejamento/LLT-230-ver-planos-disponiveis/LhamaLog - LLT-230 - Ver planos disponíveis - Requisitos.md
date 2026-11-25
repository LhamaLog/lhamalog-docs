# LLT-230 — Ver planos disponíveis — Requisitos

Versão: v7 Status: para aprovação Autor: André Felipe Data: 27/10/2026 Épico: Assinatura e cobrança (LLT-109) · Sprint 6 Mudanças da v7: cartão de débito e boleto entram no MVP (preços do Planos Ajustado para o débito; boleto com o mesmo preço do Pix); no plano semanal a franquia de GB é semanal (mesmo número do mensal, por semana) e o excedente da semana vem junto com a cobrança semanal. Mudanças da v6: os preços públicos são os da aba "Planos Ajustado" do Plano de Monetização v4 (Michel), copiados como dados, sem fórmula no sistema; o excedente de GB no plano mensal vai na mesma fatura da mensalidade; recursos de IA de Business e Enterprise com o texto literal do v4. Mudanças da v5 (mantidas): periodicidade semanal, mensal e semestral (o anual saiu), preço por forma de pagamento, armazenamento extra cobrado, limites de membros, produtos e chamadas de IA por plano.

## 1. Objetivo

Permitir que quem usa o LhamaLog compare os planos e veja qual é o plano atual da sua conta.

## 2. Quem usa

- **Dono e Administrador da conta:** vê os planos e o plano atual destacado.

- **Visitante (sem login):** vê os mesmos planos, sem destaque, para decidir antes de assinar.

## 3. O pedido no Jira

> Como administrador, quero comparar os planos.

Critérios de aceite do card:

1.  Lista os planos com preço, franquia de logs e limites.

2.  Destaca o plano atual.

## 4. Como o plano é cobrado (contexto)

A cobrança é por uso (Plano de Monetização v4):

- **Mensalidade base**, que inclui uma **franquia** de GB de logs por mês.

- **GB a mais** que a franquia: cobrado por GB (excedente).

- **Armazenamento extra:** R\$ 0,10 por GB-mês retido acima da franquia, em todos os planos pagos.

- **Periodicidade:** semanal, mensal ou semestral (no Asaas: WEEKLY, MONTHLY e SEMIANNUALLY).

- **Formas de pagamento:** cartão de crédito, Pix, cartão de débito e boleto. O crédito é cobrado sozinho a cada ciclo. Pix, débito e boleto o cliente paga a cada cobrança; débito e boleto são pagos pela fatura do Asaas, **sem débito automático** (o Asaas não debita sozinho no débito).

### 4.1 Valores líquidos (o que o LhamaLog recebe)

| **Plano**  | **Mensalidade base** | **Franquia por mês** | **Excedente por GB**                          | **Retenção** | **Chamadas de IA por mês** |
|------------|----------------------|----------------------|-----------------------------------------------|--------------|----------------------------|
| Free       | R\$ 0                | 1 GB                 | não cobra: ao chegar em 1 GB a ingestão pausa | 7 dias       | 10                         |
| Starter    | R\$ 79,00            | 10 GB                | R\$ 6,00                                      | 15 dias      | 100                        |
| Pro        | R\$ 399,00           | 100 GB               | R\$ 4,50                                      | 30 dias      | 1.000                      |
| Business   | R\$ 1.490,00         | 500 GB               | R\$ 3,50                                      | 90 dias      | 5.000                      |
| Enterprise | R\$ 2.690,00         | 1.000 GB             | R\$ 2,80                                      | 90 dias      | 15.000                     |

| **Plano**  | **Membros** | **Produtos** | **Recursos de análise e IA**                  | **Dashboard** |
|------------|-------------|--------------|-----------------------------------------------|---------------|
| Free       | 1           | 1            | Sugestões básicas                             | Básico        |
| Starter    | 3           | 3            | Sugestões por IA                              | Padrão        |
| Pro        | 10          | 10           | Detecção de anomalias + sugestões por IA      | Padrão        |
| Business   | 25          | ilimitados   | Investigação automática + anomalias           | Padrão        |
| Enterprise | ilimitados  | ilimitados   | Investigação automática + rastreio de usuário | Personalizado |

### 4.2 Preço público (o que o cliente paga)

O Plano de Monetização v4 tem duas visões: **Planos Base** (valores líquidos, o que o LhamaLog recebe, tabela 4.1) e **Planos Ajustado** (o preço público, já com a taxa do Asaas somada). **O Ajustado é o que vai para o Asaas e para a tela de planos.** O sistema não faz conta de taxa: os preços do Ajustado são copiados como dados.

Mensalidade (semanal e mensal são cobradas todo ciclo; semestral é uma cobrança só, adiantada):

| **Plano**  | **Pix semanal** | **Pix mensal** | **Pix semestral** | **Cartão semanal** | **Cartão mensal** | **Cartão semestral** |
|------------|-----------------|----------------|-------------------|--------------------|-------------------|----------------------|
| Free       | R\$ 0,00        | R\$ 0,00       | R\$ 0,00          | R\$ 0,00           | R\$ 0,00          | R\$ 0,00             |
| Starter    | R\$ 20,23       | R\$ 80,99      | R\$ 475,99        | R\$ 19,30          | R\$ 81,95         | R\$ 489,12           |
| Pro        | R\$ 94,07       | R\$ 400,99     | R\$ 2.395,99      | R\$ 95,42          | R\$ 411,81        | R\$ 2.468,30         |
| Business   | R\$ 345,84      | R\$ 1.491,99   | R\$ 8.941,99      | R\$ 354,95         | R\$ 1.536,43      | R\$ 9.216,05         |
| Enterprise | R\$ 622,76      | R\$ 2.691,99   | R\$ 16.141,99     | R\$ 640,41         | R\$ 2.773,42      | R\$ 16.637,97        |

| **Plano**  | **Débito semanal** | **Débito mensal** | **Débito semestral** |
|------------|--------------------|-------------------|----------------------|
| Free       | R\$ 0,00           | R\$ 0,00          | R\$ 0,00             |
| Starter    | R\$ 18,94          | R\$ 80,88         | R\$ 483,49           |
| Pro        | R\$ 94,21          | R\$ 407,05        | R\$ 2.440,48         |
| Business   | R\$ 350,83         | R\$ 1.519,07      | R\$ 9.112,58         |
| Enterprise | R\$ 633,09         | R\$ 2.742,18      | R\$ 16.451,28        |

**Boleto:** o v4 ainda não tem coluna de boleto. A taxa do boleto no Asaas é a mesma do Pix (R\$ 1,99 por boleto pago), então o preço público do boleto é **igual ao do Pix** (decisão de 27/10/2026). O Michel acrescenta a coluna ao plano de monetização dele.

Uso (cobrado por GB; só o percentual da taxa entra no preço, a taxa fixa já está na mensalidade):

| **Item**                                                  | **Pix e boleto** | **Cartão de crédito** | **Cartão de débito** |
|-----------------------------------------------------------|------------------|-----------------------|----------------------|
| Excedente Starter (por GB ingerido)                       | R\$ 6,00         | R\$ 6,19              | R\$ 6,12             |
| Excedente Pro                                             | R\$ 4,50         | R\$ 4,64              | R\$ 4,59             |
| Excedente Business                                        | R\$ 3,50         | R\$ 3,61              | R\$ 3,57             |
| Excedente Enterprise                                      | R\$ 2,80         | R\$ 2,89              | R\$ 2,86             |
| Armazenamento extra (por GB-mês retido acima da franquia) | R\$ 0,10         | R\$ 0,11              | R\$ 0,11             |

Como o uso é cobrado:

- **Mensal:** o excedente e o armazenamento extra do mês que fechou vão na **mesma fatura** da mensalidade seguinte (como diz o v4).

- **Semestral:** como a franquia é mensal, o excedente e o armazenamento extra são cobrados mês a mês, numa **cobrança separada**. Nela incide a taxa fixa do Asaas (nota do v4).

- **Semanal:** a franquia é **semanal** (o mesmo número de GB do mensal, por semana, zerando toda semana) e o excedente da semana vem **junto com a cobrança semanal** (decisão de 27/10/2026, conversada com o Michel). O armazenamento extra do semanal segue o mês de uso e é somado na primeira cobrança semanal depois que o mês fecha.

Os preços ficam em dados configuráveis: quando o Michel publicar uma nova versão do Plano de Monetização, troca-se o dado, sem alterar o código.

## 5. Regras

| **\#** | **Regra**                                                                                                                                                                                                                                                                                 |
|--------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| R1     | Mostra todos os planos ativos, do mais barato para o mais caro.                                                                                                                                                                                                                           |
| R2     | Cada plano mostra: nome, preço de cada periodicidade e forma de pagamento, franquia de GB, preço do GB a mais e do armazenamento extra (em cada forma de pagamento), dias de retenção, recursos de análise e IA, chamadas de IA por mês, tipo de dashboard, membros e produtos incluídos. |
| R3     | Quem está logado e tem assinatura vê o **plano atual destacado**.                                                                                                                                                                                                                         |
| R4     | Visitante e conta ainda sem assinatura veem a lista sem destaque.                                                                                                                                                                                                                         |
| R5     | Valores em reais. **O preço depende da forma de pagamento** (Pix, cartão de crédito, cartão de débito ou boleto), igual ao Planos Ajustado da seção 4.2 (boleto igual ao Pix). A tela tem seletores de periodicidade (Semanal, Mensal, Semestral) e de forma de pagamento.                |
| R6     | **Semestral:** a mensalidade é paga adiantada, numa cobrança só, por 6 meses. O excedente e o armazenamento extra são cobrados todo mês, em cobrança separada.                                                                                                                            |
| R7     | **Semanal:** a mensalidade é paga toda semana, a franquia de GB é semanal e o excedente da semana vem junto com a cobrança semanal. **Mensal:** o excedente e o armazenamento extra vão na mesma fatura da mensalidade.                                                                   |
| R8     | Plano descontinuado não aparece.                                                                                                                                                                                                                                                          |
| R9     | "GB" significa o **tamanho do log recebido** (GB bruto), e não o tamanho do pacote de transmissão.                                                                                                                                                                                        |
| R10    | A página de planos é **pública**.                                                                                                                                                                                                                                                         |
| R11    | A franquia de GB vale **por mês** (planos mensal e semestral) ou **por semana** (plano semanal) e zera no fim de cada período. O que sobra não acumula.                                                                                                                                   |
| R12    | **Login vencido ou inválido:** a pessoa é tratada como visitante (vê os planos sem destaque, sem erro) e a tela mostra um aviso sugerindo entrar novamente para ver o plano atual.                                                                                                        |
| R13    | O plano Free não passa pelo gateway de pagamento.                                                                                                                                                                                                                                         |
| R14    | **Plano Free ao chegar em 1 GB:** a ingestão de logs pausa até o mês virar ou até a conta fazer upgrade. Há avisos em 80% e 100% (LLT-234). Nada é cobrado.                                                                                                                               |
| R15    | Um plano ativo que ainda não tem preço cadastrado não aparece na lista (para nunca mostrar um plano sem preço).                                                                                                                                                                           |
| R16    | **Limites por plano:** membros, produtos e chamadas de IA por mês seguem a tabela 4.1. "Ilimitado" aparece como valor vazio na API. O uso desses limites é tratado nas tarefas dos módulos correspondentes; aqui eles só são mostrados.                                                   |
| R17    | O teste de 14 dias aparece como informação do plano só em Starter e Pro, mensal, cartão de crédito (a contratação é da LLT-231).                                                                                                                                                          |

## 6. Fora do escopo desta tarefa

- **A tela de planos (front).** Fica no épico do front web. Esta tarefa entrega a API.

- Contratar um plano (LLT-231).

- Trocar de plano ou cancelar (LLT-232).

- Reembolso (LLT-233).

- Acompanhar o consumo de GB, os avisos e o teto de gasto (LLT-234).

- Conversar com o Asaas (LLT-235).

- Plano anual.

- Tela interna para editar preços.

## 7. Critérios de aceite

1.  A API lista todos os planos ativos com preços por periodicidade e forma de pagamento, franquia, preço do GB a mais, armazenamento extra, retenção, membros, produtos e chamadas de IA.

2.  Logado com assinatura, o plano atual vem marcado e só ele.

3.  Sem login, nenhum plano vem marcado.

4.  O Free vem sem preços e sem preço de GB a mais.

5.  Os preços são exatamente os da aba Planos Ajustado do Plano de Monetização v4 (seção 4.2), com o boleto igual ao Pix.

6.  Sem planos ativos, a API devolve lista vazia, e a tela mostra "não há planos disponíveis no momento".

7.  Se houver falha ao carregar, a API responde com erro de serviço indisponível, e a tela mostra "falha ao carregar, tente novamente".

8.  Mudar um preço nos dados configuráveis muda a resposta sem alterar o código.

9.  Com login vencido, a API devolve os planos sem destaque e avisa que a sessão expirou.

## 8. Decisões tomadas

Todas do André.

Em 22/10/2026:

- Modelo de preço por uso: mensalidade base + GB, com valores configuráveis.

- Plano Free continua, com a franquia pequena; ao chegar no limite, a ingestão pausa (sem cobrança).

- Franquia por mês, zera todo mês.

- GB bruto como unidade.

- **Duas classes, como no diagrama de classes:** **Plano** guarda o que o plano é e **TabelaPrecificacao** guarda quanto custa, ligadas pelo código do plano, sem campo repetido.

- Página de planos pública.

- Só o back-end nesta tarefa; a tela fica no épico do front web.

- Login vencido: trata como visitante e sugere entrar de novo.

Em 26/10/2026, após o Plano de Monetização v4:

- O v4 é a base de preços, franquias, armazenamento e limites.

- Periodicidade: semanal, mensal e semestral (o anual com 10% saiu).

- Preço por forma de pagamento, com a taxa do Asaas somada (substitui o "preço único").

- **Preço público = aba Planos Ajustado do v4, copiada como dados.** O sistema não calcula a taxa do Asaas.

- **Mensal:** excedente e armazenamento extra na mesma fatura da mensalidade (como o v4).

- **Recursos de IA de Business e Enterprise:** texto literal do v4.

- Armazenamento extra passa a ser cobrado (substitui "não cobrar no MVP").

- Limites de membros, produtos e chamadas de IA passam a existir por plano (substitui "20 membros para todos").

- Semestral: excedente e armazenamento extra cobrados mês a mês, numa cobrança separada.

Em 27/10/2026:

- **Cartão de débito entra no MVP**, pago pela fatura do Asaas a cada cobrança (sem débito automático), com os preços de débito do Planos Ajustado.

- **Boleto entra no MVP**, com o mesmo preço do Pix; o Michel acrescenta a coluna ao plano dele.

- **Semanal:** a franquia de GB é semanal (mesmo número do mensal) e o excedente da semana vem junto com a cobrança semanal. O armazenamento extra do semanal segue o mês de uso.

## 9. Pendências

Nenhuma.

## 10. Ações decorrentes

- Michel e Pedro: registrar no diagrama de classes a divisão de campos entre Plano e TabelaPrecificacao (desenho, seção 4) e os campos novos.

- Michel: acrescentar a coluna de boleto ao plano de monetização dele.

- Se o Michel e o Pedro preferirem unificar as duas classes numa só, a API desta tarefa não muda: só muda a parte do Core que lê o banco.

- Quando o Michel publicar nova versão do Plano de Monetização, só os dados configuráveis são trocados.

- O código desta tarefa começa quando o repositório lhamalog-core receber o template do Michel (LLT-80).
