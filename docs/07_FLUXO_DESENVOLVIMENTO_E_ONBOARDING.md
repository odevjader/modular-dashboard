# docs/07_FLUXO_DESENVOLVIMENTO_E_ONBOARDING.md
# Guia de Fluxo de Desenvolvimento Híbrido IA e Onboarding

## Introdução ao Projeto e à Colaboração Humano-IA

Bem-vindo(a) ao projeto dashboard-adv! Nosso objetivo é criar uma plataforma web modular e versátil, utilizando Inteligência Artificial para acelerar e otimizar o desenvolvimento. Para uma visão completa dos objetivos, consulte o documento `docs/00_VISAO_GERAL.md`.

Este projeto adota um **fluxo de trabalho híbrido**, onde Desenvolvedores Humanos (Devs) colaboram estrategicamente com agentes de IA. Acreditamos que a IA pode potencializar o desenvolvimento, mas a direção estratégica, validação rigorosa e supervisão humana são indispensáveis. Os Devs focam na definição de requisitos, arquitetura, decisões críticas, revisão de código, testes e garantia de qualidade, enquanto os Agentes de IA auxiliam na execução de tarefas bem definidas.

Este guia detalha esse fluxo de trabalho, os papéis de cada um e como você, Desenvolvedor Humano, pode se integrar eficazmente.

## Papéis no Ecossistema de Desenvolvimento

1.  **Maestro IA (Orquestrador):**
    *   **Responsabilidades:** Mantém o contexto global do projeto, auxilia no planejamento do roadmap e na criação de tarefas detalhadas para o Google Jules. Gera documentação de alto nível e interage com os Devs para refinar requisitos.
    *   **Limitações:** Não tem acesso em tempo real às mudanças de código no repositório.

2.  **Google Jules (Agente de Desenvolvimento Primário):**
    *   **Responsabilidades:** Principal agente de desenvolvimento autônomo, operando em um ambiente de máquina virtual (VM) seguro e isolado. Recebe tarefas do Maestro IA (ou do Dev em nome do Maestro).
    *   **Interação Chave do Dev:** Fornecer prompts iniciais claros e detalhados para as tarefas, revisar e aprovar os planos de execução propostos por Jules.

3.  **IA Coder Local (Agente de Desenvolvimento Secundário):**
    *   **Responsabilidades:** Opera diretamente na máquina local do Desenvolvedor Humano.
    *   **Casos de Uso:** Debugging em ambiente local, pequenas refatorações com impacto local, integração com ferramentas específicas do desenvolvedor, ou para experimentação rápida. O Dev orienta e utiliza este agente conforme a necessidade.

4.  **Desenvolvedor Humano (Dev):**
    *   **Responsabilidades:** O elo central, responsável pela estratégia, supervisão, validação e garantia de qualidade. Define os requisitos macro, aprova os planos do Jules, valida o código gerado, gerencia o ciclo de feedback, e realiza a integração final do código.

## Fluxo de Desenvolvimento Detalhado

O processo de desenvolvimento é projetado para maximizar a eficiência da colaboração Humano-IA.

### 1. Recebimento e Preparação da Tarefa
*   O Maestro IA (ou o Dev) define uma tarefa, que é registrada como uma Issue no GitHub (conforme `docs/06_GESTAO_PROJETOS.md`).
*   O Dev garante que o Google Jules tenha um prompt claro e todos os detalhes necessários para a tarefa.

### 2. Execução pelo Google Jules
1.  **Análise e Planejamento:** Jules analisa a tarefa e o código base relevante em seu ambiente VM.
2.  **Proposta de Plano:** Jules gera um plano de execução detalhado, que o Desenvolvedor Humano deve revisar e aprovar. Ajustes podem ser solicitados antes da aprovação.
3.  **Desenvolvimento:** Após a aprovação do plano, Jules executa as modificações no código, adição de testes, etc.
4.  **Commit e Push:** Jules faz commits granulares das alterações em uma nova branch dedicada, geralmente chamada `jules` (ou um nome específico para a tarefa, ex: `jules/issue-123`), e envia (push) para o repositório GitHub.

### 3. Ciclo de Validação do Código do Jules pelo Desenvolvedor Humano
Este ciclo é crucial para garantir a qualidade e a correta integração do código:
1.  **Notificação e Obtenção do Código:** O Dev é notificado que Jules enviou o código.
    *   Execute `git fetch origin` para buscar as atualizações remotas.
    *   Execute `git checkout <nome_da_branch_do_jules>` (ex: `git checkout jules`).
2.  **Teste e Validação Local:**
    *   Revise o código.
    *   Compile o projeto e execute todos os testes automatizados (unitários, integração, etc.).
    *   Valide manualmente se a funcionalidade implementada atende aos requisitos e se integra corretamente.
3.  **Feedback e Correção (Iterativo):**
    *   **Se forem necessárias correções:** Forneça feedback detalhado ao Google Jules (via interface acordada), especificando as alterações ou ajustes.
    *   Jules processa o feedback, realiza as correções e gera novos commits na **mesma branch**.
    *   Repita os passos 1 (fetch/checkout da mesma branch, pois Jules pode ter feito `force push` após rebase ou amend) e 2. Este ciclo continua até a aprovação.
4.  **Merge e Limpeza da Branch:**
    *   **Após a aprovação:** Integre o código na branch de trabalho principal (ex: `main` ou `develop`).
        *   `git checkout <branch_principal>`
        *   `git merge <nome_da_branch_do_jules> --no-ff` (Recomenda-se `--no-ff` para manter o histórico de que o trabalho veio de uma feature branch).
        *   `git push origin <branch_principal>`
    *   Após o merge bem-sucedido, delete a branch do Jules:
        *   `git push origin --delete <nome_da_branch_do_jules>` (deleta a branch remota).
        *   `git branch -d <nome_da_branch_do_jules>` (deleta a branch local).

### 4. Uso do IA Coder Local
*   Para tarefas específicas (debug, prototipagem rápida), o Dev pode utilizar o IA Coder Local. O trabalho gerado deve ser integrado manualmente pelo Dev, seguindo as boas práticas de versionamento.

## Onboarding para Novos Desenvolvedores

Para começar a contribuir efetivamente:

1.  **Configuração do Ambiente:**
    *   Siga o guia em `docs/02_CONFIGURACAO_AMBIENTE.md` para configurar seu ambiente de desenvolvimento local.
2.  **Documentação Essencial:**
    *   Leia e familiarize-se com os seguintes documentos:
        *   `README.md` (visão geral do projeto e como executá-lo)
        *   `docs/00_VISAO_GERAL.md` (objetivos e escopo do projeto)
        *   `docs/01_ARQUITETURA.md` (detalhes da arquitetura da solução)
        *   `docs/06_GESTAO_PROJETOS.md` (como as tarefas são gerenciadas)
        *   Este guia (`docs/07_FLUXO_DESENVOLVIMENTO_E_ONBOARDING.md`)
3.  **Primeiros Passos no Projeto:**
    *   [ ] Comunique-se com o Maestro IA ou o líder técnico para receber sua primeira tarefa.
    *   [ ] Certifique-se de que a tarefa está bem definida como uma Issue no GitHub.
    *   [ ] Crie seu feature branch a partir da branch principal.
    *   [ ] Se a tarefa envolver o Google Jules, prepare um prompt claro e detalhado.
    *   [ ] Esteja pronto para revisar o plano de Jules e iniciar o ciclo de validação do código.

## Dicas para Colaboração Eficaz

*   **Comunicação Clara:** Detalhes precisos nos prompts e no feedback para o Jules (e outros agentes IA) são cruciais para o sucesso.
*   **Revisão Crítica:** Sempre revise cuidadosamente os planos e o código gerado pelas IAs. Você é o guardião da qualidade e da integridade do projeto.
*   **Paciência e Feedback Construtivo:** Este é um fluxo de trabalho em evolução. Seu feedback sobre o processo em si é valioso para aprimoramentos contínuos.
*   **Gerenciamento de Código:** Siga as práticas padrão de Git (branches significativas, commits atômicos e descritivos, Pull Requests bem documentados).

Bem-vindo(a) novamente! Estamos ansiosos pela sua contribuição para o dashboard-adv.
