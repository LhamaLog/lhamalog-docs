# Guia: deixar a conta do Asaas funcional para o LhamaLog

documentação oficial do Asaas ([https\://docs.asaas.com](https://docs.asaas.com)).

Este guia diz, do ponto de vista de quem vai usar o Asaas, **o que precisa ser feito para a conta ficar pronta** e o que cada passo tem a ver com o LhamaLog. O fluxograma está no arquivo `guia_asaas_fluxo.png`, na mesma pasta deste documento.

## 1\. Em uma frase

O LhamaLog cobra as assinaturas pelo Asaas. Para isso o Asaas precisa de uma **conta aprovada**, de uma **chave Pix**, de uma **chave de API** (que o sistema usa para falar com ele), de um **webhook** (o aviso que o Asaas manda quando um pagamento acontece) e, para emitir nota fiscal, dos **dados fiscais** da empresa.

## 2\. Duas contas, dois ambientes

|  | Sandbox (testes) | Produção (dinheiro de verdade) |
| :---- | :---- | :---- |
| Para quê | Testar e demonstrar, sem dinheiro real | Cobrar clientes de verdade |
| Endereço do painel | sandbox.asaas.com | asaas.com |
| Endereço da API | `https://api-sandbox.asaas.com/v3` | `https://api.asaas.com/v3` |
| Chave de API | Própria do sandbox | Própria da produção |
| Situação hoje | **Pronta e testada** | **Depende do CNPJ** (a empresa ainda não existe) |

As duas contas são independentes: a chave, o webhook e as configurações de uma não valem na outra. Uma chave de produção não funciona no sandbox (dá erro 401), e o contrário também.

## 3\. Passo a passo: conta de produção

### Passo 1\. Pré-requisitos (antes de abrir a conta)

- **Empresa constituída, com CNPJ.** Sem CNPJ não há conta de produção da empresa nem nota fiscal. Hoje só o sandbox está liberado.  
- Dados do responsável: CPF, data de nascimento, endereço e telefone.  
- Documento de identidade e uma conta bancária da empresa.  
- Um e-mail da equipe (não pessoal) para a conta, para não depender de uma pessoa só.

### Passo 2\. Criar a conta

1. Acessar asaas.com e fazer o cadastro pelo aplicativo ou pelo navegador, com e-mail e senha.  
2. Informar CPF ou CNPJ, data de nascimento, endereço e telefone.  
3. Enviar os documentos: pelo aplicativo, selfie e foto do documento de identidade; pelo navegador, uma conta bancária.  
4. Esperar a aprovação. Segundo o Asaas, a análise leva **até 2 dias úteis**, e a primeira cobrança pode ser emitida antes disso. Dependendo da atividade, o Asaas pode pedir documentos extras.

### Passo 3\. Cadastrar a chave Pix

A chave Pix da empresa é necessária para gerar cobranças Pix. No sandbox foi preciso cadastrar uma chave para o Pix recorrente funcionar; em produção é igual.

- Menu **Pix**, cadastrar a chave (CNPJ ou e-mail da empresa).

### Passo 4\. Pedir recursos e confirmar taxas ao Asaas

Alguns recursos dependem de liberação pelo atendimento do Asaas e de análise da conta. Pedir e anotar a resposta:

- **Tokenização de cartão** (necessária para o sistema trocar o valor de uma assinatura paga no cartão). Em produção "depende de habilitação"; no sandbox já está disponível.  
- **Taxas do contrato:** conferir em Menu do usuário, Taxas. A página pública do Asaas não tem linha própria para o cartão **recorrente**; confirmar qual taxa vale (a planilha de preços usa R$0,49+2,99%nocrédito,R$ 1,99 no Pix e no boleto e R\$ 0,35 \+ 1,89% no débito).  
- **Fatura do débito:** perguntar se dá para restringir as formas de pagamento da fatura de uma assinatura (hoje o cliente pode escolher outra forma pelo mesmo preço).  
- **Estorno de Pix:** perguntar por que, no sandbox, o estorno de Pix é negado ("Falha ao processar a transferência") mesmo depois da aprovação do evento crítico.

### Passo 5\. Gerar a chave de API

- Caminho: **Integrações, Chaves de API**, na versão web do Asaas (não dá para gerar pelo aplicativo). Só administradores criam chaves.  
- Dar um nome (por exemplo, "LhamaLog Core produção") e uma data de expiração, se quiser.  
- **A chave aparece uma única vez.** Copiar na hora e guardar em um cofre de segredos.  
- A conta aceita até 10 chaves. Chave sem uso por 3 meses é desabilitada; com 6 meses de inatividade expira de vez.  
- Recomendado: restringir a chave aos IPs do servidor do Core (lista de IPs permitidos).  
- **Nunca** colocar a chave no código, no Git, no Drive, em e-mail ou em print. Ela fica só em variável de ambiente (`ASAAS_API_KEY`). Se vazar, apagar a chave e criar outra.

### Passo 6\. Configurar o webhook (o aviso de pagamento)

O webhook é a forma de o Asaas contar para o LhamaLog que um pagamento foi feito, recusado, estornado ou venceu. Sem ele a conta do cliente não é ativada.

- Caminho: **Integrações, Webhooks, Adicionar Webhook**.  
- Preencher:  
  - **Nome** (até 50 caracteres), por exemplo "LhamaLog Core".  
  - **URL do webhook:** o endereço público do Core, por exemplo `https://api.lhamalog.com.br/webhooks/asaas` (rota `POST /webhooks/asaas`, da LLT-235).  
  - **E-mail** para receber aviso se a entrega falhar (o e-mail da equipe).  
  - **Versão da API:** v3.  
  - **Token de autenticação:** gerar um token de 32 a 255 caracteres, sem espaços e que não seja a chave de API. O Asaas manda esse valor no cabeçalho `asaas-access-token`, e o Core confere. Guardar em variável de ambiente (`ASAAS_WEBHOOK_TOKEN`).  
  - **Tipo de envio** e **fila de sincronização ativada** (deixar ativa).  
- **Eventos a marcar** (o que o LhamaLog usa):  
  - Cobranças: `PAYMENT_CREATED`, `PAYMENT_UPDATED`, `PAYMENT_CONFIRMED`, `PAYMENT_RECEIVED`, `PAYMENT_OVERDUE`, `PAYMENT_DELETED`, `PAYMENT_REFUNDED`, `PAYMENT_REFUND_IN_PROGRESS`, `PAYMENT_REFUND_DENIED`, `PAYMENT_CREDIT_CARD_CAPTURE_REFUSED`, `PAYMENT_CHARGEBACK_REQUESTED`.  
  - Assinaturas: `SUBSCRIPTION_CREATED`, `SUBSCRIPTION_UPDATED`, `SUBSCRIPTION_INACTIVATED`, `SUBSCRIPTION_DELETED`.  
  - Notas fiscais: `INVOICE_CREATED`, `INVOICE_SYNCHRONIZED`, `INVOICE_AUTHORIZED`, `INVOICE_ERROR`.  
  - Checkouts: `CHECKOUT_PAID`, `CHECKOUT_EXPIRED`, `CHECKOUT_CANCELED`.  
  - Chaves de API: `ACCESS_TOKEN_EXPIRING_SOON`, `ACCESS_TOKEN_EXPIRED`, `ACCESS_TOKEN_DISABLED`.  
- **O que o sandbox mostrou:** no **Pix**, o pagamento chega só como `PAYMENT_RECEIVED`; no **cartão**, chega `PAYMENT_CONFIRMED`. O estorno no cartão conclui na hora (`PAYMENT_REFUNDED`); o do Pix foi negado pelo sandbox (`PAYMENT_REFUND_DENIED`, com o motivo em `additionalInfo.denialReason`).  
- Liberar no firewall os **IPs oficiais do Asaas** (no sandbox podem existir IPs extras).  
- Como o Asaas funciona: manda o aviso por `POST`, espera resposta `200` e reenvia se falhar. O mesmo aviso pode chegar **mais de uma vez** (o sistema descarta repetidos pelo id **completo** do evento, no formato `evt_<hash>&<número>`: o hash antes do `&` se repete entre eventos do mesmo tipo, então só o id inteiro é único). Depois de **15 falhas seguidas** a fila **pausa**; os avisos ficam guardados por **14 dias** e depois são apagados. Por isso o Core responde `200` na hora e processa depois.  
- Para conferir: **Integrações, Logs de Webhooks** mostram cada aviso, horário, código de resposta e tentativas.

### Passo 7\. Configurar a nota fiscal (NFS-e)

O Asaas emite a nota de serviço a cada cobrança paga. **Só funciona em conta de pessoa jurídica (CNPJ):** no teste de 28/10, o sandbox com conta de pessoa física recusou a configuração fiscal.

- Preencher os **dados fiscais** da conta. As exigências variam conforme a **prefeitura** (por exemplo, inscrição municipal, forma de autenticação e regime especial de tributação).  
- Definir o **serviço municipal** (código do serviço, pela lista da LC 116/2003 ou pela listagem do município).  
- Falar com a **prefeitura ou o contador** da empresa para saber o código de serviço e o regime tributário corretos. O André combina isso com o contador.  
- No sistema, a nota é ligada a cada assinatura pela configuração de notas fiscais; o resultado chega pelos avisos `INVOICE_AUTHORIZED` (autorizada) e `INVOICE_ERROR` (erro).

### Passo 8\. Personalizar a fatura e a página de pagamento

- Caminho: Minha conta, **Personalização**: logo da LhamaLog e cor da marca.  
- É isso que o cliente vê na página de pagamento do cartão e na fatura do débito e do boleto.

### Passo 9\. Configurar o sistema com os segredos

Quem sobe o sistema (equipe do Core) configura, só como variáveis de ambiente:

- `ASAAS_BASE_URL` \= `https://api.asaas.com/v3` (produção) ou `https://api-sandbox.asaas.com/v3` (sandbox);  
- `ASAAS_API_KEY` \= a chave do passo 5;  
- `ASAAS_WEBHOOK_TOKEN` \= o token do passo 6\.

### Passo 10\. Teste final em produção

1. Contratar o plano mais barato com um valor baixo (por exemplo, uma contratação real de teste da própria equipe).  
2. Conferir que o aviso chegou nos Logs de Webhooks e que a conta foi ativada.  
3. Pedir o estorno (reembolso) e conferir o aviso de estorno.  
4. Conferir a nota fiscal emitida.  
5. Se algo falhar, corrigir e repetir.

### Checklist final: a conta está pronta quando

- [ ] Conta aprovada pelo Asaas.  
- [ ] Chave Pix cadastrada.  
- [ ] Tokenização de cartão habilitada e taxas confirmadas.  
- [ ] Chave de API gerada e guardada só em variável de ambiente.  
- [ ] Webhook ativo, com token, eventos e fila ativa; IPs do Asaas liberados.  
- [ ] Dados fiscais e serviço municipal configurados.  
- [ ] Logo e cor da fatura configurados.  
- [ ] Teste de contratação, webhook, estorno e nota fiscal funcionando.

## 4\. Passo a passo: conta de sandbox (para testar e demonstrar)

1. Criar a conta em **sandbox.asaas.com** (e-mail da equipe).  
2. **Integrações, Chaves de API:** gerar a chave do sandbox (começa com `$aact_hmlg_`) e guardar.  
3. Cadastrar um **cliente de teste** com telefone e endereço completos (o Asaas exige).  
4. Cadastrar uma **chave Pix** no sandbox.  
5. Usar os cartões de teste: aprovado `4444 4444 4444 4444` (CVV 123, validade futura); recusado `5184 0197 4037 3151`.  
6. Usar as ferramentas do sandbox para simular: confirmar um pagamento, forçar o vencimento, aprovar a conta. O código de confirmação de ações críticas é `000000`.  
7. Os testes que já fizemos, com o passo a passo, estão no roteiro de testes do sandbox (`roteiro-testes-sandbox-asaas`).  
8. Quem conferiu o sandbox é o André; as taxas do sandbox são promocionais e por isso o valor líquido sai um pouco diferente do da planilha.  
9. Para testar o webhook sem servidor público, usar um receptor temporário (por exemplo, webhook.site) e apagar o webhook de teste depois.

## 5\. Quem faz cada passo

| Passo | Quem |
| :---- | :---- |
| Constituir a empresa e obter o CNPJ | Dono da empresa, contador |
| Criar a conta e enviar documentos | Responsável legal da empresa |
| Chave Pix e conta bancária | Responsável financeiro |
| Pedidos ao Asaas (tokenização, taxas, perguntas) | André, com o gerente do Asaas |
| Chave de API e webhook | André e Michel (infraestrutura) |
| Nota fiscal (prefeitura, código, regime) | André e contador |
| Personalização (logo e cor) | Design |
| Segredos no sistema e teste final | Equipe do Core |

## 6\. Perguntas para levar ao Asaas

1. Qual a taxa do cartão de crédito em **assinatura recorrente** na nossa conta?  
2. Dá para **restringir as formas de pagamento** da fatura de uma assinatura (por exemplo, só débito)?  
3. Como habilitar a **tokenização de cartão** em produção e quanto tempo leva?  
4. Por que, no sandbox, o estorno de Pix é negado com "Falha ao processar a transferência" depois da aprovação do evento crítico? Em produção funciona?  
5. O **estorno de débito e de boleto** (pagos pela fatura) segue o mesmo caminho do cartão?  
6. A taxa do Asaas é devolvida ao LhamaLog quando há estorno?

## 7\. Pontos de atenção

- O dinheiro do **cartão** só entra na conta cerca de 30 dias depois; o do Pix entra na hora. Para estornar um Pix a conta precisa ter saldo.  
- No **débito** e no **boleto** não há cobrança automática: o cliente recebe a fatura por e-mail a cada ciclo e precisa pagar.  
- O Asaas gera as cobranças futuras com antecedência (no plano semanal, 4 de uma vez).  
- A **conta do cliente só é criada depois do aviso de pagamento confirmado**, por isso o webhook precisa estar certo antes de ir para produção.

&nbsp;