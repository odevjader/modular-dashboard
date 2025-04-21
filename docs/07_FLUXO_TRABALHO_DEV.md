# Fluxo de Trabalho de Desenvolvimento

Este documento descreve o modelo de desenvolvimento colaborativo exclusivo utilizado no projeto Modular Dashboard, envolvendo a interação entre o Usuário Humano, o Assistente de IA e a ferramenta auxiliar Roo.

## Papéis e Responsabilidades

O desenvolvimento se baseia na colaboração entre três entidades principais:

1.  **Usuário (Humano - Ex: Jader):**
    * Defines os requisitos de alto nível e as tarefas específicas.
    * Toma as decisões finais sobre arquitetura, tecnologia e funcionalidades.
    * **Executa os comandos** de terminal (Docker, Git, npm, Alembic, etc.) fornecidos pelo Assistente IA em seu ambiente local (WSL 2).
    * **Opera a ferramenta Roo**, fornecendo a ela os prompts formatados gerados pelo Assistente IA para manipulação de arquivos.
    * Realiza testes funcionais e valida as implementações.
    * Fornece feedback detalhado para o Assistente IA.
    * Gerencia o repositório Git (commits ao final da sessão, branches, push para o GitHub).

2.  **Assistente IA (Ex: Gemini, Grok, Eu):**
    * Recebe e interpreta os requisitos do Usuário.
    * Pesquisa soluções, bibliotecas e melhores práticas.
    * Propõe designs de arquitetura e soluções técnicas.
    * **Gera código-fonte**, arquivos de configuração, conteúdo de documentação e testes.
    * **Gera prompts formatados para a ferramenta Roo** realizar operações no sistema de arquivos local do Usuário.
    * **Fornece comandos exatos** para o Usuário executar no terminal.
    * Auxilia na depuração de erros, analisando logs e mensagens fornecidas pelo Usuário.
    * Mantém o contexto da sessão de trabalho atual.
    * **Gera sumários e atualizações de status** ao final da sessão.

3.  **Roo (Agente/Ferramenta Auxiliar):**
    * Atua como uma **ponte segura entre o Assistente IA (que não tem acesso direto ao filesystem) e o ambiente local do Usuário**.
    * Recebe prompts de texto formatados do Usuário (gerados originalmente pelo Assistente IA).
    * **Executa operações no sistema de arquivos local** conforme especificado no prompt (criar, sobrescrever, anexar arquivos).
    * Não possui lógica de programação própria, apenas executa as ações definidas no prompt.

## Iniciando uma Sessão de Trabalho

Para garantir que o Assistente IA tenha o contexto necessário ao iniciar uma nova sessão (especialmente se for um agente diferente ou após uma pausa longa):

1.  **Sinalização:** O Usuário informa ao AI que uma nova sessão está começando.
2.  **Contextualização:** O Usuário deve direcionar o AI para revisar (ou fornecer um resumo rápido de) documentos chave para o contexto atual da tarefa:
    * `README.md`: Principalmente a seção "Status Atual".
    * `ROADMAP.md`: Para entender a fase atual e os próximos objetivos.
    * `docs/01_ARQUITETURA.md`: Para relembrar a estrutura técnica geral.
    * `docs/07_FLUXO_TRABALHO_DEV.md` (este documento): Para alinhar as regras de interação e formatos de output esperados (prompts Roo, comandos Git, sumários).
    * (Opcional) Últimos arquivos modificados ou discussão relevante, se aplicável à tarefa da sessão.
3.  **Definição de Objetivo:** O Usuário define claramente a(s) meta(s) principal(is) para a sessão de trabalho atual.
4.  **Confirmação AI:** O AI confirma o entendimento do contexto e do objetivo antes de iniciar a tarefa.

## Fluxo de Interação Típico (Durante a Sessão)

Uma tarefa de desenvolvimento geralmente segue este ciclo:

1.  **Definição:** Usuário descreve a tarefa ou problema para o Assistente IA.
2.  **Análise/Proposta:** Assistente IA analisa, faz perguntas para esclarecer (se necessário), e propõe uma solução (ex: novo código, alteração de configuração, novo documento).
3.  **Geração de Código/Conteúdo:** Assistente IA gera o conteúdo necessário.
4.  **Operação de Arquivo (via Roo):**
    * AI gera um prompt formatado para Roo (ver seção "Detalhes da Ferramenta Roo").
    * Usuário copia o prompt completo e o fornece para Roo.
    * Roo executa a criação/modificação do arquivo no local especificado (`Relative Path`).
    * Usuário confirma (implícita ou explicitamente) a execução bem-sucedida pelo Roo para o AI.
5.  **Execução de Comando (via Terminal):**
    * Se necessário (ex: rodar `docker-compose`, `npm install`, `alembic upgrade`), AI fornece o comando exato a ser executado.
    * Usuário copia o comando e o executa em seu terminal local (WSL 2).
    * Usuário copia e cola a saída do terminal (logs, erros) de volta para o AI, se solicitado.
6.  **Recuperação de Informação:**
    * Se AI precisa ver o conteúdo atual de um arquivo antes de modificá-lo, ele pode pedir ao usuário usando um formato como `code <caminho_relativo/arquivo.ext>`.
    * Usuário usa `cat` ou um editor para obter o conteúdo e o cola para o AI.
7.  **Teste e Feedback:** Usuário testa a funcionalidade implementada ou a configuração aplicada. Fornece feedback (sucesso, erro, sugestão de melhoria) para o Assistente IA.
8.  **Iteração:** O ciclo retorna ao passo 2 ou 3 para ajustes e refinamentos com base no feedback.
9.  **Versionamento (Git):**
    * O Usuário é responsável por adicionar (`git add .` ou `git add <path>`) e commitar (`git commit -m "..."`) as mudanças realizadas durante a sessão. Conforme o acordo atual (Abril 2025), **os commits são feitos ao final de cada sessão de trabalho**, agrupando as alterações daquela sessão.
    * O Assistente IA **não** fornecerá mais comandos Git após cada prompt Roo, mas **deve** sugerir mensagens de commit apropriadas no **final da sessão**, como parte do sumário.
    * O Usuário gerencia branches, merges e sincronização com o GitHub (`git push`).

## Finalizando uma Sessão de Trabalho

Ao concluir uma sessão de trabalho, é **obrigatório** seguir estes passos para registrar o progresso e preparar para a próxima sessão:

1.  **Sinalização:** O Usuário informa ao AI que a sessão está terminando.
2.  **Sumário AI (Obrigatório):** O Assistente IA **deve** fornecer um resumo conciso e claro do que foi realizado na sessão, incluindo:
    * Tarefas concluídas.
    * Status detalhado de tarefas que ficaram em andamento (o que foi feito, o que falta?).
    * Novos problemas encontrados, bloqueios identificados ou decisões importantes que foram tomadas durante a sessão.
    * Sugestão clara e direta do(s) próximo(s) passo(s) lógico(s) para a próxima sessão.
3.  **Atualização de Status (AI Gera, User Aplica/Verifica):** Se o status geral do projeto mudou significativamente (ex: bug resolvido, fase do roadmap concluída, novo bloqueio crítico), o AI deve **gerar o texto exato** sugerido para atualizar a seção "Status Atual" no `README.md` e/ou o status das tarefas no `ROADMAP.md`. O Usuário é responsável por revisar e aplicar essa atualização (via Roo ou manualmente).
4.  **Sugestão de Commit (AI Gera):** O AI deve sugerir uma mensagem de commit concisa e informativa (seguindo o padrão Conventional Commits, ex: `feat(auth): Implement /users/me endpoint` ou `docs: Update workflow details`) que resuma as alterações feitas na sessão.
5.  **Versionamento (User Executa):** O Usuário executa os comandos Git para adicionar todas as mudanças da sessão ao stage (`git add .` ou arquivos específicos), commitar usando a mensagem sugerida pelo AI (ou uma própria) (`git commit -m "..."`) e opcionalmente sincronizar com o remoto (`git push`).

## Detalhes da Ferramenta Roo

* **Natureza:** Ferramenta/agente externo que roda no ambiente do usuário.
* **Interface:** Baseada em texto, processa prompts com formato específico e rígido.
* **Ações Suportadas (conhecidas):** `Create File`, `Overwrite File`, `Append Lines`.
* **Formato Exato do Prompt:** O prompt **deve** seguir este formato multiline, respeitando as quebras de linha e os delimitadores de bloco de código para o conteúdo:
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

* **Importância:** Essencial para o fluxo atual, pois permite que o Assistente IA, sem acesso direto, manipule arquivos no ambiente de desenvolvimento local de forma precisa e eficiente, evitando erros de cópia/cola manual em blocos grandes ou complexos.

## Comunicação

* **Confirmações:** O uso de `OK` ou `K` pelo Usuário após receber instruções do Assistente IA é comum para sinalizar entendimento antes de prosseguir. O AI deve aguardar essa confirmação quando apropriado.
* **Clareza Técnica:** A comunicação busca ser precisa. O AI deve fornecer nomes de arquivos, comandos e descrições exatas.
* **Feedback:** O feedback do Usuário sobre o resultado das ações (Roo, comandos de terminal, testes) é crucial para o Assistente IA continuar o trabalho de forma eficaz.