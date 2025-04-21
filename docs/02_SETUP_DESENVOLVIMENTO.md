# Guia de Setup de Desenvolvimento - Modular Dashboard

Este guia descreve os passos necessários para configurar e executar o projeto Modular Dashboard em um ambiente de desenvolvimento local utilizando Docker e Node.js.

## Pré-requisitos

Antes de começar, certifique-se de ter as seguintes ferramentas instaladas em seu sistema:

* [Git](https://git-scm.com/): Para clonar o repositório.
* [Docker](https://www.docker.com/products/docker-desktop/): Para gerenciamento de containers (inclui Docker Compose V2+).
* [Node.js](https://nodejs.org/): Versão 18 ou superior (inclui npm) para o desenvolvimento frontend.
* (Recomendado) WSL 2 se estiver utilizando Windows, para melhor integração com Docker.

### Dependências Externas Específicas

* **Tesseract OCR:** Necessário para o funcionamento completo do módulo `gerador_quesitos` (processamento de PDFs com imagens via DoclingLoader).
    * **Status:** *(Pendente de Clarificação)* É preciso documentar como o Tesseract está instalado e acessível para o container `api` do backend.
    * **Verificar:**
        * O Tesseract e seus pacotes de idioma (ex: `tesseract-ocr-por` para português) estão incluídos e configurados no `backend/Dockerfile`?
        * Ou ele precisa ser instalado separadamente no sistema host (WSL) e o container `api` tem acesso a ele de alguma forma?
        * Alguma variável de ambiente precisa ser configurada para indicar o caminho do Tesseract?

## Passos para Configuração

1.  **Clonar o Repositório:**
    Abra seu terminal ou prompt de comando e clone o repositório do GitHub:
    ```bash
    git clone https://github.com/odevjader/modular-dashboard.git
    cd modular-dashboard
    ```

2.  **Configurar Variáveis de Ambiente (Backend):**
    O backend FastAPI requer um arquivo `.env` para carregar configurações essenciais. Crie este arquivo em `backend/.env`.

    * **Variáveis Obrigatórias Mínimas:** Para que a aplicação suba e os módulos principais (`gerador_quesitos`, `ai_test`, `auth`) funcionem, as seguintes variáveis **precisam** ser definidas no `backend/.env`:
        * `DATABASE_URL`: String de conexão com o PostgreSQL.
        * `SECRET_KEY`: Chave secreta para assinatura dos tokens JWT (use `openssl rand -hex 32` para gerar uma).
        * `GOOGLE_API_KEY`: Chave para acesso à API do Google AI Studio (Gemini).

    * *Exemplo `backend/.env`:*
        ```.env
        # Obrigatório: Configuração do Banco de Dados (padrões do docker-compose.yml)
        DATABASE_URL=postgresql+asyncpg://appuser:password@db:5432/appdb

        # Obrigatório: Configuração JWT (gere com: openssl rand -hex 32)
        SECRET_KEY=sua_chave_secreta_muito_segura_aqui
        ALGORITHM=HS256
        ACCESS_TOKEN_EXPIRE_MINUTES=1440 # 24 horas

        # Obrigatório: Chave da API Google AI
        GOOGLE_API_KEY=sua_google_api_key_aqui

        # Opcional: Outras configurações (ver backend/app/core/config.py para lista completa)
        # ENVIRONMENT=development
        # PROJECT_NAME="Modular Dashboard"
        # ALLOWED_ORIGINS='["http://localhost:5173","http://127.0.0.1:5173"]' # Exemplo para CORS
        ```
    * **Segurança:** Nunca comite o arquivo `.env` no Git. Ele já deve estar (ou ser adicionado) no `.gitignore`.

3.  **Iniciar os Containers Docker:**
    A partir da raiz do projeto (`modular-dashboard/`), execute o Docker Compose para construir as imagens (se necessário) e iniciar os containers do backend (serviço `api`) e do banco de dados (serviço `db`).
    ```bash
    docker-compose up -d --build
    ```
    * A opção `-d` executa os containers em modo detached (background).
    * A opção `--build` força a reconstrução das imagens se houver mudanças no `Dockerfile` ou arquivos relacionados. O primeiro build pode levar alguns minutos.
    * Aguarde até que os containers estejam em execução e saudáveis. Você pode verificar com `docker-compose ps`.

4.  **Aplicar Migrações do Banco de Dados (Alembic):**
    Após o container `api` estar em execução, aplique as migrações do banco de dados para garantir que o schema esteja atualizado. Execute o comando `upgrade` do Alembic dentro do container `api`:
    ```bash
    docker-compose exec api alembic upgrade head
    ```
    *(Este comando aplica todas as migrações pendentes encontradas na pasta `backend/app/versions/`)*

5.  **Instalar Dependências do Frontend:**
    Navegue até a pasta `frontend/` e use o `npm` para instalar todas as dependências listadas no `package.json`:
    ```bash
    cd frontend
    npm install
    # Volte para a raiz do projeto se precisar executar outros comandos de lá
    # cd ..
    ```

6.  **Iniciar o Servidor de Desenvolvimento do Frontend:**
    Ainda dentro da pasta `frontend/`, inicie o servidor de desenvolvimento do Vite:
    ```bash
    # Certifique-se de estar na pasta frontend/
    npm run dev
    ```
    O terminal indicará em qual porta o servidor frontend está rodando (normalmente 5173).

7.  **Acessar a Aplicação:**
    Abra seu navegador e acesse:
    * **Frontend:** [http://localhost:5173](http://localhost:5173) (ou a porta indicada pelo `npm run dev`)
    * **Backend API Docs (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)
    * **Backend API Docs (ReDoc):** [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Parando o Ambiente

Para parar os containers Docker (API e Banco de Dados) quando terminar de trabalhar, execute o seguinte comando na raiz do projeto:

```bash
docker-compose down