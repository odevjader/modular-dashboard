# Roadmap Detalhado: Modular Dashboard

Este roadmap detalha as fases, épicos e tarefas específicas para o desenvolvimento do projeto, com foco na implementação da nova arquitetura de processamento de documentos. As tarefas são numeradas em ordem de prioridade de execução.

---

## Fase 1: Fundação e MVP (Concluído ✔️)

_Esta fase representa o estado atual do projeto, com a arquitetura modular e funcionalidades básicas já implementadas._

#### Tarefas Concluídas:

* **Estrutura do Backend:** Implementada com FastAPI, garantindo alta performance e documentação automática de APIs.
* **Estrutura do Frontend:** Desenvolvida com React, TypeScript e Vite, para um ambiente de desenvolvimento moderno e rápido.
* **Containerização:** Aplicação totalmente containerizada com Docker e Docker Compose, garantindo consistência entre ambientes.
* **Sistema de Modularidade:** Implementado no backend e frontend, permitindo a adição de novas funcionalidades de forma desacoplada.
* **Módulo de Autenticação:** Módulo central (`core_module`) com autenticação via JWT para proteger os endpoints.
* **Banco de Dados:** Configurado com PostgreSQL e Alembic para gerenciamento de migrações do schema.
* **Módulos de Exemplo:** Criados módulos iniciais (`gerador_quesitos`, `ai_test`, `info`) para validar a arquitetura.
* **Documentação Inicial:** Criada a documentação base sobre a arquitetura, estrutura de pastas e fluxo de trabalho.

---

## Fase 2: Infraestrutura de Processamento de Documentos (Foco Atual 🎯)

**Épico: Construir a Pipeline de Extração de Texto como um Microserviço.**

_Objetivo: Criar a fundação de backend necessária para o processamento de PDFs de forma isolada e escalável. Ao final desta fase, teremos um serviço `worker` funcional e a API principal pronta para delegar tarefas a ele._

#### Tarefas Priorizadas:

1.  **Definir e Implementar o Schema do Banco de Dados:**
    * **Descrição:** Criar a migração do Alembic no `backend` principal para adicionar a nova tabela.
    * **Tabela:** `pdf_processed_chunks`.
    * **Colunas:** `id` (PK), `file_hash` (VARCHAR(64), Indexed), `chunk_text` (TEXT), `page_number` (INTEGER), `created_at` (TIMESTAMPTZ).
    * **Entregável:** Um novo arquivo de migração do Alembic no diretório `backend/alembic/versions`.

2.  **Configurar o Ambiente com `docker-compose.yml`:**
    * **Descrição:** Adicionar a definição do novo `pdf_processor_service` ao arquivo `docker-compose.yml`.
    * **Especificações:**
        * Nome do serviço: `pdf_processor`.
        * Deve construir a partir de um `Dockerfile` localizado em `./pdf_processor_service/`.
        * Deve compartilhar a rede (`app-network`) e o arquivo de ambiente (`.env`) com o `backend` principal.
        * Deve ter uma dependência explícita do serviço `db` (`depends_on`).
    * **Entregável:** Arquivo `docker-compose.yml` atualizado.

3.  **Criar a Estrutura Base do Microserviço:**
    * **Descrição:** Criar a estrutura de pastas e arquivos para o novo serviço.
    * **Estrutura:**
        ```
        /pdf_processor_service
        |-- /app
        |   |-- main.py
        |   |-- processing.py
        |   |-- database.py
        |-- Dockerfile
        |-- requirements.txt
        ```
    * **Entregável:** A estrutura de pastas e arquivos básicos, incluindo um `Dockerfile` funcional e um `requirements.txt` com as dependências iniciais (`fastapi`, `uvicorn`, `pypdf`, `sqlalchemy`, `psycopg2-binary`).

4.  **Implementar a Lógica de Extração e Armazenamento no Microserviço:**
    * **Descrição:** Codificar a função principal no `processing.py` que recebe o conteúdo de um arquivo.
    * **Passos:**
        1.  Calcular o hash SHA-256 do arquivo.
        2.  Conectar-se ao PostgreSQL e verificar se o `file_hash` já existe. Se sim, retornar imediatamente.
        3.  Se não existir, usar `PyPDFLoader` para extrair o texto.
        4.  Iterar sobre os "chunks" ou páginas e inseri-los na tabela `pdf_processed_chunks`.
    * **Entregável:** Código Python funcional no `pdf_processor_service`.

5.  **Criar o Endpoint de Processamento no Microserviço:**
    * **Descrição:** No `main.py` do `pdf_processor_service`, criar um endpoint (ex: `POST /process-pdf`) que recebe um `UploadFile`, chama a lógica de processamento e retorna um JSON com o `file_hash` e uma mensagem de status.
    * **Entregável:** Endpoint FastAPI testável no microserviço.

6.  **Criar o Endpoint de Delegação na API Principal:**
    * **Descrição:** No `backend` principal, criar um novo endpoint (ex: `POST /api/v1/documents/upload-and-process`) que atua como um proxy.
    * **Passos:**
        1.  Recebe o `UploadFile` do cliente.
        2.  Usa `httpx` para repassar o arquivo para o endpoint do `pdf_processor_service`.
        3.  Aguarda a resposta e a retorna ao cliente.
    * **Entregável:** Novo endpoint na API principal que orquestra a chamada para o microserviço.

---

## Fase 3: Governança e Maturidade (Visão Futura 🔭)

**Épico: Amadurecer a Plataforma.**

_Objetivo: Com a arquitetura principal definida, o foco muda para a garantia da qualidade e segurança do sistema._

#### Tarefas (Sem ordem de prioridade definida):

* **Implementar Mecanismo de Notificação Global no Frontend:**
    * **Descrição:** Criar um sistema centralizado para exibir notificações (alertas, "snackbars" ou "toasts") ao usuário.
    * **Objetivo:** Fornecer feedback claro e consistente para ações como "Upload bem-sucedido", "Erro de processamento", etc.
    * **Tecnologia Sugerida:** Integrar uma biblioteca como `notistack` ou `react-toastify`.

* **Implementar Logging e Monitoramento:**
    * **Descrição:** Configurar um sistema de logging estruturado para todos os serviços e avaliar uma ferramenta de Application Performance Monitoring (APM).

* **Implementar Sistema de Alertas de Backend:**
    * **Descrição:** Configurar alertas proativos para falhas críticas (ex: serviço offline, erros 5xx), com notificação para a equipe de desenvolvimento via e-mail.
