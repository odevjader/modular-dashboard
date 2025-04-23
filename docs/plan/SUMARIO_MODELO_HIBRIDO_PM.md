# Sumário: Modelo Híbrido de Gestão de Projetos (Planejado)

Este documento resume a abordagem de gestão de projetos planejada para o Modular Dashboard, combinando ferramentas padrão do GitHub com um registro detalhado da execução das tarefas pelos Agentes de IA. O objetivo é fornecer clareza, rastreabilidade e persistência de contexto, especialmente em um ambiente multi-Dev.

*(Decisão tomada em: 23 de Abril de 2025)*

## Componentes Principais

O modelo híbrido se baseia na utilização integrada das seguintes ferramentas e processos:

1.  **GitHub Issues (Fonte da Verdade para Tarefas):**
    * **Uso:** Cada nova funcionalidade, bug, melhoria ou tarefa de documentação significativa **deve** ser registrada como uma GitHub Issue.
    * **Conteúdo:** A Issue deve conter uma descrição clara do objetivo, requisitos iniciais, critérios de aceitação e, se aplicável, o prompt inicial gerado pelo Maestro IA para o AI Coder.
    * **Discussão:** A thread de comentários da Issue é o local principal para discussões **entre Devs**, registro de decisões humanas e acompanhamento de bloqueios relacionados àquela tarefa específica.

2.  **GitHub Project Boards (Gerenciamento de Fluxo):**
    * **Uso:** Um Project Board (preferencialmente Kanban) será configurado no repositório para visualizar o fluxo de trabalho das Issues.
    * **Colunas (Exemplo):** `Backlog`, `Planejado (Maestro)`, `Em Andamento (Dev + Coder)`, `Revisão (PR Aberto)`, `Concluído`.
    * **Função:** Proporcionar visibilidade sobre o status de todas as tarefas, facilitar a coordenação entre Devs e permitir o acompanhamento do progresso geral do projeto ou de fases específicas do Roadmap.

3.  **Pasta `.logs/task_summaries/` (Registro Técnico da Execução IA):**
    * **Uso:** Armazenar os arquivos Markdown contendo os **"Sumários Finais para Orquestrador"** gerados pelos Agentes IA Coders ao final de cada tarefa concluída (ou sessão de trabalho).
    * **Nomeação:** Os arquivos devem seguir uma convenção clara (ex: `YYYY-MM-DD_branch-name_resumo-tarefa.md`).
    * **Conteúdo:** Captura os detalhes técnicos da implementação realizada pela IA (arquivos modificados, descrição das mudanças, resultados de validação, etc.), servindo como "memória externa" para o Maestro IA e para auditoria/consulta futura.
    * **Versionamento:** Estes sumários são versionados junto com o código no Git.

4.  **Pull Requests (PRs) e Commits (Integração e Histórico):**
    * **Uso:** Todo o trabalho de desenvolvimento é feito em **feature branches** individuais. A integração com a branch `master` ocorre **exclusivamente via Pull Requests** após revisão humana.
    * **Vinculação:** Os PRs **devem** ser vinculados às GitHub Issues correspondentes.
    * **Commits:** Devem ser frequentes, atômicos e seguir o padrão Conventional Commits dentro dos feature branches. O Maestro IA sugere mensagens de commit finais para as sessões.

5.  **Maestro IA (Conector e Guardião do Processo):**
    * **Papel:** Além de orquestrar as tarefas e a documentação, o Maestro IA auxilia na conexão entre esses componentes:
        * Usa as Issues e o Project Board para planejar as próximas tarefas.
        * Analisa os Sumários armazenados em `.logs/task_summaries/` para manter o contexto e gerar atualizações de documentação.
        * Lembra os Devs sobre o fluxo Git correto e sugere mensagens de commit padronizadas.
        * Ajuda a garantir que o processo definido em `docs/07_FLUXO_TRABALHO_DEV.md` seja seguido.

## Fluxo Integrado (Resumo)

1.  Tarefa é definida como uma **Issue**.
2.  Issue é movida para "Planejado" no **Board** e atribuída (Maestro planeja).
3.  Dev cria/entra no **feature branch**, move Issue para "Em Andamento".
4.  Dev e AI Coder trabalham na tarefa no branch, fazendo **commits frequentes**.
5.  Ao final, Coder gera **Sumário Final**.
6.  Maestro analisa Sumário, gera prompt para salvar o Sumário em `.logs/task_summaries/` e para atualizar docs oficiais. Dev aplica via RooCode.
7.  Dev faz commit final no branch, abre **PR** vinculado à **Issue**. Move Issue para "Revisão".
8.  Após revisão e aprovação, PR é mergeado. Issue é fechada e movida para "Concluído" no **Board**.

*(Este modelo será detalhado e formalizado no documento `docs/07_FLUXO_TRABALHO_DEV.md` quando iniciarmos a Fase 2 do Roadmap).*
