# Guia de Onboarding para Colaboradores Humanos - Modular Dashboard

Seja bem-vindo(a) ao projeto Modular Dashboard!

## Introdução

Este projeto visa criar uma plataforma web modular e inteligente para auxiliar em tarefas complexas, utilizando Inteligência Artificial. Para uma visão completa dos objetivos, consulte o documento [00_VISAO_GERAL.md](./00_VISAO_GERAL.md).

O desenvolvimento do Modular Dashboard utiliza um **fluxo de trabalho colaborativo único**, envolvendo uma interação intensa entre Usuários Humanos e diferentes tipos de Agentes de IA (Inteligência Artificial). Este guia tem como objetivo orientar você, novo colaborador humano, sobre como navegar neste ambiente, entender seu papel crucial e colaborar eficazmente com as IAs e outros humanos.

## Filosofia de Trabalho

Acreditamos no potencial da IA para acelerar o desenvolvimento, gerar código padrão, auxiliar na documentação e explorar soluções. No entanto, reconhecemos que a IA ainda requer **direção estratégica, validação rigorosa e execução supervisionada por humanos**.

Neste modelo:
* **Humanos focam em:** Definição de requisitos, estratégia, arquitetura de alto nível, tomada de decisões complexas, revisão crítica de código/documentação, testes funcionais, garantia de qualidade, gerenciamento de projeto/Git, coordenação entre equipes e resolução de problemas complexos ou ambíguos.
* **IAs (Maestro e Coders) focam em:** Execução de tarefas bem definidas sob supervisão, geração de código/configuração/docs, análise de contexto (com base na documentação), sugestão de soluções pontuais.

Seu papel é fundamental para **orquestrar, executar, validar e comunicar** o trabalho das IAs e garantir a integração coesa no projeto.

## Papéis Principais no Ecossistema

Para entender como operar, familiarize-se com os papéis definidos em detalhes no [07_FLUXO_TRABALHO_DEV.md](./07_FLUXO_TRABALHO_DEV.md). Um resumo rápido:

* **Usuário Humano (Você!):** O centro da comunicação e execução. Você interage com o Maestro IA para planejamento/orquestração/docs e com os Agentes IA Coders para implementação/teste. Você executa todos os comandos (terminal, Roo) e gerencia o fluxo Git da sua linha de trabalho (branch, PRs). Você é o validador final da qualidade e funcionalidade.
* **Maestro IA:** Seu principal assistente de IA para orquestração e documentação. Ele ajuda a planejar tarefas, gera prompts para os Coders, analisa sumários dos Coders, gera prompts para atualizar a documentação oficial e mantém o contexto geral do projeto. Ele *não* escreve código de aplicação. Você o inicializa usando o prompt em `.prompts/01_ONBOARDING_MAESTRO.md`.
* **Agente IA Coder:** Instâncias de IA focadas em implementar tarefas técnicas específicas, definidas pelo Maestro. Geram código, prompts Roo (para código) e comandos de terminal (para sua tarefa). Interagem com você para teste/feedback e geram um sumário ao final para o Maestro. Você os inicializa usando o prompt em `.prompts/02_ONBOARDING_CODER.md`.
* **Roo:** Ferramenta local que executa operações de arquivo (criar, sobrescrever, anexar) com base em prompts formatados gerados pelas IAs e fornecidos por você.

## Seu Papel Detalhado e Responsabilidades

Como colaborador humano neste projeto, suas principais atividades serão:

1.  **Configurar o Ambiente:** Siga **rigorosamente** o [Guia de Setup de Desenvolvimento](./02_SETUP_DESENVOLVIMENTO.md) para configurar Docker, Node, Python, Git e clonar o projeto. Crie seu arquivo `backend/.env` pessoal (não commitado).
2.  **Entender o Contexto:** Leia a documentação essencial para entender os objetivos ([00_VISAO_GERAL.md](./00_VISAO_GERAL.md)), a arquitetura ([01_ARQUITETURA.md](./01_ARQUITETURA.md)), a estrutura ([03_ESTRUTURA_PASTAS.md](./03_ESTRUTURA_PASTAS.md)) e, **crucialmente**, o fluxo de trabalho detalhado ([07_FLUXO_TRABALHO_DEV.md](./07_FLUXO_TRABALHO_DEV.md)).
3.  **Coordenar com Outros Humanos:** (Se aplicável) Utilize o quadro de tarefas ou canais de comunicação definidos para alinhar em quais tarefas/módulos você trabalhará, evitando sobreposição e conhecendo as dependências.
4.  **Gerenciar seu Fluxo Git:** Siga **rigorosamente** a estratégia de versionamento descrita em [07_FLUXO_TRABALHO_DEV.md](./07_FLUXO_TRABALHO_DEV.md) (Seção "Colaboração Multi-Usuário e Versionamento"):
    * Crie sempre um **feature branch** para sua tarefa (`git checkout -b seu_nome/feature/nome-tarefa`).
    * Mantenha seu branch **atualizado** com a `main` usando `git pull origin main --rebase`. Faça isso frequentemente.
    * Faça **commits frequentes e atômicos** no seu branch (use as sugestões de mensagem do Maestro/Coder ou crie as suas seguindo o padrão Conventional Commits).
    * Faça **push** do seu branch regularmente para o GitHub (`git push origin seu_branch`).
    * Use **Pull Requests (PRs)** para integrar suas mudanças à `main`. Aguarde revisão e aprovação. Resolva conflitos no seu branch antes do merge.
5.  **Interagir com o Maestro IA:**
    * Inicie a sessão usando o prompt de onboarding (`.prompts/01_...`).
    * Defina o objetivo da sessão e confirme o branch de trabalho atual.
    * Receba a proposta de tarefa(s) e o(s) prompt(s) detalhado(s) para o(s) AI Coder(s).
    * Repasse o **Sumário Final do Coder** para o Maestro IA.
    * Receba prompts Roo para criar/atualizar a **documentação oficial**. Execute-os.
    * Receba sugestões de mensagens de commit ao final da sessão.
    * Forneça feedback sobre o processo e o contexto geral do projeto.
6.  **Interagir com o Agente IA Coder:**
    * Forneça o prompt da tarefa específica (gerado pelo Maestro).
    * **Execute** os prompts Roo gerados pelo Coder para aplicar código/config no seu ambiente local.
    * **Execute** os comandos de terminal gerados pelo Coder no seu ambiente local.
    * **Teste** as funcionalidades implementadas pelo Coder conforme as instruções dele ou seus próprios critérios.
    * Forneça **feedback claro e direto** (sucesso, erros completos, logs relevantes, sugestões) ao Coder para permitir a iteração e correção. Seja paciente no ciclo de teste-feedback.
    * Ao final, receba o **"Sumário Final para Orquestrador"** do Coder e repasse-o integralmente para o Maestro IA.
7.  **Usar a Ferramenta Roo:** Copie e cole **exatamente** os prompts formatados (`Action:`, `Relative Path:`, `Content:`) fornecidos pelas IAs (Maestro para docs, Coder para código/config) na interface do Roo para que ele execute as operações de arquivo no seu ambiente local. **Sempre verifique o `Relative Path`** para garantir que o arquivo correto será afetado.

## Primeiros Passos (Checklist para Novos Humanos)

1.  [ ] Leia este guia (`08_ONBOARDING_HUMANO.md`) completamente.
2.  [ ] Configure seu ambiente de desenvolvimento local seguindo **cuidadosamente** o `docs/02_SETUP_DESENVOLVIMENTO.md`. Garanta que consegue rodar o projeto.
3.  [ ] Leia os seguintes documentos essenciais para entender o projeto e o fluxo de trabalho:
    * `README.md`
    * `docs/00_VISAO_GERAL.md`
    * `docs/01_ARQUITETURA.md`
    * `docs/03_ESTRUTURA_PASTAS.md`
    * **`docs/07_FLUXO_TRABALHO_DEV.md` (Fundamental! Leia e Releia!)**
4.  [ ] (Se aplicável) Entre em contato com outros colaboradores humanos. Apresente-se, entenda o quadro de tarefas atual e alinhe sua primeira contribuição.
5.  [ ] Crie seu primeiro feature branch no Git (`git checkout -b seu_nome/feature/tarefa-inicial`).
6.  [ ] Prepare uma instância de IA para ser seu **Maestro IA**. Inicie a sessão com ela utilizando o prompt de `.prompts/01_ONBOARDING_MAESTRO.md`.
7.  [ ] Informe ao seu Maestro IA o objetivo da sua tarefa inicial e o branch que você criou. Siga as instruções dele para planejar a tarefa e gerar o primeiro prompt para um AI Coder.
8.  [ ] Prepare uma instância de IA para ser seu **Agente IA Coder**. Quando receber o prompt do Maestro, inicialize o Coder usando `.prompts/02_ONBOARDING_CODER.md` e então forneça o prompt da tarefa específica. Comece a interação!

## Dicas Importantes

* **Seja Crítico(a) e Atento(a):** As IAs são ferramentas poderosas, mas não são perfeitas e não têm bom senso intrínseco. **Sempre revise** o código, os prompts Roo e os comandos de terminal gerados antes de executá-los. Verifique os caminhos de arquivo nos prompts Roo. Questione a lógica da IA se algo parecer incorreto ou perigoso. **Você é o controle de qualidade final.**
* **Feedback Claro para IA:** Quanto mais claro, específico e contextualizado for seu feedback (especialmente logs de erro completos), mais rápido e eficazmente as IAs poderão ajudar ou corrigir rotas.
* **Comunicação Humana:** A coordenação entre humanos é vital neste modelo. Mantenha os outros informados sobre seu progresso em tarefas maiores, dependências e bloqueios.
* **Paciência e Adaptação:** Este é um fluxo de trabalho experimental e em evolução. Haverá momentos de frustração e momentos de produtividade incrível. Esteja aberto(a) a aprender, adaptar-se e a **sugerir melhorias no processo** com base na sua experiência.

## Onde Obter Ajuda

* Consulte a documentação existente na pasta `docs/` e `.prompts/`.
* Converse com seu Maestro IA sobre dúvidas de processo, contexto geral ou planejamento de tarefas.
* Converse com seu Agente IA Coder sobre dúvidas técnicas específicas da tarefa que ele está implementando.
* Entre em contato com outros colaboradores humanos para dúvidas estratégicas, problemas complexos de integração, ou questões que as IAs não conseguem resolver.
* Utilize os canais de comunicação definidos pela equipe (ex: chat, quadro de tarefas).

Bem-vindo(a) novamente e boa colaboração neste projeto inovador!