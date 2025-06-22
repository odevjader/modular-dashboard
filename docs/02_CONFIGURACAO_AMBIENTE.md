# docs/02_CONFIGURACAO_AMBIENTE.md
# Guia de Configuração de Ambiente - Modular Dashboard

Este guia descreve os passos necessários para configurar e executar o projeto Modular Dashboard em um ambiente de desenvolvimento local utilizando Docker e Node.js.

## Pré-requisitos

Antes de começar, certifique-se de ter as seguintes ferramentas instaladas em seu sistema:

* [Git](https://git-scm.com/): Para clonar o repositório.
* [Docker](https://www.docker.com/products/docker-desktop/): Para gerenciamento de containers (inclui Docker Compose V2+).
* [Node.js](https://nodejs.org/): Versão 18 ou superior (inclui npm) para o desenvolvimento frontend.
* (Recomendado) WSL 2 se estiver utilizando Windows, para melhor integração com Docker.

*(Nota: Funcionalidades que dependem de OCR em PDFs, como no módulo `01_GERADOR_QUESITOS`, exigirão Tesseract OCR. Esta dependência foi removida do container principal da API e será gerenciada por um serviço dedicado futuro).*

## Passos para Configuração

1.  **Clonar o Repositório:**
    Abra seu terminal ou prompt de comando e clone o repositório do GitHub:
    ```bash
    git clone https://github.com/odevjader/modular-dashboard.git
    cd modular-dashboard
    ```

2.  **Configurar Variáveis de Ambiente (Backend):**
    O backend FastAPI requer um arquivo `.env` na pasta `backend/` para carregar configurações essenciais. O `docker-compose.yml` é configurado para carregar este arquivo.

    * **Variáveis Essenciais:** As seguintes variáveis são lidas pelo Pydantic Settings (`backend/app/core/config.py`) ou usadas pelo Docker Compose e **precisam estar definidas** no `backend/.env`:
        * `DATABASE_URL` **OU** (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`)
        * `APP_PORT`
        * `SECRET_KEY`
        * `ALGORITHM`
        * `ACCESS_TOKEN_EXPIRE_MINUTES`
        * `GOOGLE_API_KEY`

    * *Exemplo `backend/.env` (Completo com essenciais):*
        ```.env
        # Configuração do Banco de Dados (escolha UMA das opções abaixo)
        # Opção 1: Usando DATABASE_URL completa (preferível para a aplicação SQLAlchemy)
        DATABASE_URL=postgresql+asyncpg://appuser:password@db:5432/appdb
        # Opção 2: Usando variáveis individuais (usadas pelo serviço 'db' do compose para inicialização)
        POSTGRES_USER=appuser
        POSTGRES_PASSWORD=password
        POSTGRES_DB=appdb

        # Configuração da Aplicação/Uvicorn (Porta interna do container)
        APP_PORT=8000

        # Configuração JWT (gere SECRET_KEY com: openssl rand -hex 32)
        SECRET_KEY=coloque_aqui_sua_chave_secreta_muito_segura_de_pelo_menos_32_chars_hex
        ALGORITHM=HS256
        ACCESS_TOKEN_EXPIRE_MINUTES=1440 # 24 horas

        # Chaves de API Externas
        GOOGLE_API_KEY=sua_google_api_key_aqui

        # Opcional: Outras configurações (ver backend/app/core/config.py para lista completa)
        # ENVIRONMENT=development
        # PROJECT_NAME="Modular Dashboard"
        # ALLOWED_ORIGINS='["http://localhost:5173","http://127.0.0.1:5173"]' # Exemplo para CORS
        ```
    * **Segurança:** Nunca comite o arquivo `.env` no Git. Garanta que ele esteja no `.gitignore`.

3.  **Iniciar os Containers Docker:**
    A partir da raiz do projeto (`modular-dashboard/`), execute o Docker Compose para construir as imagens (se necessário) e iniciar os containers do backend (serviço `api`) e do banco de dados (serviço `db`).
    ```bash
    docker compose up -d --build
    ```
    * A opção `-d` executa os containers em modo detached (background).
    * A opção `--build` força a reconstrução das imagens se houver mudanças no `Dockerfile` ou arquivos relacionados.
    * Aguarde até que os containers estejam em execução. Você pode verificar com `docker compose ps`.

4.  **Aplicar Migrações do Banco de Dados (Alembic):**
    Após o container `api` estar em execução, aplique as migrações do banco de dados para garantir que o schema esteja atualizado.
    ```bash
    docker compose exec api alembic upgrade head
    ```

5.  **Criar Usuário Administrador Inicial (Opcional):**
    O projeto inclui um script para criar um usuário administrador padrão (`admin@gmail.com` / `admin@gmail.com`). Para executá-lo:
    ```bash
    docker compose exec api python app/create_admin_user.py
    ```
    O script verificará se o usuário já existe. Se existir e não for admin ou estiver inativo, tentará atualizá-lo.

6.  **Instalar Dependências do Frontend:**
    Navegue até a pasta `frontend/` e use `npm` para instalar as dependências:
    ```bash
    cd frontend
    npm install
    cd ..
    ```

7.  **Iniciar o Servidor de Desenvolvimento do Frontend:**
    Ainda dentro da pasta `frontend/`, inicie o servidor de desenvolvimento Vite:
    ```bash
    cd frontend
    npm run dev
    ```
    O terminal indicará em qual porta o servidor frontend está rodando (normalmente `http://localhost:5173`).

8.  **Acessar a Aplicação:**
    Abra seu navegador e acesse:
    * **Frontend:** `http://localhost:5173` (ou a porta indicada pelo `npm run dev`)
    * **Backend API Docs (Swagger UI):** `http://localhost:8000/docs` (Assumindo `APP_PORT=8000` e porta exposta `8000:8000` no compose)
    * **Backend API Docs (ReDoc):** `http://localhost:8000/redoc`

## Parando o Ambiente

Para parar os containers Docker quando terminar de trabalhar, execute na raiz do projeto:
```bash
docker compose down
```
Isto irá parar e remover os containers. Os volumes de dados do banco de dados (se configurados) geralmente são preservados.