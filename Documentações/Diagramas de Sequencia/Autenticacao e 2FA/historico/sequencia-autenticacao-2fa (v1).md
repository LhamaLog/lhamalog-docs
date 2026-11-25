# Diagramas de Sequência — Autenticação e 2FA (LhamaLog)

Baseado em: ADR_021 (Clerk como provedor de identidade e autenticação), ADR_022 (Integração do
backend Java com a Clerk), ADR_023 (Componentes de front-end da Clerk), ADR_024 (MFA obrigatório no
login via Clerk), ADR_025 (Gestão de tokens internos e app móvel em standby), ADR_026 (Backend Java
com SDK oficial da Clerk e front-end em React), ADR_027 (MVP no plano gratuito da Clerk e estratégia
de 2FA), ADR_028 (Tokens internos próprios, sem M2M nem API keys da Clerk), ADR_029 (MongoDB
confirmado e DER como artefato de restrição) e ADR_030 (Multi-tenant com Organizations, Tenant
mestre e mapeamento do clerk_user_id) — pasta `Documentações > Diagrama ADR`. Apoio: resumos
`resumo_clerk.md` e `resumo_clerk_v2.md` (02/10/2026).

**Visão geral do fluxo:** a Clerk é o provedor de identidade (usuários, sessões e MFA). O front em
React (provável, `@clerk/react`) usa os componentes prontos (`<SignIn />`, `<SignUp />`,
`<OrganizationSwitcher />`, `<TaskSetupMFA />`) com a Publishable Key. O backend Java valida o
session token em cada requisição com o SDK oficial (`com.clerk:backend-api`), e o Módulo de
Autenticação do LhamaLog só faz o mapeamento `clerk_user_id` ↔ tenant / assinatura / plano no
MongoDB. O **diagrama 1** mostra o login até a resposta da API; o **diagrama 2** detalha o 2º fator
obrigatório.

**Participantes usados:**
- `Usuario` — pessoa que acessa a Aplicação Web
- `Front React (@clerk/react)` — `<ClerkProvider>` com a Publishable Key, `<SignIn />`, `<SignUp />`,
  `<OrganizationSwitcher />`, `<TaskSetupMFA />` (ADR_023/026)
- `Clerk (Frontend API)` — login, cadastro, sessão, session token e MFA (ADR_021/024)
- `Clerk (Backend API / Webhooks Svix)` — JWKS, metadata da OrganizationMembership e webhooks
  `user.*` (ADR_022/030); no diagrama 2 aparece como `Clerk (Dashboard / Backend API)`
- `Backend Java (API REST)` — guarda a `CLERK_SECRET_KEY`, recebe o Bearer token e os webhooks
- `SDK Clerk (com.clerk:backend-api)` — `AuthenticateRequest.authenticateRequest(...)` (ADR_022/026)
- `Modulo de Autenticacao` — só mapeia `clerk_user_id` ↔ tenant, assinatura e plano; não guarda
  dados de segurança (ADR_030)
- `MongoDB (Tenant / Assinaturas / Planos)` — coleção mestre Tenant com índice único composto
  (organização + usuário + produto) → `tenant_id` (ADR_029/030)
- `Admin LhamaLog (suporte)` — só no diagrama 2, faz o reset de MFA (ADR_024)

Tudo marcado `[PENDENTE]` é requisito ainda sem definição nas ADRs; `[INFERIDO]` é ligação feita
por mim a partir das ADRs/documentação da Clerk que não está escrita literalmente nelas.

**Atenção, risco de confusão de nomes:** o status de sessão da Clerk `sts = "pending"` (sessão
esperando uma tarefa, como `setup-mfa`) **não tem relação** com a marcação `[PENDENTE]` deste
documento. Nos diagramas, os status de sessão aparecem sempre entre aspas (`"pending"`, `"active"`).

---

## 1. Autenticação — login até a resposta da API (ADR_021, 022, 023, 026, 028, 029, 030)

Arquivo: `autenticacao_login.png`

**Resumo do fluxo:** o usuário entra pelo `<SignIn />`; a Clerk verifica os fatores (detalhe no
diagrama 2) e devolve a sessão `"active"` com o session token (JWT curto, renovado a cada ~60 s).
O usuário escolhe a organização ativa (claim `o`). O front chama a API REST com
`Authorization: Bearer <token>`; o SDK valida assinatura (JWKS ou `CLERK_JWT_KEY`), `exp`/`nbf`,
`azp` e recusa `sts = "pending"`. O Módulo de Autenticação resolve `sub` (= `clerk_user_id`) +
organização ativa + produto no Tenant e busca assinatura e plano. O `tenant_id` fica só no backend.

**Fluxo principal:**
1. Usuário abre o `<SignIn />` e informa e-mail e senha; a Clerk verifica 1º e 2º fator.
2. Clerk devolve sessão `"active"` + session token; usuário escolhe a organização no `<OrganizationSwitcher />`.
3. Front obtém o token (`getToken()`) e chama a API REST com Bearer token.
4. Backend chama `AuthenticateRequest.authenticateRequest(...)` (`secretKey` + `authorizedParty`); `isSignedIn() = true` e `claims()`.
5. Módulo de Autenticação busca o Tenant (organização, usuário, produto) e a assinatura/plano pelo `clerk_user_id`.
6. Backend executa a operação isolada pelo `tenant_id` e responde 200.

**Fluxos alternativos:**
- **FA-01** — token inválido, expirado ou ausente: `isSignedIn() = false` → 401; o front tenta token novo ou volta ao `<SignIn />`.
- **FA-02** — sessão `"pending"` (MFA não configurado, tarefa `setup-mfa`): conta como deslogada → 403/401 `[PENDENTE]` e redireciona para o setup do MFA (diagrama 2).
- **FA-03** — organização não selecionada (token sem a claim `o`): 403 `[PENDENTE]` e pede a escolha no `<OrganizationSwitcher />` / `<TaskChooseOrganization />`.
- **FA-04** — usuário sem Tenant para o produto: 403 `[PENDENTE]` (encaminhamento para contratação não definido).
- **opt** — primeiro acesso/cadastro: `<SignUp />` → webhook `user.created` (Svix) → verificação da assinatura, dedupe por `svix-id`, upsert do `clerk_user_id` em Assinaturas e Planos, criação do Tenant e espelho do `tenant_id` no privateMetadata da OrganizationMembership.
- **opt** — verificação com JWKS quando não há `CLERK_JWT_KEY` (modo networkless).

```mermaid
sequenceDiagram
    actor Usuario
    participant Front as Front React (@clerk/react)
    participant ClerkFAPI as Clerk (Frontend API)
    participant Backend as Backend Java (API REST)
    participant SDK as SDK Clerk (com.clerk:backend-api)
    participant ModAuth as Modulo de Autenticacao
    participant Mongo as MongoDB (Tenant / Assinaturas / Planos)
    participant ClerkBAPI as Clerk (Backend API / Webhooks Svix)

    Note over Front,ClerkFAPI: #lt;ClerkProvider#gt; com a Publishable Key (VITE_CLERK_PUBLISHABLE_KEY) no front<br/>(ADR_023/026)<br/>CLERK_SECRET_KEY so no backend (ADR_026)

    opt primeiro acesso (cadastro) -- sincronizacao por webhook (ADR_022/030)
        Usuario->>Front: abre #lt;SignUp /#gt; e cria a conta
        Front->>ClerkFAPI: cria o usuario (sign-up)
        ClerkFAPI-->>Front: usuario criado -- segue para o setup-mfa (ver<br/>autenticacao_2fa)
        ClerkBAPI->>Backend: webhook user.created (enviado pelo Svix, assinado)
        Backend->>Backend: verifica a assinatura Svix com<br/>CLERK_WEBHOOK_SIGNING_SECRET [INFERIDO - SDK Java sem<br/>helper]
        Backend->>Mongo: deduplica pelo header svix-id (idempotente)
        Backend->>ModAuth: registra o clerk_user_id do novo usuario
        ModAuth->>Mongo: upsert do clerk_user_id em Assinaturas e Planos<br/>(ADR_030)
        ModAuth->>Mongo: cria o Tenant (organizacao + usuario + produto) com<br/>indice unico composto -- gera o tenant_id<br/>[PENDENTE - momento exato: na contratacao do produto ou<br/>na entrada na Organization]
        ModAuth->>ClerkBAPI: OrganizationMemberships updateMetadata --<br/>privateMetadata: produto para tenant_id [INFERIDO -<br/>ADR_030]
        Backend-->>ClerkBAPI: 2xx (recebimento confirmado)
        Note over Backend,Mongo: user.updated e user.deleted usam o mesmo endpoint: compara updated_at, upsert e soft<br/>delete (deleted_at)
    end

    Usuario->>Front: acessa o LhamaLog
    Front->>Usuario: exibe #lt;SignIn /#gt;
    Usuario->>Front: informa e-mail e senha
    Front->>ClerkFAPI: envia as credenciais (sign-in)
    ClerkFAPI->>ClerkFAPI: verifica o 1o e o 2o fator (detalhe no diagrama<br/>autenticacao_2fa, ADR_024/027)
    ClerkFAPI-->>Front: sessao active + session token (JWT curto, renovado a<br/>cada ~60 s, claims sub, sid, azp, sts, o)
    Usuario->>Front: escolhe a organizacao ativa no<br/>#lt;OrganizationSwitcher /#gt;<br/>(ADR_030)
    Front->>ClerkFAPI: define a organizacao ativa
    ClerkFAPI-->>Front: novo session token com a claim o (id, rol, per)
    Front->>Front: getToken()
    Front->>Backend: requisicao a API REST com Authorization: Bearer token<br/>(ou cookie __session na mesma origem)
    Backend->>SDK: AuthenticateRequest.authenticateRequest(request,<br/>secretKey + authorizedParty)
    opt verificacao com JWKS (sem CLERK_JWT_KEY para modo networkless)
        SDK->>ClerkBAPI: obtem a chave publica (JWKS)
        ClerkBAPI-->>SDK: JWKS
    end
    SDK->>SDK: valida assinatura, exp/nbf, azp (authorizedParty) e<br/>rejeita sts = "pending" (ADR_022)
    SDK-->>Backend: requestState.isSignedIn() = true + requestState.claims()
    Backend->>ModAuth: resolve o contexto: sub = clerk_user_id, o.id =<br/>organizacao ativa, produto da requisicao [INFERIDO]
    ModAuth->>Mongo: busca o Tenant por (organizacao, usuario, produto)<br/>(ADR_029/030)
    Mongo-->>ModAuth: tenant_id
    ModAuth->>Mongo: busca Assinatura e Plano pelo clerk_user_id
    Mongo-->>ModAuth: assinatura e plano
    ModAuth-->>Backend: contexto: clerk_user_id, tenant_id, plano, papel (o.rol)
    Note over Backend,Mongo: o tenant_id fica so no backend, NUNCA vai no session token (ADR_030)
    Backend->>Backend: executa a operacao isolada pelo tenant_id
    Backend-->>Front: 200 OK + resposta
    Front-->>Usuario: exibe os dados do produto

    alt FA-01: token invalido, expirado ou ausente
        SDK-->>Backend: isSignedIn() = false (assinatura, exp/nbf ou azp<br/>invalidos)
        Backend-->>Front: 401 Unauthorized
        Front->>ClerkFAPI: getToken() obtem um token novo, se a sessao ainda<br/>estiver ativa [INFERIDO]
        Front->>Usuario: sem sessao valida: volta para o #lt;SignIn /#gt;
    else FA-02: sessao pending (MFA nao configurado, sts = "pending", tarefa setup-mfa)
        SDK-->>Backend: sessao "pending" conta como deslogada (ADR_022/024)
        Backend-->>Front: 403 / 401 [PENDENTE - codigo HTTP nao definido]
        Front->>Usuario: redireciona para a tarefa setup-mfa (#lt;SignIn /#gt; ou<br/>#lt;TaskSetupMFA /#gt;) -- ver autenticacao_2fa
    else FA-03: organizacao nao selecionada (token sem a claim o)
        Backend-->>Front: 403 -- organizacao ativa obrigatoria [PENDENTE - codigo<br/>HTTP]
        Front->>Usuario: pede a escolha da organizacao<br/>(#lt;OrganizationSwitcher /#gt; ou<br/>#lt;TaskChooseOrganization /#gt;)<br/>[PENDENTE - Membership required, ADR_030]
    else FA-04: usuario sem Tenant para o produto
        Mongo-->>ModAuth: nenhum Tenant para (organizacao, usuario, produto)
        ModAuth-->>Backend: sem tenant_id para o produto
        Backend-->>Front: 403 -- sem acesso ao produto [PENDENTE - codigo HTTP e<br/>encaminhamento para contratacao]
    end

    Note over Backend,ClerkBAPI: fora do escopo: chamadas entre modulos usam JWT proprio, sem M2M da Clerk (ADR_028)<br/>app movel em STANDBY (ADR_025)
```

**Notas sobre este diagrama:**
- `[INFERIDO]` a verificação da assinatura Svix em Java: o README do SDK não lista helper (ADR_022).
- `[INFERIDO]` o espelho do `tenant_id` vai no privateMetadata da OrganizationMembership, como mapa
  produto → `tenant_id`, via `OrganizationMemberships` `updateMetadata` (ADR_030, a doc não é decisiva).
- `[PENDENTE]` o momento exato de criar o Tenant (contratação do produto ou entrada na Organization)
  e se a chave "usuário" do Tenant é o `clerk_user_id` ou um id interno (ADR_030). O diagrama coloca
  a criação no `opt` de primeiro acesso, como pedido, sem decidir isso.
- O encaixe do SDK como filtro/middleware depende do framework Java, ainda `[PENDENTE]` (ADR_022/026).
- Fora do escopo (nota no rodapé): comunicação entre módulos com JWT próprio, sem M2M da Clerk
  (ADR_028); app móvel em STANDBY (ADR_025).

## 2. 2FA obrigatório — do 1º fator à sessão ativa (ADR_022, 023, 024, 026, 027)

Arquivo: `autenticacao_2fa.png`

**Resumo do fluxo:** com "Require multi-factor authentication" ligado (TOTP, SMS e backup codes),
depois da senha a Clerk decide: quem não tem MFA fica com a sessão `"pending"` e a tarefa
`setup-mfa`, tratada sozinha pelo `<SignIn />` (ou `<TaskSetupMFA />`); quem já tem informa o código
TOTP/SMS ou um backup code; quem perdeu tudo depende de um admin. Só a sessão `"active"` é aceita
pelo backend. No MVP, o MFA só funciona na instância de desenvolvimento (ADR_027).

**Fluxo principal:**
1. Usuário informa e-mail e senha no `<SignIn />`; a Clerk verifica o 1º fator.
2. A Clerk exige o 2º fator conforme o estado do usuário (FA-01, FA-02 ou FA-03).
3. Sessão `"active"`: o front obtém o token e chama a API com Bearer token.
4. Backend valida com `AuthenticateRequest.authenticateRequest(...)`, recusa `sts = "pending"` e aceita a requisição (segue o diagrama 1).

**Fluxos alternativos:**
- **FA-01** — usuário sem MFA cadastrado: sessão `"pending"` + tarefa `setup-mfa`; cadastro de TOTP (QR code) ou SMS, confirmação do código, entrega dos backup codes; sessão passa a `"active"`.
- **FA-02** — usuário com MFA cadastrado: pede o código TOTP ou SMS; `opt` código inválido (novo código); `opt` usa um backup code; claim `fva` registra a verificação.
- **FA-03** — perdeu o 2º fator e os backup codes: não há reset pelo usuário final; admin verifica a identidade e reseta no Dashboard ou via `disableUserMFA()`; no próximo login o usuário cai no FA-01.
- **opt** — produção no plano gratuito (Hobby), sem MFA: FA-01 a FA-03 não ocorrem; Device Trust pede código por e-mail em dispositivo novo `[INFERIDO]`; benefício de estudante (ADR_031 proposta) `[PENDENTE]`.

```mermaid
sequenceDiagram
    actor Usuario
    participant Front as Front React (SignIn / TaskSetupMFA)
    participant ClerkFAPI as Clerk (Frontend API)
    actor Admin as Admin LhamaLog (suporte)
    participant ClerkBAPI as Clerk (Dashboard / Backend API)
    participant Backend as Backend Java (SDK Clerk)

    Note over Front,ClerkBAPI: instancia com "Require multi-factor authentication" ligado. Metodos: TOTP, SMS e backup codes<br/>(ADR_024)<br/>MVP: MFA so na instancia de desenvolvimento, ate 100 usuarios, sem dados reais (ADR_027)

    Usuario->>Front: abre o #lt;SignIn /#gt; e informa e-mail e senha
    Front->>ClerkFAPI: envia o 1o fator (senha)
    ClerkFAPI->>ClerkFAPI: verifica o 1o fator

    alt FA-01: usuario sem MFA cadastrado (primeiro login ou cadastro novo)
        ClerkFAPI-->>Front: sessao criada com sts = "pending" e tarefa setup-mfa<br/>(tratada como deslogada)
        Front->>Usuario: exibe a tarefa setup-mfa (o #lt;SignIn /#gt; trata<br/>sozinho, ou #lt;TaskSetupMFA /#gt; em rota propria via<br/>taskUrls)
        Usuario->>Front: escolhe o metodo: TOTP (app autenticador) ou SMS
        Front->>ClerkFAPI: cadastra o fator: TOTP (QR code) ou SMS [PENDENTE -<br/>incluir o Brasil na SMS allowlist e custo por SMS]
        ClerkFAPI-->>Front: pede o codigo de confirmacao
        Usuario->>Front: informa o codigo gerado no app (TOTP) ou recebido por<br/>SMS
        Front->>ClerkFAPI: confirma o codigo
        ClerkFAPI-->>Front: fator cadastrado + backup codes
        Front->>Usuario: exibe os backup codes para guardar (a doc recomenda<br/>cadastrar mais de um 2o fator)
        ClerkFAPI->>ClerkFAPI: conclui a tarefa setup-mfa: sessao passa de "pending"<br/>para "active"
    else FA-02: usuario com MFA cadastrado
        ClerkFAPI-->>Front: pede o 2o fator
        Front->>Usuario: pede o codigo TOTP ou SMS
        Usuario->>Front: informa o codigo
        Front->>ClerkFAPI: envia o codigo do 2o fator
        opt codigo invalido
            ClerkFAPI-->>Front: codigo invalido
            Front->>Usuario: mostra o erro e pede um novo codigo [PENDENTE - limite<br/>de tentativas e bloqueio nao definidos nas ADRs]
        end
        opt sem acesso ao TOTP/SMS: usa um backup code
            Usuario->>Front: informa um backup code
            Front->>ClerkFAPI: envia o backup code
            ClerkFAPI->>ClerkFAPI: aceita o backup code (uso unico) [INFERIDO]
        end
        ClerkFAPI->>ClerkFAPI: 2o fator verificado -- claim fva registra ha quantos<br/>minutos cada fator foi verificado
        ClerkFAPI-->>Front: sessao "active"
    else FA-03: perdeu o 2o fator e os backup codes
        Note over Usuario,ClerkFAPI: a Clerk nao tem reset de MFA pelo usuario final (ADR_024)
        Usuario->>Admin: pede o reset do MFA [PENDENTE - canal e processo de<br/>suporte]
        Admin->>Admin: verifica a identidade do usuario [PENDENTE -<br/>responsabilidade do LhamaLog, ADR_024]
        Admin->>ClerkBAPI: reseta o MFA no Dashboard ou via Backend API<br/>disableUserMFA()
        ClerkBAPI-->>Admin: fatores de MFA do usuario removidos
        Admin-->>Usuario: avisa que o MFA foi resetado
        Note over Usuario,ClerkFAPI: no proximo login o usuario cai no FA-01 (setup-mfa obrigatorio de novo)
    end

    Front->>Front: getToken() -- session token com sts "active" e claim fva
    Front->>Backend: requisicao a API REST com Authorization: Bearer token
    Backend->>Backend: AuthenticateRequest.authenticateRequest(...) valida o<br/>token e recusa sts = "pending" (ADR_022/026)
    Backend-->>Front: requisicao aceita -- segue o fluxo do diagrama<br/>autenticacao_login

    opt producao no plano gratuito (Hobby): sem MFA [PENDENTE - ADR_031 em avaliacao]
        Note over Front,ClerkBAPI: MFA (TOTP, SMS, backup codes) nao disponivel em producao no Hobby: FA-01 a FA-03 nao ocorrem<br/>(ADR_027)<br/>requisito de 2FA so parcialmente atendido -- risco aceito no MVP [PENDENTE - criterio de migracao<br/>para o Pro]
        ClerkFAPI->>ClerkFAPI: Device Trust: login por senha, em dispositivo novo, de<br/>usuario sem MFA [INFERIDO - disponivel no Hobby,<br/>confirmar no Dashboard]
        ClerkFAPI-->>Front: pede o 2o passo por e-mail (email code ou email link)
        Usuario->>Front: informa o codigo recebido por e-mail
        Front->>ClerkFAPI: envia o codigo do e-mail
        ClerkFAPI-->>Front: sessao "active" (nao e MFA a cada login)
        Note over Front,ClerkBAPI: [PENDENTE - ADR_031 proposta] beneficio de estudante (GitHub Student Developer Pack = plano Pro sem<br/>custo) em avaliacao:<br/>se aprovado, o MFA obrigatorio de FA-01 a FA-03 passa a valer tambem em producao
    end
```

**Notas sobre este diagrama:**
- Senha incorreta no 1º fator é tratada pelo próprio `<SignIn />` e não foi detalhada.
- `[INFERIDO]` backup code de uso único; a ADR_024 só diz que a doc recomenda habilitá-los.
- `[PENDENTE]` SMS: incluir o Brasil na SMS allowlist (padrão só EUA e Canadá) e custo por mensagem
  (ADR_024). A ADR_024 propõe TOTP + backup codes como base e SMS opcional `[INFERIDO]`.
- `[PENDENTE]` passkeys: se forem habilitados com "Passkeys satisfy multi-factor authentication",
  o login por passkey dispensa o 2º fator (ADR_024). Não desenhado.
- A ADR_031 (benefício de estudante, GitHub Student Developer Pack) ainda não está na pasta
  `Diagrama ADR`; aparece só como `[PENDENTE - ADR_031]` no `opt` de produção gratuita.

---

## Notas obrigatórias (pendências)

- **`[PENDENTE]`** código HTTP para sessão `"pending"`, organização não selecionada e usuário sem Tenant (401 × 403) — não definido nas ADRs.
- **`[PENDENTE]`** momento de criar o Tenant (contratação ou entrada na Organization) e chave "usuário" do Tenant (ADR_030).
- **`[PENDENTE]`** modo "Membership required" / `<TaskChooseOrganization />` (ADR_021/030).
- **`[PENDENTE]`** encaminhamento do usuário sem Tenant para o produto (contratação/Assinatura).
- **`[PENDENTE]`** SMS: Brasil na allowlist e custo por SMS (ADR_024).
- **`[PENDENTE]`** limite de tentativas e bloqueio para código de 2º fator inválido — não definido nas ADRs.
- **`[PENDENTE]`** canal/processo de suporte e verificação de identidade antes do reset de MFA (ADR_024).
- **`[PENDENTE]`** critério de migração para o Pro: produção no Hobby sem MFA, 2FA só parcial (ADR_027).
- **`[PENDENTE]`** ADR_031 (proposta): benefício de estudante / Pro sem custo, em avaliação.
- **`[PENDENTE]`** framework Java (encaixe do filtro) e React final, Vite ou Next.js (ADR_022/026).
- Nenhuma API foi inventada: só aparecem `AuthenticateRequest.authenticateRequest`, `requestState.isSignedIn()/claims()`,
  `getToken()`, `OrganizationMemberships updateMetadata`, `disableUserMFA()`, os webhooks `user.*` e os componentes
  `@clerk/react` citados nas ADRs. Endpoints da API REST do LhamaLog não foram nomeados.

**Rastreabilidade:** ADR_021–030 (`Documentações > Diagrama ADR`), `resumo_clerk.md` e `resumo_clerk_v2.md`.

**Renderização:** PNGs gerados com o mermaid-cli 12 (`mmdc`, tema neutral, fundo branco) e escala 2, com o mesmo ajuste de estilo preto e branco usado em `Varredura e Finder` (auto-mensagens, setas abertas e caixas retas).
