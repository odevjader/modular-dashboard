# Guia de Setup de Desenvolvimento - Modular Dashboard

Este guia descreve os passos necessários para configurar e executar o projeto Modular Dashboard em um ambiente de desenvolvimento local utilizando Docker e Node.js.

## Pré-requisitos

Antes de começar, certifique-se de ter as seguintes ferramentas instaladas em seu sistema:

* [Git](https://git-scm.com/): Para clonar o repositório.
* [Docker](https://www.docker.com/products/docker-desktop/): Para gerenciamento de containers (inclui Docker Compose V2+).
* [Node.js](https://nodejs.org/): Versão 18 ou superior (inclui npm) para o desenvolvimento frontend.
* (Recomendado) WSL 2 se estiver utilizando Windows, para melhor integração com Docker.

## Passos para Configuração

1.  **Clonar o Repositório:**
    Abra seu terminal ou prompt de comando e clone o repositório do GitHub:
    ```bash
    git clone https://github.com/odevjader/modular-dashboard.git
    cd modular-dashboard
    ```

2.  **Configurar Variáveis de Ambiente (Backend):**
    O backend FastAPI requer um arquivo `.env` para carregar configurações essenciais, como credenciais do banco de dados e chaves de API.

    * Navegue até a pasta `backend/`.
    * Crie um arquivo chamado `.env` nesta pasta (`backend/.env`).
    * Preencha o arquivo `backend/.env` com as variáveis necessárias. Consulte a classe `Settings` no arquivo `backend/app/core/config.py` para a lista completa de variáveis possíveis. As variáveis mínimas essenciais são:

        ```.env
        # PostgreSQL Settings (Estes são os valores padrão definidos no docker-compose.yml)
        # Certifique-se que correspondem ao serviço 'db' no compose.
        DATABASE_URL=postgresql+asyncpg://appuser:password@db:5432/appdb

        # JWT Settings
        # Gere uma chave segura usando: openssl rand -hex 32
        SECRET_KEY=coloque_aqui_sua_chave_secreta_muito_segura_gerada_com_openssl_rand_hex_32
        ALGORITHM=HS256
        ACCESS_TOKEN_EXPIRE_MINUTES=1440 # Expiração do token em minutos (1440 = 24 horas)

        # Google API Key
        # Insira sua chave de API obtida do Google AI Studio (Makersuite) para usar o Gemini
        GOOGLE_API_KEY=sua_google_api_key_aqui

        # Outras configurações podem ser adicionadas conforme necessário (veja config.py)
        # ENVIRONMENT=development
        # PROJECT_NAME="Modular Dashboard"
        ```
    * **Segurança:** Nunca comite o arquivo `.env` no Git. Ele já deve estar incluído no `.gitignore`.

3.  **Iniciar os Containers Docker:**
    A partir da raiz do projeto (`modular-dashboard/`), execute o Docker Compose para construir as imagens (se necessário) e iniciar os containers do backend (serviço `api`) e do banco de dados (serviço `db`).
    ```bash
    docker-compose up -d --build
    ```
    * A opção `-d` executa os containers em modo detached (background).
    * A opção `--build` força a reconstrução das imagens se houver mudanças no `Dockerfile` ou arquivos relacionados. O primeiro build pode levar alguns minutos.
    * Aguarde até que os containers estejam em execução e saudáveis. Você pode verificar com `docker-compose ps`.

4.  **Aplicar Migrações do Banco de Dados (Alembic):**
    Após o container `api` estar em execução, é recomendado aplicar as migrações do banco de dados para garantir que o schema esteja atualizado. Execute o comando `upgrade` do Alembic dentro do container `api`:
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

Pronto! Agora você deve ter o ambiente de desenvolvimento do Modular Dashboard rodando localmente. Lembre-se que o backend está atualmente com um bug no login que precisa ser resolvido.