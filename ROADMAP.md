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

## Fase 3: Módulo Piloto Autônomo e Integração (Próximos Passos 🚀)

**Épico: Refatorar o `gerador_quesitos` para Usar a Nova Arquitetura.**

_Objetivo: Transformar o primeiro módulo para que ele consuma a nova pipeline de processamento, servindo como um modelo para todos os futuros módulos de IA._

#### Tarefas Priorizadas:

7.  **Refatorar o Frontend do Módulo `gerador_quesitos`:**
    * **Descrição:** Modificar o componente React (`GeradorQuesitos.tsx`).
    * **Passos:**
        1.  Adicionar um componente de UI para upload de arquivo (`<input type="file">`).
        2.  Implementar a lógica no frontend para chamar o novo endpoint de delegação (`/api/v1/documents/upload-and-process`).
        3.  Armazenar o `file_hash` retornado no estado do componente.
    * **Entregável:** Interface do módulo `gerador_quesitos` com capacidade de upload.

8.  **Refatorar o Backend do Módulo `gerador_quesitos`:**
    * **Descrição:** Modificar o endpoint existente do módulo.
    * **Passos:**
        1.  O endpoint não receberá mais o arquivo, mas sim o `file_hash` e a pergunta do usuário.
        2.  A lógica interna buscará os `chunk_text` da tabela `pdf_processed_chunks` usando o `file_hash`.
        3.  Com os textos recuperados, a lógica existente do LangChain será executada para vetorizar o texto, fazer a busca e gerar a resposta.
    * **Entregável:** Endpoint do `gerador_quesitos` atualizado e funcional com a nova arquitetura.

---

## Fase 4: Expansão, Refinamento e Governança (Visão Futura 🔭)

**Épico: Amadurecer a Plataforma e Expandir Funcionalidades.**

_Objetivo: Com a arquitetura principal definida e validada, o foco muda para a construção de novas funcionalidades, melhoria da experiência do usuário e garantia da qualidade e segurança do sistema._

#### Tarefas (Sem ordem de prioridade definida):

* **Desenvolver Novo Módulo: Analisador de Documentos (RAG):**
    * Criar um novo módulo autônomo que permite ao usuário "conversar" com um documento enviado, implementando o fluxo completo validado na Fase 3.

* **Implementar Controle de Acesso (RBAC):**
    * Associar permissões a perfis de usuário (`Admin`, `User`).
    * Proteger módulos e endpoints com base no perfil do usuário logado.

* **Melhorar a Experiência do Frontend:**
    * Implementar um seletor de tema (claro/escuro).
    * Preparar a estrutura para internacionalização (i18n).

* **Estabelecer CI/CD:**
    * Criar um pipeline no GitHub Actions para rodar testes e, futuramente, automatizar o deploy.

* **Implementar Logging e Monitoramento:**
    * Configurar um sistema de logging estruturado para todos os serviços.
    * Avaliar e implementar uma ferramenta de Application Performance Monitoring (APM).
