# Fluxo de Trabalho de Desenvolvimento

Este documento descreve o modelo de desenvolvimento colaborativo exclusivo utilizado no projeto Modular Dashboard, envolvendo a interação entre o Usuário Humano, o Assistente de IA e a ferramenta auxiliar Roo.

## Papéis e Responsabilidades

O desenvolvimento se baseia na colaboração entre três entidades principais:

1.  **Usuário (Humano - Ex: Jader):**
    * Define los requisitos de alto nivel y las tareas específicas.
    * Toma las decisiones finales sobre arquitectura, tecnología y funcionalidades.
    * **Executa os comandos** de terminal (Docker, Git, npm, Alembic, etc.) fornecidos pelo Assistente IA em seu ambiente local (WSL 2).
    * **Opera a ferramenta Roo**, fornecendo a ela os prompts formatados gerados pelo Assistente IA para manipulação de arquivos.
    * Realiza testes funcionais e valida as implementações.
    * Fornece feedback detalhado para o Assistente IA.
    * Gerencia o repositório Git (commits, branches, push para o GitHub).

2.  **Assistente IA (Ex: Gemini, Grok, Eu):**
    * Recebe e interpreta os requisitos do Usuário.
    * Pesquisa soluções, bibliotecas e melhores práticas.
    * Propõe designs de arquitetura e soluções técnicas.
    * **Gera código-fonte**, arquivos de configuração, conteúdo de documentação e testes.
    * **Gera prompts formatados para a ferramenta Roo** realizar operações no sistema de arquivos local do Usuário.
    * **Fornece comandos exatos** para o Usuário executar no terminal.
    * Auxilia na depuração de erros, analisando logs e mensagens fornecidas pelo Usuário.
    * Mantém o contexto da sessão de trabalho atual.

3.  **Roo (Agente/Ferramenta Auxiliar):**
    * Atua como uma **ponte segura entre o Assistente IA (que não tem acesso direto ao filesystem) e o ambiente local do Usuário**.
    * Recebe prompts de texto formatados do Usuário (gerados originalmente pelo Assistente IA).
    * **Executa operações no sistema de arquivos local** conforme especificado no prompt (criar, sobrescrever, anexar arquivos).
    * Não possui lógica de programação própria, apenas executa as ações definidas no prompt.

## Fluxo de Interação Típico

Uma tarefa de desenvolvimento geralmente segue este ciclo:

1.  **Definição:** Usuário descreve a tarefa ou problema para o Assistente IA.
2.  **Análise/Proposta:** Assistente IA analisa, faz perguntas para esclarecer (se necessário), e propõe uma solução (ex: novo código, alteração de configuração, novo documento).
3.  **Geração de Código/Conteúdo:** Assistente IA gera o conteúdo necessário.
4.  **Operação de Arquivo (via Roo):**
    * AI gera um prompt formatado para Roo (ex: `Action: Create File...`).
    * Usuário copia o prompt completo e o fornece para Roo.
    * Roo executa a criação/modificação do arquivo no local especificado (`Relative Path`).
    * Usuário confirma (implícita ou explicitamente) a execução bem-sucedida pelo Roo.
5.  **Execução de Comando (via Terminal):**
    * Se necessário (ex: rodar `docker-compose`, `npm install`, `alembic upgrade`), AI fornece o comando exato.
    * Usuário copia o comando e o executa em seu terminal local (WSL 2).
    * Usuário copia e cola a saída do terminal (logs, erros) de volta para o AI, se solicitado.
6.  **Recuperação de Informação:**
    * Se AI precisa ver o conteúdo atual de um arquivo antes de modificá-lo, ele pode pedir ao usuário usando um formato como `code <caminho_relativo/arquivo.ext>`.
    * Usuário usa `cat` ou um editor para obter o conteúdo e o cola para o AI.
7.  **Teste e Feedback:** Usuário testa a funcionalidade implementada ou a configuração aplicada. Fornece feedback (sucesso, erro, sugestão de melhoria) para o Assistente IA.
8.  **Iteração:** O ciclo retorna ao passo 2 ou 3 para ajustes e refinamentos com base no feedback.
9.  **Versionamento (Git):**
    * Após uma alteração significativa ou criação de arquivo (geralmente via Roo), AI fornece os comandos `git add <arquivo>` e `git commit -m "mensagem descritiva"`.
    * Usuário executa os comandos Git para versionar as mudanças.
    * O Usuário é responsável por gerenciar branches, merges e sincronizar com o repositório remoto no GitHub (`git push`).

## Detalhes da Ferramenta Roo

* **Natureza:** Ferramenta/agente externo que roda no ambiente do usuário.
* **Interface:** Baseada em texto, processa prompts com formato específico.
* **Ações Suportadas (conhecidas):** `Create File`, `Overwrite File`, `Append Lines`.
* **Formato do Prompt:**
    ```text
    Action: [Create File | Overwrite File | Append Lines]
    Relative Path: caminho/relativo/partindo/da/raiz/do/projeto/arquivo.ext
    Content:
    ```[language]
    # Conteúdo completo a ser escrito/anexado
    ...
    ```
    ```
* **Importância:** Essencial para o fluxo atual, pois permite que o Assistente IA, sem acesso direto, manipule arquivos no ambiente de desenvolvimento local de forma precisa e eficiente, evitando erros de cópia/cola manual em blocos grandes ou complexos.

## Comunicação

* **Confirmações:** O uso de `OK` ou `K` pelo Usuário após receber instruções do Assistente IA é comum para sinalizar entendimento antes de prosseguir.
* **Clareza:** A comunicação busca ser tecnicamente precisa, embora às vezes possa ser mais direta ou concisa, dependendo do contexto.
* **Feedback:** O feedback do Usuário sobre o resultado das ações (Roo, comandos de terminal, testes) é crucial para o Assistente IA continuar o trabalho de forma eficaz.