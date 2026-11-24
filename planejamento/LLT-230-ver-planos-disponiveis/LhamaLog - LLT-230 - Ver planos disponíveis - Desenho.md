# LLT-230 — Ver planos disponíveis — Desenho

Versão: v7 Status: para aprovação Autor: André Felipe Data: 27/10/2026 Base: documento de Requisitos da LLT-230 (v7) Mudanças da v7: as formas de pagamento passam a ser PIX, BOLETO, CARTAO e DEBITO (boleto com o preço do Pix); a franquia tem a unidade do período (semana no semanal, mês nos demais). Mudanças da v6: sem fórmula de preço: os preços públicos (aba Planos Ajustado do Plano de Monetização v4) são gravados como dados e devolvidos como estão; some a coleção parametros_cobranca e a CalculadoraPreco; recursos de IA de Business e Enterprise com o texto literal do v4.

Este documento diz **como** a tarefa será construída. O **o quê** está no documento de Requisitos.

## 1. Onde cada parte roda

| **Parte** | **Onde**                          | **O que faz**                                                     |
|-----------|-----------------------------------|-------------------------------------------------------------------|
| Back      | lhamalog-core (Java, Spring Boot) | Entrega a lista de planos com os preços e marca o plano atual     |
| Dados     | MongoDB                           | Guarda os planos, os preços e as assinaturas                      |
| Front     | Épico do front web                | Mostra os cartões. **Fora desta tarefa**: usa a API definida aqui |

Esta tarefa não fala com o Asaas.

## 2. Fluxo passo a passo

1.  A pessoa abre a página de planos.

2.  O front pede a lista ao Core: GET /api/v1/planos. Se a pessoa estiver logada, envia o token do login.

3.  O Core lê os planos ativos na coleção planos e, pelo código de cada plano, os preços na coleção tabela_precificacao.

4.  Se veio um token válido com conta (tenant), o Core também lê a assinatura dessa conta e descobre o plano atual.

5.  O Core junta plano e preços, ordena da mensalidade mais barata para a mais cara e marca o plano atual.

6.  O front mostra os cartões, com o plano atual destacado.

Situações especiais:

- **Nenhum plano ativo:** responde 200 com lista vazia. A tela mostra "não há planos disponíveis no momento".

- **Plano ativo sem preço cadastrado:** esse plano não entra na lista, e o Core registra um aviso no log (regra R15).

- **Falha no banco:** responde 503. A tela mostra "falha ao carregar, tente novamente".

- **Login vencido ou inválido:** responde 200, trata como visitante (sem destaque) e devolve sessaoExpirada: true.

- **Sem login nenhum:** responde 200 com sessaoExpirada: false. Sem aviso.

## 3. Contrato da API

GET /api/v1/planos: público; o token do login é opcional.

Resposta 200 (exemplo):

{

"moeda": "BRL",

"planoAtual": "PRO",

"sessaoExpirada": false,

"planos": \[

{

"codigo": "PRO",

"nome": "Pro",

"precos": {

"SEMANAL": { "PIX": 9407, "BOLETO": 9407, "CARTAO": 9542, "DEBITO": 9421 },

"MENSAL": { "PIX": 40099, "BOLETO": 40099, "CARTAO": 41181, "DEBITO": 40705 },

"SEMESTRAL": { "PIX": 239599, "BOLETO": 239599, "CARTAO": 246830, "DEBITO": 244048 }

},

"franquiaGb": 100,

"franquiaPor": { "SEMANAL": "SEMANA", "MENSAL": "MES", "SEMESTRAL": "MES" },

"precoGbExcedenteCentavos": { "PIX": 450, "BOLETO": 450, "CARTAO": 464, "DEBITO": 459 },

"precoArmazenamentoExtraCentavos": { "PIX": 10, "BOLETO": 10, "CARTAO": 11, "DEBITO": 11 },

"retencaoDias": 30,

"dashboard": "PADRAO",

"recursosAnalise": \["DETECCAO_ANOMALIAS", "SUGESTOES_IA"\],

"chamadasIaMes": 1000,

"membrosIncluidos": 10,

"produtosIncluidos": 10,

"testeGratisDias": 14,

"atual": true

}

\]

}

Escolhas:

- **Valores em centavos, inteiros.** O front formata como "R\$ 411,81".

- **Todos os preços vêm prontos** da aba Planos Ajustado. O front e o Core não calculam taxa.

- **franquiaPor:** diz se a franquia é por semana ou por mês, conforme a periodicidade.

- **Free:** precos, precoGbExcedenteCentavos e precoArmazenamentoExtraCentavos vêm null; a ingestão pausa ao chegar na franquia.

- **Ilimitado:** membrosIncluidos ou produtosIncluidos vêm null (a tela mostra "ilimitado").

- **testeGratisDias:** 14 só em Starter e Pro; null nos demais.

- **Ordem:** pela mensalidade mensal no Pix, do menor para o maior.

## 4. Dados

Duas coleções no MongoDB, ligadas pelo código do plano. Cada campo existe em **um lugar só**.

**Coleção planos: o que o plano é**

| **Campo**         | **Tipo**         | **Observação**                                                                                                                                                                                          |
|-------------------|------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| codigo            | texto            | FREE, STARTER, PRO, BUSINESS, ENTERPRISE (chave)                                                                                                                                                        |
| nome              | texto            |                                                                                                                                                                                                         |
| retencaoDias      | inteiro          | 7, 15, 30, 90, 90                                                                                                                                                                                       |
| dashboard         | texto            | BASICO, PADRAO, PERSONALIZADO                                                                                                                                                                           |
| recursosAnalise   | lista            | Free: SUGESTOES_BASICAS · Starter: SUGESTOES_IA · Pro: DETECCAO_ANOMALIAS, SUGESTOES_IA · Business: INVESTIGACAO_AUTOMATICA, DETECCAO_ANOMALIAS · Enterprise: INVESTIGACAO_AUTOMATICA, RASTREIO_USUARIO |
| chamadasIaMes     | inteiro          | 10, 100, 1.000, 5.000, 15.000                                                                                                                                                                           |
| membrosIncluidos  | inteiro ou vazio | 1, 3, 10, 25; vazio = ilimitado                                                                                                                                                                         |
| produtosIncluidos | inteiro ou vazio | 1, 3, 10; vazio = ilimitado                                                                                                                                                                             |
| testeGratisDias   | inteiro ou vazio | 14 em Starter e Pro                                                                                                                                                                                     |
| ativo             | verdadeiro/falso | plano descontinuado = falso                                                                                                                                                                             |

**Coleção tabela_precificacao: quanto custa (preço público, aba Planos Ajustado)**

| **Campo**                       | **Tipo**        | **Observação**                                                                                                    |
|---------------------------------|-----------------|-------------------------------------------------------------------------------------------------------------------|
| codigoPlano                     | texto           | mesmo valor de planos.codigo (chave)                                                                              |
| precos                          | objeto          | periodicidade (SEMANAL, MENSAL, SEMESTRAL) → forma (PIX, BOLETO, CARTAO, DEBITO) → centavos (BOLETO igual ao PIX) |
| franquiaGb                      | inteiro         | por mês nos planos mensal e semestral; por semana no semanal (o mesmo número)                                     |
| precoGbExcedenteCentavos        | objeto ou vazio | PIX, BOLETO, CARTAO e DEBITO; vazio no Free                                                                       |
| precoArmazenamentoExtraCentavos | objeto ou vazio | PIX, BOLETO, CARTAO e DEBITO, por GB-mês retido; vazio no Free                                                    |
| versaoPlanoMonetizacao          | texto           | "v4"; mostra de qual versão da planilha vieram os preços                                                          |

**Carga inicial:** na subida do Core, cada coleção que estiver vazia recebe os dados do documento de Requisitos (seções 4.1 e 4.2). Coleção que já tem dados não é alterada, para não apagar mudanças feitas depois.

## 5. Organização do código (arquitetura hexagonal leve)

- **Entrada:** PlanoController recebe o GET e chama o gerenciador.

- **Regra de negócio:** GerenciadorAssinatura.listarPlanosDisponiveis junta cada Plano aos seus preços e marca o plano atual. Já existe com esse nome no diagrama de classes. As tarefas 231, 232 e 235 leem o valor a cobrar da mesma tabela, para o valor cobrado nunca diferir do valor mostrado.

- **Portas:** PlanoRepository, TabelaPrecificacaoRepository e AssinaturaRepository.

- **Adaptadores:** versões MongoDB dessas três portas.

- A regra de negócio **não conhece** Spring nem MongoDB: isso fica só nos adaptadores.

## 6. Segurança

- O endpoint é público: não exige login.

- Se vier token, o Core valida com o provedor de login e só então lê o tenant.

- Token inválido ou vencido não gera erro: a pessoa é tratada como visitante e a resposta traz sessaoExpirada: true.

- Responde apenas dados de planos, nada de dados de outras contas.

## 7. Testes (make test)

| **Teste**                                                                                                                                                                | **O que garante** |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| Lista os planos ativos do mais barato ao mais caro                                                                                                                       | Regra R1          |
| Conta com plano PRO recebe atual: true só no PRO                                                                                                                         | Regra R3          |
| Visitante recebe todos com atual: false, planoAtual vazio e sessaoExpirada: false                                                                                        | Regra R4          |
| Conta ainda sem assinatura não tem destaque                                                                                                                              | Regra R4          |
| Os 48 preços de mensalidade da resposta (4 planos × 3 periodicidades × 4 formas) são iguais aos do Planos Ajustado, com o boleto igual ao Pix (seção 4.2 dos Requisitos) | Critério 5        |
| Os preços de uso (excedente e armazenamento) em Pix, boleto, cartão e débito são iguais ao Planos Ajustado                                                               | Critério 5        |
| Free vem sem preços e sem preço de excedente                                                                                                                             | Regras R13 e R14  |
| Business e Enterprise vêm com produtosIncluidos ilimitado; Enterprise também em membros                                                                                  | Regra R16         |
| Recursos de IA de Business e Enterprise iguais ao texto do v4                                                                                                            | Seção 4           |
| testeGratisDias só em Starter e Pro                                                                                                                                      | Regra R17         |
| Plano com ativo = false não aparece                                                                                                                                      | Regra R8          |
| Plano ativo sem linha em tabela_precificacao não aparece e gera aviso no log                                                                                             | Regra R15         |
| Token vencido: 200, sem destaque, sessaoExpirada: true                                                                                                                   | Regra R12         |
| Sem planos ativos: 200 com lista vazia                                                                                                                                   | Critério 6        |
| Falha no banco: 503                                                                                                                                                      | Critério 7        |
| Mudar um preço em tabela_precificacao muda a resposta                                                                                                                    | Critério 8        |
| Carga inicial não apaga dados já gravados em nenhuma das duas coleções                                                                                                   | Seção 4           |

## 8. Git

- Branch já criada pelo Jira no lhamalog-core: LLT-230-Ver-planos-disponiveis.

- Commits começam com LLT-230.

- PR com a chave no título, template preenchido e pelo menos um revisor.

## 9. Pendências

Nenhuma.

## 10. Ações decorrentes

- Michel e Pedro: registrar no diagrama de classes a divisão de campos da seção 4 e os campos novos de Plano.

- Se o Michel e o Pedro preferirem unificar planos e tabela_precificacao numa só, a API da seção 3 não muda: só mudam os adaptadores da seção 5 e a carga inicial.

- O código começa quando o repositório lhamalog-core receber o template do Michel (LLT-80).
