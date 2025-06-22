# Modular Dashboard

> Uma **plataforma base versátil e extensível** projetada para acelerar o desenvolvimento de aplicações web modulares e dashboards interativos, com capacidade de integração com Inteligência Artificial.

## Visão Geral da Arquitetura

O projeto segue uma arquitetura com Frontend SPA (React/Vite) e Backend API RESTful (FastAPI), orquestrados via Docker Compose. Foi projetado para ser uma base modular versátil, onde os módulos são carregados dinamicamente com base em configurações centrais, permitindo maior flexibilidade tanto no backend quanto no frontend.

* **Frontend:** React (TypeScript) com Material UI, Vite e Zustand.
* **Backend:** API RESTful Assíncrona com FastAPI (Python), SQLAlchemy. Provê os serviços Core (em `core_modules`) e os endpoints para os módulos plugáveis (`modules`).
* **Banco de Dados:** PostgreSQL com extensão pgvector.
* **Infraestrutura:** Docker e docker compose.

*(Consulte [docs/01_ARQUITETURA.md](./docs/01_ARQUITETURA.md) para detalhes arquiteturais e [docs/07_FLUXO_DESENVOLVIMENTO_E_ONBOARDING.md](./docs/07_FLUXO_DESENVOLVIMENTO_E_ONBOARDING.md) para o fluxo de desenvolvimento).*

Para informações detalhadas sobre como desenvolver e integrar novos módulos à plataforma, consulte o **[Guia de Desenvolvimento de Novos Módulos](./docs/modules/00_DEVELOPING_MODULES.md)**.

## Principais Tecnologias

- **Frontend:** React, TypeScript, Vite, Material UI (MUI), Zustand, react-router-dom
- **Backend:** Python, FastAPI, SQLAlchemy (Asyncio), Alembic, Langchain, Pydantic, Uvicorn
- **Banco de Dados:** PostgreSQL, pgvector
- **Infraestrutura:** Docker, Docker Compose, Git, GitHub

## Configuração do Ambiente de Desenvolvimento

Consulte o guia detalhado em **[docs/02_CONFIGURACAO_AMBIENTE.md](./docs/02_CONFIGURACAO_AMBIENTE.md)**.

## Estrutura do Projeto (Resumo)

* `/frontend`: Código da aplicação React (SPA).
* `/backend`: Código da API FastAPI.
    * `/backend/app/core_modules`: Módulos essenciais (ex: `auth`, `health`).
    * `/backend/app/modules`: Módulos funcionais plugáveis.
* `/docs`: Documentação geral do projeto.
* `docker-compose.yml`: Serviços Docker.
* `README.md`: Este arquivo.
* `ROADMAP.md`: Fases de desenvolvimento.

*(Consulte [docs/03_ESTRUTURA_PASTAS.md](./docs/03_ESTRUTURA_PASTAS.md) para mais detalhes).*

## Próximos Passos

Consulte o [ROADMAP.md](./ROADMAP.md) para detalhes sobre as próximas funcionalidades e fases de desenvolvimento do projeto.
