# Modular Dashboard

> Uma **plataforma base versátil e extensível** projetada para acelerar o desenvolvimento de aplicações web modulares e dashboards interativos, com capacidade de integração com Inteligência Artificial.

## Status Atual

**(Abril de 2025)**: 🚧 Desenvolvimento Ativo - **Foco no Core da Plataforma / Build Bloqueado** 🚧

O projeto está em desenvolvimento ativo, focado na construção do núcleo (Core) da plataforma. A refatoração para remover dependências não-core (PDF/OCR/IA) do container `api` foi concluída no código, **mas a validação está bloqueada pelo erro de build descrito abaixo**. Como resultado, o **módulo exemplo** "Gerador de Quesitos" (`docs/modules/01_GERADOR_QUESITOS.md`) e o módulo `AI Test` (`docs/modules/03_AI_TEST.md`) estão **temporariamente desativados**. A estrutura base do **módulo core** de Autenticação e Gerenciamento de Usuários no backend está implementada, aguardando testes após resolução dos bloqueios.

**⚠️ Bloqueio Atual:** Erro durante o build da imagem Docker da API (`failed to fetch oauth token` ao baixar `python:3.11-slim`), impedindo a inicialização e validação da API. A resolução deste problema de infraestrutura/rede é a **prioridade máxima** atual.

## Visão Geral da Arquitetura

O projeto segue uma arquitetura com Frontend SPA (Single Page Application) e Backend API RESTful, orquestrados via Docker Compose, projetado para ser uma base modular versátil.

*   **Frontend:** React (TypeScript) com Material UI, Vite e Zustand. Fornece o shell da aplicação e a interface para os módulos.
*   **Backend:** API RESTful Assíncrona com FastAPI (Python), SQLAlchemy. Provê os serviços Core (Auth, User) e os endpoints para os módulos. Permite integração com IA (Langchain).
*   **Banco de Dados:** PostgreSQL com extensão pgvector. Usado pelo Core e potencialmente pelos módulos.
*   **Infraestrutura:** Docker e Docker Compose para containerização e ambiente de desenvolvimento.

*(Consulte [docs/01_ARQUITETURA.md](./docs/01_ARQUITETURA.md) para detalhes arquiteturais).*

## Principais Tecnologias

### Frontend

*   Linguagem: TypeScript
*   Framework/Lib: React 18+
*   Build: Vite
*   UI Kit: Material UI (MUI) v5+
*   Roteamento: react-router-dom v6+
*   Estado: Zustand (para estado global/compartilhado), estado local React.
*   HTTP Client: `Workspace` API nativa

### Backend

*   Linguagem: Python 3.12
*   Framework: FastAPI
*   ORM: SQLAlchemy 2+ (Asyncio)
*   Banco de Dados Driver: `asyncpg`
*   Migrações: Alembic
*   IA Libs: Langchain, `langchain-google-genai`, `google-generativeai` *(Nota: Uso principal adiado para Fase 2+)*
*   Processamento PDF: `docling` *(Nota: Removido do Core API na Fase 1)*
*   Servidor ASGI: Uvicorn (com `uvloop`)
*   Outros: Pydantic v2, Passlib (`bcrypt`), python-jose (`cryptography`), `pydantic-settings`

### Banco de Dados

*   SGBD: PostgreSQL 16+
*   Extensões: pgvector

### Infraestrutura & DevOps

*   Containerização: Docker, Docker Compose
*   Ambiente Dev Principal: WSL 2 (recomendado)
*   Controle de Versão: Git, GitHub

## Configuração do Ambiente de Desenvolvimento

Instruções detalhadas para clonar o repositório, configurar as variáveis de ambiente (`.env`), iniciar os containers Docker e rodar os servidores de desenvolvimento podem ser encontradas no **[Guia de Setup de Desenvolvimento](./docs/02_SETUP_DESENVOLVIMENTO.md)**.

## Estrutura do Projeto (Resumo)

*   `/frontend`: Contém o código da aplicação React (SPA - Shell da plataforma e UI de módulos).
*   `/backend`: Contém o código da API FastAPI (Core da plataforma e APIs de módulos).
*   `/docs`: Contém a documentação geral (`00_` a `NN_...`) e a subpasta `/modules`.
*   `/docs/modules`: Contém a documentação específica de cada módulo (`01_...`, `02_...`).
*   `/.prompts`: Contém templates de prompts para AIs (uso restrito).
*   `docker-compose.yml`: Define os serviços Docker (`api`, `db`).
*   `README.md`: Este arquivo.
*   `ROADMAP.md`: Fases de desenvolvimento planejadas.
*(Consulte [docs/03_ESTRUTURA_PASTAS.md](./docs/03_ESTRUTURA_PASTAS.md) para mais detalhes).*

## Próximos Passos (Foco na Plataforma Core - Fase 1)

Consulte o [ROADMAP.md](./ROADMAP.md) para detalhes completos da Fase 1 e além. As prioridades imediatas são:

1.  **Resolver erro de build Docker (`failed to fetch oauth token`)** - **Bloqueador Atual.**
2.  Corrigir o bug no endpoint de login (`/api/auth/v1/login`) do módulo core de Autenticação.
3.  Finalizar e testar funcionalmente o módulo core de Autenticação e Gerenciamento de Usuários (backend e frontend).
4.  **Definir e implementar o Mecanismo de Modularidade** (backend e frontend) - Decisão arquitetural chave.
5.  Solidificar e documentar as APIs do Core da plataforma (Auth, User, etc.).
6.  Estabelecer padrões claros para o desenvolvimento de novos módulos.