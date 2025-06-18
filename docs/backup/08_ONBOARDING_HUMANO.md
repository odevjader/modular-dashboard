# Guia de Onboarding para Devs - Modular Dashboard

Seja bem-vindo(a) ao projeto Modular Dashboard!

## Introdução

Este projeto visa criar uma plataforma web modular e versátil para auxiliar em tarefas complexas, utilizando Inteligência Artificial. Para uma visão completa dos objetivos, consulte o documento [00_VISAO_GERAL.md](./00_VISAO_GERAL.md).

O desenvolvimento do Modular Dashboard utiliza um **fluxo de trabalho colaborativo único**, envolvendo uma interação intensa entre **Devs (Desenvolvedores Humanos)** e diferentes tipos de Agentes de IA. Este guia tem como objetivo orientar você, novo Dev, sobre como navegar neste ambiente, entender seu papel crucial e colaborar eficazmente com as IAs e outros Devs.

## Filosofia de Trabalho

Acreditamos no potencial da IA para acelerar o desenvolvimento, gerar código padrão, auxiliar na documentação e explorar soluções. No entanto, reconhecemos que a IA ainda requer **direção estratégica, validação rigorosa e execução supervisionada por Devs**.

Neste modelo:
* **Devs focam em:** Definição de requisitos, estratégia, arquitetura, tomada de decisões complexas, revisão crítica, testes funcionais, garantia de qualidade, gerenciamento Git, coordenação entre equipes e resolução de problemas complexos.
* **IAs (Maestro e Coders) focam em:** Execução de tarefas bem definidas sob supervisão, geração de código/config/docs (ou prompts para aplicá-los), análise de contexto, sugestão de soluções pontuais.

Seu papel é fundamental para **orquestrar, executar, validar e comunicar** o trabalho das IAs e garantir a integração coesa no projeto.

## Papéis Principais no Ecossistema

Para entender como operar, familiarize-se com os papéis definidos em detalhes no [07_FLUXO_TRABALHO_DEV.md](./07_FLUXO_TRABALHO_DEV.md). Um resumo rápido:

* **Dev (Você!):** O centro da comunicação e execução. Você interage com o Maestro IA (planejamento/docs) e com os Agentes IA Coders (implementação). Você executa comandos de terminal, opera a ferramenta RooCode no VS Code para aplicar mudanças de arquivo (baseado em prompts do Maestro ou do Coder Tipo 2), supervisiona o Coder Tipo 1, gerencia o Git e valida tudo.
* **Maestro IA:** Orquestrador e coordenador de documentação. Planeja tarefas, gera prompts de tarefa para Coders, analisa sumários, gera prompts RooCode **apenas para atualizações de documentação**, sugere commits. Não executa ações. Onboarding: `.prompts/01_ONBOARDING_MAESTRO.md`.
* **Agente IA Coder (Tipo 1 - Integrado/RooCode):** **Opção Primária.** Roda no VS Code, lê/escreve arquivos diretamente, pode rodar comandos no terminal. Recebe tarefa, implementa, interage com Dev no IDE, gera sumário. Não gera prompts RooCode. Onboarding: `.prompts/02_ONBOARDING_ROOCODE.md`.
* **Agente IA Coder (Tipo 2 - Chat):** **Opção Alternativa.** Roda em chat externo, sem acesso direto. Recebe tarefa, pede contexto (`code <path>`), gera texto de código/config, **gera prompts RooCode** para aplicar o código/config, gera comandos de terminal (para Dev executar), gera sumário. Onboarding: `.prompts/03_ONBOARDING_CODER.md`.
* **RooCode (Ferramenta VS Code):** Além de ser o Coder Tipo 1, atua como a **ferramenta** que executa os prompts `Action/Path/Content` gerados pelo Maestro (para docs) ou pelo Coder Tipo 2 (para código/config), aplicando as mudanças no workspace quando instruída pelo Dev.

## Seu Papel Detalhado e Responsabilidades como Dev

Suas principais atividades serão:

1.  **Configurar o Ambiente:** Siga **rigorosamente** o [Guia de Setup de Desenvolvimento](./02_SETUP_DESENVOLVIMENTO.md).
2.  **Entender o Contexto:** Leia a documentação essencial ([00_VISAO_GERAL.md](./00_VISAO_GERAL.md), [01_ARQUITETURA.md](./01_ARQUITETURA.md), [03_ESTRUTURA_PASTAS.md](./03_ESTRUTURA_PASTAS.md), e **crucialmente**, [07_FLUXO_TRABALHO_DEV.md](./07_FLUXO_TRABALHO_DEV.md)).
3.  **Coordenar com Outros Devs:** (Se aplicável) Alinhe tarefas via quadro ou comunicação.
4.  **Gerenciar seu Fluxo Git:** Siga **rigorosamente** a estratégia em [07_FLUXO_TRABALHO_DEV.md](./07_FLUXO_TRABALHO_DEV.md) (Feature Branch, Rebase, Commits Frequentes, Push, PRs). Use sugestões de commit do Maestro.
5.  **Interagir com o Maestro IA:** Inicie sessões, defina objetivos, confirme branch, receba prompts de tarefa para Coders, repasse Sumários Finais dos Coders, receba prompts RooCode para **atualizar documentação**, receba sugestões de commit. Forneça feedback sobre o processo.
6.  **Interagir com o Agente IA Coder (Depende do Tipo):**
    * **Com Coder Tipo 1 (RooCode):** Forneça o prompt da tarefa (gerado pelo Maestro). Supervisione as ações diretas dele no VS Code (leitura/escrita de arquivos, execução de terminal). Teste as mudanças localmente. Forneça feedback claro e direto na interface do RooCode. Receba o Sumário Final.
    * **Com Coder Tipo 2 (Chat):** Forneça o prompt da tarefa. Forneça conteúdo de arquivos (`code <path>`) quando solicitado. Receba o texto do código/config E os **prompts RooCode** gerados por ele. Receba comandos de terminal gerados por ele. **Execute** os comandos de terminal. **Execute** os prompts RooCode (usando a ferramenta RooCode no VS Code) para aplicar o código/config. Teste. Forneça feedback/resultados no chat. Receba o Sumário Final.
7.  **Usar a Ferramenta RooCode (VS Code):** Copie e cole os prompts formatados (`Action/Path/Content` com `---START/END---`) fornecidos **pelo Maestro IA** (para docs) ou **pelo Coder Tipo 2** (para código/config) na interface do RooCode para que ele execute as operações de arquivo no seu workspace. Verifique sempre o `Relative Path`.

## Primeiros Passos (Checklist para Novos Devs)

1.  [ ] Leia este guia (`08_ONBOARDING_HUMANO.md`, ou como for renomeado) completamente.
2.  [ ] Configure seu ambiente local seguindo **cuidadosamente** o `docs/02_SETUP_DESENVOLVIMENTO.md`.
3.  [ ] Leia a documentação essencial (`README.md`, `docs/00_...`, `docs/01_...`, `docs/03_...`, **`docs/07_FLUXO_TRABALHO_DEV.md`**).
4.  [ ] (Se aplicável) Entre em contato com outros **Devs**. Apresente-se, entenda tarefas atuais, alinhe sua contribuição.
5.  [ ] Crie seu primeiro feature branch (`git checkout -b seu_nome/feature/<tarefa-inicial>`).
6.  [ ] Prepare uma instância de IA para ser seu **Maestro IA** (use o prompt `.prompts/01_ONBOARDING_MAESTRO.md`).
7.  [ ] Informe ao Maestro IA o objetivo da tarefa e o branch. Siga as instruções dele para gerar o prompt para um AI Coder.
8.  [ ] Prepare uma instância de IA para ser seu **Agente IA Coder** (Preferencialmente **Tipo 1 - RooCode**, usando `.prompts/02_ONBOARDING_ROOCODE.md`; ou como alternativa **Tipo 2 - Chat**, usando `.prompts/03_ONBOARDING_CODER.md`). Forneça o prompt da tarefa específica gerado pelo Maestro. Comece a interação!

## Dicas Importantes

* **Seja Crítico(a) e Atento(a):** Revise **sempre** o código e os prompts/ações das IAs. Você é o controle de qualidade. Questione a lógica. Verifique caminhos de arquivo.
* **Feedback Claro para IA:** Feedback específico (logs completos!) acelera a correção.
* **Comunicação Humana:** Mantenha outros **Devs** informados.
* **Paciência e Adaptação:** O fluxo é experimental e em evolução. Sugira melhorias!

## Onde Obter Ajuda

* Consulte a documentação (`docs/`, `.prompts/`).
* Converse com seu Maestro IA (processo, contexto).
* Converse com seu Agente IA Coder (dúvidas técnicas da tarefa).
* Entre em contato com outros **Devs** (dúvidas estratégicas, problemas complexos).
* Use os canais de comunicação da equipe.

Bem-vindo(a) novamente e boa colaboração neste projeto inovador!