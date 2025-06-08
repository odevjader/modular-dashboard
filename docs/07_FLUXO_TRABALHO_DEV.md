#docs/07_FLUXO_TRABALHO_DEV.md
# Fluxo de Trabalho de Desenvolvimento (Híbrido IA)

Este documento descreve o modelo de desenvolvimento colaborativo Humano-IA para o projeto Modular Dashboard, envolvendo Desenvolvedores Humanos (Devs), o Maestro IA (Orquestrador de alto nível), Google Jules (Agente de desenvolvimento primário) e IA Coder (Agente de desenvolvimento secundário local).

*(Última atualização: 29 de Maio de 2024)*

## Filosofia e Papéis

A filosofia central é a colaboração eficiente entre humanos e IAs, onde cada um desempenha o papel para o qual é mais adequado.

1.  **Maestro IA (Orquestrador):**
    *   **Responsabilidades:** Mantém o contexto global do projeto, planeja o roadmap, cria tarefas detalhadas (como esta) para o Google Jules. Gera documentação de alto nível e auxilia no planejamento estratégico.
    *   **Limitações:** Não tem acesso em tempo real às mudanças de código no repositório. Baseia-se nos relatórios e no código enviado.

2.  **Google Jules (Agente de Desenvolvimento Primário):**
    *   **Responsabilidades:** Principal agente de desenvolvimento autônomo. Recebe tarefas do Maestro IA.
    *   **Fluxo de Trabalho Típico:**
        1.  Recebe uma tarefa detalhada.
        2.  Clona o repositório GitHub para um ambiente de máquina virtual (VM) seguro e isolado.
        3.  Analisa a tarefa e o código base relevante.
        4.  Gera um plano de execução detalhado para aprovação do Desenvolvedor Humano.
        5.  Após a aprovação, executa o plano, modificando o código, adicionando testes, e realizando outras ações necessárias.
        6.  Envia (push) as alterações para uma nova branch, tipicamente denominada `jules`, no repositório GitHub.
    *   **Interação:** Comunica o plano, progresso e resultados ao Desenvolvedor Humano para validação.

3.  **IA Coder (Agente de Desenvolvimento Secundário Local):**
    *   **Responsabilidades:** Opera diretamente na máquina local do Desenvolvedor Humano. Utilizado para tarefas que exigem acesso ao ambiente local específico do desenvolvedor, configurações particulares, ou para experimentação rápida que não necessita do ciclo completo de validação do Jules.
    *   **Casos de Uso:** Debugging em ambiente local, pequenas refatorações com impacto local, integração com ferramentas específicas do desenvolvedor.

4.  **Desenvolvedor Humano (Dev):**
    *   **Responsabilidades:** Ponto central de decisão e validação. Define os requisitos macro, aprova os planos do Jules, valida o código gerado pelo Jules, e gerencia o ciclo de feedback. Orienta o uso do IA Coder local.
    *   **Foco:** Revisão estratégica, garantia de qualidade, testes funcionais, integração final e merge do código.

## Fluxo de Validação do Desenvolvedor para o Código do Jules

Este fluxo é crucial para garantir a qualidade e a correta integração do código produzido pelo Google Jules.

1.  **Notificação e Checkout:** Após o Google Jules enviar o código para a branch `jules`, o Desenvolvedor Humano é notificado.
    *   O Desenvolvedor executa `git fetch origin` para buscar as atualizações remotas.
    *   Em seguida, executa `git checkout jules` para mudar para a branch do Jules.

2.  **Teste e Validação Local:**
    *   O Desenvolvedor revisa o código, executa os testes automatizados (unitários, integração, etc.).
    *   Valida se a funcionalidade implementada atende aos requisitos da tarefa e se integra corretamente ao restante do projeto.

3.  **Ciclo de Feedback e Correção (Se Necessário):**
    *   **Se forem necessárias correções:** O Desenvolvedor fornece feedback detalhado ao Google Jules, especificando as alterações ou ajustes requeridos.
    *   O Google Jules processa o feedback, realiza as correções e gera novos commits na **mesma branch `jules`**.
    *   Este ciclo de `git fetch`, teste local e feedback se repete até que o código seja aprovado pelo Desenvolvedor.

4.  **Merge e Limpeza:**
    *   **Após a aprovação:** O Desenvolvedor faz o merge da branch `jules` na branch de trabalho principal (ex: `main`, `develop`).
        *   `git checkout <branch_principal>`
        *   `git merge jules --no-ff` (Recomenda-se `--no-ff` para manter o histórico de que o trabalho veio de uma feature branch).
    *   Após o merge bem-sucedido e push da branch principal, a branch `jules` pode ser deletada:
        *   `git push origin --delete jules` (deleta a branch remota)
        *   `git branch -d jules` (deleta a branch local)

## Colaboração e Versionamento

*   **Commits:** O Google Jules fará commits granulares em sua branch `jules`.
*   **Branching:** A branch `jules` é dedicada ao trabalho do Google Jules para uma tarefa específica. O Desenvolvedor Humano integra esse trabalho na branch principal.
*   **Comunicação:** A comunicação clara entre o Maestro IA, Google Jules e o Desenvolvedor Humano é essencial, utilizando as ferramentas e plataformas acordadas.

*(Este documento reflete o fluxo de trabalho de desenvolvimento híbrido Humano-IA adotado pelo projeto Modular Dashboard).*
