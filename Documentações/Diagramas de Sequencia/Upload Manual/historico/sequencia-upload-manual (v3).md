# Diagramas de Sequência v3 — Upload Manual (LhamaLog)

**Versão 3 (10/10/2026).** Atualiza **só o diagrama 1** (`upload_manual_envio.png`) com as decisões do Michel de
10/10/2026, registradas nas ADR_041 a ADR_046. O diagrama 2 (acompanhamento) fica como na v2 e será revisado depois;
ganhou apenas uma nota curta apontando as decisões que o afetam. A v2 deste documento e o PNG anterior do diagrama 1
(`selecao_validacao_envio.png`) foram copiados para a subpasta `v2` (os originais ainda precisam ser movidos para lá); a v1 (4 diagramas) continua na subpasta `v1`.

**Escopo:** seleção (no card do Produto), validação e envio do arquivo até ele entrar no **fim da `FilaOrdenada`** e o
retorno ao usuário (diagrama 1); acompanhamento dos arquivos importados (diagrama 2). O processamento (Finder →
Ocorrência) é o do diagrama oficial `Varredura e Finder`; a Ocorrência segue o modelo das ADR_035/040.

Marcações: `[PENDENTE]` requisito sem definição nas fontes; `[INFERIDO]` ligação feita por nós entre o modelo de
classes, os casos de uso e as ADRs; `[CONFLITO]` duas fontes dizem coisas diferentes; **Resolvido (ADR_0xx)** item que
uma ADR fechou. Valores de enum entre aspas (`"PENDING"`), sem relação com `[PENDENTE]`.

**Base:** USID_006 (Importar Arquivo), SSID_013 (Importar arquivo para varredura), USID_007 (Consultar Arquivos
Processados) (`LhamaLog_casos_de_uso.xlsx`); abas `Coletor`, `Arquivo`, `Arquivo Varredura`, `LogNormalizado`
(`Modelo_de_Classes_LhamaLog.xlsx`); `diagrama_classes_varredura_finder_v2.md`; `der.md` v2; ADR_007, 009, 014, 017,
020, 022, 026, 028, 029, 030, 032, 035, 040 e **ADR_041 a ADR_046** (decisões do upload manual, 10/10/2026).

**Visão geral do fluxo:** dentro do card de um Produto, o usuário envia um ou mais arquivos; o front checa extensão e
tamanho (100 MB). O backend recebe tudo em **uma** requisição `POST /manual/upload`, valida a sessão da Clerk e o tenant,
guarda o nome enviado e chama a API de importação do **Coletor** (JWT interno, ADR_028). O Coletor faz as etapas de
validação e proteção (binário/executável/malware e prompt injection); se a proteção falha, a execução para e o cliente é
alertado. Se passa, a seção paralela "manual" do Coletor normaliza, anexa o owner, registra o `Arquivo` (que passa a ser
tratado só pelo id), agrupa os arquivos num **lote** e o coloca no **fim da `FilaOrdenada`**, sem passar pela Varredura.
O usuário vê "Arquivo enfileirado" e, ao fim, recebe a notificação "varredura finalizada"; erros de processamento vão à
DLQ com até 3 tentativas (**diagrama 1**). Depois, o usuário acompanha o status, o resumo e as Ocorrências (**diagrama 2**).

**Participantes usados (diagrama 1):**
- `Usuario (Gestor / Analista)` — atores da USID_006/007
- `Front Web (React + Clerk)` / `Backend Java (API REST)` — sessão da Clerk validada no backend (ADR_022/026/032)
- `Coletor` — porta única de entrada; seção paralela "manual" (pass-through com proteção) (ADR_042)
- `Arquivo` — conteúdo no bucket e metadados (`id`, `nome`, `bucket_URL`, `extension`, `size_mb`, `owner_id`,
  `product_id`, `company_id`, `imported_at`) (ADR_044)
- `FilaOrdenada` — fila já consumida pelo Finder (ADR_007/017); o lote manual entra no fim (ADR_041)
- `Finder` — consome a `FilaOrdenada` normalmente
- `DLQ (reprocessamento)` — até 3 tentativas no total (ADR_046)

## ⚠️ Pontos críticos

**1. Resolvido (ADR_041) — SSID_013 × USID_006.** O upload é **enfileirado**, não síncrono, e nunca vai direto ao
Finder. O arquivo pula a Varredura e entra no **fim da `FilaOrdenada`** (ex.: se a Varredura acabou de montar 10
arquivos, o manual é o 11º); não é priorizado dentro da fila, mas fica à frente de tudo que ainda está na
`FilaDesordenada`. O ramo "direto ao Finder" da SSID_013 saiu do diagrama 1, **substituído por esta decisão**.

**2. Resolvido (ADR_041) — SSID_013 × arquitetura do Finder.** O Finder continua consumindo só a `FilaOrdenada`
(ADR_007/017); o upload manual apenas entra nessa fila.

**3. Resolvido (ADR_043) — Formatos aceitos.** Inicialmente `.txt`, `.json`, `.csv` e `.log`; lista **extensível**, não
fechada. Limite de **100 MB**. O front checa extensão e tamanho. (A transcrição da aba `LogNormalizado` continua
`[PENDENTE]`, fora deste diagrama.)

**4. Resolvido (ADR_042) — Onde é checada a assinatura.** Só no **backend**, pelo Coletor, como etapa de recebimento,
junto com a proteção contra prompt injection. Executável/malware ou prompt injection = **erro crítico**: execução
interrompida, arquivo não processado, alerta "Seu arquivo contem um malware e nao sera executado" (FA-06).

**5. Resolvido (ADR_046) — SSID_013 "Fluxo Alternativo 2".** Vira tratamento de erro: (a) erro crítico de proteção no
Coletor (FA-06, ADR_042); (b) erro de processamento após o enfileiramento → DLQ automática, até 3 tentativas no total;
depois, "Nao foi possivel fazer a varredura desse arquivo, tente novamente com outro arquivo" (FA-07).

**6. Resolvido (ADR_042) — Entrada pelo Coletor.** O Coletor recebe **sempre** todos os arquivos (regra-base). O backend
chama a mesma API de importação do Coletor pela API interna com JWT próprio (ADR_028); o Coletor roda as mesmas etapas de
validação/proteção, normaliza, anexa o owner e encaminha para uma seção paralela "manual", que enfileira direto na
`FilaOrdenada`. Sai o `[INFERIDO]` de `EnviarArquivo()` e da `FilaDesordenada` do OTel para o upload.

**7. Resolvido (ADR_044) — Produto do arquivo.** O usuário não escolhe: o upload é feito dentro do card do Produto
(menu principal > cards de Produto > detalhes com logs recentes e Ocorrências > botão de upload) e o front envia esse
`product_id`.

**8. Resolvido (ADR_044) — "Nome do Arquivo".** O backend guarda o nome enviado pelo front; ao passar pelo Coletor, o
arquivo recebe o id e passa a ser tratado só por ele. A classe `Arquivo` ganha o atributo `nome` (alinha com o DER v2).

**9. Resolvido (ADR_041/042) — Origem OTel × upload.** A origem fica separada pelas duas seções/filas do Coletor (OTel →
`FilaDesordenada`; manual → direto na `FilaOrdenada`). Prioridade de arquivo manual na Varredura (ADR_009) não se aplica:
ele não passa pela Varredura e não é priorizado (ADR_045). Para a listagem da USID_007 (diagrama 2), se é preciso um
campo de origem persistido no `Arquivo` continua `[PENDENTE]`.

**10. `[CONFLITO]` Status do processamento** — a planilha (`Arquivo Varredura`) tem `"PENDING"`, `"PROCESSING"`,
`"COMPLETED"`, `"ERROR"`, `"FAILED"`; o DER v2 tem `"PENDING"`, `"PROCESSING"`, `"COMPLETED"`, `"COMPLETED_WITH_ERROR"`;
a USID_007 mostra "Concluído", "Processando" e "Falha". O mapeamento entre eles não está definido. Diagrama 2 (o
"enfileirado" da ADR_046 e a falha após 3 tentativas também precisam entrar nesse mapeamento).

**11. `[PENDENTE]` Resumo mostrado na USID_007** — a tela pede "quantidade exata de logs válidos inseridos" e "avisos
sobre linhas ignoradas"; nenhum contador do resumo por Arquivo (ADR_020/035) corresponde a "linhas ignoradas". Diagrama 2.

**12. Parcialmente resolvido (ADR_046) — Arquivo ilegível / limite de `attempts`.** Erro de processamento após o
enfileiramento vai à DLQ, com até 3 tentativas no total. Se um erro de parsing determinístico também gasta as 3
tentativas ou falha direto continua `[PENDENTE]`. Diagrama 2 a revisar.

**13. `[PENDENTE]` Nome e chave do resumo por Arquivo** — a ADR_035 sugere `ResumoArquivo` ou `RelatorioProcessamento`;
a chave de idempotência da Ocorrência concreta também ficou em aberto (ADR_035/040).

**14. Observação** — o 403 da ADR_032 revoga todas as sessões do usuário; vale para o upload como para qualquer
requisição.

**15. Resolvido (ADR_045) — Vários arquivos.** Um ou mais arquivos vão em **uma** requisição; o Coletor agrupa num único
lote e coloca o lote no fim da `FilaOrdenada`. Prioridade é irrelevante para o upload manual.

---

## 1. Upload manual — seleção, validação e envio até a FilaOrdenada (USID_006 + SSID_013; ADR_041 a 046)

Arquivo: `upload_manual_envio.png`

**Resumo do fluxo:** no card de um Produto, o usuário aciona o upload, escolhe os arquivos e confirma. O front checa
extensão e tamanho; o backend recebe tudo em `POST /manual/upload`, valida session token, Organization ativa e Tenant,
guarda os nomes e chama o Coletor. O Coletor valida e protege (erro crítico interrompe), normaliza, anexa o owner,
registra cada `Arquivo`, agrupa num lote e o coloca no fim da `FilaOrdenada`. O usuário vê "Arquivo enfileirado"; o
Finder consome o lote normalmente e o usuário recebe "varredura finalizada"; erro de processamento vai à DLQ (até 3
tentativas).

**Fluxo principal:**
1. Usuário entra nos detalhes de um Produto (menu principal > cards de Produto) e aciona o upload; o front mostra formatos
   aceitos (.txt, .json, .csv, .log — lista extensível) e o limite de 100 MB.
2. Usuário seleciona um ou mais arquivos e confirma; o front checa extensão e tamanho.
3. O front envia uma requisição `POST /manual/upload` com os arquivos, o `product_id` do card e os nomes; o backend valida
   a sessão, gera o JWT interno e guarda os nomes.
4. O backend chama a API de importação do Coletor; o Coletor roda validação + proteção (binário/executável/malware e
   prompt injection).
5. A seção "manual" do Coletor normaliza, anexa o owner, registra o `Arquivo` (id + nome), agrupa os arquivos num lote e
   faz `enqueue` no fim da `FilaOrdenada`.
6. O front mostra "Arquivo enfileirado".
7. O Finder consome o lote da `FilaOrdenada`; ao concluir, o usuário recebe a notificação "varredura finalizada".

**Fluxos alternativos:**
- **FA-01** extensão não permitida (front; ADR_043).
- **FA-02** arquivo acima de 100 MB (front; ADR_043).
- **FA-03** falha de conexão ou timeout durante o upload (USID_006).
- **FA-04** 401 — session token inválido ou expirado (ADR_032).
- **FA-05** 403 — sem organização ativa, sem Tenant ou sem permissão (ADR_032).
- **FA-06** erro crítico de proteção no Coletor — executável/malware ou prompt injection (ADR_042; SSID_013 FA 2a).
- **FA-07** erro de processamento após o enfileiramento — DLQ, até 3 tentativas (ADR_046; SSID_013 FA 2b).
- ~~Ramo SSID_013 direto ao Finder~~ — **removido, substituído pela ADR_041** (o FA "falha ao enviar arquivo" da SSID_013
  passa a ser coberto pelos FA-06/FA-07).

```mermaid
sequenceDiagram
    actor Usuario as Usuario (Gestor / Analista)
    participant Front as Front Web (React + Clerk)
    participant Backend as Backend Java (API REST)
    participant Coletor
    participant Arquivo
    participant FilaOrdenada
    participant Finder
    participant DLQ as DLQ (reprocessamento)

    Note over Usuario,Backend: pre-condicao: usuario autenticado na Clerk -- formatos aceitos e limite de 100 MB configurados (USID_006, ADR_043)

    Note over Usuario,Front: ETAPA 1 -- selecao no card do Produto e validacao rapida no front (USID_006 passos 1 e 2 -- ADR_043/044)
    Usuario->>Front: menu principal > cards de Produto > detalhes do Produto (logs recentes e Ocorrencias)
    Usuario->>Front: aciona "Upload" dentro do card do Produto
    Front-->>Usuario: area de upload com formatos aceitos (.txt, .json, .csv, .log -- lista extensivel) e limite de 100 MB
    Usuario->>Front: seleciona um ou mais arquivos e confirma
    Front->>Front: verifica extensao e tamanho de cada arquivo (checagem rapida, sem assinatura binaria)

    alt FA-01: extensao nao permitida (ADR_043)
        Front-->>Usuario: bloqueia: "Arquivo invalido. Formato nao aceito." -- volta a selecao
    else FA-02: arquivo acima de 100 MB (ADR_043)
        Front-->>Usuario: avisa que excede o limite de 100 MB e orienta dividir o log -- volta a selecao
    else arquivos validos no front
        Note over Front,Backend: ETAPA 2 -- envio unico e validacao da sessao (ADR_022/026/030/032)
        Front->>Backend: POST /manual/upload -- uma requisicao com todos os arquivos,<br/>product_id do card e nome de cada arquivo, com o session token da Clerk (ADR_041/044/045)
        Backend->>Backend: authenticateRequest() -- valida o token, Organization ativa e Tenant<br/>e gera o JWT interno (ADR_028)
        Backend->>Backend: guarda o nome enviado pelo front de cada arquivo (ADR_044)

        Note over Backend,Coletor: ETAPA 3 -- Coletor como porta unica de entrada (ADR_042)
        Backend->>Coletor: chama a API de importacao do Coletor (API interna, JWT proprio -- ADR_028)
        Coletor->>Coletor: etapas de recebimento: validacao + protecao<br/>(checagem de binario/executavel/malware e de prompt injection)

        alt FA-06: erro critico de protecao -- executavel/malware ou prompt injection (ADR_042)
            Coletor-->>Backend: erro critico -- execucao interrompida, arquivo nao processado
            Backend-->>Front: erro critico com o motivo
            Front-->>Usuario: alerta: "Seu arquivo contem um malware e nao sera executado"
        else protecao aprovada
            Coletor->>Coletor: secao paralela "manual" (pass-through): normaliza o arquivo e anexa o owner
            Coletor->>Arquivo: grava o conteudo no bucket e registra o Arquivo (id, nome, bucket_URL, extension,<br/>size_mb, owner_id, product_id, company_id, imported_at) no MongoDB (ADR_029/044)
            Note over Coletor,Arquivo: a partir daqui o arquivo e tratado so pelo arquivo_id (ADR_044)
            Coletor->>Coletor: agrupa os arquivos da requisicao em um unico lote (ADR_045)
            Coletor->>FilaOrdenada: enqueue(lote) no FIM da FilaOrdenada -- sem passar pela Varredura,<br/>sem priorizacao -- fica a frente do que ainda esta na FilaDesordenada (ADR_041)
            Note over Coletor,FilaOrdenada: so a FilaDesordenada (OTel) espera a Varredura -- a origem e separada<br/>pelas duas secoes do Coletor (OTel -> FilaDesordenada -- manual -> FilaOrdenada)
            Coletor-->>Backend: lote enfileirado (arquivo_ids)
            Backend-->>Front: 202 aceito -- arquivos enfileirados
            Front-->>Usuario: "Arquivo enfileirado"

            Note over FilaOrdenada,DLQ: ETAPA 4 -- processamento assincrono pelo Finder (diagrama oficial "Varredura e Finder" -- ADR_007/017)
            FilaOrdenada->>Finder: proximo Arquivo do lote (consumo normal da FilaOrdenada)
            Finder->>Finder: processar() -- analise do Arquivo
            alt processamento concluido
                Finder-->>Backend: varredura do Arquivo concluida
                Backend-->>Front: notificacao
                Front-->>Usuario: notificacao no front: "varredura finalizada" (ADR_046)<br/>[PENDENTE - mecanismo da notificacao: push/websocket ou polling]
            else FA-07: erro de processamento apos o enfileiramento (ADR_046)
                Finder->>DLQ: Arquivo com erro (possivel instabilidade do sistema)
                loop ate 3 tentativas no total
                    DLQ->>FilaOrdenada: recoloca o Arquivo no fim da FilaOrdenada como nova tentativa<br/>(attempts + 1) [INFERIDO - posicao do reenvio]
                end
                opt 3 tentativas falharam
                    DLQ-->>Backend: falha definitiva do Arquivo
                    Backend-->>Front: erro de processamento
                    Front-->>Usuario: "Nao foi possivel fazer a varredura desse arquivo,<br/>tente novamente com outro arquivo"
                end
            end
        end
    end

    alt FA-03: falha de conexao ou timeout durante o upload (USID_006)
        Front-->>Usuario: interrompe a barra de progresso, cancela a operacao parcial e alerta<br/>"Falha na comunicacao com o servidor. Verifique sua conexao e tente novamente."
    else FA-04: 401 -- session token invalido ou expirado (ADR_032)
        Backend-->>Front: 401 Unauthorized + erro basico
        Front-->>Usuario: "Voce foi deslogado" e volta ao login
    else FA-05: 403 -- sem organizacao ativa, sem Tenant ou sem permissao (ADR_032)
        Backend->>Backend: revoga todas as sessoes do usuario na Clerk
        Backend-->>Front: 403 Forbidden + erro basico
        Front-->>Usuario: "Voce foi deslogado" e volta ao login
    end
```

**Notas sobre este diagrama:**
- O ramo SSID_013 "direto ao Finder" foi removido: **substituído pela ADR_041** (upload enfileirado no fim da
  `FilaOrdenada`).
- O loop por arquivo da v2 deu lugar ao lote único (ADR_045): uma requisição, um lote, um `enqueue`.
- FA-03 vale para a ETAPA 2 (transferência ao servidor); FA-04 e FA-05 valem para qualquer resposta do backend (ADR_032).
- FA-06 interrompe a execução antes de qualquer registro na fila; FA-07 acontece depois do "Arquivo enfileirado".
- `[INFERIDO]` o reenvio da DLQ volta ao fim da `FilaOrdenada`.
- `[PENDENTE]` mecanismo da notificação "varredura finalizada" no front (push/websocket ou polling).
- `202` como código de "aceito/enfileirado" é `[INFERIDO]` (a decisão só fixa o retorno "Arquivo enfileirado").

---

## 2. Acompanhamento — Consultar Arquivos Processados (USID_007; Ocorrência pelas ADR_035/040)

Arquivo: `upload_manual_acompanhamento.png`

**Resumo do fluxo:** o usuário abre o histórico de importação; o backend lista os Arquivos do tenant com o status do
processamento e o total de Ocorrências. Em um arquivo concluído, "Ver Detalhes" mostra o resumo por Arquivo e o atalho
para as Ocorrências concretas daquele arquivo (USID_005). Arquivo com falha mostra o erro; arquivo em processamento fica
com os detalhes desabilitados.

**Fluxo principal:**
1. Usuário abre "Arquivos Processados"; o backend busca `Arquivo`, `ArquivoVarredura` e o resumo de cada Arquivo.
2. A tela lista Nome do Arquivo, Data de Envio, Status e Total de Ocorrências geradas.
3. Em um arquivo "Concluído", "Ver Detalhes" mostra o resumo e o atalho "Ver ocorrências deste arquivo".
4. O usuário encerra os detalhes e volta à listagem.

**Fluxos alternativos:**
- **FA-01** arquivo com "Falha" (erro de parsing).
- **FA-02** nenhum arquivo importado.
- **FA-03** arquivo ainda "Processando".

```mermaid
sequenceDiagram
    actor Usuario as Usuario (Gestor / Analista)
    participant Front as Front Web (React + Clerk)
    participant Backend as Backend Java (API REST)
    participant Arquivo
    participant ArqVarr as ArquivoVarredura
    participant Resumo as Resumo por Arquivo [PENDENTE - nome, ADR_035]
    participant Ocorrencia as Ocorrencia (concreta, ADR_035/040)

    Note over Usuario,Backend: pre-condicao: usuario autenticado com acesso ao modulo de importacoes (USID_007) -- 401/403 como no diagrama 1 (ADR_032)

    Note over Usuario,Resumo: ETAPA 1 -- listagem do historico (USID_007 passo 1)
    Usuario->>Front: acessa "Arquivos Processados" / "Historico de Importacao"
    Front->>Backend: lista os arquivos importados (session token da Clerk)
    Backend->>Arquivo: busca os Arquivos do tenant (owner_id, product_id)<br/>[PENDENTE - sem campo que separe upload manual de pacote OTel]
    Backend->>ArqVarr: status do processamento de cada Arquivo<br/>[CONFLITO - valores da planilha x DER v2 x USID_007]
    Backend->>Resumo: contadores de cada Arquivo (ADR_020/035)
    Backend-->>Front: listagem
    Front-->>Usuario: Nome do Arquivo [CONFLITO - so no DER], Data de Envio, Status e Total de<br/>Ocorrencias geradas [INFERIDO - numero de Ocorrencias concretas do Arquivo]

    alt arquivo "Concluido" -- Ver Detalhes (USID_007 passos 2 a 4)
        Note over Usuario,Ocorrencia: ETAPA 2 -- detalhes do arquivo
        Usuario->>Front: seleciona o arquivo e aciona "Ver Detalhes" (ou expande a linha)
        Front->>Backend: detalhes do Arquivo
        Backend->>Resumo: resumo do processamento do Arquivo
        Resumo-->>Backend: registrosProcessados, achadosIdentificados, spamIdentificados,<br/>dadosSensiveisIdentificados + referencias as Ocorrencias (ADR_035)
        Backend-->>Front: resumo
        Front-->>Usuario: logs validos inseridos, avisos de linhas ignoradas e atalho "Ver ocorrencias<br/>deste arquivo" [PENDENTE - nenhum contador do resumo para linhas ignoradas]
        opt "Ver ocorrencias deste arquivo" (redireciona para USID_005 Filtrar Ocorrencia)
            Usuario->>Front: aciona o atalho
            Front->>Backend: Ocorrencias do arquivoId
            Backend->>Ocorrencia: busca as Ocorrencias concretas do arquivoId (tipo "ERRO" ou "WARNING",<br/>gravidade, linha, conteudo) -- spam nao gera Ocorrencia (ADR_035/040)
            Backend-->>Front: Ocorrencias do arquivo
            Front-->>Usuario: lista filtrada (USID_005, fora deste escopo)
        end
        Usuario->>Front: encerra a visualizacao dos detalhes
        Front-->>Usuario: volta a listagem do historico
    else FA-01: arquivo com "Falha" -- erro de parsing (USID_007)
        Usuario->>Front: seleciona o arquivo com "Falha" e aciona "Ver Detalhes"
        Front->>Backend: detalhes do erro
        Backend->>ArqVarr: erro registrado (error, attempts)
        Backend-->>Front: detalhamento do erro
        Front-->>Usuario: ex.: "Erro de leitura: Estrutura JSON invalida na linha 45" ou "Codificacao nao<br/>suportada" -- orienta corrigir o arquivo
        Note over Backend,ArqVarr: ADR_014 so trata falha da LLM: regra para arquivo ilegivel e limite<br/>de attempts [PENDENTE]
    else FA-02: nenhum arquivo importado (USID_007)
        Front-->>Usuario: estado vazio "Nenhum arquivo processado ainda" + atalho<br/>"Importar Novo Arquivo" (diagrama 1)
    else FA-03: arquivo ainda "Processando" (USID_007)
        Usuario->>Front: tenta ver os detalhes de um arquivo "Processando"
        Front-->>Usuario: detalhes desabilitados: "O arquivo ainda esta sendo lido e indexado.<br/>Aguarde a conclusao para visualizar o resumo."
    end
```

> **Nota (v3, 10/10/2026):** este diagrama não foi revisado nesta versão. Decisões do diagrama 1 que o afetam: o `Arquivo`
> ganha `nome` (ADR_044, resolve o `[CONFLITO]` do "Nome do Arquivo"); a origem é separada pelas seções do Coletor
> (ADR_041/042); "enfileirado", notificação "varredura finalizada" e DLQ com até 3 tentativas (ADR_046) precisam entrar
> no mapeamento de status e no FA-01. Revisão pendente.

**Notas sobre este diagrama:**
- `[CONFLITO]` status e "Nome do Arquivo": pontos críticos 8 e 10.
- A Ocorrência segue as ADR_035/040: cada erro/warning do Arquivo é uma Ocorrência concreta, e o resumo por Arquivo
  guarda os contadores e as referências a elas. O diagrama oficial `finder.png` (r3, 02/10) ainda mostra a
  Ocorrência-resumo da ADR_020, anterior às ADR_035/040.
- A criação de cada Ocorrência concreta dispara a Sugestão automática quando o plano tem o recurso (ADR_036/040); isso
  está no diagrama oficial `Sugestao por IA`, não aqui.
- USID_007 é consulta sob demanda; a notificação das Ocorrências é outro fluxo (módulo de Notificação).

---

## Notas obrigatórias (pendências)
- **Resolvido (ADR_041)** SSID_013 (direto ao Finder, síncrono) × USID_006 (fila assíncrona): upload enfileirado no fim da
  `FilaOrdenada`, sem Varredura; o ramo SSID_013 foi removido do diagrama 1.
- **Resolvido (ADR_041)** SSID_013 × ADR_007/017: o Finder continua consumindo só a `FilaOrdenada`.
- **Resolvido (ADR_044)** `Arquivo.nome`: a classe `Arquivo` ganha `nome`; depois do Coletor o arquivo é tratado pelo id.
- **`[CONFLITO]`** valores de status do processamento: planilha × DER v2 × USID_007 (diagrama 2).
- **Resolvido (ADR_043)** formatos aceitos: `.txt`, `.json`, `.csv`, `.log`, lista extensível; limite 100 MB. Continua
  `[PENDENTE]` a transcrição da aba `LogNormalizado`.
- **Resolvido (ADR_042)** assinatura do arquivo: só no backend, pelo Coletor, com proteção contra prompt injection.
- **Resolvido (ADR_044)** Produto no upload: vem do card do Produto (`product_id` enviado pelo front).
- **Resolvido (ADR_041/042)** origem do `Arquivo`: separada pelas seções do Coletor; prioridade na Varredura não se aplica
  (ADR_045). Continua `[PENDENTE]` um campo de origem persistido para a listagem da USID_007 (diagrama 2).
- **`[PENDENTE]`** contador de "linhas ignoradas" no resumo; nome da entidade do resumo; chave de idempotência da
  Ocorrência concreta (ADR_035/040).
- **Parcialmente resolvido (ADR_046)** limite de `attempts`: 3 tentativas no total via DLQ. Continua `[PENDENTE]` se erro
  de parsing determinístico gasta as 3 tentativas.
- **Resolvido (ADR_046)** SSID_013 "Fluxo Alternativo 2": erro crítico de proteção (FA-06) e DLQ (FA-07).
- **Resolvido (ADR_045)** vários arquivos: uma requisição, um lote.
- **Resolvido (ADR_042)** `[INFERIDO]` da v2 sobre `Coletor.EnviarArquivo()`, JWT interno (ADR_028) e uso da
  `FilaDesordenada` do OTel.
- **`[PENDENTE]`** mecanismo da notificação "varredura finalizada" (diagrama 1).
- **`[INFERIDO]`** reenvio da DLQ no fim da `FilaOrdenada`; código `202` no aceite (diagrama 1).
- **`[INFERIDO]`** "Total de Ocorrências geradas" = número de Ocorrências concretas do Arquivo (diagrama 2).
- **`[PENDENTE]`** ajustes no Modelo de Classes/DER: `Arquivo.nome`, seção "manual" do Coletor, DLQ (ADR_042/044/046).

**Rastreabilidade:** USID_006, SSID_013, USID_007 (`LhamaLog_casos_de_uso.xlsx`); `Modelo_de_Classes_LhamaLog.xlsx`
(`Coletor`, `Arquivo`, `Arquivo Varredura`, `LogNormalizado`); `diagrama_classes_varredura_finder_v2.md`; `der.md` v2;
ADR_007, 009, 014, 016, 017, 020, 022, 026, 028, 029, 030, 032, 035, 036, 040, 041, 042, 043, 044, 045, 046; quadro-branco.

**Renderização:** PNGs gerados com o mermaid-cli (`mmdc`, tema neutral, fundo branco) e escala 2. Na v3 só o
`upload_manual_envio.png` foi regerado.
