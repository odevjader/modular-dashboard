#docs/01_ARQUITETURA.md
# Arquitetura do Modular Dashboard

Este documento descreve a arquitetura de alto nível do projeto Modular Dashboard, seus principais componentes, o fluxo de dados, as decisões de design fundamentais, o mecanismo de modularidade e a estratégia de configuração.

*(Última atualização: 25 de Abril de 2025 - Refletindo estrutura core_modules e fluxo de trabalho V5)*

## Visão Geral

O Modular Dashboard adota uma arquitetura de **Monorepo** contendo:
* Uma aplicação **Frontend SPA (Single Page Application)** responsável pela interface do **Dev** (React/TypeScript/Vite).
* Um **Backend API RESTful Assíncrono** que expõe os endpoints e contém a lógica de negócio (FastAPI/Python/SQLAlchemy).
* Um **Banco de Dados Relacional** para persistência (PostgreSQL/pgvector).

O ambiente é orquestrado via **Docker e Docker Compose**, e a arquitetura é projetada para ser uma **plataforma base versátil e extensível**.

## Componentes Principais

1.  **Frontend (React SPA):** Responsável pela interface do usuário (UI), interação com o **Dev**, gerenciamento de estado da UI (local e global com Zustand), e chamadas para a API Backend. Atua como o "shell" ou "casca" onde as UIs dos diferentes módulos são carregadas e apresentadas de forma integrada.
2.  **Backend (FastAPI API):** Expõe endpoints RESTful para o frontend e potencialmente para outros serviços. Lida com a lógica de negócios **Core** da plataforma (localizada em `app/core_modules/`, ex: Autenticação, Health Check) e também expõe as funcionalidades específicas de cada **módulo plugável** carregado (localizados em `app/modules/`). Realiza validação de dados, interage com o banco de dados de forma assíncrona, integra com serviços de IA (via Langchain) e gerencia a segurança. (Ver `docs/03_ESTRUTURA_PASTAS.md` para detalhes).
3.  **Banco de Dados (PostgreSQL + pgvector):** Armazena os dados persistentes da aplicação. Isso inclui dados do Core (tabelas `users`, `configuracoes_aplicacao`, `user_preferences`) e potentially tabelas específicas criadas e gerenciadas por módulos individuais (requer definição de estratégia de migração e nomes). A extensão `pgvector` habilita capacidades de busca semântica.
4.  **Docker / Docker Compose:** Containeriza os serviços principais (Backend API, Banco de Dados e, futuramente, o serviço de processamento de PDF/OCR) para garantir um ambiente de desenvolvimento consistente, portátil e facilmente replicável. Gerencia a rede interna, volumes de dados e variáveis de ambiente. (Nota: Considera-se mover o processamento pesado de PDF/OCR para um container dedicado no futuro - ver `ROADMAP.md`).
5.  **RooCode (Ferramenta VS Code):** Ferramenta integrada que atua como **Agente IA Coder** (com acesso direto a arquivos/terminal supervisionado pelo Dev) e como executor de prompts `Action/Path/Content` gerados pelo **Maestro IA** (para aplicar atualizações de documentação), operado pelo **Dev**.

## Diagrama de Arquitetura (Containers C4)

O diagrama abaixo ilustra os principais containers (componentes de alto nível) do sistema e suas interações primárias:

C4Container
  title Diagrama de Containers - Modular Dashboard

  Person(dev, "Dev", "Desenvolvedor Humano (Admin, User, etc.)")

  System_Boundary(platform, "Modular Dashboard") {
    Container(frontend, "Frontend SPA", "React, TypeScript, Vite", "Interface com o Dev (Shell + UIs dos Módulos)")
    Container(backend, "Backend API", "FastAPI, Python", "Core Modules (Auth, Health), Pluggagle Modules, Lógica, Orquestração IA") # Descrição Atualizada
    ContainerDb(db, "Banco de Dados", "PostgreSQL, pgvector", "Armazena dados da plataforma e módulos")
    Container(ocr_service, "Serviço PDF/OCR", "Python/Tesseract (TBD)", "Processamento pesado de PDFs/OCR (Futuro, container separado)")
  }

  System_Ext(google_ai, "Google AI API", "Serviço Externo (Gemini/Gemma)")

  Rel(dev, frontend, "Usa (Navegador)", "HTTPS")
  Rel(frontend, backend, "Faz chamadas API", "HTTPS/JSON")
  Rel(backend, db, "Lê/Escreve", "JDBC/TCP (via SQLAlchemy)")
  Rel(backend, google_ai, "Chama API", "HTTPS")
  Rel(backend, ocr_service, "Delega Processamento", "HTTP/RPC? (Futuro)")

  UpdateLayoutConfig({
    "layout": {
      "default": {
        "nodeMargin": 15,
        "rankMargin": 60
      }
    }
  })

## Mecanismo de Modularidade (Abordagem Inicial Planejada)

A capacidade de "plugar" módulos independentes é central para a visão do projeto. A abordagem inicial planejada busca um equilíbrio entre flexibilidade e simplicidade:

### Backend (FastAPI)

* **Carregamento Dinâmico de Roteadores via Configuração:** Em vez de registrar rotas de módulos estaticamente no código (`app.include_router(...)` hardcoded), a aplicação Core lerá um arquivo de configuração central na inicialização (ex: `backend/app/modules.yaml`). *Nota: Módulos Core (em `core_modules`) podem ser carregados estaticamente ou via config, a definir.*
* **`modules.yaml` (Exemplo Conceitual):**

# backend/app/modules.yaml
# Lista de módulos plugáveis backend ativos e suas configurações de roteamento
active_pluggable_modules:
  # Exemplo de um módulo core que *poderia* ser configurável (alternativa ao hardcoding)
  # - name: auth_user
  #   router_path: app.core_modules.auth.v1.endpoints.router
  #   prefix: /api/auth/v1
  #   tags: ["Core", "Autenticação", "Usuários"]
  - name: gerador_quesitos
    router_path: app.modules.gerador_quesitos.v1.endpoints.router # Módulo plugável
    prefix: /api/gerador_quesitos/v1
    tags: ["Módulo Exemplo", "IA", "Jurídico"]
  # Novos módulos plugáveis são adicionados/removidos aqui

* **Processo de Inicialização:** O Core FastAPI itera sobre os módulos configurados, importa dinamicamente o `router_path` e chama `app.include_router()` com os metadados.
* **Vantagens:** Flexibilidade para ativar/desativar módulos plugáveis via configuração.
* **Dependências Core:** Módulos plugáveis podem acessar serviços Core através da injeção de dependências padrão do FastAPI.

### Frontend (React)

* **Code Splitting Baseado em Rota:** Utilizaremos o padrão `React.lazy()` e `import()` dinâmico do JavaScript para carregar o código de um módulo apenas quando o **Dev** navegar para uma rota pertencente àquele módulo.
* **Registro de Módulos:** Um arquivo central (ex: `frontend/src/config/moduleRegistry.ts`) definirá o mapeamento entre uma chave de identificação de módulo (string) e o carregamento dinâmico do seu componente principal.

// Exemplo: frontend/src/config/moduleRegistry.ts
import { lazy } from 'react';
const moduleRegistry: Record<string, React.LazyExoticComponent<any>> = {
  'GERADOR_QUESITOS': lazy(() => import('../modules/gerador-quesitos/GeradorQuesitosPage')),
  'AUTH_USER_ADMIN': lazy(() => import('../modules/auth-user/AdminUsersPage')),
  // Novos módulos adicionam sua entrada aqui
};
export default moduleRegistry;

* **Roteamento:** O roteador principal (`react-router-dom`) usará esse registro para definir as rotas, envolvendo os componentes importados com `React.Suspense`.
* **Vantagens:** Otimiza o carregamento inicial. Abordagem padrão React/Vite. Permite compartilhamento fácil de estado/componentes Core.

## Estratégia de Configuração Geral

A gestão de configurações segue uma abordagem em camadas:

1.  **Arquivos `.env` (Não Versionados):**
    * **Uso:** Segredos, URLs externas, configs que variam por **ambiente**.
    * **Localização:** `backend/.env`, `frontend/.env` (con `VITE_`).
    * **NUNCA** commitados.
2.  **Arquivos de Configuração Versionados (YAML/JSON no Backend, TS/JSON no Frontend):**
    * **Uso:** Configs **estruturais** não secretas (módulos ativos, navegação).
    * **Exemplos:** `backend/app/modules.yaml`, `frontend/src/config/navigation.ts`, `frontend/src/config/moduleRegistry.ts`.
    * **DEVEM** ser commitados.
3.  **Banco de Dados:**
    * **Uso:** Configs alteráveis **dinamicamente em runtime** ou **específicas por entidade** (Admin ou Dev).
    * **Exemplos:** Configs Globais/Admin (modelo IA padrão) na tabela `configuracoes_aplicacao`; Preferências do **Dev** (tema) na tabela `user_preferences`.
    * **Versionamento:** Schema via Alembic; dados não ficam no Git.

*(Esta estratégia busca equilibrar flexibilidade, segurança e manutenibilidade).*

## Fluxo de Dados Típico (Alto Nível)

1.  **Dev** interage com o **Frontend**.
2.  Frontend envia requisição HTTP (com JWT) para o **Backend**.
3.  Backend processa: valida, autentica/autoriza, executa lógica (Core ou Módulo).
4.  Se necessário, Backend interage com o **Banco de Dados**.
5.  Se necessário, Backend interage com **Serviços Externos** (Google AI, futuro OCR).
6.  Backend retorna JSON para o Frontend.
7.  Frontend atualiza estado e re-renderiza UI.

**Diagrama Simplificado (Texto):** *(Nota: O diagrama Mermaid acima oferece uma visão mais estruturada)*

 [Frontend: React SPA] <--(HTTP/REST + JWT)--> [Backend: FastAPI Core + Módulos] <--(SQLAlchemy/asyncpg)--> [PostgreSQL + pgvector]
         ^                                                    |
         |                                                    | (LangChain / Outras Libs)
         +--------------------------------------------------- V
                                                       [APIs Externas (Ex: Google AI)]
                                                       [Futuro: Serviço PDF/OCR Dedicado]

*(Nota: Interação do Dev com Frontend omitida para simplicidade no diagrama texto)*

## Pilha Tecnológica (Resumo)

* **Frontend:** React, TypeScript, Vite, Material UI (MUI), Zustand, react-router-dom
* **Backend:** Python, FastAPI, SQLAlchemy (Asyncio), Alembic, Langchain, Pydantic, Uvicorn
* **Banco de Dados:** PostgreSQL, pgvector
* **Infraestrutura:** Docker, Docker Compose, Git, GitHub

*(Consulte o README.md para links e versões específicas)*

## Decisões Arquiteturais Chave (Revisado)

* Monorepo
* SPA + API RESTful
* Backend Assíncrono
* Tipagem Estática Forte (TS/Python+Pydantic)
* Containerização (Docker)
* PostgreSQL + pgvector
* Modularidade via Configuração e Carregamento Dinâmico
* Autenticação JWT
* Estratégia de Configuração em Camadas (Env/Versioned/DB)

## Estrutura de Pastas

Uma descrição detalhada da organização das pastas do projeto pode ser encontrada em **[docs/03_ESTRUTURA_PASTAS.md](./03_ESTRUTURA_PASTAS.md)**. *(Este arquivo foi atualizado para refletir a estrutura `core_modules`)*.