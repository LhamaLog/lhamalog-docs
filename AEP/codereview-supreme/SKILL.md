---
name: codereview-supreme
description: Reviews and validates pull request code, uncommitted changes, and diffs in any programming language (backend and frontend). Finds bugs, security issues, inefficient code, and problems of readability, performance, and maintainability. Use when the user asks for code review, revisão de código, review de PR, análise de diff, código não commitado, CodeReview-Supreme, or when reviewing a pull request.
---

# CodeReview-Supreme

Skill utilizado para a revisão e validação de código de pull request. A skill deve trabalhar com qualquer tipo de código de programação (BackEnd e FrontEnd), deve encontrar bugs, código ineficientes e demais.

## Objetivo

Analisar DIffs enviadas, codigos não commitados e PR para realizar a revisão técnica de códigos, encontrado bugs, falhas, codigos ineficientes, legibilidade, performace e manuteilidade

## Instruções

Ao revisar o código:

1. Entenda primeiro a responsabilidade da classe, método ou módulo.
2. Não sugira mudanças apenas por preferência pessoal.
3. Priorize problemas que possam causar:
   - Bugs em produção
   - Falhas de segurança
   - Perda de dados
   - Exceções inesperadas
   - Problemas de concorrência
   - Problemas de performance
4. Verifique se o código segue os padrões existentes no projeto.
5. Evite sugerir refatorações grandes quando uma alteração simples resolver o problema.

## Escopo da análise

Identifique a fonte antes de revisar:

- **PR**: use o diff completo do pull request (`gh pr diff` ou equivalente), não só o último commit.
- **Não commitado**: use `git diff` e `git diff --staged`, incluindo arquivos novos.
- **Diff enviada**: revise exatamente o trecho fornecido; não invente contexto fora do diff.

Revise backend e frontend. Linguagem, framework ou camada não restringem o escopo.

## Classificação

Classifique todos os erros encotrados de forma que seja de simples e facil de compreender, também não sugira codigo apenas por preferencia.

Classifique cada problema encontrado como:

### Critical

Problema que pode causar:

- perda de dados;
- vulnerabilidade;
- indisponibilidade;
- comportamento incorreto grave.

### High

Problema relevante que pode gerar bugs ou manutenção difícil.

### Medium

Melhoria recomendável, mas sem impacto imediato significativo.

### Low

Melhoria pequena de legibilidade, organização ou consistência.

## Formato da revisão

Responda no idioma do usuário. Liste só problemas reais; omita severidades sem achados.

Para cada problema:

```markdown
### [Critical|High|Medium|Low] <título curto>

- **Onde:** `arquivo:linha` (símbolo ou trecho)
- **Problema:** o que está errado
- **Impacto:** o que pode acontecer
- **Correção:** alteração mínima suficiente (não refatore além do necessário)
```

Ordem: Critical → High → Medium → Low.

Ao final, um resumo:

- quantidade por severidade
- veredito: pode mergear / corrigir antes do merge / bloquear
