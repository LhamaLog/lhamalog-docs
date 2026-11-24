# LLT-235 — Criar a interface genérica do gateway de pagamento — Requisitos

Versão: v1 Status: para aprovação Autor: André Felipe Data: 27/10/2026 Épico: Assinatura e cobrança (LLT-109) · Sprint 6 Relacionadas: LLT-89 (eleger o gateway), LLT-90 (diagramas), LLT-230 a 234 (usam esta interface)

## 1. Objetivo

Criar, dentro do Core, uma porta de pagamento independente do provedor (GatewayPagamento) e o adaptador do Asaas (ApiPagamento), com o recebimento seguro dos avisos do Asaas (webhooks) tratando avisos repetidos e fora de ordem. As tarefas de contratar, alterar, cancelar, reembolsar e cobrar excedente usam só essa porta.

## 2. Quem usa

- **O próprio sistema:** as tarefas LLT-231 a 234 chamam a porta.

- **A equipe LhamaLog:** reprocessa avisos que falharam, por rota interna, e recebe e-mail quando algo falha.

## 3. O pedido no Jira

> Porta de domínio independente do provedor + adaptador do gateway escolhido; tratamento de webhooks fora de ordem e repetidos.

## 4. Contexto

- Gateway: **Asaas** (ADR_163), sandbox até a empresa ter CNPJ.

- O Asaas não assina os avisos com HMAC e entrega "pelo menos uma vez"; a fila dele pausa depois de 15 falhas seguidas, por isso o Core responde na hora e processa depois.

- O Asaas não tem Idempotency-Key; a idempotência é pela referência (externalReference).

- A página de pagamento do cartão não grava a referência; o elo é o código do checkout (checkoutSession).

## 5. Regras

| **\#** | **Regra**                                                                                                                                                                                                                                                              |
|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| R1     | Toda conversa com o provedor passa por GatewayPagamento. Nenhuma regra de negócio conhece o Asaas.                                                                                                                                                                     |
| R2     | A porta tem estas operações: enviarCobranca (página de pagamento ou assinatura direta), consultarStatus, alterarAssinatura, gravarDescricaoReferencia, cancelarAssinatura, solicitarReembolsoExterno, registrarExcedente, configurarNotaFiscal e validarAutenticidade. |
| R3     | O adaptador ApiPagamento (gateway ativo = ASAAS) traduz cada operação para as chamadas do Asaas e usa o sandbox ou a produção conforme a configuração.                                                                                                                 |
| R4     | **Autenticidade do aviso:** o Core confere o token do cabeçalho asaas-access-token contra o segredo guardado, aceita só os IPs oficiais do Asaas e **reconsulta o recurso na API** antes de aplicar. O estado aplicado é sempre o da API, nunca o do corpo do aviso.   |
| R5     | **Aviso repetido** (mesmo id de evento) é registrado uma vez e não é reaplicado.                                                                                                                                                                                       |
| R6     | **Aviso fora de ordem** não sobrescreve um estado mais novo: como o estado vem da reconsulta, um aviso atrasado não desfaz nada.                                                                                                                                       |
| R7     | O Core **responde 200 na hora** ao aviso e processa depois.                                                                                                                                                                                                            |
| R8     | Todo aviso recebido fica registrado (id, tipo, conteúdo, estado do processamento: RECEBIDO, EXECUTADO, FALHA).                                                                                                                                                         |
| R9     | **Falha ao processar** um aviso (Clerk, banco ou Asaas fora do ar): o Core tenta de novo **3 vezes sozinho** (depois de 1, 5 e 30 minutos). Se continuar falhando, o aviso fica FALHA, a equipe recebe **e-mail** e o aviso aparece no painel interno.                 |
| R10    | **Reprocessamento manual:** a equipe reprocessa um aviso FALHA por rota interna; o reprocessamento respeita a idempotência (não aplica duas vezes).                                                                                                                    |
| R11    | Os eventos do Asaas viram os 9 tipos de operação já definidos (PRIMEIRA_COMPRA, RENOVACAO, ATRASO, RECUSA, UPGRADE_DOWNGRADE, CANCELAMENTO, REEMBOLSO, CHARGEBACK e NOTA_FISCAL); avisos sem tipo mapeado são registrados sem efeito.                                  |
| R12    | **Idempotência das chamadas:** toda criação no Asaas leva a referência do sistema. Antes de repetir uma chamada que deu tempo esgotado, o Core consulta se o recurso já existe.                                                                                        |
| R13    | **Erros do Asaas:** erro 4xx (dado inválido) não é repetido e volta ao chamador com a mensagem do Asaas traduzida; erro 5xx ou tempo esgotado é repetido com espera crescente até 3 vezes e depois vira "Asaas indisponível" (503).                                    |
| R14    | **Segredos** (chave de API, token do aviso) ficam só em variáveis de ambiente, nunca no Git, no Drive, no Jira ou em log.                                                                                                                                              |
| R15    | O log nunca grava dados de cartão, CPF/CNPJ completo ou a chave de API.                                                                                                                                                                                                |
| R16    | Trocar de provedor no futuro só exige um adaptador novo e mudar a configuração do gateway ativo.                                                                                                                                                                       |

## 6. Fora do escopo desta tarefa

- As regras de negócio de contratar, alterar, cancelar, reembolsar e cobrar excedente (LLT-231 a 234).

- Tela interna para a equipe (no MVP é rota interna).

- Pix Automático (só depois de 6 meses de CNPJ) e boleto.

- Segundo gateway.

## 7. Critérios de aceite

1.  As tarefas 231 a 234 só falam com o gateway pela porta, nunca pelo Asaas.

2.  O aviso com token ou IP inválido é recusado e nada é gravado.

3.  Aviso repetido não é reaplicado; aviso fora de ordem não muda o estado.

4.  O estado aplicado vem sempre da reconsulta na API.

5.  Falhas passam por 3 tentativas automáticas; depois ficam FALHA, com e-mail para a equipe e reprocessamento manual.

6.  As operações da porta batem com as chamadas testadas no sandbox.

7.  Nenhum segredo aparece em arquivo versionado nem em log.

## 8. Decisões tomadas

Do André, em 17/10/2026 (ADR_163): Asaas, aviso verificado por token + IP + reconsulta, idempotência pela referência, 9 tipos de operação.

Do André, em 22/10/2026: métodos novos da interface aprovados (alterarAssinatura, cancelarAssinatura, configurarNotaFiscal e registrarExcedente); reembolso e reprocessamento por rota interna sem tela.

Do André, em 27/10/2026:

- Tentativas automáticas: 3, depois manual.

- Falha: e-mail para a equipe e registro no painel interno.

Achados do sandbox (24 a 27/10/2026) que viraram regra:

- Cartão pela página de pagamento: sem referência na cobrança; elo pelo checkoutSession (R2, gravarDescricaoReferencia).

- Pix criado direto: referência e descrição já vão na criação.

- Fila de avisos do Asaas pausa depois de 15 falhas seguidas (R7).

## 9. Pendências

Nenhuma.

## 10. Ações decorrentes

- Michel: configurar o endereço público do Core para receber os avisos e o segredo do aviso no ambiente.

- Michel e Pedro: registrar no diagrama de classes as operações novas da porta e o EventoGateway com os estados.

- O código desta tarefa começa quando o repositório lhamalog-core receber o template do Michel (LLT-80).
