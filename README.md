#README.md
# Modular Dashboard

> Uma **plataforma base versátil e extensível** projetada para acelerar o desenvolvimento de aplicações web modulares e dashboards interativos, com capacidade de integração com Inteligência Artificial.

## Status Atual

**(Abril de 2025)**: 🚧 Desenvolvimento Ativo - **Foco na Arquitetura Core e Processos** 🚧

O projeto está em desenvolvimento ativo, com foco na refatoração da estrutura da API Core, na implementação do mecanismo de modularidade e na solidificação dos processos de desenvolvimento.

* **Processo de Gestão:** O modelo inicial de gestão de projetos usando GitHub Issues e Project Board foi definido e documentado (ver `docs/08_PROJECT_MANAGEMENT.md`).
* **Status Técnico:**
    * O bloqueio anterior relacionado ao build da imagem Docker da API (`failed to fetch oauth token`) foi reportado como resolvido (pendente de verificação final no próximo build/execução).
    * O **foco técnico atual** é a **Refatoração da Estrutura da API Core** para separar módulos Core dos opcionais (Issue #9).
    * A implementação do **Mecanismo de Modularidade V1** (Issue #8) é a próxima tarefa técnica principal.
    * A correção do bug no endpoint de login (`/api/auth/v1/login`) está planejada para após a implementação da modularidade V1.
    * A estrutura base do módulo core de Autenticação e Gerenciamento de Usuários no backend está implementada, aguardando testes após a correção do login.
* **Melhorias de Processo Adiadas:** A implementação de templates de Issue/PR e Milestones foi adiada (ver backlog).
* **Módulos Exemplo:** Continuam temporariamente desativados.

## Visão Geral da Arquitetura

O projeto segue uma arquitetura com Frontend SPA (Single Page Application) e Backend API RESTful, orquestrados via Docker Compose, projetado para ser uma base modular versátil.

* **Frontend:** React (TypeScript) com Material UI, Vite e Zustand. Fornece o shell da aplicação e a interface para os módulos. O fluxo de login está temporariamente desativado na UI.
* **Backend:** API RESTful Assíncrona com FastAPI (Python), SQLAlchemy. Provê os serviços Core (Auth, User) e os endpoints para os módulos. Permite integração com IA (Langchain).
* **Banco de Dados:** PostgreSQL com extensão pgvector. Usado pelo Core e potencialmente pelos módulos.
* **Infraestrutura:** Docker e Docker Compose para containerização e ambiente de desenvolvimento.

*(Consulte [docs/01_ARQUITETURA.md](./docs/01_ARQUITETURA.md) para detalhes arquiteturais e `docs/08_PROJECT_MANAGEMENT.md` para o fluxo de gestão).*

## Principais Tecnologias

### Frontend

* Linguagem: TypeScript
* Framework/Lib: React 18+
* Build: Vite
* UI Kit: Material UI (MUI) v5+
* Roteamento: react-router-dom v6+
* Estado: Zustand (para estado global/compartilhado), estado local React.
* HTTP Client: `Workspace` API nativa (ou Axios, a verificar)

### Backend

* Linguagem: Python 3.12
* Framework: FastAPI
* ORM: SQLAlchemy 2+ (Asyncio)
* Banco de Dados Driver: `asyncpg`
* Migrações: Alembic
* IA Libs: Langchain, `langchain-google-genai`, `google-generativeai` *(Nota: Uso principal adiado para Fase 2+)*
* Processamento PDF: `docling` *(Nota: Removido do Core API na Fase 1)*
* Servidor ASGI: Uvicorn (com `uvloop`)
* Outros: Pydantic v2, Passlib (`bcrypt`), python-jose (`cryptography`), `pydantic-settings`

### Banco de Dados

* SGBD: PostgreSQL 16+
* Extensões: pgvector

### Infraestrutura & DevOps

* Containerização: Docker, Docker Compose
* Ambiente Dev Principal: WSL 2 (recomendado)
* Controle de Versão: Git, GitHub, GitHub CLI (`gh`)

## Configuração do Ambiente de Desenvolvimento

Instruções detalhadas para clonar o repositório, configurar as variáveis de ambiente (`.env`), iniciar os containers Docker e rodar os servidores de desenvolvimento podem ser encontradas no **[Guia de Setup de Desenvolvimento](./docs/02_SETUP_DESENVOLVIMENTO.md)**. *(Nota: Verificar se o build Docker está estável conforme reportado)*.

## Estrutura do Projeto (Resumo)

* `/frontend`: Contém o código da aplicação React (SPA - Shell da plataforma e UI de módulos).
* `/backend`: Contém o código da API FastAPI (Core da plataforma e APIs de módulos). Espera-se refatoração para `/backend/app/core_modules/` e `/backend/app/modules/`.
* `/docs`: Contém a documentação geral (`00_` a `NN_...`) e a subpasta `/modules`.
* `/docs/modules`: Contém a documentação específica de cada módulo (`01_...`, `02_...`).
* `/.github`: Contém configurações do GitHub (ex: templates, workflows - futuramente).
* `/.logs`: Contém logs e sumários (ex: `task_summaries/`). *(Nota: Verificar regras do .gitignore)*.
* `/.prompts`: Contém templates de prompts para AIs (uso restrito).
* `docker-compose.yml`: Define os serviços Docker (`api`, `db`).
* `README.md`: Este arquivo.
* `ROADMAP.md`: Fases de desenvolvimento planejadas.
*(Consulte [docs/03_ESTRUTURA_PASTAS.md](./docs/03_ESTRUTURA_PASTAS.md) para mais detalhes).*

## Próximos Passos (Foco Atual)

Consulte o [ROADMAP.md](./ROADMAP.md) para detalhes completos. As prioridades imediatas são (referências de Issue do GitHub):

1.  **Refatorar Estrutura: Mover APIs Core para `core_modules/` (#9)** - *(Prioridade Atual)*.
2.  **Implementar Mecanismo de Modularidade v1 (Backend/Frontend - Revisado) (#8)** - *(Depende de #9)*.
3.  **Corrigir bug crítico no endpoint de login (`/api/auth/v1/login`)** - *(Após Modularidade V1)*.
4.  Verificar estabilidade do build Docker e inicialização da API.
5.  Testar e finalizar endpoints Core de Autenticação (`/users/me`) e CRUD Admin (`/admin/users/*`) - *(Depende de #3)*.
6.  Re-integrar fluxo de autenticação e telas de Gerenciamento de Usuários no Frontend Core - *(Depende de #5)*.
7.  Solidificar e documentar as APIs do Core (Auth, User).
8.  Estabelecer padrões claros para desenvolvimento de novos módulos.
9.  Revisitar implementação de Templates de Issue/PR e Milestones (adiados).