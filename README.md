#README.md
# Modular Dashboard

> Uma **plataforma base versátil e extensível** projetada para acelerar o desenvolvimento de aplicações web modulares e dashboards interativos, com capacidade de integração com Inteligência Artificial.

## Status Atual

**(Abril de 2025)**: 🚧 Desenvolvimento Ativo - **Foco na Resolução de Bloqueios Técnicos e Processos** 🚧

O projeto está em desenvolvimento ativo, focado na construção do núcleo (Core) da plataforma e na solidificação dos processos de desenvolvimento.

* **Processo de Gestão:** O modelo inicial de gestão de projetos usando GitHub Issues e Project Board foi definido e documentado (ver `docs/08_PROJECT_MANAGEMENT.md`).
* **Status Técnico:**
    * O bloqueio anterior relacionado ao build da imagem Docker da API (`failed to fetch oauth token`) foi reportado como resolvido (pendente de verificação final no próximo build/execução).
    * O **foco técnico atual** é a correção de um bug conhecido no endpoint de login (`/api/auth/v1/login`).
    * A estrutura base do módulo core de Autenticação e Gerenciamento de Usuários no backend está implementada, aguardando testes após a correção do login.
* **Melhorias de Processo Adiadas:** A implementação de templates de Issue/PR e Milestones foi adiada para focar nas prioridades atuais.
* **Módulos Exemplo:** Continuam temporariamente desativados até a estabilização do Core e do fluxo de login.

## Visão Geral da Arquitetura

O projeto segue uma arquitetura com Frontend SPA (Single Page Application) e Backend API RESTful, orquestrados via Docker Compose, projetado para ser uma base modular versátil.

* **Frontend:** React (TypeScript) com Material UI, Vite e Zustand. Fornece o shell da aplicação e a interface para os módulos. O fluxo de login está temporariamente desativado na UI.
* **Backend:** API RESTful Assíncrona com FastAPI (Python), SQLAlchemy. Provê os serviços Core (Auth, User) e os endpoints para os módulos. Permite integração com IA (Langchain).
* **Banco de Dados:** PostgreSQL com extensão pgvector. Usado pelo Core e potencialmente pelos módulos.
* **Infraestrutura:** Docker e Docker Compose para containerização e ambiente de desenvolvimento.

*(Consulte [docs/01_ARQUITETURA.md](./docs/01_ARQUITETURA.md) para detalhes arquiteturais).*

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
* `/backend`: Contém o código da API FastAPI (Core da plataforma e APIs de módulos).
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

Consulte o [ROADMAP.md](./ROADMAP.md) para detalhes completos. As prioridades imediatas são:

1.  **Corrigir o bug no endpoint de login (`/api/auth/v1/login`)** do módulo core de Autenticação - **Principal Bloqueio Funcional.**
2.  Verificar estabilidade do build Docker e inicialização da API.
3.  Finalizar e testar funcionalmente o módulo core de Autenticação e Gerenciamento de Usuários (backend e frontend) - *Depende do passo 1*.
4.  **Definir e implementar o Mecanismo de Modularidade** (backend e frontend) - Decisão arquitetural chave.
5.  Solidificar e documentar as APIs do Core da plataforma (Auth, User, etc.).
6.  Estabelecer padrões claros para o desenvolvimento de novos módulos.
7.  Revisitar implementação de Templates de Issue/PR e Milestones (adiados).