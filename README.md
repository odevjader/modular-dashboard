#README.md
# Modular Dashboard

> Uma **plataforma base versátil e extensível** projetada para acelerar o desenvolvimento de aplicações web modulares e dashboards interativos, com capacidade de integração com Inteligência Artificial.

## Status Atual

**(Dezembro de 2025)**: ✅ **Funcional e em Desenvolvimento Ativo** 🚧

O projeto está com seu ambiente de desenvolvimento 100% funcional. O bug crítico de login (Issue #11), que antes impedia o progresso, foi **resolvido** através da correta configuração do ambiente (proxy do Vite e limpeza de dependências).

Com a autenticação funcionando, o projeto está desbloqueado e o foco agora se volta para as próximas prioridades do roadmap.

* **Processo de Gestão:** Definido e documentado (ver `docs/08_PROJECT_MANAGEMENT.md`).
* **Status Técnico:**
    * O fluxo de autenticação base (login, validação de token) está **operacional**.
    * As refatorações do Core (Issues #9, #17) foram **concluídas**.
    * A **Implementação do Mecanismo de Modularidade V1** (Issue #8) foi **concluída**.
    * Os **Padrões para desenvolvimento de novos módulos (Issue #16)** foram estabelecidos e documentados. A Fase 1 do projeto foi concluída. A próxima prioridade é **Criar Serviço Dedicado para PDF/OCR (Issue #7)** da Fase 2.

## Visão Geral da Arquitetura

O projeto segue uma arquitetura com Frontend SPA (React/Vite) e Backend API RESTful (FastAPI), orquestrados via Docker Compose, projetado para ser uma base modular versátil.

* **Frontend:** React (TypeScript) com Material UI, Vite e Zustand.
* **Backend:** API RESTful Assíncrona com FastAPI (Python), SQLAlchemy. Provê os serviços Core (em `core_modules`) e os endpoints para os módulos plugáveis (`modules`).
    * Os módulos agora são carregados dinamicamente com base em configurações centrais, tanto no backend quanto no frontend, permitindo maior flexibilidade.*
* **Banco de Dados:** PostgreSQL com extensão pgvector.
* **Infraestrutura:** Docker e Docker Compose.

*(Consulte [docs/01_ARQUITETURA.md](./docs/01_ARQUITETURA.md) para detalhes arquiteturais e [docs/07_FLUXO_TRABALHO_DEV.md](./docs/07_FLUXO_TRABALHO_DEV.md) para o fluxo de desenvolvimento).*

Para informações detalhadas sobre como desenvolver e integrar novos módulos à plataforma, consulte o **[Guia de Desenvolvimento de Novos Módulos](./docs/modules/00_DEVELOPING_MODULES.md)**.

## Principais Tecnologias

- **Frontend:** React, TypeScript, Vite, Material UI (MUI), Zustand, react-router-dom
- **Backend:** Python, FastAPI, SQLAlchemy (Asyncio), Alembic, Langchain, Pydantic, Uvicorn
- **Banco de Dados:** PostgreSQL, pgvector
- **Infraestrutura:** Docker, Docker Compose, Git, GitHub

## Configuração do Ambiente de Desenvolvimento

Consulte o guia detalhado em **[docs/02_SETUP_DESENVOLVIMENTO.md](./docs/02_SETUP_DESENVOLVIMENTO.md)**.

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

## Próximos Passos (Foco Atual)

Consulte o [ROADMAP.md](./ROADMAP.md) para detalhes completos. As prioridades imediatas são (referências de Issue do GitHub):

1.  **Criar Serviço Dedicado para PDF/OCR (Issue #7)** - *(Prioridade Atual)*.