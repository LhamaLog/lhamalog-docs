# Diagramas de Sequência — Ciclo de Assinatura (LhamaLog)

Baseado em: USID_039 (Visualizar), USID_040 (Contratar), USID_041 (Alterar), USID_042 (Cancelar),
USID_043 (Reembolsar), SSID_016 (Manter Assinatura) e SSID_018 (Integração de Pagamento) —
texto completo lido do `LhamaLog_casos_de_uso.xlsx`.

**Revisão aplicada** (autoauditoria linha a linha contra o texto original): removidas 2 chamadas
que não estavam em nenhum caso de uso (`calcularValorProporcional()` no diagrama 3,
`validarTransicaoDeStatus()` no diagrama 6 — ambas são métodos do modelo de classes antigo, mas
não aparecem descritos nestes fluxos específicos); corrigida 1 seta que fazia o Usuário falar
direto com o Gateway quando o texto diz que é o sistema quem direciona (diagrama 3); e removida
1 marcação `[PENDENTE]` usada errado (não era requisito em aberto, era um princípio já discutido
em outro momento da conversa, fora do escopo deste caso de uso).

**Participantes usados em todos os diagramas:**
- `Usuario` — ator humano (USID_039–043)
- `GerenciadorAssinatura` — orquestra o ciclo de vida da assinatura
- `ProcessamentoPagamento` — processa cobrança/eventos de pagamento
- `GatewayPagamento` — representa ao mesmo tempo a interface conceitual do gateway **e** a fronteira
  com o ator externo "Sistema Terceiro de Assinatura/Pagamento" / "Gateway de Pagamento" — nenhum
  provedor foi escolhido, por isso ele nunca aparece com comportamento interno concreto, só como
  fronteira de troca de mensagens.

Tudo marcado `[PENDENTE]` é requisito ainda sem definição — não foi assumido nenhum valor, regra
de gateway, moeda, periodicidade, imposto, proration ou política de reembolso.

---

## 1. Visualização (USID_039)

```mermaid
sequenceDiagram
    actor Usuario
    participant GerenciadorAssinatura
    participant GatewayPagamento

    Usuario->>GerenciadorAssinatura: acessa interface de assinaturas/planos
    GerenciadorAssinatura-->>Usuario: lista de planos (nome, valor, caracteristicas, beneficios) [PROPOSTO - dados da tabela de monetizacao]
    Usuario->>GerenciadorAssinatura: seleciona plano para consultar mais informacoes
    GerenciadorAssinatura-->>Usuario: detalhes do plano selecionado
    Usuario->>GerenciadorAssinatura: seleciona a opcao para realizar a assinatura
    GerenciadorAssinatura->>GatewayPagamento: direciona para o sistema terceiro (interface)

    alt FA-01: nenhum plano disponivel
        GerenciadorAssinatura-->>Usuario: "nao ha planos disponiveis no momento"
    else FA-02: falha ao carregar planos
        GerenciadorAssinatura-->>Usuario: "falha ao carregar, tente novamente"
    else FA-03: sistema terceiro indisponivel
        GatewayPagamento-->>GerenciadorAssinatura: sem resposta / indisponivel
        GerenciadorAssinatura-->>Usuario: "assinatura nao pode ser iniciada agora"
    end
```

## 2. Contratação (USID_040)

```mermaid
sequenceDiagram
    actor Usuario
    participant GerenciadorAssinatura
    participant GatewayPagamento
    participant ProcessamentoPagamento

    Usuario->>GatewayPagamento: confere dados do plano (valor, condicoes)
    Usuario->>GatewayPagamento: informa/adiciona forma de pagamento
    GatewayPagamento-->>GatewayPagamento: recebe e valida dados da forma de pagamento
    Usuario->>GatewayPagamento: confirma contratacao e pagamento
    GatewayPagamento-->>GatewayPagamento: processa transacao [PENDENTE - moeda, impostos nao definidos]
    GatewayPagamento->>ProcessamentoPagamento: evento de pagamento confirmado (SSID_018)
    ProcessamentoPagamento->>ProcessamentoPagamento: recebe e valida os dados do evento
    ProcessamentoPagamento->>GerenciadorAssinatura: aplicarEventoDeAssinatura(PRIMEIRA_COMPRA)
    GerenciadorAssinatura-->>GerenciadorAssinatura: registra a assinatura contratada
    GerenciadorAssinatura-->>Usuario: confirmacao de que a assinatura foi realizada

    alt FA-01: forma de pagamento invalida
        GatewayPagamento-->>Usuario: dados invalidos, solicita correcao
    else FA-02: pagamento nao autorizado
        GatewayPagamento-->>Usuario: pagamento nao aprovado, tentar novamente ou trocar forma de pagamento
    else FA-03: usuario cancela antes da confirmacao do pagamento
        Usuario->>GatewayPagamento: interrompe o processo
        GatewayPagamento-->>GatewayPagamento: nenhuma assinatura e efetivada
    else FA-04: sistema terceiro indisponivel (ao solicitar contratacao)
        GerenciadorAssinatura-->>Usuario: "nao foi possivel iniciar a contratacao, tente depois"
    else FA-05: falha na confirmacao apos pagamento processado
        GerenciadorAssinatura-->>Usuario: "confirmacao nao pode ser concluida agora" (processo fica pendente)
    end
```

## 3. Alteração / Upgrade (USID_041)

```mermaid
sequenceDiagram
    actor Usuario
    participant GerenciadorAssinatura
    participant GatewayPagamento
    participant ProcessamentoPagamento

    Usuario->>GerenciadorAssinatura: acessa area de gerenciamento da assinatura
    GerenciadorAssinatura-->>Usuario: informacoes da assinatura atual
    Usuario->>GerenciadorAssinatura: seleciona a opcao de alteracao
    GerenciadorAssinatura-->>Usuario: opcoes disponiveis (upgrade ou cancelamento)
    Usuario->>GerenciadorAssinatura: seleciona a opcao de upgrade
    GerenciadorAssinatura-->>Usuario: planos disponiveis para alteracao
    Usuario->>GerenciadorAssinatura: seleciona o novo plano desejado
    GerenciadorAssinatura->>GatewayPagamento: direciona a solicitacao ao sistema terceiro (interface)
    Usuario->>GerenciadorAssinatura: confirma a alteracao para o novo plano
    GerenciadorAssinatura->>GatewayPagamento: encaminha confirmacao
    GatewayPagamento->>ProcessamentoPagamento: evento de alteracao processada
    ProcessamentoPagamento->>GerenciadorAssinatura: aplicarEventoDeAssinatura(UPGRADE_DOWNGRADE)
    GerenciadorAssinatura-->>Usuario: nova condicao da assinatura apos confirmacao do terceiro

    alt FA-02: desistencia antes de confirmar upgrade ou cancelamento
        GerenciadorAssinatura-->>Usuario: mantem assinatura atual, sem modificacoes
    else FA-03: falha ao realizar upgrade
        GerenciadorAssinatura-->>Usuario: "nao foi possivel realizar o upgrade, assinatura mantida"
    else FA-05: sistema terceiro indisponivel
        GerenciadorAssinatura-->>Usuario: "alteracao nao pode ser realizada agora"
    end

    Note over GerenciadorAssinatura,GatewayPagamento: FA-01 e FA-04 (cancelamento a partir desta tela)<br/>repetem o mesmo fluxo do diagrama 4 - USID_041 descreve<br/>o cancelamento de novo dentro do proprio caso de uso
```

**Nota sobre este diagrama:** a versão anterior tinha um passo `calcularValorProporcional()`
aqui. Removido — a USID_041 não menciona cálculo de valor proporcional em nenhum lugar do texto.
O método existe no modelo de classes (herdado do diagrama antigo), mas incluí-lo neste fluxo
seria afirmar algo que o caso de uso não descreve. Fica como gap conhecido, não como passo do
diagrama: **proration continua sem nenhuma descrição de quando/como é calculado.**

## 4. Cancelamento (USID_042) — com cancelamento programado

```mermaid
sequenceDiagram
    actor Usuario
    participant GerenciadorAssinatura
    participant GatewayPagamento
    participant ProcessamentoPagamento

    Usuario->>GerenciadorAssinatura: acessa area de gerenciamento da assinatura
    GerenciadorAssinatura-->>Usuario: informacoes da assinatura atual
    Usuario->>GerenciadorAssinatura: seleciona a opcao de cancelamento
    GerenciadorAssinatura-->>Usuario: informacoes e condicoes do cancelamento
    Usuario->>GerenciadorAssinatura: confirma a solicitacao de cancelamento
    GerenciadorAssinatura->>GatewayPagamento: encaminha a solicitacao (interface)
    GatewayPagamento->>ProcessamentoPagamento: confirmacao do cancelamento
    ProcessamentoPagamento->>GerenciadorAssinatura: aplicarEventoDeAssinatura(CANCELAMENTO)
    GerenciadorAssinatura-->>GerenciadorAssinatura: status = CANCELAMENTO_AGENDADO (mantem vigenciaAte)
    GerenciadorAssinatura-->>Usuario: "assinatura permanecera valida ate o termino do periodo contratado"

    Note over GerenciadorAssinatura: ao final do periodo contratado (evento agendado, fora deste diagrama)
    GerenciadorAssinatura-->>GerenciadorAssinatura: status = CANCELADA
    GerenciadorAssinatura->>GerenciadorAssinatura: desativa produtos e funcionalidades vinculados [dependencia externa - modulo Sistema/Produto]

    alt FA-01: desistencia antes de confirmar
        GerenciadorAssinatura-->>Usuario: mantem assinatura ativa, sem alteracoes
    else FA-02: falha no processamento do cancelamento
        GerenciadorAssinatura-->>Usuario: "nao foi possivel concluir, assinatura mantida ativa"
    else FA-03: sistema terceiro indisponivel
        GerenciadorAssinatura-->>Usuario: "solicitacao nao pode ser processada agora"
    else FA-04: assinatura ja tem cancelamento programado
        GerenciadorAssinatura-->>Usuario: informa que ja esta cancelada + data prevista de encerramento
    else FA-05: falha ao desativar produtos apos o fim da vigencia
        GerenciadorAssinatura-->>GerenciadorAssinatura: identifica a falha, registra ocorrencia para tratamento, mantem status encerrada [PENDENTE - como essa ocorrencia e tratada depois nao esta definido]
    end
```

## 5. Reembolso (USID_043)

```mermaid
sequenceDiagram
    actor Usuario
    participant GerenciadorAssinatura
    participant GatewayPagamento
    participant ProcessamentoPagamento

    Usuario->>GerenciadorAssinatura: acessa area de gerenciamento da assinatura
    GerenciadorAssinatura-->>Usuario: informacoes da assinatura contratada
    Usuario->>GerenciadorAssinatura: seleciona a opcao de solicitar reembolso
    GerenciadorAssinatura-->>Usuario: informacoes e condicoes necessarias
    Usuario->>GerenciadorAssinatura: informa o motivo da solicitacao
    GerenciadorAssinatura-->>GerenciadorAssinatura: registra as informacoes fornecidas
    Usuario->>GerenciadorAssinatura: confirma a solicitacao de reembolso
    GerenciadorAssinatura->>GerenciadorAssinatura: avalia elegibilidade [PENDENTE - criterio de elegibilidade nao definido]
    GerenciadorAssinatura->>GatewayPagamento: encaminha a solicitacao ao sistema terceiro (interface)
    GatewayPagamento->>ProcessamentoPagamento: retorno do pedido [PENDENTE - politica de reembolso do terceiro]
    ProcessamentoPagamento-->>GerenciadorAssinatura: atualiza status do Reembolso
    GerenciadorAssinatura-->>Usuario: status retornado (aprovado / recusado / em analise)

    alt FA-01: desistencia antes de confirmar
        GerenciadorAssinatura-->>Usuario: mantem assinatura sem alteracoes
    else FA-02: assinatura nao elegivel
        GerenciadorAssinatura-->>Usuario: "nao esta elegivel", motivo quando disponivel [PENDENTE - criterio]
    else FA-03: reembolso recusado
        GerenciadorAssinatura-->>Usuario: status recusado + motivo, quando disponivel
    else FA-04: sistema terceiro indisponivel
        GerenciadorAssinatura-->>Usuario: "nao foi possivel encaminhar agora"
    else FA-05: consulta antes da analise terminar
        GerenciadorAssinatura-->>Usuario: status pendente / em analise
    end
```

## 6. Eventos externos do Gateway (SSID_016 + SSID_018)

```mermaid
sequenceDiagram
    actor GatewayExterno as Gateway de Pagamento
    participant GatewayPagamento
    participant ProcessamentoPagamento
    participant GerenciadorAssinatura

    GatewayExterno->>GatewayPagamento: envia evento relacionado a uma assinatura
    GatewayPagamento->>ProcessamentoPagamento: encaminha o evento (EventoGateway)
    ProcessamentoPagamento->>ProcessamentoPagamento: recebe e valida os dados enviados

    alt dados validos
        ProcessamentoPagamento->>GerenciadorAssinatura: identifica o usuario e a assinatura relacionados ao evento
        ProcessamentoPagamento->>ProcessamentoPagamento: identifica/processa o tipo de operacao recebida
        ProcessamentoPagamento->>GerenciadorAssinatura: aplicarEventoDeAssinatura(tipoOperacao)
        GerenciadorAssinatura-->>GerenciadorAssinatura: atualiza a assinatura conforme a operacao realizada
        GerenciadorAssinatura-->>ProcessamentoPagamento: novo status registrado
        ProcessamentoPagamento-->>ProcessamentoPagamento: registra o resultado da operacao
    else FA-07: dados incompletos, invalidos ou assinatura nao identificada
        ProcessamentoPagamento-->>ProcessamentoPagamento: nao realiza alteracao, registra a falha, mantem estado atual
    else FA-06: pagamento recusado
        ProcessamentoPagamento-->>ProcessamentoPagamento: mantem estado anterior ou atualiza conforme regra de pagamento [PENDENTE - qual das duas nao esta definido], registra ocorrencia
    else FA-01: pagamento em atraso
        ProcessamentoPagamento-->>GerenciadorAssinatura: atualiza status conforme regra de atraso [PENDENTE - regra de atraso nao definida]
    else FA-05 / FA-08: falha na integracao ou gateway indisponivel
        ProcessamentoPagamento-->>ProcessamentoPagamento: mantem ultimo estado valido, registra a indisponibilidade
    end
```

**Nota sobre este diagrama:** a versão anterior tinha um passo `validarTransicaoDeStatus()` aqui.
Removido pelo mesmo motivo do diagrama 3 — é um método privado do modelo de classes, mas nenhuma
das duas SSIDs descreve essa validação explicitamente. Também separei os fluxos alternativos
FA-01 e FA-06 (que antes estavam agrupados) porque o texto os trata como casos distintos: atraso
tem regra própria ainda não definida, pagamento recusado tem uma ambiguidade textual própria
("mantém OU atualiza" — o texto não diz qual dos dois).

---

## Notas obrigatórias (não inventar / pendências)

- **`[CONFLITO]` SSID_016 e SSID_018 continuam mescladas no diagrama 6** — descrevem quase o
  mesmo fluxo em granularidade ligeiramente diferente; sobreposição ainda sem resolução do time.
- **`[RISCO]` Duplicidade e ordem de eventos**: nenhum dos 6 diagramas define o que acontece se
  dois eventos da mesma assinatura chegarem fora de ordem ou repetidos.
- **`[GAP]` Proration** (upgrade/downgrade, diagrama 3): a USID_041 não descreve quando ou como
  o valor proporcional é calculado — não modelado como passo, só citado como lacuna.
- **`[PENDENTE]` Cancelamento programado → falha ao desativar produtos** (diagrama 4): o texto só
  diz "registra a ocorrência para tratamento" — não define reprocessamento nem alerta.
- **`[PENDENTE]` FA-06 de SSID_016** (diagrama 6): o texto diz "mantém a assinatura no estado
  anterior OU atualiza seu status" — ambíguo de propósito no original, não resolvi a ambiguidade.
- Gateway concreto, moeda, periodicidade, impostos, proration e política de reembolso **não foram
  assumidos em nenhum dos 6 diagramas**.

**Rastreabilidade:** USID_039–043, SSID_016, SSID_018 — todos os 6 diagramas cruzados linha a
linha com o texto completo das páginas originais do `LhamaLog_casos_de_uso.xlsx`.
