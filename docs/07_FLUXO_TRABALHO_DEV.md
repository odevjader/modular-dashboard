# Fluxo de Trabalho de Desenvolvimento

Este documento descreve o modelo de desenvolvimento colaborativo utilizado no projeto Modular Dashboard, envolvendo a interação entre Usuários Humanos, o Maestro IA (Orquestrador & Coordenador), e Agentes IA Codificadores (principalmente Integrados como RooCode, ou alternativamente baseados em Chat), utilizando a ferramenta RooCode (no VS Code) para aplicar alterações de arquivo, em um ambiente potencialmente multi-usuário.

*(Última atualização: 22 de Abril de 2025, aprox. 14:30 -03)*

## Papéis e Responsabilidades

O desenvolvimento se baseia na colaboração entre as seguintes entidades:

1.  **Usuário (Humano):**
    * Define requisitos, coordena com outros humanos, toma decisões finais.
    * Gerencia o fluxo Git (Branches, Commits Frequentes, PRs, Merges).
    * **Executa comandos de terminal** (Docker, Git, etc.) conforme instruído pelas IAs ou necessário.
    * **Atua como interface principal com as IAs e Ferramentas:**
        * Interage com o Maestro IA para planejamento, contexto e recebimento de prompts (para Coders, para RooCode).
        * Interage com o Agente IA Coder para execução da tarefa e feedback.
        * **Opera a ferramenta RooCode (no VS Code):** Fornece a ela os prompts formatados (`Action/Path/Content`) gerados pelo **Maestro IA** para aplicar **todas** as mudanças de arquivo (código, config, docs) no workspace.
        * (Opcional) Opera a ferramenta Roo externa apenas como fallback se usar um Coder Tipo 2 (Chat).
    * Realiza testes funcionais e valida implementações.
    * Valida o "Sumário Final para Orquestrador" antes de repassá-lo ao Maestro IA.

2.  **Maestro IA (Orquestrador & Coordenador):**
    * Mantém contexto geral, planeja tarefas, sugere branches.
    * Gera **prompts detalhados de tarefa** para AIs Codificadores.
    * Analisa **"Sumários Finais para Orquestrador"** dos Coders e o código/config gerado (repassado pelo Usuário).
    * **Gera prompts RooCode (`Action/Path/Content`)** para o Usuário aplicar via RooCode:
        * As mudanças de **código/configuração** propostas pelo AI Coder (após análise/aprovação conceitual).
        * As atualizações na **documentação oficial** com base nos sumários.
    * Gera sumários de sessão e sugere **mensagens de commit**.
    * Auxilia na depuração de nível superior e na manutenção da documentação.
    * NÃO gera código de aplicação diretamente, nem executa comandos Git/RooCode/Terminal.
    * *Inicialização:* Via prompt `../.prompts/01_ONBOARDING_MAESTRO.md`.

3.  **Agente IA Coder (Dois Tipos):** Responsável pela implementação técnica de tarefas específicas.
    * **3.1. Tipo 1: Coder Integrado (Ex: RooCode no VS Code) - *Opção Primária***
        * **Capacidades:** Roda dentro do IDE; tem **acesso direto para ler arquivos** no workspace; pode **executar comandos no terminal integrado** (sob supervisão).
        * **Interação:** Recebe prompt de tarefa. Lê arquivos necessários **diretamente**. Gera **texto** de código/configuração. Executa/sugere comandos de terminal. Interage com Usuário no IDE para teste/feedback. Gera Sumário Final. **Não gera prompts Roo nem modifica arquivos diretamente** (aguarda instrução do Maestro via prompt RooCode).
        * *Inicialização:* Via prompt `../.prompts/02_ONBOARDING_CODER.md`. *(Nota: Este prompt precisa ser atualizado para remover a instrução de gerar prompts Roo).*
    * **3.2. Tipo 2: Coder Baseado em Chat (Ex: Gemini/Grok via Web/API) - *Opção Alternativa***
        * **Capacidades:** Sem acesso direto a arquivos/terminal.
        * **Interação:** Recebe prompt de tarefa. Pede contexto ao Usuário (`code <path>`). Gera **texto** de código/configuração. Gera **comandos de terminal** para o Usuário executar. Recebe feedback/resultados do Usuário. Gera Sumário Final. **Não gera prompts Roo** (Maestro IA gera para execução via Roo externo).
        * *Inicialização:* Via prompt `../.prompts/02_ONBOARDING_CODER.md`. *(Nota: Este prompt precisa ser atualizado para remover a instrução de gerar prompts Roo).*

    *(Nota Importante: O prompt de onboarding do Coder (`../.prompts/02_ONBOARDING_CODER.md`) precisará ser atualizado em breve para refletir que NENHUM Coder gera mais prompts Roo - apenas o Maestro IA o faz).*

4.  **RooCode (Ferramenta Integrada ao VS Code):**
    * **Uso:** Ferramenta **principal** para aplicar todas as alterações de arquivo (código, config, docs) no workspace do VS Code, quando instruída por um prompt `Action/Path/Content` fornecido pelo Usuário (gerado pelo Maestro IA).
    * **Interface:** Recebe prompts no formato `Action/Path/Content`.
    * **Execução:** Modifica/Cria arquivos diretamente no workspace com base no prompt recebido.

5.  **Roo (Ferramenta Externa Auxiliar):** *(Uso de Fallback)*
    * **Uso:** Necessário **apenas** se um **AI Coder Tipo 2 (Baseado em Chat)** estiver sendo usado *e* o RooCode não estiver disponível/funcional por algum motivo. Usado para aplicar prompts `Action/Path/Content` gerados pelo Maestro ou Coder Tipo 2.
    * Ponte segura entre prompts e o filesystem local do Usuário. Executa `Create File`, `Overwrite File`, `Append Lines` quando instruído por um prompt formatado.

## Colaboração Multi-Usuário e Versionamento (Git)

Trabalhar com múltiplos humanos (e seus times de IA) no mesmo projeto exige uma estratégia de versionamento clara e disciplinada para evitar caos e perda de trabalho. Adotaremos o seguinte fluxo baseado em **Feature Branches** e **Pull Requests**.

**Princípios:**
* **Isolamento:** O trabalho em cada nova funcionalidade, correção ou tarefa significativa é feito em um branch separado.
* **Atualização Contínua:** Mantenha seu branch atualizado com a base principal (`main`) para detectar e resolver conflitos cedo.
* **Revisão:** Integre o trabalho de volta à branch principal apenas após revisão (via Pull Request).
* **`main` Estável:** A branch `main` deve sempre refletir um estado estável e funcional do projeto.

**Fluxo Detalhado:**

1.  **Iniciar uma Nova Tarefa:**
    * **Coordenação Humana:** Verifique com outros usuários para alinhar tarefas.
    * **Sincronize `main`:** `git checkout main && git pull origin main`.
    * **Crie seu Feature Branch:** `git checkout -b <tipo>/<nome-descritivo>`.
    * **Informe o Maestro IA:** Comunique o branch ativo.

2.  **Desenvolver no Feature Branch:**
    * Siga o "Fluxo de Interação Típico" abaixo.
    * **Faça Commits Frequentes e Atômicos:** `git add <arquivos>` -> `git commit -m "tipo(escopo): Mensagem"`.
    * **Mantenha Atualizado (Pull com Rebase):** Periodicamente: `git pull origin main --rebase` (resolva conflitos se houver).
    * **Compartilhe Progresso (Push):** Regularmente: `git push origin <nome-do-seu-branch>`.

3.  **Concluindo a Tarefa e Integrando:**
    * **Finalize e Atualize:** Garanta tarefa completa, testada e branch atualizado com `main` via rebase.
    * **Push Final:** `git push origin <nome-do-seu-branch>`.
    * **Abra um Pull Request (PR):** No GitHub, do seu branch para `main`. Descreva claramente.
    * **Revisão do PR:** Aguarde revisão humana. Faça ajustes no branch e push se necessário.
    * **Merge:** Após aprovação, faça o merge (via interface GitHub).
    * **Limpeza (Opcional):** Apague branches local e remoto após o merge.

## Iniciando uma Sessão de Trabalho

Para garantir que o **Maestro IA** tenha o contexto necessário:

1.  **Sinalização:** Usuário informa ao Maestro IA o início da sessão.
2.  **Atualização e Branch:** Usuário garante repositório atualizado e entra no **feature branch** correto. Informa ao Maestro IA qual branch está ativo.
3.  **Contextualização:** Usuário direciona o Maestro IA para revisar docs chave (`README` Status, `ROADMAP`, Arquitetura, este Fluxo, Sumário anterior, etc.).
4.  **Definição de Objetivo:** Usuário define a(s) meta(s) da sessão.
5.  **Confirmação AI:** Maestro IA confirma entendimento.

## Fluxo de Interação Típico (Dentro de um Feature Branch - Revisado Final)

1.  **Definição da Tarefa (Maestro IA & Você):** Definimos a meta, eu gero o prompt para o Coder (adequado ao Tipo 1 ou Tipo 2).
2.  **Geração de Código/Solução (Você & AI Coder):** Você entrega o prompt ao Coder. Vocês iteram (Coder gera **texto** de código/config, pode gerar comandos de terminal, você testa/fornece contexto/feedback) até a solução em texto estar pronta.
3.  **Sumarização e Handoff (AI Coder -> Você -> Maestro IA):** Coder gera o "Sumário Final" + o **bloco final de código/config em texto**. Você cola ambos para mim.
4.  **Preparação para Aplicação (Maestro IA -> Você):** Eu analiso o sumário e o código/config. Se ok, eu gero o(s) **Prompt(s) RooCode (`Action/Path/Content`)** para aplicar o código/config.
5.  **Aplicação do Código/Config (Você -> RooCode):** Você executa o(s) prompt(s) no **RooCode** para modificar os arquivos do projeto. Confirma para mim. *(Nota: Se por acaso estiver usando Coder Tipo 2, você usaria o Roo externo aqui)*.
6.  **Atualização Docs (Maestro IA -> Você -> RooCode):** Eu gero o(s) **Prompt(s) RooCode** para atualizar a documentação. Você executa o(s) prompt(s) no **RooCode**. Confirma para mim. *(Nota: Se por acaso estiver usando Coder Tipo 2, você usaria o Roo externo aqui)*.
7.  **Teste Final/Validação (Você):** Você faz um teste final se necessário.
8.  **(Repetir Passos 1-7 se houver mais tarefas na sessão/branch)**

## Finalizando uma Sessão de Trabalho

Ao concluir uma sessão (pausando ou finalizando a tarefa no branch):

1.  **Sinalização:** Usuário informa ao Maestro IA o fim da sessão.
2.  **Sumário AI Coder (se aplicável):** Garantir que o sumário da última tarefa trabalhada foi recebido por mim.
3.  **Sumário Geral da Sessão (Maestro IA):** Eu forneço um resumo do que foi feito.
4.  **Atualização de Status (Maestro IA Gera, User Aplica/Verifica):** Eu gero texto para `README`/`ROADMAP`. Você aplica/verifica (via RooCode ou Roo externo) e commita no branch.
5.  **Sugestão de Commit (Maestro IA Gera):** Eu sugiro a mensagem para o(s) último(s) commit(s) da sessão no feature branch.
6.  **Versionamento (User Executa):** Usuário executa `git add .` (ou arquivos específicos), `git commit -m "..."` (usando sugestão ou própria) e `git push origin <nome-do-seu-branch>` para salvar o trabalho da sessão no remoto. O merge para `main` via PR acontece separadamente.

## Comunicação

* **Confirmações:** O uso de `OK` ou `K` pelo Usuário após receber instruções é útil para sinalizar entendimento. As IAs devem aguardar essa confirmação quando apropriado.
* **Clareza Técnica:** A comunicação deve ser precisa. As IAs (Maestro e Coder) devem fornecer nomes de arquivos, comandos e descrições exatas. Os prompts `Action/Path/Content` gerados pelo Maestro devem ser perfeitos.
* **Feedback:** O feedback do Usuário sobre o resultado das ações (testes, execução de comandos/prompts) é crucial para a iteração e correção.