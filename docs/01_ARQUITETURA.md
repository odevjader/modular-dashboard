# Arquitetura do dashboard-adv

Este documento descreve a arquitetura de alto nível do projeto dashboard-adv, seus principais componentes, o fluxo de dados, as decisões de design fundamentais, o mecanismo de modularidade e a estratégia de configuração.

## Visão Geral

O dashboard-adv adota uma arquitetura de **Monorepo** contendo:
* Uma aplicação **Frontend SPA (Single Page Application)** responsável pela interface do usuário final (React/TypeScript/Vite).
* Um **Backend API RESTful Assíncrono** que expõe os endpoints e contém a lógica de negócio (FastAPI/Python/SQLAlchemy).
* Um **Banco de Dados Relacional** para persistência (PostgreSQL/pgvector).

O ambiente é orquestrado via **Docker e Docker Compose**, e a arquitetura é projetada para ser uma **plataforma base versátil e extensível**.

## Componentes Principais

1.  **Frontend (React SPA):** Responsável pela interface do usuário (UI), interação com o usuário final, gerenciamento de estado da UI (local e global com Zustand), e chamadas para a API Backend. Atua como o "shell" ou "casca" onde as UIs dos diferentes módulos são carregadas e apresentadas de forma integrada.
2.  **Backend (FastAPI API):** Expõe endpoints RESTful para o frontend e potencialmente para outros serviços. Lida com a lógica de negócios **Core** da plataforma (localizada em `app/core_modules/`, ex: Autenticação, Health Check) e também expõe as funcionalidades específicas de cada **módulo plugável** carregado (localizados em `app/modules/`). Realiza validação de dados, interage com o banco de dados de forma assíncrona, integra com serviços de IA (via Langchain) e gerencia a segurança. (Ver `docs/03_ESTRUTURA_PASTAS.md` para detalhes).
3.  **Banco de Dados (PostgreSQL + pgvector):** Armazena os dados persistentes da aplicação. Isso inclui dados do Core (tabelas `users`, `configuracoes_aplicacao`, `user_preferences`) e potencialmente tabelas específicas criadas e gerenciadas por módulos individuais (requer definição de estratégia de migração e nomes). A extensão `pgvector` habilita capacidades de busca semântica.
4.  **Serviço Transcritor PDF (`transcritor-pdf`):** Um microserviço FastAPI/Python dedicado que utiliza Celery para processamento assíncrono de arquivos PDF. Ele é responsável por extrair texto e informações estruturadas de documentos (potencialmente usando LLMs), gerar embeddings vetoriais e armazená-los no banco de dados PostgreSQL/pgvector. O Backend API principal delega o processamento de PDFs para este serviço.
5.  **Docker / Docker Compose:** Containeriza os serviços principais (Backend API, Frontend, Banco de Dados, Serviço Transcritor PDF) para garantir um ambiente de desenvolvimento consistente, portátil e facilmente replicável. Gerencia a rede interna, volumes de dados e variáveis de ambiente.
6.  **Google Jules (Agente de Desenvolvimento Primário):** Opera em um ambiente VM seguro e isolado, recebendo tarefas do Maestro IA, planejando e executando a implementação, e enviando o código para uma branch `jules` para validação do Desenvolvedor Humano.
7.  **IA Coder (Agente de Desenvolvimento Secundário Local):** Opera diretamente na máquina local do Desenvolvedor Humano, utilizado para tarefas que exigem acesso ao ambiente local específico, debug ou prototipagem rápida sob orientação do Dev.

## Diagrama de Arquitetura (Containers C4)

O diagrama abaixo ilustra os principais containers (componentes de alto nível) do sistema e suas interações primárias:

C4Container
  title Diagrama de Containers - dashboard-adv

  Person(user, "Usuário Final", "Admin, Usuário comum, etc.") # Representa o usuário final interagindo com o sistema

  System_Boundary(platform, "dashboard-adv") {
    Container(frontend, "Frontend SPA", "React, TypeScript, Vite", "Interface com o Usuário Final (Shell + UIs dos Módulos)")
    Container(backend, "Backend API", "FastAPI, Python", "Core Modules (Auth, Health), Módulos Plugáveis, Lógica, Orquestração IA")
    ContainerDb(db, "Banco de Dados", "PostgreSQL, pgvector", "Armazena dados da plataforma e módulos")
    Container(transcritor_pdf_service, "Serviço Transcritor PDF", "FastAPI, Python, Celery, Langchain", "Processamento de PDFs, extração de texto via LLM, vetorização")
  }

  System_Ext(google_ai, "Google AI API", "Serviço Externo (Gemini/Gemma)")

  Rel(user, frontend, "Usa (Navegador)", "HTTPS")
  Rel(frontend, backend, "Faz chamadas API", "HTTPS/JSON")
  Rel(backend, db, "Lê/Escreve", "JDBC/TCP (via SQLAlchemy)")
  Rel(backend, google_ai, "Chama API", "HTTPS")
  Rel(backend, transcritor_pdf_service, "Delega Processamento PDF", "HTTP/JSON")

  UpdateLayoutConfig({
    "layout": {
      "default": {
        "nodeMargin": 15,
        "rankMargin": 60
      }
    }
  })

## Mecanismo de Modularidade

A capacidade de "plugar" módulos independentes é central para a visão do projeto. A abordagem inicial planejada busca um equilíbrio entre flexibilidade e simplicidade:

### Backend (FastAPI)

* **Carregamento Dinâmico de Roteadores via Configuração:** Em vez de registrar rotas de módulos estaticamente no código (`app.include_router(...)` hardcoded), a aplicação Core lerá um arquivo de configuração central na inicialização (ex: `backend/app/modules.yaml`). *Nota: Módulos Core (em `core_modules`) podem ser carregados estaticamente ou via config, a definir.*
* **`modules.yaml` (Exemplo Conceitual):**
  ```yaml
  # backend/app/modules.yaml
  # Lista de módulos plugáveis backend ativos e suas configurações de roteamento.
  # Exemplo:
  active_pluggable_modules:
    - name: gerador_quesitos
      router_path: app.modules.gerador_quesitos.v1.endpoints.router # Módulo plugável
      prefix: /api/gerador_quesitos/v1
      tags: ["Módulo Exemplo", "IA", "Jurídico"]
    # Adicione novos módulos plugáveis aqui.
  ```

* **Processo de Inicialização:** Na inicialização da aplicação, o arquivo `main.py` invoca a função `load_and_register_modules` (localizada em `app.core.module_loader.py`). Esta função é responsável por:
    * Ler o arquivo de configuração `modules.yaml`.
    * Descobrir os roteadores (`APIRouter`) dos módulos habilitados, importando dinamicamente o `router_path` especificado.
    * Registrar cada roteador descoberto na instância principal do `api_router` (definida em `app.api_router.py`) usando os prefixos e tags configurados.
  A instância `api_router`, agora populada com todas as rotas (core e dinâmicas), é então incluída na aplicação FastAPI principal em `main.py`.
* **Vantagens:** Flexibilidade para ativar/desativar módulos plugáveis via configuração.
* **Dependências Core:** Módulos plugáveis podem acessar serviços Core através da injeção de dependências padrão do FastAPI.

### Frontend (React)

* **Code Splitting Baseado em Rota:** Utilizaremos o padrão `React.lazy()` e `import()` dinâmico do JavaScript para carregar o código de um módulo apenas quando o usuário final navegar para uma rota pertencente àquele módulo.
* **Registro de Módulos:** Um arquivo central (ex: `frontend/src/config/moduleRegistry.ts`) definirá o mapeamento entre uma chave de identificação de módulo (string) e o carregamento dinâmico do seu componente principal.
  ```typescript
  // Exemplo: frontend/src/config/moduleRegistry.ts
  import { lazy } from 'react';
  const moduleRegistry: Record<string, React.LazyExoticComponent<any>> = {
    'GERADOR_QUESITOS': lazy(() => import('../modules/gerador-quesitos/GeradorQuesitosPage')),
    'AUTH_USER_ADMIN': lazy(() => import('../modules/auth-user/AdminUsersPage')),
    // Novos módulos adicionam sua entrada aqui
  };
  export default moduleRegistry;
  ```
* **Roteamento:** O roteador principal (`react-router-dom`) usará esse registro para definir as rotas, envolvendo os componentes importados com `React.Suspense`.
* **Vantagens:** Otimiza o carregamento inicial. Abordagem padrão React/Vite. Permite compartilhamento fácil de estado/componentes Core.

## Estratégia de Configuração Geral

A gestão de configurações segue uma abordagem em camadas:

1.  **Arquivos `.env` (Não Versionados):**
    * **Uso:** Segredos, URLs externas, configs que variam por **ambiente**.
    * **Localização:** `backend/.env`, `frontend/.env` (com `VITE_`).
    * **NUNCA** commitados.
2.  **Arquivos de Configuração Versionados (YAML/JSON no Backend, TS/JSON no Frontend):**
    * **Uso:** Configs **estruturais** não secretas (módulos ativos, navegação).
    * **Exemplos:** `backend/app/modules.yaml`, `frontend/src/config/navigation.ts`, `frontend/src/config/moduleRegistry.ts`.
    * **DEVEM** ser commitados.
3.  **Banco de Dados:**
    * **Uso:** Configs alteráveis **dinamicamente em runtime** ou **específicas por entidade** (Admin ou usuário final).
    * **Exemplos:** Configs Globais/Admin (modelo IA padrão) na tabela `configuracoes_aplicacao`; Preferências do usuário final (tema) na tabela `user_preferences`.
    * **Versionamento:** Schema via Alembic; dados não ficam no Git.

*(Esta estratégia busca equilibrar flexibilidade, segurança e manutenibilidade).*

## Fluxo de Dados Típico (Alto Nível)

1.  O usuário final interage com o **Frontend**.
2.  Frontend envia requisição HTTP (com JWT) para o **Backend**.
3.  Backend processa: valida, autentica/autoriza, executa lógica (Core ou Módulo).
4.  Se necessário, Backend interage com o **Banco de Dados**.
5.  Se necessário, Backend delega tarefas de processamento de PDF para o **Serviço Transcritor PDF**.
6.  Se necessário, Backend interage com **Serviços Externos** (Google AI).
7.  Backend retorna JSON para o Frontend.
8.  Frontend atualiza estado e re-renderiza UI.

## Pilha Tecnológica (Resumo)

* **Frontend:** React, TypeScript, Vite, Material UI (MUI), Zustand, react-router-dom
* **Backend:** Python, FastAPI, SQLAlchemy (Asyncio), Alembic, Langchain, Pydantic, Uvicorn
* **Banco de Dados:** PostgreSQL, pgvector
* **Infraestrutura:** Docker, Docker Compose, Git, GitHub

*(Consulte o README.md para links e versões específicas)*

## Decisões Arquiteturais Chave

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