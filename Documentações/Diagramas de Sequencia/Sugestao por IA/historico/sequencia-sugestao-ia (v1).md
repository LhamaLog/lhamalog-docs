# Diagramas de Sequência — Sugestão por IA (LhamaLog)

> **Versão 1 (Out 03, 2026, Michel Bocchi Junior)** — LLT-64. Pasta nova, sem versão anterior. Regra de versionamento
> do LhamaLog: a versão atual fica nesta pasta com os nomes oficiais (sem sufixo `_v2`) e, quando houver uma nova versão,
> a anterior é movida sem alteração para a subpasta `v1` desta pasta.

Baseado em: decisões do Michel de Out 03, 2026, registradas nas novas ADRs (pasta `Documentações > Diagrama ADR`):
- **ADR_035** — Ocorrência concreta e vínculo de 1 Ocorrência para N Sugestões (altera/complementa a ADR_020) —
  https://docs.google.com/document/d/1VHD4bazA8HDPH5feZ4NK8KUQYIBXa77eMYjtm2Ea0V8/edit
- **ADR_036** — Gatilho da Sugestão: automático por plano e manual com fila de menor prioridade (altera/complementa a
  ADR_035, a ADR_020 e a ADR_018) — https://docs.google.com/document/d/18eIcWPN4y_AhtXlqLXkRACiZgpRBRgU_XH50B6fua3M/edit
- **ADR_037** — Falhas na geração da Sugestão: aviso na notificação, retry e estado FALHA (altera/complementa a ADR_036) —
  https://docs.google.com/document/d/1VW_brVCsw2zMWVx9omG5y4mCQUi6Jk58XMXZdTvSs4I/edit
- **ADR_038** — Consumo de créditos/tokens da Sugestão por reserva (altera/complementa a ADR_036 e a ADR_018) —
  https://docs.google.com/document/d/1FKLLDLOF9dJCpUFlTt4_Tbc3Ya_xVe2A1ve9kUG7ZNc/edit
- **ADR_039** — Avaliação das Sugestões, realimentação do contexto e GatewayLLMSugestao (altera/complementa a ADR_018 e
  a ADR_020) — https://docs.google.com/document/d/1wMGFV1c3OihOsC_AEsq4inbLN3g-2nE9kONcCG-URLo/edit

Também usados: ADR_011/017 (Finder), ADR_018 (GatewayLLM exclusivo do Finder), ADR_019 (Tipo ERRO/WARNING/SPAM),
ADR_020 (Ocorrência-resumo por Arquivo), Modelo de Classes (abas `Sugestao`, `ContextoSugestao`, `GatewayLLM`,
`RespostaLLM`, `SaldoTokens`, `Plano`, `Notificação`), DER v2 (`Levantamento de Entidades DER`) e os diagramas de
Notificação do Pedro (`sequencia-notificacao.md` e PNGs da pasta `Notificação`). O Modelo de Classes, o DER e os
arquivos do Pedro **não foram alterados**; os impactos estão nas seções finais.

**Visão geral do fluxo:** cada erro ou warning que o Finder encontra num Arquivo vira uma **Ocorrência concreta**
(documento próprio no MongoDB); o resumo por Arquivo só agrupa as N Ocorrências e o spam não gera Ocorrência
(ADR_035). A Sugestão pertence a **uma** Ocorrência e pode ser gerada de dois jeitos (ADR_036):
- **automática** — se o plano do cliente tem o recurso de Sugestão, a criação da Ocorrência dispara a Sugestão, o fluxo
  espera a resposta e envia **Ocorrência + Sugestão** juntas ao módulo de Notificação (**diagrama 1**);
- **manual** — o usuário pede, na tela da Ocorrência, quantas Sugestões quiser; o pedido entra numa fila de **menor
  prioridade**, é processado de forma assíncrona e **não** vai nas notificações (**diagrama 2**).

Nos dois caminhos o consumo de tokens é **reservado antes** da chamada à IA e **efetivado** com o consumo oficial da
resposta (ADR_038); a IA é chamada pela integração própria **GatewayLLMSugestao** (ADR_039), separada do GatewayLLM do
Finder (ADR_018). O prompt usa ContextoEmpresa, ContextoProduto, os dados da Ocorrência (tipo, gravidade, linha) e,
no manual, as avaliações das Sugestões anteriores da mesma Ocorrência.

**Participantes usados:**
- `Modulo de Ocorrencia` — cria a Ocorrência concreta, consulta o plano, dispara a Sugestão automática, espera a resposta
  e entrega a Ocorrência (com ou sem Sugestão) ao módulo de Notificação (ADR_035/036)
- `Assinatura / Plano` — diz se o plano tem o recurso de Sugestão (`Plano.recursoIA` do DER ou novo item no enum
  `RecursosAnaliseIA` `[PENDENTE]`)
- `Modulo de Sugestao` / `Modulo de Sugestao (API)` — cria e grava a `Sugestao`, recebe os pedidos manuais, as
  avaliações e o fechamento
- `FilaSugestaoManual (baixa prioridade)` — fila dos pedidos manuais, com prioridade menor que o fluxo automático
  (tecnologia `[PENDENTE]`)
- `WorkerSugestao` — consome a fila quando o módulo tem vazão, faz a reserva, monta o contexto, chama a IA e trata o retry
- `Creditos (SaldoTokens / Transacao)` — reserva, efetivação/ajuste e liberação do consumo (ADR_038); unificação de
  `SaldoTokens` com o módulo Créditos `[PENDENTE]`
- `ContextoSugestao` — `montarPrompt()` com ContextoEmpresa, ContextoProduto, dados da Ocorrência e avaliações anteriores
- `GatewayLLMSugestao` — `solicitar(prompt): RespostaLLM(conteudo, tokens_consumidos)`; nome novo para a interface
  `GatewayLLM` do módulo Sugestão (ADR_018/039)
- `LLM externa` — provedor e modelo `[PENDENTE]`
- `MongoDB (Ocorrencia / Sugestao / AvaliacaoSugestao)` — coleções `Ocorrencia`, `Sugestao` e `AvaliacaoSugestao`
- `Modulo de Notificacao` — o módulo do Pedro (`PreferenciaNotificacao`, `Notificacao`, `Servico de Notificacoes`)
- `Usuario (equipe tecnica do cliente)` e `Front Web / App` — só no diagrama 2

Tudo marcado `[PENDENTE]` é requisito ainda sem definição; `[INFERIDO]` é ligação feita por mim a partir das decisões do
Michel e dos artefatos, que não está dita literalmente por ele.

**Atenção, risco de confusão de nomes:** o status `FALHA` da Sugestão (`[INFERIDO]`, ADR_037) **não é** o
`FALHA` de `TentativaEntrega` / `StatusEnvioNotificacao` do módulo de Notificação (falha de entrega de uma notificação).
E o valor de enum `"PENDENTE"` da Notificação continua sem relação com a marcação `[PENDENTE]`.

---

## 1. Sugestão automática (ADR_035–039)

Arquivo: `sugestao_automatica.png`

**Resumo do fluxo:** o Módulo de Ocorrência grava a Ocorrência concreta, confere no plano se o recurso de Sugestão está
ativo e dispara a Sugestão automática, aguardando a resposta `[INFERIDO — síncrono do ponto de vista da Ocorrência,
confirmar com Michel]`. O Módulo de Sugestão cria o registro (`PROCESSANDO`, origem `AUTOMATICA`), reserva a prévia de
tokens, monta o contexto, chama a LLM pela GatewayLLMSugestao, efetiva o consumo oficial, grava a Sugestão
`DISPONIVEL` e devolve. O Módulo de Ocorrência envia Ocorrência + Sugestão ao módulo de Notificação, que distribui pelos
canais habilitados.

**Fluxo principal:**
1. Ocorrência concreta gravada (tipo, gravidade, linha, conteúdo, arquivoId) e vinculada ao resumo por Arquivo; spam não chega aqui.
2. Consulta ao plano: recurso de Sugestão ativo.
3. Dispara a Sugestão automática e aguarda; o Módulo de Sugestão cria a `Sugestao` (`PROCESSANDO`, `AUTOMATICA`).
4. Calcula a prévia X e reserva X tokens como valor em aberto / a haver.
5. `montarPrompt()` com ContextoEmpresa, ContextoProduto e dados da Ocorrência (mascaramento `[PENDENTE]`).
6. `GatewayLLMSugestao.solicitar(prompt)` → LLM → `RespostaLLM(conteudo, tokens_consumidos)`.
7. Efetiva o consumo oficial e ajusta a diferença da reserva; grava a Sugestão `DISPONIVEL`.
8. Ocorrência + Sugestão vão ao módulo de Notificação → `possuiCanalHabilitado` → `Notificacao` → Serviço de Notificações.

**Fluxos alternativos:**
- **FA-01 plano sem o recurso:** não enfileira Sugestão nem reserva créditos; a Ocorrência segue sozinha para a notificação.
- **FA-02 saldo insuficiente:** a reserva é recusada e a IA não é chamada; a Ocorrência segue sem Sugestão. Se o registro
  vira `FALHA` ou nem é criado, e se a notificação leva um aviso de saldo, está `[PENDENTE]`.
- **FA-03 falha da LLM (erro, timeout ou resposta inválida):** libera a reserva `[INFERIDO]`, Sugestão `FALHA`
  `[INFERIDO]` e a notificação sai mesmo assim com a mensagem **"Não foi possível criar uma sugestão"** (ADR_037).
  Timeout e retry no automático `[PENDENTE]`.

```mermaid
sequenceDiagram
    participant ModOcorr as Modulo de Ocorrencia
    participant Assin as Assinatura / Plano
    participant ModSug as Modulo de Sugestao
    participant Creditos as Creditos (SaldoTokens / Transacao)
    participant Ctx as ContextoSugestao
    participant Gw as GatewayLLMSugestao
    participant LLM as LLM externa
    participant Mongo as MongoDB (Ocorrencia / Sugestao)
    participant ModNotif as Modulo de Notificacao

    Note over ModOcorr,Mongo: o Finder classificou o Arquivo (ADR_011/017) -- cada erro ou warning vira uma Ocorrencia<br/>concreta, e spam nao gera Ocorrencia nem Sugestao (ADR_035)
    ModOcorr->>Mongo: grava a Ocorrencia concreta (tipo, gravidade, linha,<br/>conteudo, arquivoId) e vincula ao resumo por Arquivo<br/>(ADR_035)
    ModOcorr->>Assin: o plano do cliente tem o recurso de Sugestao? [PENDENTE -<br/>Plano.recursoIA ou item SUGESTAO no enum RecursosAnaliseIA]
    Assin-->>ModOcorr: recurso de Sugestao ativo
    ModOcorr->>ModSug: dispara a Sugestao automatica (ocorrenciaId) e aguarda a<br/>resposta [INFERIDO - sincrono do ponto de vista da<br/>Ocorrencia, confirmar com Michel]
    ModSug->>Mongo: cria a Sugestao (ocorrenciaId, origem AUTOMATICA, status<br/>PROCESSANDO) [INFERIDO - campo origem]
    ModSug->>ModSug: calcula a previa de consumo X (dados da Ocorrencia + teto de<br/>resposta) [PENDENTE - formula e margem de erro]
    ModSug->>Creditos: reserva X tokens e debita do saldo como valor em aberto / a<br/>haver (ADR_038)
    Creditos-->>ModSug: reserva registrada (saldo disponivel = saldo - reservas em<br/>aberto)
    ModSug->>Ctx: montarPrompt(): ContextoEmpresa, ContextoProduto e dados da<br/>Ocorrencia (tipo, gravidade, linha, conteudo) (ADR_039)
    Note over ModSug,Ctx: mascaramento de dados sensiveis antes do envio a LLM [PENDENTE - nao definido, ADR_039]
    Ctx-->>ModSug: prompt
    ModSug->>Gw: solicitar(prompt)
    Gw->>LLM: envia o prompt [PENDENTE - provedor e modelo]
    LLM-->>Gw: texto da sugestao + consumo oficial de tokens
    Gw-->>ModSug: RespostaLLM(conteudo, tokens_consumidos)
    ModSug->>Creditos: efetiva o consumo oficial e ajusta a diferenca da reserva<br/>(devolve ou cobra)
    ModSug->>Mongo: grava a Sugestao (conteudo, tokensConsumidos, status<br/>DISPONIVEL, dataConclusao)
    ModSug-->>ModOcorr: Sugestao gerada pela IA
    ModOcorr->>ModNotif: envia Ocorrencia + Sugestao (ocorrenciaId, sugestaoId)<br/>[divergencia: o construtor Notificacao do Pedro nao recebe<br/>sugestao_id]
    ModNotif->>ModNotif: possuiCanalHabilitado por<br/>destinatario e cria a Notificacao<br/>(diagrama gerar_notificacao<br/>do Pedro)
    ModNotif->>ModNotif: enfileira no Servico de<br/>Notificacoes (EMAIL / PUSH / WEB)<br/>[PENDENTE - provedor, retries<br/>e templates]

    alt FA-01: plano sem o recurso de Sugestao
        Assin-->>ModOcorr: recurso de Sugestao inativo
        ModOcorr->>ModNotif: envia so a Ocorrencia -- nenhuma Sugestao enfileirada e<br/>nenhuma reserva de creditos
    else FA-02: saldo insuficiente para a reserva
        Creditos-->>ModSug: saldo insuficiente -- reserva recusada, a IA nao e chamada
        ModSug->>Mongo: Sugestao nao gerada [PENDENTE - marcar FALHA (saldo<br/>insuficiente) ou nem criar o registro]
        ModSug-->>ModOcorr: sem Sugestao
        ModOcorr->>ModNotif: envia so a Ocorrencia [PENDENTE - incluir aviso de saldo<br/>insuficiente na notificacao]
    else FA-03: falha da LLM (erro, timeout ou resposta invalida)
        Gw-->>ModSug: erro ou timeout [PENDENTE - valor do timeout e retry no<br/>automatico]
        ModSug->>Creditos: libera a reserva -- o valor em aberto volta ao saldo<br/>[INFERIDO]
        ModSug->>Mongo: Sugestao status FALHA [INFERIDO - novo estado, ADR_037]
        ModSug-->>ModOcorr: falha na geracao da Sugestao
        ModOcorr->>ModNotif: envia a Ocorrencia + mensagem "Nao foi possivel criar uma<br/>sugestao" (ADR_037)
    end

    Note over ModOcorr,ModNotif: a notificacao nunca deixa de sair por causa da Sugestao (ADR_036/037)<br/>a reserva vem antes de montar o contexto -- se a previa depender do prompt montado, a reserva<br/>passa para logo apos o montarPrompt() [INFERIDO]
```

**Notas sobre este diagrama:**
- A ordem "verifica plano → reserva créditos → monta contexto" segue o pedido. Se a prévia precisar do prompt montado
  (ADR_038), a reserva passa para logo depois do `montarPrompt()` `[INFERIDO]`; o efeito é o mesmo: nada é enviado à
  LLM sem reserva.
- O Michel disse "assíncrono" nos dois trechos da transcrição de voz. Aqui o automático está como **síncrono do ponto de
  vista da Ocorrência** (a notificação espera a Sugestão) `[INFERIDO — confirmar com Michel]`. Na implementação, ele
  pode rodar numa fila de alta prioridade com o fluxo da Ocorrência aguardando o resultado `[INFERIDO]`.
- A criação do registro `Sugestao` antes da reserva permite ligar a reserva à Sugestão (`sugestaoId`) `[INFERIDO]`.
- Os dois passos internos do `Modulo de Notificacao` resumem o diagrama `gerar_notificacao.png` do Pedro, sem alterá-lo.

---

## 2. Sugestão manual, falha com retry e avaliação (ADR_035–039)

Arquivo: `sugestao_manual.png`

**Resumo do fluxo:** o usuário pede uma Sugestão na tela da Ocorrência (pode pedir várias). O backend cria o registro na
coleção `Sugestao` com status `PROCESSANDO` (origem `MANUAL`), coloca o pedido na fila de **menor prioridade** e responde
na hora. Quando o módulo tem vazão, o worker reserva os tokens, busca as Sugestões anteriores da mesma Ocorrência com as
avaliações, monta o contexto, chama a LLM, efetiva o consumo e grava a Sugestão `DISPONIVEL`; só então ela aparece na
listagem do front. A Sugestão manual **não** vai nas notificações.

**Fluxo principal:**
1. Usuário pede a Sugestão; o front chama o Módulo de Sugestão (rota `[PENDENTE]`).
2. Valida a Ocorrência do tenant e cria a `Sugestao` (`MANUAL`, `PROCESSANDO`, `tentativas = 0` `[INFERIDO]`).
3. Enfileira na `FilaSugestaoManual` (prioridade menor que a automática) e responde "pedido aceito" `[INFERIDO — 202]`.
4. O `WorkerSugestao` consome quando há vazão, calcula a prévia e reserva X tokens.
5. Busca as Sugestões anteriores da mesma Ocorrência e as `AvaliacaoSugestao`, e monta o prompt pedindo para não repetir
   o que foi mal avaliado (ADR_039).
6. `GatewayLLMSugestao` → LLM → `RespostaLLM`; efetiva o consumo e grava a Sugestão `DISPONIVEL`.
7. O front lista as Sugestões da Ocorrência (atualização por polling, WebSocket ou evento `[PENDENTE]`); as `PROCESSANDO`
   não aparecem.

**Fluxos alternativos e opcionais:**
- **FA-01 falha na geração:** libera a reserva `[INFERIDO]` e tenta de novo pela fila de baixa prioridade até N
  tentativas (N e backoff `[PENDENTE]`). Esgotadas, a Sugestão vai para `FALHA` `[INFERIDO]` e o módulo de Notificação
  envia **push no site e no aplicativo**: "Não foi possível criar a sugestão solicitada" (ADR_037).
- **FA-02 saldo insuficiente:** reserva recusada, sem retry; comportamento exato `[PENDENTE]` (recusar já no pedido ou
  marcar `FALHA` e avisar).
- **opt avaliação e fechamento:** a equipe técnica do cliente abre a Sugestão, vê se foi finalizada, quanto resolveu e o
  que trouxe, e avalia com estrelas e comentário; cada avaliação vira uma `AvaliacaoSugestao` `[INFERIDO]` e a Sugestão
  fica `AVALIADA`. Depois pode ser fechada (`FECHADA`; significado `[PENDENTE]`). As avaliações realimentam o contexto
  das próximas Sugestões da mesma Ocorrência.

```mermaid
sequenceDiagram
    actor Usuario as Usuario (equipe tecnica do cliente)
    participant Front as Front Web / App
    participant ModSug as Modulo de Sugestao (API)
    participant Fila as FilaSugestaoManual (baixa prioridade)
    participant Worker as WorkerSugestao
    participant Creditos as Creditos (SaldoTokens / Transacao)
    participant Ctx as ContextoSugestao
    participant Gw as GatewayLLMSugestao
    participant LLM as LLM externa
    participant Mongo as MongoDB (Ocorrencia / Sugestao / AvaliacaoSugestao)
    participant ModNotif as Modulo de Notificacao

    Usuario->>Front: abre uma Ocorrencia e pede uma Sugestao (pode pedir varias<br/>para a mesma Ocorrencia)
    Front->>ModSug: solicita a Sugestao manual (ocorrenciaId) [PENDENTE - rota<br/>da API]
    ModSug->>Mongo: valida a Ocorrencia do tenant e cria a Sugestao (origem<br/>MANUAL, status PROCESSANDO, tentativas 0) [INFERIDO - campos<br/>origem e tentativas]
    ModSug->>Fila: enfileira o pedido (sugestaoId) com prioridade MENOR que o<br/>fluxo automatico (ADR_036)
    ModSug-->>Front: pedido aceito [INFERIDO - 202 Accepted]
    Front-->>Usuario: avisa que a Sugestao esta sendo gerada -- ela ainda nao<br/>aparece na listagem
    Note over Usuario,Fila: assincrono via fila de baixa prioridade [INFERIDO - confirmar com Michel]<br/>a Sugestao manual NAO vai nas notificacoes (ADR_036)

    Worker->>Fila: consome o proximo pedido quando o modulo tem vazao (as<br/>automaticas tem prioridade)
    Fila-->>Worker: sugestaoId
    Worker->>Worker: calcula a previa de consumo X [PENDENTE - formula e margem<br/>de erro]
    Worker->>Creditos: reserva X tokens e debita do saldo como valor em aberto / a<br/>haver (ADR_038)
    Creditos-->>Worker: reserva registrada
    Worker->>Mongo: busca as Sugestoes anteriores da mesma Ocorrencia e as<br/>AvaliacaoSugestao (notas e comentarios)
    Mongo-->>Worker: historico avaliado [PENDENTE - quantas entram no contexto]
    Worker->>Ctx: montarPrompt(): ContextoEmpresa, ContextoProduto, dados da<br/>Ocorrencia e avaliacoes anteriores -- nao repetir o que foi<br/>mal avaliado (ADR_039)
    Note over Worker,Ctx: mascaramento de dados sensiveis antes do envio a LLM [PENDENTE - nao definido, ADR_039]
    Ctx-->>Worker: prompt
    Worker->>Gw: solicitar(prompt)
    Gw->>LLM: envia o prompt [PENDENTE - provedor e modelo]
    LLM-->>Gw: texto da sugestao + consumo oficial de tokens
    Gw-->>Worker: RespostaLLM(conteudo, tokens_consumidos)
    Worker->>Creditos: efetiva o consumo oficial e ajusta a diferenca da reserva
    Worker->>Mongo: grava a Sugestao (conteudo, tokensConsumidos, status<br/>DISPONIVEL, dataConclusao)
    Front->>ModSug: lista as Sugestoes da Ocorrencia [PENDENTE - polling,<br/>WebSocket ou evento para atualizar a tela]
    ModSug-->>Front: Sugestoes DISPONIVEL (as que estao PROCESSANDO nao aparecem)
    Front-->>Usuario: mostra a nova Sugestao na listagem da Ocorrencia

    alt FA-01: falha na geracao (erro, timeout ou resposta invalida da LLM)
        Gw-->>Worker: erro ou timeout
        Worker->>Creditos: libera a reserva -- o valor em aberto volta ao saldo<br/>[INFERIDO]
        loop retry ate N tentativas [PENDENTE - N e intervalo / backoff]
            Worker->>Mongo: incrementa tentativas da Sugestao [INFERIDO]
            Worker->>Fila: reenfileira o pedido com baixa prioridade e tenta de novo
        end
        Worker->>Mongo: tentativas esgotadas -- Sugestao status FALHA [INFERIDO -<br/>novo estado, ADR_037]
        Worker->>ModNotif: pede o aviso de falha para o usuario que solicitou<br/>(sugestaoId, usuarioId) [divergencia: nao existe nos<br/>diagramas do Pedro]
        ModNotif-->>Front: push no site e no aplicativo: "Nao foi possivel criar a<br/>sugestao solicitada"
        Front-->>Usuario: exibe o aviso de falha
    else FA-02: saldo insuficiente para a reserva
        Creditos-->>Worker: saldo insuficiente -- reserva recusada, sem retry
        Worker->>Mongo: Sugestao nao gerada [PENDENTE - comportamento exato: recusar<br/>ja no pedido ou marcar FALHA e avisar]
    end

    opt avaliacao pela equipe tecnica e fechamento (ADR_039)
        Usuario->>Front: abre a Sugestao e ve se foi finalizada, quanto resolveu e o<br/>que trouxe
        Usuario->>Front: avalia com estrelas e comentario (ex.: "ja foi tentada e nao<br/>deu certo" = nota baixa)
        Front->>ModSug: envia a avaliacao (sugestaoId, nota, comentario) [PENDENTE -<br/>escala e quem pode avaliar]
        ModSug->>Mongo: cria AvaliacaoSugestao (autor, nota, comentario, criadaEm) e<br/>Sugestao status AVALIADA [INFERIDO]
        Note over ModSug,Mongo: cada Sugestao e avaliada separadamente (Sugestao 1:N AvaliacaoSugestao)<br/>as avaliacoes entram no contexto das proximas Sugestoes da mesma Ocorrencia (ADR_039)
        opt fechamento
            Usuario->>Front: fecha a Sugestao
            Front->>ModSug: fechar()
            ModSug->>Mongo: Sugestao status FECHADA e dataFechamento [PENDENTE -<br/>significado de fechar: resolvida ou descartada]
        end
    end
```

**Notas sobre este diagrama:**
- O próprio registro `Sugestao` em `PROCESSANDO` funciona como o pedido; a fila só carrega o `sugestaoId` `[INFERIDO]`.
- Ao verificar saldo já no pedido (antes de enfileirar), o sistema evitaria enfileirar além do limite; aqui a reserva
  está no worker, como no pedido do Michel ("worker → reserva"). Se a reserva for feita já no pedido, ela fica presa
  enquanto o item espera na fila `[PENDENTE — escolher o momento da reserva no manual]`.
- O retry está modelado como reenfileiramento na mesma fila de baixa prioridade `[INFERIDO]`.
- "Site" = canal `WEB` (EnviadorWeb, caixa de correios da plataforma web) e "aplicativo" = canal `PUSH` (EnviadorPush /
  DispositivoPush) do módulo do Pedro `[INFERIDO]`. O app móvel está em STANDBY (ADR_025).

---

## Ponte com Notificações (diagramas do Pedro) — divergências

Conferido em Out 03, 2026 com `sequencia-notificacao.md` e os PNGs da pasta `Notificação` (`gerar_notificacao.png`,
`entrega_push.png`, `visualizacao_web_runtime.png`). Nada foi editado nos arquivos do Pedro.

**O que bate:** o módulo de Notificação recebe uma Ocorrência, checa `PreferenciaNotificacao.possuiCanalHabilitado`,
cria a `Notificacao` e enfileira no Serviço de Notificações; os canais `PUSH` e `WEB` existem; a classe `Notificacao`
do Modelo de Classes já tem o atributo `sugestao_id`.

**Divergências:**
1. **Entrada Ocorrência + Sugestão:** no `gerar_notificacao.png` o construtor é `Notificacao(ocorrencia_id, usuario_id,
   canal, conteudo)`, sem `sugestao_id`, embora a classe tenha o atributo. A entrada da ADR_036 precisa passar o
   `sugestao_id` (ou o texto da Sugestão) para a Notificação. No DER, a entidade `Notificacao` também não tem `sugestaoId`.
2. **Origem genérica:** o Pedro usa o ator `Sistema (origem da Ocorrencia)` e marca `[RISCO]` a falta de orquestrador.
   Aqui a origem é o `Modulo de Ocorrencia`, depois de esperar a Sugestão; no aviso de falha da manual, a origem é o
   `Modulo de Sugestao` (`WorkerSugestao`).
3. **Espera pela Sugestão:** no Pedro, "reconhece uma Ocorrência" já gera a notificação. Com a ADR_036, quando o plano tem
   o recurso, a notificação só é gerada depois da Sugestão (ou da falha/timeout). Esse passo e o timeout não existem lá.
4. **Conteúdo:** os enviadores formatam "os dados essenciais da ocorrência". Não há previsão para o texto da Sugestão nem
   para a mensagem "Não foi possível criar uma sugestão" (templates continuam `[PENDENTE]` no Pedro).
5. **Push de falha da Sugestão manual:** não existe. Todos os diagramas do Pedro (USID_009–014, SSID_019) notificam
   Ocorrências. O aviso de falha precisa de um tipo de notificação novo, ligado à Sugestão e só para o usuário que pediu,
   nos canais `PUSH` e `WEB` `[INFERIDO]`, e o clique deve levar à tela da Ocorrência / Sugestões, não à "tela de
   detalhes do erro" `[INFERIDO]`.
6. **Preferências:** se o usuário desabilitou `PUSH` e `WEB`, o aviso de falha não chega; se ele deve ignorar as
   preferências está `[PENDENTE]`.
7. **Destinatários:** a ADR_036 diz "distribui a quem deve receber"; nem o Pedro nem as ADRs definem quem recebe a
   notificação de uma Ocorrência (todos do tenant? por papel?) `[PENDENTE]`.
8. **Retries são coisas diferentes:** o retry da Sugestão manual (ADR_037) não é o retry de entrega da notificação
   (`TentativaEntrega`, `[PENDENTE]` no Pedro).

---

## Impactos no DER (não alterado agora)

O DER v2 (`Levantamento de Entidades DER`) **não foi alterado**. Mudanças que as ADR_035–039 pedem quando ele for revisado:

| Entidade | Impacto | Marcação |
|---|---|---|
| `Ocorrencia` | Passa a ser concreta (grão do erro/warning): tipo, gravidade, linha, conteúdo, traceId, correlationId, hostName, moduloId, arquivoId e referência ao resumo. Deixa de ter os contadores. | ADR_035 |
| `AchadoAnalise` | Recomendação: fundir com a `Ocorrencia` concreta (deixa de existir como entidade); alternativa: manter e mapear 1:1. | `[INFERIDO]` / `[PENDENTE]` |
| Resumo por Arquivo | Nova entidade (nome `[PENDENTE]`, ex.: `ResumoArquivo`) com os contadores da ADR_020; `Arquivo 1:1 Resumo`, `Resumo 1:0..N Ocorrencia`. | `[INFERIDO]` |
| `Sugestao` | `ocorrenciaId` obrigatório (`Ocorrencia 1:0..N Sugestao` deixa de ser inferido); novos campos `origem` (AUTOMATICA/MANUAL), `tentativas`, `motivoFalha`, `usuarioSolicitanteId` (só manual), `dataSolicitacao`, `dataConclusao`; status com `FALHA`. | ADR_035/036/037 + `[INFERIDO]` |
| `AvaliacaoSugestao` | `Sugestao 1:N AvaliacaoSugestao` confirmado; incluir o autor (`usuarioId`) e definir a escala da nota. | `[INFERIDO]` / `[PENDENTE]` |
| Créditos (`Saldo`, `Transacao`) | Reserva: `Transacao` com tipos RESERVA, EFETIVACAO/AJUSTE e ESTORNO ligada à Sugestão (`Sugestao 1:N Transacao`, era 0..1:N), ou entidade `ReservaCreditos`; saldo com valor em aberto. Unificar com `SaldoTokens` do Modelo de Classes. | ADR_038 + `[PENDENTE]` |
| `Notificacao` | Incluir `sugestaoId` (opcional) e um tipo (Ocorrência, Ocorrência + Sugestão, falha da Sugestão). | `[INFERIDO]` |
| `Plano` | `recursoIA` (Boolean) não distingue a Sugestão; criar recurso específico de Sugestão (campo ou item de enum). | `[PENDENTE]` |
| Idempotência | A chave da ADR_014/020 (`arquivoId`) muda para a Ocorrência concreta (ex.: arquivoId + traceId/correlationId + linha). | `[INFERIDO]` / `[PENDENTE]` |

---

## Notas obrigatórias (pendências)

- **`[INFERIDO — confirmar com Michel]`** automático = síncrono do ponto de vista da Ocorrência; manual = assíncrono via
  fila de baixa prioridade (a transcrição de voz diz "assíncrono" nos dois trechos).
- **`[PENDENTE]`** mascaramento de dados sensíveis antes de enviar à LLM — não definido agora (ADR_039).
- **`[PENDENTE]`** provedor, modelo, hospedagem e credenciais da LLM da `GatewayLLMSugestao`.
- **`[PENDENTE]`** onde fica a flag do recurso de Sugestão no plano (`Plano.recursoIA` ou item no enum `RecursosAnaliseIA`).
- **`[PENDENTE]`** timeout do automático e se ele tem retry antes de notificar (recomendação: sem retry `[INFERIDO]`).
- **`[PENDENTE]`** número de tentativas e backoff do retry manual.
- **`[PENDENTE]`** comportamento com saldo insuficiente (automático: aviso na notificação?; manual: recusar no pedido ou `FALHA` + aviso).
- **`[PENDENTE]`** fórmula da prévia de consumo, margem de erro, período do saldo e expiração de reservas presas.
- **`[PENDENTE]` / `[INFERIDO]`** unificação `SaldoTokens` × módulo Créditos (`Credito`, `Saldo`, `Controle`, `Transacao`); recomendação: Créditos como fonte única.
- **`[INFERIDO]`** liberação da reserva em qualquer falha; consumo cobrado numa resposta inválida `[PENDENTE]`.
- **`[INFERIDO]`** estado `FALHA` na Sugestão e campos `origem` / `tentativas`.
- **`[PENDENTE]`** AchadoAnalise vira a própria Ocorrência ou mapeia 1:1; nome da entidade do resumo por Arquivo; nova chave de idempotência.
- **`[PENDENTE]`** escala da avaliação, quem pode avaliar/fechar, se cada membro avalia uma vez e o significado de "fechar".
- **`[PENDENTE]`** quantas Sugestões/avaliações anteriores entram no contexto e limite de Sugestões manuais por Ocorrência.
- **`[PENDENTE]`** tecnologia das filas (uma fila com prioridade ou duas filas) e como o front fica sabendo que a Sugestão voltou.
- **`[PENDENTE]`** no módulo de Notificação: `sugestao_id` na criação da Notificação, template com a Sugestão e com a
  mensagem de falha, tipo de notificação de falha da Sugestão, destinatários e preferências (ver divergências).
- **`[PENDENTE]`** revisar agrupamento/recorrência (ADR_013) com a Ocorrência concreta para não notificar o mesmo erro várias vezes.

**Rastreabilidade:** ADR_011, 013, 014, 017–020, 025, 029 e as novas ADR_035–039 (`Documentações > Diagrama ADR`);
Modelo de Classes (`Sugestao`, `ContextoSugestao`, `GatewayLLM`, `RespostaLLM`, `SaldoTokens`, `Plano`, `Notificação`);
DER v2 (`Sugestao`, `AvaliacaoSugestao`, `Transacao`, `Plano`, `Notificacao`); `sequencia-notificacao.md` (Pedro); Jira LLT-64.

**Renderização:** PNGs gerados com o mermaid-cli (`mmdc`, tema neutral, fundo branco) e escala 2, com o mesmo ajuste de
estilo preto e branco usado em `Autenticacao e 2FA` e `Varredura e Finder` (auto-mensagens em laço, setas abertas,
rótulos de `alt`/`opt` em negrito e caixas retas).
