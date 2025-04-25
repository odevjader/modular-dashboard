#docs/03_ESTRUTURA_PASTAS.md
# Estrutura de Pastas - Modular Dashboard

Este documento descreve a organização das pastas e arquivos principais do projeto Modular Dashboard, ajudando a navegar pela base de código.

*(Última atualização: 25 de Abril de 2025 - Refletindo introdução de core_modules e movimentação de auth/health)*

## Estrutura Raiz
*(... seção raiz como estava ...)*

## Estrutura do Backend (`backend/`)

A pasta `backend/` contém a aplicação FastAPI e seus arquivos relacionados:

* **`app/`**: O diretório principal do código da aplicação FastAPI.
    * **`main.py`**: Ponto de entrada da aplicação FastAPI.
    * **`api_router.py`**: Agrega os roteadores (de `core_modules` e `modules`).
    * **`core/`**: Lógica central e configurações compartilhadas (config, database, security, dependencies).
    * **`models/`**: Modelos SQLAlchemy (ex: `user.py`, `enums.py`).
    * **`core_modules/`**: Contém módulos **essenciais** para o funcionamento base da plataforma.
        * `auth/`
            * `v1/` (endpoints, schemas, etc. para Auth/User)
        * `health/`
            * `v1/` (endpoints, schemas, etc. para Health Check)
    * **`modules/`**: Contém módulos **funcionais plugáveis e opcionais**.
        * `info/`
        * `ai_test/`
        * `gerador_quesitos/`
        * *(Novos módulos funcionais serão adicionados aqui)*
    * **`versions/`**: Scripts de migração Alembic.
    * **`alembic.ini`**: Configuração Alembic.
* **`Dockerfile`**: Build da imagem Docker backend.
* **`.env`**: Variáveis de ambiente (não versionado).
* **`requirements.txt` ou `pyproject.toml`**: Dependências Python.

## Estrutura do Frontend (`frontend/`)
*(... seção frontend como estava ...)*

## Estrutura da Documentação (`docs/`)
*(... seção docs como estava ...)*