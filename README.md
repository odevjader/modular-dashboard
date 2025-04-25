#README.md
# Modular Dashboard

> Uma **plataforma base versátil e extensível** projetada para acelerar o desenvolvimento de aplicações web modulares e dashboards interativos, com capacidade de integração com Inteligência Artificial.

## Status Atual

**(Abril de 2025)**: 🚧 Desenvolvimento Ativo - **Foco na Modularidade** 🚧

O projeto está em desenvolvimento ativo. As refatorações da estrutura da API Core para separar módulos Core (`auth`, `health` em `core_modules/`) foram concluídas (Issues #9, #17). O fluxo de trabalho Humano-IA foi refinado e formalizado (ver `docs/07_FLUXO_TRABALHO_DEV.md`). O foco agora está na implementação do mecanismo de modularidade V1 (Issue #8).

* **Processo de Gestão:** Definido e documentado (ver `docs/08_PROJECT_MANAGEMENT.md`).
* **Status Técnico:**
    * Refatorações Core (Issues #9, #17) **concluídas**. Módulos `auth` e `health` movidos para `backend/app/core_modules/`.
    * O **foco técnico atual** é a **Implementação do Mecanismo de Modularidade V1** (Backend/Frontend) (Issue #8).
    * A correção do bug no endpoint de login (`/api/auth/v1/login`) (Issue #11) está planejada para após a implementação da modularidade V1.
    * O fluxo de login do Frontend continua temporariamente desativado/mantido (Issue #12).
* **Melhorias de Processo Adiadas:** Templates de Issue/PR e Milestones (ver backlog).
* **Módulos Exemplo:** Continuam temporariamente desativados.

## Visão Geral da Arquitetura

O projeto segue uma arquitetura com Frontend SPA (React/Vite) e Backend API RESTful (FastAPI), orquestrados via Docker Compose, projetado para ser uma base modular versátil.

* **Frontend:** React (TypeScript) com Material UI, Vite e Zustand.
* **Backend:** API RESTful Assíncrona com FastAPI (Python), SQLAlchemy. Provê os serviços Core (agora em `core_modules`) e os endpoints para os módulos plugáveis (`modules`).
* **Banco de Dados:** PostgreSQL com extensão pgvector.
* **Infraestrutura:** Docker e Docker Compose.

*(Consulte [docs/01_ARQUITETURA.md](./docs/01_ARQUITETURA.md) para detalhes arquiteturais, [docs/07_FLUXO_TRABALHO_DEV.md](./docs/07_FLUXO_TRABALHO_DEV.md) para o fluxo de desenvolvimento, e `docs/08_PROJECT_MANAGEMENT.md` para a gestão).*

## Principais Tecnologias
*(... seção de tecnologias como estava ...)*

## Configuração do Ambiente de Desenvolvimento
*(... seção de setup como estava ...)*

## Estrutura do Projeto (Resumo)

* `/frontend`: Código da aplicação React (SPA).
* `/backend`: Código da API FastAPI.
    * `/backend/app/core_modules`: Módulos essenciais (ex: `auth`, `health`).
    * `/backend/app/modules`: Módulos funcionais plugáveis.
* `/docs`: Documentação geral (`00_` a `NN_...`) e subpasta `/modules`.
* `/docs/modules`: Documentação específica de módulos plugáveis.
* `/.github`: Configurações GitHub (futuro).
* `/.logs`: Logs e sumários.
* `/.prompts`: Templates de prompts (uso restrito).
* `docker-compose.yml`: Serviços Docker.
* `README.md`: Este arquivo.
* `ROADMAP.md`: Fases de desenvolvimento.
*(Consulte [docs/03_ESTRUTURA_PASTAS.md](./docs/03_ESTRUTURA_PASTAS.md) para mais detalhes).*

## Próximos Passos (Foco Atual)

Consulte o [ROADMAP.md](./ROADMAP.md) para detalhes completos. As prioridades imediatas são (referências de Issue do GitHub):

1.  **Implementar Mecanismo de Modularidade v1 (Backend/Frontend - Revisado) (#8)** - *(Prioridade Atual)*.
2.  **Corrigir bug crítico no endpoint de login (`/api/auth/v1/login`) (#11)** - *(Depende de #8)*.
3.  Verificar estabilidade do build Docker e inicialização da API.
4.  Testar e finalizar endpoints Core de Autenticação (`/users/me`) e CRUD Admin (`/admin/users/*`) (#13) - *(Depende de #11)*.
5.  Re-integrar fluxo de autenticação e telas de Gerenciamento de Usuários no Frontend Core (#14) - *(Depende de #13)*.
6.  Solidificar e documentar as APIs do Core (Auth, User) (#15) - *(Idealmente após #13)*.
7.  Estabelecer padrões claros para desenvolvimento de novos módulos (#16) - *(Depende de #8)*.
8.  Revisitar implementação de Templates de Issue/PR e Milestones (adiados).