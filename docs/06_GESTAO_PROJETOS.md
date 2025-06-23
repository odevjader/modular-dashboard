# docs/06_GESTAO_PROJETOS.md
# Gestão de Projetos com GitHub e IA

Este documento descreve a abordagem de gestão de projetos para o dashboard-adv, utilizando as ferramentas do GitHub (Issues, Project Boards) de forma integrada com o trabalho dos Agentes de IA e Desenvolvedores Humanos. O objetivo é manter um processo eficiente, transparente, com rastreabilidade e que sirva de memória para o projeto.

## GitHub Issues: A Fonte da Verdade para Tarefas

Todas as unidades de trabalho – sejam bugs, novas funcionalidades, melhorias, tarefas de documentação ou configurações internas – devem ser registradas como uma GitHub Issue. Cada Issue funciona como o ponto central de referência para uma tarefa específica.

**Ao criar uma Issue:**

*   **Título:** Deve ser claro, conciso e indicar o objetivo principal (ex: "Implementar autenticação de dois fatores").
*   **Descrição:** Detalhar o objetivo da tarefa, o contexto (por que é necessária?), e idealmente, o prompt inicial gerado pelo Maestro IA para os AI Coders (quando aplicável).
*   **Critérios de Aceite:** Incluir uma lista (usando markdown checklists ` - [ ] `) do que define a tarefa como concluída.
*   **Labels:** Aplicar uma ou mais labels relevantes para categorização e filtragem. Labels comuns incluem: `bug`, `feature`, `docs`, `internal`, `backend`, `frontend`, `ai-task`.
*   **Assignees:** Atribuir o desenvolvedor humano responsável pela supervisão e integração da tarefa.
*   **Projects:** Vincular a Issue ao Project Board "Gestão Modular Dashboard" para acompanhamento visual.

A seção de comentários da Issue é o local para discussões técnicas, registro de decisões e acompanhamento de bloqueios relacionados à tarefa.

## GitHub Project Board: Gerenciamento Visual do Fluxo

Utilizamos um GitHub Project Board no estilo Kanban para visualizar e gerenciar o fluxo de trabalho das Issues.

*   **Nome do Board:** Gestão Modular Dashboard
*   **Acesso:** Aba "Projects" no repositório GitHub.
*   **Colunas Principais:**
    *   `Backlog`: Ideias e tarefas ainda não priorizadas ou detalhadas.
    *   `Ready`: Tarefas detalhadas, priorizadas e prontas para serem iniciadas.
    *   `In Progress`: Tarefas que estão sendo trabalhadas ativamente (por Desenvolvedor Humano e/ou Agentes IA).
    *   `In Review`: Tarefas concluídas que aguardam revisão (geralmente associadas a um Pull Request aberto).
    *   `Done`: Tarefas concluídas, revisadas e integradas à base de código (Pull Request mergeado, Issue fechada).

As Issues são movidas entre as colunas conforme progridem, refletindo o status atual do desenvolvimento.

## Maestro IA: Orquestração e Suporte ao Processo

O Maestro IA desempenha um papel crucial na gestão:

*   Auxilia no planejamento, utilizando as Issues e o Project Board.
*   Analisa os sumários de tarefas gerados pelos AI Coders para manter o contexto e sugerir atualizações na documentação.
*   Orienta sobre o fluxo Git correto e sugere mensagens de commit padronizadas.

## Pull Requests (PRs) e Commits: Integração e Histórico

Todo o desenvolvimento é realizado em *feature branches* individuais. A integração com a branch principal (ex: `main` ou `master`) ocorre exclusivamente via Pull Requests (PRs) após revisão humana.

*   **Commits:** Devem ser frequentes, atômicos e seguir o padrão [Conventional Commits](https://www.conventionalcommits.org/). O Maestro IA pode auxiliar na formulação das mensagens de commit.
    *   **Vinculando Issues em Commits:** Incluir a referência da Issue no final da mensagem do commit. Ex: `git commit -m "feat(auth): Add JWT generation (#42)"`
*   **Pull Requests:**
    *   Devem ser vinculados às GitHub Issues correspondentes.
    *   O título e a descrição do PR devem ser claros. O Maestro IA pode sugerir o conteúdo inicial.
    *   Utilizar palavras-chave na descrição do PR para fechar Issues automaticamente ao fazer o merge (ex: `Resolves #42`, `Closes #42`, `Fixes #42`).

## Sumários de Tarefas da IA: Registro Técnico Detalhado

Ao final de cada tarefa significativa executada por um Agente IA Coder, um sumário técnico é gerado e salvo.

*   **Propósito:** Servem como um registro detalhado da implementação realizada pela IA (arquivos modificados, descrição das mudanças, resultados de testes/validações), atuando como uma "memória externa" para o Maestro IA e para consultas futuras.
*   **Localização:** Armazenados no diretório `.logs/task_summaries/` do repositório.
*   **Nomeação:** `YYYY-MM-DD_HHMM_issue<numero_issue>_sumario_descritivo.md` (ex: `2025-05-15_1430_issue42_sumario_jwt_auth.md`).
*   **Versionamento:** Estes sumários são versionados junto com o código no Git.

## Fluxo de Trabalho Integrado (Visão Geral)

1.  Uma nova tarefa é definida como uma **Issue** no GitHub.
2.  A Issue é priorizada e movida para `Ready` no **Project Board**.
3.  Um desenvolvedor (humano ou o Maestro IA) inicia a tarefa, criando um *feature branch* e movendo a Issue para `In Progress`.
4.  O trabalho é realizado no branch com **commits** regulares.
5.  Ao concluir a implementação, o Agente IA (se aplicável) gera um **Sumário de Tarefa**, que é salvo em `.logs/task_summaries/`.
6.  Um **Pull Request** é aberto, vinculando a **Issue** e detalhando as mudanças. A Issue é movida para `In Review`.
7.  Após a revisão e aprovação do PR, ele é mergeado à branch principal. A Issue é fechada e automaticamente (ou manualmente) movida para `Done`.

Esta abordagem visa garantir que todas as tarefas sejam rastreadas, o progresso seja visível e o conhecimento gerado (especialmente pelas IAs) seja preservado e acessível.
