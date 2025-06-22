# docs/04_BANCO_DE_DADOS.md
# Banco de Dados - Modular Dashboard

Este documento descreve a configuração do banco de dados, o schema das tabelas existentes e o processo de gerenciamento de migrações para o projeto Modular Dashboard.

## Tecnologia

* **SGBD:** PostgreSQL v16+ (Executando em um container Docker separado, serviço `db` no `docker-compose.yml`).
* **Extensões:** `pgvector` (Habilitada via imagem Docker `pgvector/pgvector:pg16` para suportar armazenamento e consulta de embeddings vetoriais).
* **ORM:** SQLAlchemy v2+ (Utilizado no modo assíncrono com `asyncpg`).
* **Migrações:** Alembic (Para gerenciar alterações no schema do banco de dados de forma versionada).
* **Conexão:** A string de conexão é configurada via variável de ambiente `DATABASE_URL` no arquivo `backend/.env`, seguindo o formato `postgresql+asyncpg://USER:PASSWORD@HOST:PORT/DBNAME` (ex: `postgresql+asyncpg://appuser:password@db:5432/appdb`).

## Schema Atual

Atualmente, o banco de dados contém a seguinte tabela principal, definida em `backend/app/models/user.py`:

### Tabela: `users`

* **Propósito:** Armazena informações sobre os usuários registrados na plataforma, incluindo credenciais para login e seus níveis de permissão (roles).
* **Definição do Modelo:** Classe `User` em `backend/app/models/user.py`
* **Colunas (conforme `models/user.py`):**

| Nome Coluna       | Tipo de Dados (SQLAlchemy / PostgreSQL) | Descrição                                                                 | Restrições/Notas Importantes                                                     |
| :---------------- | :-------------------------------------- | :------------------------------------------------------------------------ | :------------------------------------------------------------------------------- |
| `id`              | `Integer`                               | Identificador único numérico para cada usuário.                           | Chave Primária (primary_key=True)                                                |
| `email`           | `String`                                | Endereço de e-mail do usuário, usado para login.                          | Único (unique=True), Indexado (index=True), Não Nulo (nullable=False)            |
| `hashed_password` | `String`                                | Senha do usuário armazenada de forma segura (hash usando Passlib/bcrypt). | Não Nulo (nullable=False)                                                        |
| `role`            | `Enum(UserRole)`                        | Nível de permissão do usuário, referenciando o Enum `UserRole`.           | Não Nulo (nullable=False), Padrão: `USER` (default=UserRole.USER)                |
| `is_active`       | `Boolean`                               | Indica se a conta do usuário está ativa (pode fazer login).               | Não Nulo (nullable=False), Padrão no Servidor: `True` (server_default='true')    |
| `created_at`      | `DateTime(timezone=True)`               | Data e hora de quando o usuário foi criado (com fuso horário).            | Não Nulo (nullable=False), Padrão no Servidor: `now()` (server_default=func.now()) |
| `updated_at`      | `DateTime(timezone=True)`               | Data e hora da última atualização do registro (com fuso horário).         | Não Nulo (nullable=False), Padrão no Servidor: `now()`, Atualiza em UPDATE (onupdate=func.now()) |

* **Enum `UserRole`:**
    * Definido em: `backend/app/models/enums.py`
    * Valores Possíveis: `ADMIN`, `USER`.

### Outras Tabelas

Atualmente, além da tabela `users`, não há outras tabelas de aplicação definidas no schema principal do Core. Módulos plugáveis podem definir suas próprias tabelas.

## Migrações (Alembic)

O Alembic é utilizado para gerenciar as alterações no schema do banco de dados de forma incremental e versionada.

* **Configuração:** `backend/app/alembic.ini`
* **Scripts de Migração:** Armazenados na pasta `backend/app/versions/`. Cada arquivo representa uma revisão do schema.
* **Execução de Comandos:** Os comandos do Alembic devem ser executados dentro do container `api` usando `docker compose exec`.

**Comandos Comuns:**

* **Gerar uma nova revisão de migração (após alterar modelos SQLAlchemy):**
    ```bash
    docker compose exec api alembic revision --autogenerate -m "Descreva a mudança aqui"
    ```
    *(Revise o script gerado em `versions/` antes de aplicá-lo!)*

* **Aplicar todas as migrações pendentes (atualizar BD para a última versão):**
    ```bash
    docker compose exec api alembic upgrade head
    ```

* **Reverter a última migração aplicada:**
    ```bash
    docker compose exec api alembic downgrade -1
    ```

* **Verificar a revisão atual do banco de dados:**
    ```bash
    docker compose exec api alembic current