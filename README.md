# Modular Dashboard

> Um dashboard web modular projetado para automatizar e auxiliar em tarefas complexas, com foco inicial em aplicações jurídicas/previdenciárias, utilizando Inteligência Artificial generativa.

## Status Atual

**(Abril de 2025)**: 🚧 Desenvolvimento Ativo 🚧

O projeto está em desenvolvimento ativo. O módulo principal "Gerador de Quesitos" está funcional (v1). A estrutura base para Autenticação e Gerenciamento de Usuários no backend está implementada, e o banco de dados está configurado com migrações via Alembic.

**⚠️ Bloqueio Atual:** Existe um bug conhecido no endpoint de login (`/api/auth/v1/login`) que retorna 401 (Usuário não encontrado), impedindo testes do CRUD de usuários e a integração completa do frontend.

## Visão Geral da Arquitetura

O projeto segue uma arquitetura com Frontend SPA (Single Page Application) e Backend API RESTful, orquestrados via Docker Compose.

* **Frontend:** React (TypeScript) com Material UI, Vite e Zustand.
* **Backend:** API RESTful Assíncrona com FastAPI (Python), SQLAlchemy e Langchain para integração com IA.
* **Banco de Dados:** PostgreSQL com extensão pgvector.
* **Infraestrutura:** Docker e Docker Compose para containerização e ambiente de desenvolvimento.

## Principais Tecnologias

### Frontend

* Linguagem: TypeScript
* Framework/Lib: React 18+
* Build: Vite
* UI Kit: Material UI (MUI) v5+
* Roteamento: react-router-dom v6+
* Estado: Zustand
* HTTP Client: `Workspace` API nativa

### Backend

* Linguagem: Python 3.12
* Framework: FastAPI
* ORM: SQLAlchemy 2+ (Asyncio)
* Banco de Dados: PostgreSQL 16+ (com `asyncpg`)
* Migrações: Alembic
* IA: Langchain, `langchain-google-genai`, `google-generativeai`
* Processamento PDF: `docling`
* Servidor ASGI: Uvicorn (com `uvloop`)
* Outros: Pydantic v2, Passlib (`bcrypt`), python-jose (`cryptography`), `pydantic-settings`

### Banco de Dados

* SGBD: PostgreSQL 16+
* Extensões: pgvector

### Infraestrutura & DevOps

* Containerização: Docker, Docker Compose
* Ambiente Dev Principal: WSL 2 (recomendado)
* Controle de Versão: Git, GitHub

## Configuração do Ambiente de Desenvolvimento

Instruções detalhadas para clonar o repositório, configurar as variáveis de ambiente, iniciar os containers Docker e rodar os servidores de desenvolvimento podem ser encontradas no **[Guia de Setup de Desenvolvimento](./docs/02_SETUP_DESENVOLVIMENTO.md)** (Arquivo a ser criado).

## Estrutura do Projeto

* `/frontend`: Contém o código da aplicação React (SPA).
* `/backend`: Contém o código da API FastAPI.
* `docker-compose.yml`: Define os serviços Docker (`api`, `db`).
* *(Futuro: Link para `docs/03_ESTRUTURA_PASTAS.md` para mais detalhes).*

## Próximos Passos

* **Prioridade:** Corrigir o bug no endpoint de login (`/api/auth/v1/login`).
* Testar endpoints de Gerenciamento de Usuários (`/api/auth/v1/admin/users`).
* Integrar fluxo de autenticação e gerenciamento de usuários no Frontend.
* Investigar e otimizar performance do build Docker e do processamento de PDF.
* *(Futuro: Link para `ROADMAP.md` ou documento similar).*