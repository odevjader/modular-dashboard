#docs/08_ONBOARDING_HUMANO.md
# Guia de Onboarding para Desenvolvedores Humanos - Modular Dashboard (Fluxo Híbrido IA)

Bem-vindo(a) ao projeto Modular Dashboard!

## Introdução

Este projeto visa criar uma plataforma web modular e versátil, utilizando Inteligência Artificial para acelerar e otimizar o desenvolvimento. Para uma visão completa dos objetivos, consulte o documento `docs/00_VISAO_GERAL.md`.

O desenvolvimento no Modular Dashboard adota um **fluxo de trabalho híbrido**, onde Desenvolvedores Humanos (Devs) colaboram estrategicamente com agentes de IA: o Maestro IA, o Google Jules (nosso agente de desenvolvimento primário) e um IA Coder secundário para tarefas locais.

Este guia irá orientá-lo(a) sobre como navegar neste ecossistema, entender seu papel crucial e colaborar eficazmente.

*(Última atualização: 29 de Maio de 2024)*

## Filosofia de Trabalho

Acreditamos que a IA pode potencializar o desenvolvimento, mas a direção estratégica, validação rigorosa e supervisão humana são indispensáveis.

*   **Desenvolvedores Humanos (Devs):** Focam na definição de requisitos, arquitetura, decisões críticas, revisão de código, testes, garantia de qualidade, e gerenciamento do ciclo de vida do código (incluindo o feedback e merge do trabalho do Google Jules).
*   **Agentes de IA:** Auxiliam na execução de tarefas bem definidas, geração de código, análise e documentação, sob a orientação e aprovação dos Devs.

## Papéis no Ecossistema de Desenvolvimento

1.  **Maestro IA (Orquestrador):**
    *   Responsável pelo planejamento de altoível, roadmap, e criação de tarefas detalhadas para o Google Jules.
    *   Interage com os Devs para refinar requisitos e comunicar planos.
    *   Não acessa o código diretamente em tempo real.

2.  **Google Jules (Agente de Desenvolvimento Primário):**
    *   Principal agente de desenvolvimento, operando em um ambiente VM seguro e isolado.
    *   **Seu Papel na Interação com Jules:**
        *   Fornecer prompts iniciais claros e detalhados para as tarefas atribuídas pelo Maestro IA.
        *   Revisar e aprovar os planos de execução propostos pelo Jules.
        *   Executar o ciclo de validação (fetch -> test -> feedback) do código que o Jules produz.

3.  **IA Coder (Agente de Desenvolvimento Secundário Local):**
    *   Opera na máquina local do Dev.
    *   Usado para tarefas que necessitam de acesso ao ambiente local, debug específico, ou prototipagem rápida.
    *   O Dev orienta e utiliza este agente conforme a necessidade.

4.  **Desenvolvedor Humano (Você!):**
    *   O elo central, responsável pela estratégia, supervisão e validação.
    *   Gerencia o fluxo de trabalho com todos os agentes de IA.
    *   Garante a qualidade e a integração do código final.

## Seu Papel Detalhado e Responsabilidades

1.  **Configuração do Ambiente:** Siga o `docs/02_SETUP_DESENVOLVIMENTO.md`.
2.  **Entendimento do Contexto:** Leia a documentação chave: `README.md`, `docs/00_VISAO_GERAL.md`, `docs/01_ARQUITETURA.md`, `docs/03_ESTRUTURA_PASTAS.md`, e crucialmente, o `docs/07_FLUXO_TRABALHO_DEV.md` que detalha o novo processo.
3.  **Interação com o Maestro IA:**
    *   Receber tarefas e briefings.
    *   Clarificar requisitos e fornecer contexto adicional quando solicitado.
4.  **Interação com Google Jules:**
    *   **Fornecer Prompts Claros:** Para cada tarefa vinda do Maestro IA, certifique-se de que o Jules tenha toda a informação necessária.
    *   **Revisão de Planos:** Analise cuidadosamente os planos de execução que o Jules propõe. Solicite ajustes antes de aprovar.
    *   **Ciclo de Validação do Código do Jules:**
        1.  Após o Jules enviar o código para a branch `jules`, faça `git fetch` e `git checkout jules`.
        2.  Compile, execute testes e valide a funcionalidade localmente.
        3.  Se encontrar problemas ou áreas para melhoria, forneça feedback detalhado ao Jules. Ele irá iterar sobre o código na mesma branch `jules`.
        4.  Repita o processo de teste e feedback até que o código esteja pronto para ser integrado.
        5.  Faça o merge da branch `jules` na branch principal e delete a branch `jules` (local e remotamente).
5.  **Uso do IA Coder Local:**
    *   Utilize para tarefas específicas que se beneficiem do acesso direto ao seu ambiente local.
    *   Integre o trabalho do IA Coder com o fluxo principal conforme apropriado.
6.  **Gerenciamento de Código e Versionamento:**
    *   Siga as práticas padrão de Git (branches, commits, PRs).
    *   Você é responsável pelo merge final do código validado do Jules.

## Primeiros Passos (Checklist para Novos Devs)

1.  [ ] Leia este guia (`docs/08_ONBOARDING_HUMANO.md`) completamente.
2.  [ ] Configure seu ambiente local (`docs/02_SETUP_DESENVOLVIMENTO.md`).
3.  [ ] Leia a documentação essencial mencionada acima, com foco no `docs/07_FLUXO_TRABALHO_DEV.md`.
4.  [ ] Crie seu primeiro feature branch para uma tarefa designada.
5.  [ ] Comunique-se com o Maestro IA para receber os detalhes da sua primeira tarefa para o Google Jules.
6.  [ ] Esteja preparado para revisar o plano do Jules e iniciar o ciclo de validação.

## Dicas Importantes

*   **Comunicação Clara:** Detalhes precisos nos prompts e no feedback para o Jules são cruciais.
*   **Revisão Crítica:** Sempre revise os planos e o código gerado pelas IAs. Você é o guardião da qualidade.
*   **Paciência e Colaboração:** Este é um fluxo de trabalho em evolução. Seu feedback sobre o processo é valioso.

Bem-vindo(a) novamente! Estamos ansiosos pela sua contribuição.
