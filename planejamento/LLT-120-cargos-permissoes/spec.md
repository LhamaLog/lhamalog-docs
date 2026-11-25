# Escopo e critérios de aceite — LLT-120

## Itens da Feature

- LLT-169: catálogo de cargos e matriz de permissões (documentada na pasta da LLT-169).
- LLT-170: atribuir cargo a um usuário.
- LLT-171: restringir o acesso de usuários por produto.

## Base

Seguir as ADRs, sem a chave secreta da Clerk. Os papéis de acesso são **Dono, Administrador e Membro** (ADR_122 e ADR_123), e a Clerk continua só com `admin` e `member`. O Dono é o `member` com papel `DONO` da coleção da LLT-163. Quem atribui o Dono é o fluxo de compra (ADR_121; desde a LLT-289, a confirmação do pagamento). Esta entrega só lê esse papel.

## Histórias

1. **Saber o papel e o que ele permite (P1):** o Web consulta o papel da sessão e a matriz para desenhar as telas.
2. **Restringir o acesso de um Membro por produto (P1):** Dono e Administrador escolhem os produtos de cada Membro. A mudança vale na próxima requisição, sem novo login. Dono e Administrador acessam todos os produtos.
3. **Manter os cargos de notificação (P2):** Dono e Administrador criam, renomeiam, configuram e excluem cargos que decidem quem recebe cada alerta (ADR_136 a ADR_140). Cargos de notificação **não dão permissão de acesso**.
4. **Atribuir cargo a um usuário (P2):** incluir e tirar pessoas dos cargos de notificação.
5. **Proteger o Dono (P3):** o Dono nunca pode ser desativado pelo sistema.

## Regras principais

- A matriz é fixa no código, porque a ADR_123 descartou papéis de acesso customizáveis. Algumas permissões (convite e promoção pela Clerk, assinatura e acesso pendente) aparecem na matriz só para o Web desenhar as telas. O Core não as aplica nesta entrega.
- Membro sem acesso a um produto não o vê na lista, e o detalhe responde 404 (negação simples, ADR_126).
- Cargos padrão: Dono, Administrador, Gestor, Supervisor e Membro. Dono e Administrador recebem todos os alertas e não podem ser alterados. Gestor, Supervisor e Membro nascem com as listas vazias.
- Gravidades `ERROR`, `WARNING` e `INFO` (ADR_170). Tipos de alerta `OCCURRENCE`, `CRITICAL_STATE` e `SYSTEM_ALERT` (ADR_060).
- Desativar o Dono responde 403 com o código `owner_protected`.

## Fora do escopo

Transferir ou gravar o Dono, o acesso pendente (ADR_129 e ADR_135), a entrega dos alertas pelo módulo Notificação, a auditoria em tela, o limite de membros por plano e mudanças no convite (LLT-167).

## Pronto quando

- O papel, a matriz, o acesso por produto, os cargos de notificação e a proteção do Dono funcionam no Core, com testes verdes.
- Nenhum segredo da Clerk no repositório.
- As divergências com a matriz da LLT-169 estão registradas e levadas ao time.
