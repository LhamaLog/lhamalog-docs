# Tenant e Multi-tenant — modelo SaaS pool (LhamaLog)

**Versão 1 (11/10/2026, Michel Bocchi Junior).** Decisões registradas nas ADR_121 a ADR_124 (pasta `Documentações > Diagrama ADR`).
Substitui o modelo hierárquico hash → metadata da ADR_105 para usuários; a ideia de hash + metadata fica só para máquinas
(`TokenApi`). Marcações: `[PENDENTE]` sem definição; `[INFERIDO]` ligação feita por nós a partir das decisões.

## 1. O que é o tenant

- **Tenant = a empresa cliente**, e só ela. Espelha a **Organization da Clerk** (`clerkOrgId`).
- Nasce na **compra da assinatura**: o Core cria `Tenant` + `Assinatura` + Organization na Clerk, e o comprador vira `Membro` com papel **DONO**.
- **Todo documento no MongoDB e todo log no Elasticsearch carrega `tenantId`.** Toda consulta passa por uma **camada centralizada do Core** que aplica o filtro `tenantId` — nenhum módulo consulta sem ele.
- Modelo **pool**: um único banco e as mesmas coleções para todos os tenants, isolados pelo `tenantId` (sem banco por cliente).

## 2. Coleções e relacionamentos (ER)

| Coleção | Campos principais | Observação |
|---|---|---|
| `Tenant` | tenantId, clerkOrgId, nome, status | 1 por empresa cliente |
| `Assinatura` | tenantId, plano, status, limites (IA, retenção, créditos) | downgrade = trocar só este documento (ADR_124) |
| `Membro` | tenantId, clerkUserId, papel (DONO, ADMIN, MEMBRO) | papel por pessoa, no nosso banco (ADR_123) |
| `Produto` | tenantId, config | |
| `AcessoProduto` | membroId, produtoId | só para MEMBRO; DONO e ADMIN veem todos |
| `Produtor` | producerId, tenantId, produtoId | um Produto tem vários produtores (ADR_115) |
| `TokenApi` | producerId, token cifrado (AES-256-GCM), hash SHA-256, revokedAt | máquinas; busca pelo hash (ADR_113) |

```mermaid
erDiagram
    TENANT ||--|| ASSINATURA : possui
    TENANT ||--o{ MEMBRO : tem
    TENANT ||--o{ PRODUTO : tem
    MEMBRO ||--o{ ACESSOPRODUTO : recebe
    PRODUTO ||--o{ ACESSOPRODUTO : libera
    PRODUTO ||--o{ PRODUTOR : tem
    PRODUTOR ||--o{ TOKENAPI : usa
    TENANT {
        string tenantId
        string clerkOrgId
        string nome
        string status
    }
    ASSINATURA {
        string tenantId
        string plano
        string status
        object limites
    }
    MEMBRO {
        string tenantId
        string clerkUserId
        string papel
    }
    PRODUTO {
        string tenantId
        object config
    }
    ACESSOPRODUTO {
        string membroId
        string produtoId
    }
    PRODUTOR {
        string producerId
        string tenantId
        string produtoId
    }
    TOKENAPI {
        string producerId
        string tokenCifrado
        string hashSha256
        date revokedAt
    }
```

Os demais documentos do sistema (`Arquivo`, lote, `Ocorrencia`, `Sugestao`, `Notificacao`, histórico de execuções, chaves
de lock, `BancoVetorial`) também levam `tenantId` (e `produtoId` quando aplicável) `[INFERIDO — lista completa a revisar no DER]`.

## 3. Modelo antigo × novo — as 7 falhas corrigidas

| # | Falha do modelo hash → metadata (ADR_105) | Como o modelo pool resolve |
|---|---|---|
| 1 | Permissões espalhadas na metadata de cada hash | Papel no `Membro` e acesso no `AcessoProduto`, coleções próprias |
| 2 | enterpriseId e productId duplicados em várias entradas | Um `tenantId` e referências por id; nada repetido em metadata |
| 3 | Downgrade difícil (mexer em várias entradas) | Downgrade = alterar só a `Assinatura` (ADR_124) |
| 4 | Sem um `tenantId` único para isolar dados | `tenantId` em todo documento/log + filtro centralizado no Core |
| 5 | Usuários e máquinas misturados na mesma tabela | Usuários em `Membro`; máquinas em `Produtor`/`TokenApi` |
| 6 | Sem papel por pessoa | `Membro.papel` = DONO, ADMIN ou MEMBRO |
| 7 | Desalinhado com a Clerk | Tenant = Organization; org:admin ↔ DONO/ADMIN, org:member ↔ MEMBRO |

## 4. Cadeia de validação por requisição de usuário

1. **Identidade (Clerk):** session token válido → `clerkUserId` e `clerkOrgId` (Organization ativa) (ADR_022/032).
2. **Tenant + papel (`Membro`):** `Tenant` pelo `clerkOrgId`; `Membro` pelo (tenantId, clerkUserId) → papel.
3. **Acesso ao Produto (`AcessoProduto`):** MEMBRO precisa do registro; DONO/ADMIN veem todos.
4. **Limites (`Assinatura`):** status e limites do plano (IA, retenção, créditos).
5. **Filtro `tenantId`:** a consulta sai da camada centralizada do Core sempre com `tenantId`.

Máquinas (OTel Collector) não passam pela Clerk: Bearer → SHA-256 → `TokenApi` → `Produtor` → tenantId + produtoId → `Assinatura`.
Serviços internos (Coletor, Varredura, Finder, Ocorrência) recebem o `tenantId` no item da fila e no JWT interno (ADR_028) `[INFERIDO]`.

## 5. Como cada módulo obtém e valida o tenant

| Módulo / ponto | Como obtém o tenantId | Como valida | Diagrama |
|---|---|---|---|
| Core / API Core (Backend Java) | session token da Clerk → clerkOrgId → `Tenant` | cadeia completa (seção 4); filtro centralizado | tenant_requisicao_usuario |
| Auth / webhooks da Clerk | `organization.*` e `organizationMembership.*` → clerkOrgId | assinatura do webhook `[PENDENTE — Svix]`; Tenant existente | tenant_convite_promocao_membro |
| Assinatura | criada com o Tenant na compra | só DONO altera `[INFERIDO]`; gateway de pagamento `[PENDENTE]` | tenant_criacao_assinatura, tenant_downgrade_plano |
| Coletor — ingestão OTLP | Bearer → SHA-256 → `TokenApi` → `Produtor` | token não revogado; Assinatura ativa; cota `[PENDENTE]` | tenant_ingestao_coletor |
| Upload Manual | cadeia do usuário no Core; repassado ao Coletor no JWT interno `[INFERIDO]` | AcessoProduto ao Produto do card | tenant_upload_manual |
| Varredura | tenantId + produtoId no item da `FilaDesordenada` do Produto | item coerente com o Produto `[INFERIDO]` | tenant_varredura_finder |
| Finder | tenantId no item da `FilaOrdenada` | consultas ao Elasticsearch e ao BancoVetorial filtradas por tenant/Produto | tenant_varredura_finder |
| Ocorrência | tenantId do `ResumoAnalise` | cria Ocorrências com tenantId; APIs de consulta pela cadeia do usuário | tenant_ocorrencia_sugestao |
| Sugestão por IA (automática/manual, BYOK, Créditos) | automática: tenantId da Ocorrência; manual: cadeia do usuário | `Assinatura.limites.IA` + `produtoAtivouIA`; Créditos do tenant; chave BYOK do tenant `[PENDENTE — coleção]` | tenant_ocorrencia_sugestao |
| Notificações / WebSocket | conexão WebSocket validada pela Clerk → tenantId + membroId | envio só para conexões do mesmo tenant com acesso ao Produto | tenant_notificacao_websocket |
| Gestão de tokens | cadeia do usuário (DONO/ADMIN) | Produto do tenant; `Produtor` + `TokenApi` | tenant_produtor_token |
| Convite / promoção de membros | cadeia do usuário (DONO/ADMIN) | regras da ADR_114; limite de 20 membros/org da Clerk | tenant_convite_promocao_membro |
| Health (`GET /health`, grpc.health.v1) | não usa tenant | público, sem token (ADR_118) | — |

## 6. Clerk — decisão de custo (ADR_123)

- **Organizations gratuitas** da Clerk: até 100 organizações retidas por mês (MRO), 20 membros por organização, papéis Admin/Member e convites (fonte: https://clerk.com/pricing).
- **MFA** pelo plano Clerk Student do GitHub Student Developer Pack: limites do Pro, grátis enquanto o estudante estiver verificado, um único workspace, sem SMS (fonte: https://clerk.com/github-student-developer-pack).
- **Sem o add-on B2B Enhanced** (US$ 85–100/mês, papéis customizados): os papéis ficam na nossa coleção `Membro`; org:admin ↔ DONO/ADMIN, org:member ↔ MEMBRO.
- **Vigiar** os limites de 20 membros por organização e 100 MRO. `[PENDENTE]` MFA por organização não confirmado (a configuração parece ser do app inteiro).

---

## Criação do tenant na compra da assinatura

Arquivo: `tenant_criacao_assinatura.png`

```mermaid
sequenceDiagram
    actor Comprador
    participant Front as Front Web (React + Clerk)
    participant Clerk
    participant Core as Backend Java / API Core
    participant Pag as Gateway de Pagamento [PENDENTE - provedor]
    participant Mongo as MongoDB (Tenant / Assinatura / Membro)

    Note over Comprador,Clerk: pre-condicao: comprador com conta na Clerk (sign-up), ainda sem Organization
    Comprador->>Front: escolhe o plano e compra a assinatura
    Front->>Core: POST compra (session token da Clerk)
    Core->>Clerk: valida o session token -- clerkUserId
    Core->>Pag: cobra o plano
    Pag-->>Core: pagamento aprovado
    Core->>Clerk: cria a Organization (nome da empresa) com o comprador como org:admin
    Clerk-->>Core: clerkOrgId
    Core->>Mongo: cria Tenant (tenantId, clerkOrgId, nome, status ATIVO) (ADR_121)
    Core->>Mongo: cria Assinatura (tenantId, plano, status ATIVA, limites: IA, retencao, creditos) (ADR_122)
    Core->>Mongo: cria Membro (tenantId, clerkUserId, papel DONO) (ADR_122/123)
    Core-->>Front: assinatura ativa -- usuario entra na Organization
    Note over Core,Mongo: as tres gravacoes sao uma unidade [INFERIDO - transacao MongoDB ou compensacao]

    alt FA-01: pagamento recusado
        Pag-->>Core: recusado
        Core-->>Front: erro de pagamento -- nada e criado
    else FA-02: falha ao criar a Organization na Clerk
        Clerk-->>Core: erro
        Core->>Core: estorna ou reprocessa [PENDENTE - compensacao]
        Core-->>Front: erro -- tente novamente
    else FA-03: limite de 100 organizacoes retidas por mes do plano gratuito da Clerk (ADR_123)
        Clerk-->>Core: limite atingido [PENDENTE - comportamento exato da Clerk]
        Core-->>Front: cadastro temporariamente indisponivel -- alerta interno para a equipe
    end
```

## Cadeia de validação por requisição de usuário

Arquivo: `tenant_requisicao_usuario.png`

```mermaid
sequenceDiagram
    actor Usuario
    participant Front as Front Web (React + Clerk)
    participant Core as Backend Java / API Core
    participant Clerk
    participant Mongo as MongoDB (Membro / AcessoProduto / Assinatura)
    participant Repo as Camada de dados do Core (filtro tenantId)

    Usuario->>Front: acao num Produto (ex.: listar Ocorrencias)
    Front->>Core: requisicao com o session token da Clerk (Organization ativa)
    Note over Core,Repo: cadeia de validacao por requisicao (ADR_121)
    Core->>Clerk: 1. identidade -- authenticateRequest(): clerkUserId + clerkOrgId (claim o) (ADR_022/032)
    Core->>Mongo: Tenant pelo clerkOrgId -- tenantId
    Core->>Mongo: 2. Membro (tenantId, clerkUserId) -- papel DONO, ADMIN ou MEMBRO
    Core->>Mongo: 3. AcessoProduto (membroId, produtoId) -- DONO e ADMIN veem todos
    Core->>Mongo: 4. Assinatura do tenantId -- status e limites (IA, retencao, creditos)
    Core->>Repo: 5. consulta SEMPRE com tenantId no filtro (camada centralizada)
    Repo-->>Core: so documentos do tenant
    Core-->>Front: resposta

    alt FA-01: session token invalido ou expirado (ADR_032)
        Core-->>Front: 401 -- volta ao login
    else FA-02: usuario nao e Membro do tenant da Organization ativa
        Core-->>Front: 403 de acesso [PENDENTE - revogar sessoes como na ADR_032 ou negacao simples]
    else FA-03: MEMBRO sem AcessoProduto para o Produto
        Core-->>Front: acesso negado ao Produto -- negacao simples (como ADR_109)
    else FA-04: Assinatura inativa ou limite do plano atingido
        Core-->>Front: bloqueio do recurso + aviso de plano
    end
```

## Convite e promoção de membro

Arquivo: `tenant_convite_promocao_membro.png`

```mermaid
sequenceDiagram
    actor Admin as DONO ou ADMIN
    participant Core as Backend Java / API Core
    participant Clerk
    participant Mongo as MongoDB (Membro / AcessoProduto)
    actor Convidado

    Note over Admin,Core: so backend, sem telas (ADR_114) -- validacao pela cadeia da requisicao (tenant_requisicao_usuario)
    Admin->>Core: convidar email (papel desejado, produtos opcionais) [PENDENTE - rota]
    Core->>Mongo: papel do solicitante no tenantId
    alt DONO convida direto como ADMIN (ADR_114)
        Core->>Clerk: cria convite da Organization com role org:admin
    else ADMIN convida como MEMBRO (ADR_114)
        Core->>Clerk: cria convite da Organization com role org:member
    end
    Clerk-->>Convidado: email de convite (recurso gratuito de Organizations, ADR_123)
    Convidado->>Clerk: aceita o convite
    Clerk->>Core: webhook organizationMembership.created (assinado) [PENDENTE - verificacao Svix]
    Core->>Mongo: cria Membro (tenantId, clerkUserId, papel ADMIN ou MEMBRO)
    Core->>Mongo: cria AcessoProduto para os produtos indicados (so MEMBRO)

    opt promocao de MEMBRO a ADMIN (ADR_114)
        Admin->>Core: promover membro [PENDENTE - rota]
        Core->>Mongo: Membro.papel = ADMIN
        Core->>Clerk: atualiza role para org:admin (mapeamento ADR_123)
    end

    alt FA-01: solicitante e MEMBRO
        Core-->>Admin: acesso negado -- negacao simples (ADR_109)
    else FA-02: limite de 20 membros por Organization da Clerk gratuita (ADR_123)
        Clerk-->>Core: limite atingido
        Core-->>Admin: limite de membros atingido [PENDENTE - plano LhamaLog com mais membros]
    end
```

## Produtor e TokenApi

Arquivo: `tenant_produtor_token.png`

```mermaid
sequenceDiagram
    actor Admin as DONO ou ADMIN
    participant Core as Backend Java / API Core
    participant Mongo as MongoDB (Produtor / TokenApi)
    participant KMS as KMS / secret manager

    Note over Admin,Core: cadeia de validacao da requisicao -- so DONO ou ADMIN (ADR_109/121)
    Admin->>Core: cria token para o Produto (nome, modulo opcional)
    Core->>Mongo: Produto pertence ao tenantId? (filtro centralizado)
    Core->>Mongo: cria Produtor (producerId, tenantId, produtoId) (ADR_115/122)
    Core->>Core: gera o token Bearer aleatorio
    Core->>KMS: chave de cifragem
    Core->>Mongo: TokenApi (producerId, token cifrado AES-256-GCM, hash SHA-256, revokedAt nulo) (ADR_113/122)
    Core-->>Admin: token -- copiavel a qualquer momento (decifra sob demanda)
    Note over Core,Mongo: hash + metadata so para maquinas (TokenApi), nao para usuarios (ADR_121)

    opt revogacao
        Admin->>Core: revoga o token
        Core->>Mongo: TokenApi.revokedAt = agora
    end
```

## Ingestão OTLP no Coletor

Arquivo: `tenant_ingestao_coletor.png`

```mermaid
sequenceDiagram
    participant OtelCol as OTel Collector (cliente)
    participant Coletor
    participant Mongo as MongoDB (TokenApi / Produtor / Assinatura)
    participant ES as Elasticsearch (logs)
    participant Fila as FilaDesordenada do Produto

    OtelCol->>Coletor: POST /v1/logs ou /v1/traces (HTTP 4318 / gRPC 4317) -- Authorization: Bearer token (ADR_119)
    Coletor->>Coletor: SHA-256 do token
    Coletor->>Mongo: TokenApi pelo hash (revokedAt nulo) -- producerId
    Coletor->>Mongo: Produtor -- tenantId e produtoId (ADR_122)
    Coletor->>Mongo: Assinatura do tenantId -- ativa e dentro da cota [PENDENTE - cota de ingestao]
    Coletor->>ES: grava os logs com tenantId e produtoId (ADR_116/121)
    Coletor->>Fila: enfileira o Arquivo (tenantId, produtoId) (ADR_057)
    Coletor-->>OtelCol: 200 OK
    Note over Coletor,Mongo: cache do hash para producerId/tenantId [INFERIDO - com invalidacao na revogacao]

    alt FA-01: token inexistente ou revogado
        Coletor-->>OtelCol: 401 -- nao retentavel (ADR_118)
    else FA-02: Assinatura inativa ou cota excedida
        Coletor-->>OtelCol: recusa [PENDENTE - 403 ou 429]
    else FA-03: sobrecarga
        Coletor-->>OtelCol: 429 / 503 com Retry-After: 120 (ADR_120)
    end
```

## Upload manual

Arquivo: `tenant_upload_manual.png`

```mermaid
sequenceDiagram
    actor Usuario
    participant Core as Backend Java / API Core
    participant Coletor
    participant VarAPI as API da Varredura
    participant Fila as FilaOrdenada

    Usuario->>Core: POST /manual/upload no card do Produto (ADR_041/044)
    Core->>Core: cadeia de validacao (tenant_requisicao_usuario) -- tenantId, Membro, AcessoProduto
    Core->>Coletor: envia arquivos + tenantId + produtoId + membroId pela API interna com JWT proprio (ADR_028/042)
    Note over Core,Coletor: o tenantId vai em claim do JWT interno [INFERIDO]
    Coletor->>Coletor: protecao, normalizacao e lote -- tudo marcado com tenantId
    Coletor->>VarAPI: pede execId M-uuid (tenantId, produtoId) (ADR_075)
    Coletor->>Fila: enfileira o lote no fim da FilaOrdenada (tenantId, produtoId) (ADR_041)
    Core-->>Usuario: 202 Accepted (ADR_053)
    Note over Coletor,Fila: chave de lock lock:{tenantProduto}:{execId}:{loteId}:{arquivoId} (ADR_069) passa a usar tenantId:produtoId [INFERIDO]

    alt FA-01: MEMBRO sem acesso ao Produto
        Core-->>Usuario: acesso negado
    end
```

## Varredura e Finder

Arquivo: `tenant_varredura_finder.png`

```mermaid
sequenceDiagram
    participant Varredura
    participant FilaD as FilaDesordenada do Produto
    participant FilaO as FilaOrdenada
    participant Finder
    participant ES as Elasticsearch
    participant BV as BancoVetorial do Produto
    participant ModOcorr as Modulo de Ocorrencia

    Varredura->>FilaD: le os itens do Produto (tenantId, produtoId) (ADR_057)
    Varredura->>FilaO: ordena e enfileira -- cada item carrega tenantId
    Finder->>FilaO: consome item (tenantId, produtoId, execId, arquivoId) -- qualquer worker (ADR_065)
    Finder->>ES: le os logs filtrando por tenantId e produtoId
    Finder->>BV: consulta recorrencia isolada por Produto do tenant (ADR_074)
    Finder->>ModOcorr: ResumoAnalise com tenantId e produtoId (ADR_062)
    Finder->>Varredura: arquivo X da execucao Y finalizado (tenantId) (ADR_061/070)
    Note over Varredura,ModOcorr: servicos internos nao tem usuario -- o tenantId viaja no item da fila e no JWT interno (ADR_028) [INFERIDO]

    alt FA-01: item sem tenantId ou tenantId de Produto que nao confere
        Finder->>Finder: descarta e registra erro critico [INFERIDO]
    end
```

## Ocorrência e Sugestão por IA (BYOK e Créditos)

Arquivo: `tenant_ocorrencia_sugestao.png`

```mermaid
sequenceDiagram
    participant ModOcorr as Modulo de Ocorrencia
    participant Mongo as MongoDB (Ocorrencia / Sugestao / Assinatura)
    participant ModSug as Modulo de Sugestao
    participant Cred as Creditos do tenant
    participant Gw as GatewayLLMSugestao
    participant LLM as LLM (LhamaLog ou BYOK do tenant)

    ModOcorr->>Mongo: cria Ocorrencias com tenantId e produtoId (ADR_062)
    ModOcorr->>Mongo: Assinatura.limites.IA do tenantId e produtoAtivouIA (ADR_076/124)
    ModOcorr->>ModSug: Sugestao automatica (ocorrenciaId, tenantId)
    ModSug->>Cred: reserva de Creditos do tenantId (ADR_078/117)
    ModSug->>Mongo: chave BYOK do tenantId, se houver (ADR_080) [PENDENTE - colecao da chave BYOK]
    ModSug->>Gw: solicitar(prompt mascarado)
    Gw->>LLM: chamada com a chave do LhamaLog ou do tenant
    LLM-->>Gw: resposta
    ModSug->>Mongo: Sugestao (tenantId, ocorrenciaId, AGUARDANDO_REVISAO) (ADR_096)
    Note over ModOcorr,LLM: Sugestao manual: entra pela cadeia de validacao do usuario (tenant_requisicao_usuario) e segue igual

    alt FA-01: plano sem IA ou Produto sem IA
        ModOcorr->>ModOcorr: notificacao OCORRENCIA sem Sugestao (ADR_081)
    else FA-02: Creditos insuficientes do tenant
        ModSug-->>ModOcorr: FALHA (ADR_077) -- manual: 402 (ADR_092)
    end
```

## Notificações e WebSocket

Arquivo: `tenant_notificacao_websocket.png`

```mermaid
sequenceDiagram
    participant Origem as Coletor / Varredura / Ocorrencia
    participant Core as Backend Java / API Core
    participant Mongo as MongoDB (Membro / AcessoProduto / Notificacao)
    participant WS as WebSocket (Core)
    actor Usuario

    Usuario->>WS: conecta com o session token da Clerk
    WS->>Core: valida identidade e Membro -- associa a conexao a tenantId + membroId (ADR_121)
    Origem->>Core: evento (tenantId, produtoId, tipo) pela API interna (ADR_028/051)
    Core->>Mongo: destinatarios: Membros do tenantId com AcessoProduto ao Produto (DONO/ADMIN sempre)
    Core->>Mongo: grava Notificacao com tenantId (historico 3 meses, ADR_071)
    Core->>WS: envia so para conexoes do mesmo tenantId
    WS-->>Usuario: alerta
    Note over Core,WS: push e email so para Ocorrencias, estados criticos e alertas do sistema (ADR_060)<br/>destinatarios por papel [PENDENTE]
```

## Downgrade / troca de plano

Arquivo: `tenant_downgrade_plano.png`

```mermaid
sequenceDiagram
    actor Dono as DONO
    participant Core as Backend Java / API Core
    participant Pag as Gateway de Pagamento
    participant Mongo as MongoDB (Assinatura / Produto)

    Dono->>Core: troca o plano (cadeia de validacao -- so DONO [INFERIDO])
    Core->>Pag: altera a cobranca
    Pag-->>Core: confirmado
    Core->>Mongo: atualiza SO a Assinatura do tenantId (plano, limites) (ADR_124)
    Note over Core,Mongo: nada muda em Tenant, Membro, Produto ou TokenApi -- os limites sao lidos da Assinatura em cada requisicao
    opt plano novo sem IA (ADR_076)
        Core->>Mongo: produtoAtivouIA = false em todos os Produtos do tenant
    end
    opt plano novo com menos Produtos ou membros que os atuais
        Core->>Core: [PENDENTE - bloquear excedentes ou impedir o downgrade]
    end
    opt retencao menor (ADR_104)
        Core->>Core: expurgo pelo novo prazo [PENDENTE - rotina]
    end
```

---

## Pendências

- **`[PENDENTE]`** gateway de pagamento e compensação se a criação da Organization falhar após o pagamento.
- **`[PENDENTE]`** comportamento da Clerk ao atingir 100 MRO; plano do LhamaLog para empresas com mais de 20 membros.
- **`[PENDENTE]`** MFA por organização (parece ser do app inteiro).
- **`[PENDENTE]`** verificação dos webhooks da Clerk (Svix) e eventos usados.
- **`[PENDENTE]`** rotas de convite e promoção (ADR_114).
- **`[PENDENTE]`** 403 com revogação de sessões (ADR_032) × negação simples quando o usuário não é Membro do tenant.
- **`[PENDENTE]`** cota de ingestão por plano e código de recusa (403 ou 429).
- **`[PENDENTE]`** coleção da chave BYOK do tenant.
- **`[PENDENTE]`** downgrade com Produtos/membros acima do novo limite; expurgo pela nova retenção.
- **`[PENDENTE]`** destinatários de notificação por papel.
- **`[INFERIDO]`** tenantId no JWT interno e nos itens das filas; chave de lock passa a usar tenantId:produtoId (ADR_069).
- **`[INFERIDO]`** gravação de Tenant + Assinatura + Membro como uma unidade (transação ou compensação).
- **`[INFERIDO]`** cache hash → producerId/tenantId no Coletor, invalidado na revogação.
- **`[INFERIDO]`** só o DONO troca o plano.
- **`[PENDENTE]`** atualizar DER, Modelo de Classes e os .md dos outros fluxos que citam a tabela de tenant da ADR_105 (Ingestão de Telemetria, Upload Manual, Varredura e Finder).

**Rastreabilidade:** ADR_022, 028, 030, 032, 041–075, 076, 078, 080, 104, 105, 109, 113–120 e ADR_121–124.

**Renderização:** PNGs com o mermaid-cli (`mmdc`, tema neutral, fundo branco), escala 2.
