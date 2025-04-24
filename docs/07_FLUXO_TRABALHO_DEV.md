#docs/07_FLUXO_TRABALHO_DEV.md
# Fluxo de Trabalho de Desenvolvimento

Este documento descreve o modelo de desenvolvimento colaborativo utilizado no projeto Modular Dashboard, envolvendo a interação entre Desenvolvedores (Devs) Humanos, o Maestro IA (Orquestrador & Coordenador), e Agentes IA Codificadores (Integrado ou Chat), utilizando a ferramenta RooCode (no VS Code) para aplicar alterações de arquivo, em um ambiente potencialmente multi-usuário.

*(Última atualização: 24 de Abril de 2025)*

## Papéis e Responsabilidades

O desenvolvimento se baseia na colaboração entre as seguintes entidades:

1.  **Dev (Desenvolvedor Humano):**
    * Defines requisitos, coordena com outros Devs, toma decisões finais.
    * Gerencia o fluxo Git (Branches, Commits Frequentes, PRs, Merges).
    * **Executa comandos de terminal** (Docker, Git, etc.) conforme instruído pelas IAs ou necessário.
    * **Atua como interface principal com as IAs e Ferramentas:**
        * Interage com o Maestro IA para planejamento, contexto e recebimento de prompts (para Coders, ou para aplicar atualizações de docs via RooCode). Solicitado a fornecer conteúdo de arquivos via comando `code <path>`.
        * Interage com o Agente IA Coder para execução da tarefa e feedback.
        * **Opera a ferramenta RooCode (no VS Code):** Fornece a ela os prompts formatados (`Action/Path/Content`) gerados pelo **Maestro IA** (para docs) ou pelo **AI Coder Tipo 2** (para código/config) para aplicar mudanças de arquivo no workspace. Supervisiona ações do Coder Tipo 1.
    * Realiza testes funcionais e valida implementações.
    * Valida o "Sumário Final para Orquestrador", salva-o em `.logs/task_summaries/` e então repassa o conteúdo ao Maestro IA.

2.  **Maestro IA (Orquestrador & Coordenador):**
    * Mantém contexto geral, planeja tarefas, sugere branches.
    * Solicita conteúdo de arquivos ao Dev usando o formato `code <caminho_do_arquivo>`.
    * Gera **prompts detalhados de tarefa** para AIs Codificadores.
    * Analisa **"Sumários Finais para Orquestrador"** dos Coders (fornecidos pelo Dev após salvamento) e o código/config gerado. Revisa conceitualmente os prompts RooCode gerados pelo Coder Tipo 2.
    * **Gera prompts no Formato Padrão RooCode (sem a linha `Content:`)** para o **Dev** aplicar via RooCode, especificamente para atualizações na **documentação oficial**.
    * Gera sumários de sessão e sugere **mensagens de commit**.
    * Auxilia na depuração de nível superior.
    * NÃO gera código de aplicação diretamente, nem executa comandos Git/RooCode/Terminal.
    * *Inicialização:* Via prompt `../.prompts/01_ONBOARDING_MAESTRO.md`.

3.  **Agente IA Coder (Dois Tipos):** Responsável pela implementação técnica de tarefas específicas.
    * **3.1. Tipo 1: Coder Integrado (Ex: RooCode no VS Code) - *Opção Primária***
        * **Capacidades:** Roda dentro do IDE; tem **acesso direto para ler e modificar arquivos** no workspace (código, config, documentação); pode **executar comandos no terminal integrado** (sob supervisão).
        * **Interação:** Recebe prompt de tarefa. Lê/Modifica arquivos **diretamente**. Executa/sugere comandos de terminal. Interage com Dev no IDE. Gera Sumário Final. **Aplica atualizações de documentação** diretamente, com base em instruções/conteúdo do Maestro (via Dev). **Não gera prompts no formato RooCode.**
        * *Inicialização:* Via prompt `../.prompts/02_ONBOARDING_ROOCODE.md`.
    * **3.2. Tipo 2: Coder Baseado em Chat (Ex: Gemini/Grok via Web/API) - *Opção Alternativa***
        * **Capacidades:** Sem acesso direto a arquivos/terminal.
        * **Interação:** Recebe prompt de tarefa. Pede contexto ao Dev (`code <path>`). Gera **texto** de código/configuração. **Gera prompts RooCode (`Action/Path/Content`)** para o Dev executar e aplicar suas mudanças de código/config. Gera **comandos de terminal** para o Dev executar. Recebe feedback/resultados do Dev. Gera Sumário Final.
        * *Inicialização:* Via prompt `../.prompts/03_ONBOARDING_CODER.md`.

4.  **RooCode (Ferramenta Integrada ao VS Code):**
    * **Uso:** Ferramenta **principal** para aplicar todas as alterações de arquivo (código, config, docs) no workspace do VS Code, quando instruída por um prompt `Action/Path/Content` fornecido pelo **Dev** (prompt gerado pelo **Maestro IA** para docs, ou pelo **AI Coder Tipo 2** para código/config). Também atua como **Agente IA Coder Tipo 1**.
    * **Interface:** Recebe prompts `Action/Path/Content` ou interage via chat/comandos no VS Code.
    * **Execução:** Modifica/Cria arquivos e pode executar comandos no terminal integrado.

## Formato Padrão de Prompt para RooCode (Gerado pelo Maestro IA ou Coder Tipo 2)

Para garantir clareza, execução correta pelo RooCode e facilitar a cópia pelo Dev, todos os prompts de modificação de arquivo gerados seguirão **exatamente** a estrutura abaixo.

**Estrutura:**

Linha 1: `Action: [Create File | Overwrite File | Append Lines]`
Linha 2: `Relative Path: [Caminho/Relativo/Do/Arquivo.ext]`
Linha 3: `--- START CONTENT ---`
Linha 4 em diante: Conteúdo completo e exato do arquivo, linha por linha.
                 *(A formatação interna do conteúdo é preservada).*
Última Linha + 1: `--- END CONTENT ---`

**Observações Cruciais:**

* O bloco de texto entre os marcadores `--- START CONTENT ---` e `--- END CONTENT ---` representa o **conteúdo literal e integral** a ser escrito no arquivo.
* **NÃO DEVE HAVER** delimitadores de bloco de código Markdown (como aspas triplas ```) em volta ou dentro deste conteúdo quando o prompt é gerado pelo Maestro ou Coder Tipo 2.
* O Maestro IA (ou Coder Tipo 2) apresentará o prompt completo dentro de um bloco ```text no chat apenas para facilitar a cópia pelo Dev. O que deve ser passado ao RooCode é o texto *dentro* desse bloco ```text.
* **Padrão de Primeira Linha:** Adicionalmente, todo arquivo criado ou modificado através deste fluxo deve ter como **primeira linha** um comentário contendo seu caminho relativo. O formato do comentário depende do tipo de arquivo (ex: `#docs/07_FLUXO_TRABALHO_DEV.md` para Markdown, `#backend/app/main.py` para Python/YAML, `//frontend/src/App.tsx` para TS/JS).

*(Esta padronização visa evitar os problemas de formatação/renderização encontrados anteriormente e garantir rastreabilidade).*

## Colaboração Multi-Usuário e Versionamento (Git)

Trabalhar com múltiplos Devs (e seus times de IA) no mesmo projeto exige uma estratégia de versionamento clara e disciplinada. Adotaremos o seguinte fluxo baseado em **Feature Branches** e **Pull Requests**.

**Princípios:**
* **Isolamento:** Trabalho em branches separados.
* **Atualização Contínua:** `git pull origin master --rebase` frequente no feature branch.
* **Revisão:** Integração via Pull Requests (PRs) com revisão humana.
* **`master` Estável:** Branch principal sempre funcional.

**Fluxo Detalhado:**

1.  **Iniciar uma Nova Tarefa:**
    * **Coordenação Humana:** Alinhar tarefas com outros Devs.
    * **Sincronize `master`:** `git checkout master && git pull origin master`.
    * **Crie seu Feature Branch:** `git checkout -b <tipo>/<nome-descritivo>`.
    * **Informe o Maestro IA:** Comunique o branch ativo.

2.  **Desenvolver no Feature Branch:**
    * Siga o "Fluxo de Interação Típico" abaixo:
    * **Commits Frequentes e Atômicos:** `git add <arquivos>` -> `git commit -m "tipo(escopo): Mensagem"`.
    * **Mantenha Atualizado (Rebase):** Periodicamente: `git pull origin master --rebase`.
    * **Compartilhe Progresso (Push):** Regularmente: `git push origin <nome-do-seu-branch>`.

3.  **Concluindo a Tarefa e Integrando:**
    * **Finalize e Atualize:** Garanta tarefa completa, testada e branch atualizado com `master` via rebase.
    * **Push Final:** `git push origin <nome-do-seu-branch>`.
    * **Abra um Pull Request (PR):** No GitHub, do seu branch para `master`. Descreva.
    * **Revisão do PR:** Aguarde revisão humana. Ajuste/Push se necessário.
    * **Merge:** Após aprovação, faça o merge via interface GitHub.
    * **Limpeza (Opcional):** Apague branches local e remoto.

## Iniciando uma Sessão de Trabalho

Para garantir que o **Maestro IA** tenha o contexto necessário:

1.  **Sinalização:** Dev informa ao Maestro IA o início da sessão.
2.  **Atualização e Branch:** Dev garante repositório atualizado e entra no **feature branch** correto. Informa ao Maestro IA qual branch está ativo.
3.  **Contextualização:** Dev direciona o Maestro IA para revisar docs chave e fornece conteúdo de arquivos quando solicitado via `code <path>`.
4.  **Definição de Objetivo:** Dev define a(s) meta(s) da sessão.
5.  **Confirmação AI:** Maestro IA confirma entendimento.

## Fluxo de Interação Típico (Dentro de um Feature Branch)

1.  **Definição da Tarefa (Maestro IA & Você):** Definimos a meta, eu gero o prompt para o Coder.
2.  **Geração de Código/Solução (Você & AI Coder):** Você entrega o prompt ao Coder. Vocês iteram até a solução estar pronta.
    * *Se Coder Tipo 1 (RooCode):* Ele lê/modifica arquivos e roda comandos diretamente no VS Code sob sua supervisão. Gera **texto** final do código/config (incluindo comentário na primeira linha).
    * *Se Coder Tipo 2 (Chat):* Ele gera **texto** de código/config (incluindo comentário na primeira linha), **prompts RooCode** para aplicar esse código/config, e **comandos de terminal**.
3.  **Sumarização, Salvamento e Handoff (AI Coder -> Você -> Maestro IA):** Coder (qualquer tipo) gera o "Sumário Final para Orquestrador". Se for Tipo 2, ele também fornece o(s) prompt(s) RooCode gerado(s) no passo anterior. **Você salva este sumário como um arquivo Markdown (`.md`) no diretório `.logs/task_summaries/` (use um nome descritivo, ex: `YYYY-MM-DD_HHMM_sumario_tarefa_X.md`)**. Em seguida, você cola o conteúdo do sumário (e os prompts RooCode, se aplicável) para mim analisar.
4.  **Análise do Maestro e Preparação Docs (Maestro IA -> Você):** Eu analiso o Sumário (e o prompt RooCode do Coder Tipo 2, se aplicável). Aprovo conceitualmente. Gero o(s) **Prompt(s) RooCode** para atualizar a **documentação** relevante para a tarefa concluída (garantindo o comentário na primeira linha e formato correto).
5.  **Aplicação das Mudanças (Você -> RooCode):**
    * Se Coder foi Tipo 1: Mudanças de código/config já foram aplicadas por ele no Passo 2. *(Maestro IA não gera prompt para aplicar código/config neste caso)*.
    * Se Coder foi Tipo 2: Você executa o(s) **prompt(s) RooCode gerados pelo Coder (no passo 3)** usando a ferramenta RooCode no VS Code para aplicar o código/config. Confirma para mim.
    * Em ambos os casos: Você executa o(s) **prompt(s) RooCode gerados pelo Maestro (no passo 4)** no RooCode para aplicar a documentação. Confirma para mim.
6.  **Teste Final/Validação (Você):** Você faz um teste final da funcionalidade completa.
7.  **(Repetir Passos 1-6 se houver mais tarefas na sessão/branch)**

## Finalizando uma Sessão de Trabalho

Ao concluir uma sessão (pausando ou finalizando a tarefa no branch):

1.  **Sinalização:** Dev informa ao Maestro IA o fim da sessão.
2.  **Sumário AI Coder (se aplicável):** Garantir que o sumário da última tarefa trabalhada foi recebido por mim (e salvo por você em `.logs/`).
3.  **Sumário Geral da Sessão (Maestro IA):** Eu forneço um resumo do que foi feito.
4.  **Atualização de Status (Maestro IA Gera, Dev Aplica/Verifica):** Eu gero o **conteúdo** (com comentário na 1ª linha) para atualizar `README`/`ROADMAP`. Você instrui o RooCode a aplicá-lo e commita no branch.
5.  **Sugestão de Commit (Maestro IA Gera):** Eu sugiro a mensagem para o(s) último(s) commit(s) da sessão no feature branch.
6.  **Versionamento (Dev Executa):** Dev executa `git add .` (ou arquivos específicos), `git commit -m "..."` (usando sugestão ou própria) e `git push origin <nome-do-seu-branch>`. O merge para `master` via PR acontece separadamente.

## Comunicação

* **Confirmações:** O uso de `OK` ou `K` pelo Dev após receber instruções é útil. As IAs devem aguardar.
* **Clareza Técnica:** Comunicação precisa é essencial. As IAs devem fornecer nomes de arquivos/comandos exatos. Os prompts `Action/Path/Content` (gerados pelo Maestro ou Coder Tipo 2) devem ser perfeitos (sem a linha `Content:`, com comentário apropriado na 1ª linha do conteúdo).
* **Solicitação de Arquivos (Maestro IA -> Dev):** Quando o Maestro IA precisar ler o conteúdo de um arquivo, ele solicitará usando o formato `code <caminho_do_arquivo>`. O Dev deve usar este comando para abrir rapidamente o arquivo no VS Code e facilitar a cópia do conteúdo para o Maestro.
* **Feedback:** O feedback do Dev sobre resultados é crucial para a iteração.