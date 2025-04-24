#docs/08_PROJECT_MANAGEMENT.md
# Guia de Gestão de Projetos (Issues e Board)

Este documento descreve como utilizamos as GitHub Issues e o GitHub Project Board para gerenciar as tarefas de desenvolvimento do projeto Modular Dashboard.

*(Última atualização: 24 de Abril de 2025)*

## Visão Geral

Utilizamos uma abordagem baseada em Kanban para visualizar o fluxo de trabalho e Issues detalhadas para rastrear cada unidade de trabalho (bugs, features, tarefas internas, docs). O objetivo é manter um processo eficiente, simples e com boa rastreabilidade.

## GitHub Project Board

* **Nome:** Gestão Modular Dashboard
* **Tipo:** Board (Kanban)
* **Acesso:** Aba "Projects" no repositório GitHub.
* **Colunas:** O fluxo de trabalho é representado pelas seguintes colunas:
    * `Backlog`: Ideias e tarefas ainda não priorizadas ou detalhadas. Issues novas geralmente aparecem aqui ao serem vinculadas ao projeto.
    * `Ready`: Tarefas detalhadas, priorizadas e prontas para serem iniciadas pela equipe de desenvolvimento.
    * `In Progress`: Tarefas que estão sendo trabalhadas ativamente no momento por um membro da equipe (Dev + IAs).
    * `In Review`: Tarefas concluídas que aguardam revisão (geralmente associadas a um Pull Request aberto).
    * `Done`: Tarefas concluídas, revisadas e integradas ao código base (PR mergeado, Issue fechada).
* **Workflow:** Inicialmente, os cartões (Issues) são movidos manualmente entre as colunas pelo Dev conforme o progresso. Automações básicas (como mover para `Done` ao fechar Issue/PR) podem ser exploradas futuramente nas configurações do Project Board.

## GitHub Issues

* **Propósito:** Rastrear todas as unidades de trabalho: bugs, novas funcionalidades, melhorias, tarefas de documentação, configuração ou manutenção (`internal`). Cada Issue tem um número único (ex: `#1`, `#2`).
* **Criação de Issues:** Ao criar uma nova Issue:
    * **Título:** Deve ser claro, conciso e indicar o objetivo principal da tarefa (ex: "Setup Hybrid Project Management").
    * **Descrição (Corpo):** Explicar o objetivo, o contexto (por que é necessário?) e, idealmente, incluir uma seção `## Critérios de Aceite` com uma lista (markdown checklist ` - [ ] `) do que define a tarefa como concluída.
    * **Labels:** Aplicar uma ou mais labels relevantes para categorização e filtragem. As labels básicas definidas são:
        * `bug`: Erros ou comportamentos inesperados.
        * `feature`: Novas funcionalidades para o usuário final ou sistema.
        * `docs`: Tarefas relacionadas à escrita ou atualização da documentação.
        * `internal`: Manutenção, configuração, refatoração, ou outras tarefas internas que não são `bug` ou `feature`.
        * `backend`: Tarefa relacionada primariamente ao código do FastAPI.
        * `frontend`: Tarefa relacionada primariamente ao código React.
    * **Assignees:** Atribuir o Dev responsável pela execução da tarefa (opcional, mas recomendado).
    * **Projects:** Vincular a Issue ao projeto "Gestão Modular Dashboard" para que ela apareça no board.

## Vinculando Trabalho (Linking)

Para manter a rastreabilidade entre a tarefa, o código e os sumários, utilizamos o número da Issue (#<número>) da seguinte forma:

1.  **Mensagens de Commit:** Incluir a referência da Issue no final da mensagem do commit.
    * Formato: `git commit -m "tipo(escopo): Mensagem descritiva (#<numero_issue>)"`
    * Exemplo: `git commit -m "docs: Add project management guide (#2)"`

2.  **Pull Requests (PRs):** Mencionar a Issue que o PR resolve na descrição do PR, preferencialmente usando palavras-chave que o GitHub reconhece para fechamento automático.
    * Formato (na descrição): `Este PR implementa a funcionalidade X. Resolves #<numero_issue>.`
    * Exemplo: `Corrige o fluxo de login. Closes #42.`

3.  **Sumários de Tarefa (AI):** Incluir o número da Issue no nome do arquivo Markdown salvo pelo Dev no diretório `.logs/task_summaries/`.
    * Formato: `YYYY-MM-DD_HHMM_issue<numero_issue>_sumario_descritivo.md`
    * Exemplo: `2025-04-24_0900_issue2_sumario_setup_gestao.md`