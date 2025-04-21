# Fluxo de Trabalho de Desenvolvimento

Este documento descreve o modelo de desenvolvimento colaborativo utilizado no projeto Modular Dashboard, envolvendo a interação entre Usuários Humanos, o Maestro IA (Orquestrador & Coordenador), Agentes IA Codificadores e a ferramenta auxiliar Roo, em um ambiente potencialmente multi-usuário.

## Papéis e Responsabilidades

O desenvolvimento se baseia na colaboração entre as seguintes entidades:

1.  **Usuário (Humano - Ex: Jader):**
    * Define os requisitos de alto nível e as tarefas específicas para o Maestro IA.
    * **Coordena com outros usuários humanos** para evitar sobreposição de tarefas e alinhar prioridades (via quadro de tarefas, chat, etc.).
    * Toma as decisões finais sobre arquitetura, tecnologia e funcionalidades.
    * **Gerencia o fluxo Git para sua linha de trabalho:** Cria/atualiza feature branches, realiza commits frequentes, faz push/pull, abre e gerencia Pull Requests, realiza merges após aprovação.
    * Executa os comandos de terminal fornecidos pelo Maestro IA ou pelo AI Coder em seu ambiente local (WSL 2).
    * Opera a ferramenta Roo, fornecendo os prompts formatados gerados pelas IAs.
    * Realiza testes funcionais e valida as implementações interagindo com o AI Coder.
    * Fornece feedback detalhado para o Maestro IA (processo geral, sumários) e para o AI Coder (tarefa específica).
    * Atua como **ponte de comunicação** essencial entre o Maestro IA e os AIs Codificadores que ele está supervisionando.

2.  **Maestro IA (Orquestrador & Coordenador - Ex: Gemini, Grok, Eu):**
    * Recebe e interpreta os requisitos do Usuário no início da sessão, considerando o contexto multi-usuário (branch atual).
    * Mantém o **contexto geral do projeto** (estado atual via README/Roadmap, arquitetura, documentação).
    * Planeja e define tarefas específicas a serem executadas, sugerindo nomes para feature branches apropriados.
    * Gera prompts detalhados de tarefa e contextualização (incluindo links para docs e código relevante no branch atual) para serem entregues aos AIs Codificadores via Usuário.
    * Recebe e analisa os "Sumários Finais para Orquestrador" fornecidos pelos AIs Codificadores (via Usuário).
    * Gera prompts formatados para a ferramenta Roo para criar ou atualizar os arquivos de **documentação oficial** (geralmente no mesmo feature branch do código relacionado).
    * Gera sumários gerais da sessão de trabalho e sugere **mensagens de commit** (padrão Conventional Commits) para o Usuário executar no feature branch ao final da sessão ou em marcos importantes.
    * Lembra o usuário sobre boas práticas Git (pull/rebase, commits frequentes).
    * Auxilia na depuração de erros em nível de orquestração ou integração.
    * **NÃO executa comandos Git.**

3.  **Agente IA Codificador (Instância separada):**
    * Recebe um prompt de tarefa detalhado do Maestro IA (via Usuário), incluindo o contexto do branch atual.
    * **Lidera a implementação técnica** da tarefa específica **no feature branch designado**.
    * Gera código-fonte, snippets de configuração ou testes.
    * **Gera prompts formatados para a ferramenta Roo** para aplicar suas mudanças de código/configuração nos arquivos locais do Usuário.
    * **Gera comandos de terminal** (relacionados à sua tarefa) para o Usuário executar (ex: rodar um script específico, lint, teste unitário do seu código).
    * Interage com o Usuário para receber feedback, resultados de testes e fazer iterações/correções na sua tarefa.
    * Ao finalizar a tarefa (validada pelo Usuário), gera o **"Sumário Final para Orquestrador"** detalhado (conforme template definido) e entrega ao Usuário.
    * Pode sugerir mensagens de commit para suas próprias alterações de código (a serem usadas pelo Usuário no feature branch).
    * **NÃO executa comandos Git.**

4.  **Roo (Agente/Ferramenta Auxiliar):**
    * Ponte segura entre os prompts gerados pelas IAs e o filesystem local do Usuário.
    * Recebe prompts formatados do Usuário.
    * Executa operações de arquivo (`Create File`, `Overwrite File`, `Append Lines`).

## Colaboração Multi-Usuário e Versionamento (Git)

Trabalhar com múltiplos humanos (e seus times de IA) no mesmo projeto exige uma estratégia de versionamento clara e disciplinada para evitar caos e perda de trabalho. Adotaremos o seguinte fluxo baseado em **Feature Branches** e **Pull Requests**.

**Princípios:**

* **Isolamento:** O trabalho em cada nova funcionalidade, correção ou tarefa significativa é feito em um branch separado.
* **Atualização Contínua:** Mantenha seu branch atualizado com a base principal (`main`) para detectar e resolver conflitos cedo.
* **Revisão:** Integre o trabalho de volta à branch principal apenas após revisão (via Pull Request).
* **`main` Estável:** A branch `main` deve sempre refletir um estado estável e funcional do projeto.

**Fluxo Detalhado:**

1.  **Iniciar uma Nova Tarefa:**
    * **Coordenação Humana:** Verifique com outros usuários (via quadro de tarefas ou chat) para garantir que não há sobreposição direta na tarefa planejada.
    * **Sincronize `main`:** Atualize sua cópia local da branch `main`.
        ```bash
        git checkout main
        git pull origin main
        ```
    * **Crie seu Feature Branch:** Crie um novo branch a partir da `main` atualizada. Use um nome descritivo (o Maestro IA pode sugerir).
        ```bash
        # Ex: git checkout -b jader/feature/modulo-relatorios
        # Ex: git checkout -b fix/corrigir-bug-login
        git checkout -b <nome-do-seu-branch>
        ```
    * **Informe o Maestro IA:** Comunique ao seu Maestro IA em qual branch você está trabalhando nesta sessão.

2.  **Desenvolver no Feature Branch:**
    * Siga o "Fluxo de Interação Típico" para executar a tarefa com seus AIs.
    * **Faça Commits Frequentes e Atômicos:** Após cada passo lógico ou funcionalidade mínima concluída (conforme sugerido pelo Maestro IA ou AI Coder):
        * Adicione os arquivos relevantes ao stage: `git add <arquivo_modificado_1> <arquivo_novo_2>` ou `git add .` (use com cuidado para adicionar apenas o relacionado ao commit).
        * Faça o commit com uma mensagem clara seguindo o padrão Conventional Commits: `git commit -m "tipo(escopo): Mensagem clara"` (Coder/Maestro podem sugerir a mensagem).
    * **Mantenha seu Branch Atualizado (Pull com Rebase):** Periodicamente (ex: diariamente, ou antes de fazer um push significativo), atualize seu branch com as últimas mudanças da `main` para evitar grandes conflitos depois:
        ```bash
        # Garanta que sua main local está atualizada (opcional se já fez no início)
        # git checkout main
        # git pull origin main
        # Volte para seu branch
        git checkout <nome-do-seu-branch>

        # Tente aplicar seus commits sobre os últimos da main
        git pull origin main --rebase
        ```
        * **Resolva Conflitos:** Se o `rebase` encontrar conflitos, o Git pausará. Edite os arquivos conflitantes para resolver as diferenças, use `git add <arquivo_resolvido>` para marcar como resolvido, e continue o rebase com `git rebase --continue`. Se tiver problemas, `git rebase --abort` cancela. Peça ajuda se necessário.
    * **Compartilhe seu Progresso (Push):** Envie seu branch local para o repositório remoto no GitHub regularmente para backup e para permitir que outros (ou o Maestro IA, conceitualmente) vejam seu progresso:
        ```bash
        # Na primeira vez para um novo branch:
        git push -u origin <nome-do-seu-branch>
        # Nas vezes seguintes:
        git push origin <nome-do-seu-branch>
        # ou apenas 'git push' se o upstream já estiver configurado
        ```
        * Se precisar que o Maestro IA revise algo específico no código via GitHub, informe o nome do branch e o que deve ser revisado.

3.  **Concluindo a Tarefa e Integrando:**
    * **Finalize e Atualize:** Garanta que a tarefa está completa, testada (por você e pelo Coder), e que seu branch está atualizado com `main` (`git pull origin main --rebase`).
    * **Push Final:** Envie a versão final do seu branch: `git push origin <nome-do-seu-branch>`.
    * **Abra um Pull Request (PR):** No GitHub (ou ferramenta similar), crie um novo Pull Request comparando seu `<nome-do-seu-branch>` com a branch `main`.
        * Escreva uma descrição clara no PR explicando o que foi feito, por que, e como testar. Pode incluir um link para a tarefa no quadro de coordenação.
    * **Revisão do PR:** Notifique o revisor designado (outro humano). O revisor irá analisar o código, a documentação e os testes. Comentários e solicitações de mudança podem ser feitos diretamente no PR. Faça os ajustes necessários no seu branch e envie-os (`git commit`, `git push`).
    * **Merge:** Após o PR ser aprovado e passar por quaisquer verificações automáticas (CI), ele pode ser mergeado na branch `main` (geralmente através da própria interface do PR no GitHub, que pode oferecer opções como "Squash and merge" ou "Rebase and merge").
    * **Limpeza (Opcional):** Após o merge ser confirmado na `main`, você pode apagar seu branch local (`git checkout main && git branch -d <nome-do-seu-branch>`) e o branch remoto (`git push origin --delete <nome-do-seu-branch>`).

## Iniciando uma Sessão de Trabalho

Para garantir que o **Maestro IA** tenha o contexto necessário:

1.  **Sinalização:** Usuário informa ao Maestro IA o início da sessão.
2.  **Atualização e Branch:** Usuário garante repositório atualizado (`git checkout main && git pull origin main`) e entra no **feature branch** correto para a tarefa da sessão (`git checkout <meu-feature-branch>`). Se necessário, cria o branch (`git checkout -b ...`). Informa ao Maestro IA qual branch está ativo.
3.  **Contextualização:** Usuário direciona o Maestro IA para revisar docs chave (`README` Status, `ROADMAP`, Arquitetura, este Fluxo, Sumário anterior, etc.) conforme necessário para a tarefa.
4.  **Definição de Objetivo:** Usuário define a(s) meta(s) da sessão.
5.  **Confirmação AI:** Maestro IA confirma entendimento.

## Fluxo de Interação Típico (Dentro de um Feature Branch)

1.  **Definição da Tarefa (Maestro IA & Você):** Definimos a meta da tarefa atual dentro do escopo do branch.
2.  **Geração do Prompt para Coder (Maestro IA -> Você):** Eu gero o prompt detalhado para o AI Coder.
3.  **Execução da Tarefa (Você & AI Coder):** Você entrega o prompt ao Coder. Vocês iteram (Coder gera código/Roo/terminal -> Você executa/testa/feedback) **fazendo commits frequentes no feature branch**.
4.  **Sumarização (AI Coder -> Você -> Maestro IA):** Ao final da tarefa (ou marco importante), Coder gera o "Sumário Final para Orquestrador". Você cola para mim.
5.  **Atualização Docs (Maestro IA -> Você -> Roo):** Eu analiso o sumário e gero prompts Roo para atualizar a documentação **no feature branch**. Você executa.
6.  **(Repetir se houver mais tarefas na sessão/branch)**

## Finalizando uma Sessão de Trabalho

Ao concluir uma sessão (pausando ou finalizando a tarefa no branch):

1.  **Sinalização:** Usuário informa ao Maestro IA o fim da sessão.
2.  **Sumário AI Coder (se aplicável):** Garantir que o sumário da última tarefa trabalhada foi recebido por mim.
3.  **Sumário Geral da Sessão (Maestro IA):** Eu forneço um resumo do que foi feito.
4.  **Atualização de Status (Maestro IA Gera, User Aplica/Verifica):** Eu gero texto para `README`/`ROADMAP`. Você aplica/verifica (e commita no branch).
5.  **Sugestão de Commit (Maestro IA Gera):** Eu sugiro a mensagem para o(s) último(s) commit(s) da sessão no feature branch.
6.  **Versionamento (User Executa):** Usuário executa `git add .`, `git commit -m "..."` (usando sugestão ou própria) e `git push origin <nome-do-seu-branch>` para salvar o trabalho da sessão no remoto. O merge para `main` via PR acontece separadamente quando a feature estiver pronta.

## Detalhes da Ferramenta Roo

* **Natureza:** Ferramenta/agente externo que roda no ambiente do usuário.
* **Interface:** Baseada em texto, processa prompts com formato específico e rígido.
* **Ações Suportadas (conhecidas):** `Create File`, `Overwrite File`, `Append Lines`.
* **Formato Exato do Prompt (Gerado por Maestro IA ou AI Coder):** O prompt **deve** seguir este formato multiline, respeitando as quebras de linha e os delimitadores de bloco de código para o conteúdo:
    ```text
    Action: [Create File | Overwrite File | Append Lines]
    Relative Path: caminho/relativo/partindo/da/raiz/do/projeto/arquivo.ext
    Content:
    ```[language]
    # Conteúdo completo a ser escrito/anexado.
    # Preservar indentação e formatação original aqui dentro.
    ...
    ```
    ```
    * **Notas sobre o Formato:**
        * `[language]` no delimitador do bloco de código (ex: ```markdown, ```python, ```bash) é opcional mas recomendado para clareza.
        * O conteúdo entre os delimitadores ``` é inserido exatamente como está no arquivo.
        * O `Relative Path` deve ser sempre relativo à raiz do projeto (`modular-dashboard/`).

* **Importância:** Essencial para o fluxo atual, pois permite que as IAs, sem acesso direto, manipulem arquivos no ambiente de desenvolvimento local de forma precisa e eficiente.

## Comunicação

* **Confirmações:** O uso de `OK` ou `K` pelo Usuário após receber instruções (minhas ou do Coder) é útil para sinalizar entendimento. As IAs devem aguardar essa confirmação quando apropriado.
* **Clareza Técnica:** A comunicação deve ser precisa. As IAs devem fornecer nomes de arquivos, comandos e descrições exatas. Os prompts para Roo devem ser perfeitos.
* **Feedback:** O feedback do Usuário sobre o resultado das ações é crucial para a iteração e correção.