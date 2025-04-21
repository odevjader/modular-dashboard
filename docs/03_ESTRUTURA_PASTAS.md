# Estrutura de Pastas - Modular Dashboard

Este documento descreve a organização das pastas e arquivos principais do projeto Modular Dashboard, ajudando a navegar pela base de código.

## Estrutura Raiz

A pasta raiz do projeto (`modular-dashboard/`) contém os seguintes diretórios e arquivos principais:

* **`backend/`**: Contém todo o código-fonte da API Backend (FastAPI).
* **`frontend/`**: Contém todo o código-fonte da aplicação Frontend (React SPA).
* **`docs/`**: Contém a documentação do projeto (como este arquivo).
* **`docker-compose.yml`**: Arquivo de configuração do Docker Compose para orquestrar os serviços `api` (backend) e `db` (banco de dados) no ambiente de desenvolvimento.
* **`.gitignore`**: Especifica arquivos e pastas a serem ignorados pelo Git.
* **`README.md`**: Ponto de entrada da documentação, com visão geral do projeto.
* *(Outros arquivos de configuração podem existir na raiz, como `.editorconfig`, `.prettierrc`, etc.)*

## Estrutura do Backend (`backend/`)

A pasta `backend/` contém a aplicação FastAPI e seus arquivos relacionados:

* **`app/`**: O diretório principal do código da aplicação FastAPI.
    * **`main.py`**: Ponto de entrada da aplicação FastAPI, onde a instância `FastAPI()` é criada e os roteadores são incluídos.
    * **`api_router.py`**: Agrega os roteadores dos diferentes módulos da API (`modules/`).
    * **`core/`**: Contém a lógica central e configurações compartilhadas da aplicação backend.
        * `config.py`: Carregamento de configurações (variáveis de ambiente via Pydantic Settings).
        * `database.py`: Configuração da sessão assíncrona do banco de dados SQLAlchemy.
        * `security.py`: Utilitários relacionados à segurança (hashing de senha com Passlib, operações JWT com python-jose).
        * `dependencies.py`: Dependências reutilizáveis do FastAPI injetáveis nas rotas (ex: `get_current_active_user`).
    * **`models/`**: Contém as definições dos modelos SQLAlchemy (ex: `user.py`, `enums.py`) que mapeiam para as tabelas do banco de dados.
    * **`modules/`**: Contém os diferentes módulos funcionais da API (ex: `auth`, `gerador_quesitos`). Cada submódulo geralmente segue uma estrutura como:
        * `{nome_modulo}/`
            * `v1/` (ou outra versão da API para o módulo)
                * `endpoints.py`: Define os endpoints da API (`@router.get`, `@router.post`, etc.) para este módulo.
                * `schemas.py`: Define os schemas Pydantic usados para validação de dados de entrada (corpo da requisição) e serialização de dados de saída (resposta).
                * `(opcional) services.py`: Camada de serviço para encapsular a lógica de negócio mais complexa ou interações entre diferentes partes (ex: chamar Langchain, interagir com `crud.py`).
                * `(opcional) crud.py`: Funções que realizam operações básicas de Create, Read, Update, Delete no banco de dados para os modelos relacionados a este módulo, usando a sessão SQLAlchemy.
    * **`versions/`**: Contém os scripts de migração de banco de dados gerados pelo Alembic. Cada arquivo aqui representa uma mudança versionada no schema.
    * **`alembic.ini`**: Arquivo de configuração principal do Alembic.
* **`Dockerfile`**: Define as instruções para construir a imagem Docker para a aplicação backend (serviço `api`). Pode usar multi-stage build para otimização.
* **`.env`**: Arquivo (não versionado pelo Git) contendo as variáveis de ambiente (chaves de API, URL do banco, `SECRET_KEY`, etc.). **Localização:** Esperado diretamente dentro da pasta `backend/`.
* **`requirements.txt` ou `pyproject.toml`**: Arquivos que definem as dependências Python do projeto backend.

## Estrutura do Frontend (`frontend/`)

A pasta `frontend/` contém a aplicação React e seus arquivos relacionados, gerenciados via Vite:

* **`public/`**: Contém arquivos estáticos que são copiados para a raiz do build final sem processamento pelo Vite (ex: `favicon.ico`, `robots.txt`).
* **`src/`**: O diretório principal do código-fonte da aplicação React.
    * **`main.tsx`**: Ponto de entrada da aplicação React, onde o componente `App` é instanciado e renderizado no elemento raiz do `index.html`. Configurações globais (como Providers de contexto ou tema MUI) podem ser aplicadas aqui.
    * **`App.tsx`**: Componente React raiz da aplicação. Geralmente configura o roteador principal (`react-router-dom`) e o layout base da aplicação (ex: Topbar, Sidebar, área de conteúdo).
    * **`assets/`**: Imagens (logos, ícones), fontes e outros recursos estáticos que são importados e processados pelo build (Vite).
    * **`components/`**: Componentes React reutilizáveis e genéricos, que não representam páginas inteiras (ex: botões customizados, modais, cards, inputs de formulário). Podem ser organizados em subpastas.
    * **`config/`**: Arquivos de configuração específicos do frontend (ex: instâncias de bibliotecas, temas MUI, definições de rotas de navegação como em `navigation.ts`).
    * **`hooks/`**: Custom Hooks do React, para encapsular lógica de estado e efeitos colaterais reutilizáveis entre componentes.
    * **`pages/`** ou **`views/`**: Componentes React que representam páginas completas ou visões principais da aplicação (ex: `LoginPage.tsx`, `DashboardPage.tsx`, `AdminUsersPage.tsx`). Geralmente utilizam componentes de `components/` e `hooks/`, e interagem com `services/`.
    * **`services/`**: Módulos responsáveis pela comunicação com a API backend. Contém funções que encapsulam as chamadas `Workspace` (ou Axios, se usado) para os diferentes endpoints da API (ex: `api.ts`, `authService.ts`).
    * **`store/`** ou **`state/`**: Lógica relacionada ao gerenciamento de estado global da aplicação (usando Zustand neste caso). Arquivos como `authStore.ts` definiriam o estado e as ações relacionadas à autenticação.
    * **`styles/`**: Arquivos de estilização global (CSS, SCSS) ou configurações/extensões de tema (ex: tema MUI customizado).
    * **`types/`**: Definições de tipos e interfaces TypeScript compartilhadas através da aplicação frontend.
    * **`utils/`**: Funções utilitárias genéricas que não se encaixam em outras categorias (ex: formatação de datas, validações simples).
* **`index.html`**: O arquivo HTML raiz da SPA, servido pelo Vite em desenvolvimento e como base para o build de produção. Contém o elemento (geralmente `<div id="root">`) onde a aplicação React será montada.
* **`package.json`**: Arquivo padrão do Node.js que lista as dependências do projeto (React, MUI, Vite, etc.) e define scripts úteis (`dev`, `build`, `lint`, `test`).
* **`tsconfig.json`**: Arquivo de configuração do compilador TypeScript para o projeto frontend.
* **`vite.config.ts`**: Arquivo de configuração do Vite, onde plugins e opções de build/desenvolvimento são definidos.

## Estrutura da Documentação (`docs/`)

Esta pasta (`docs/`) é destinada a conter toda a documentação do projeto (incluindo este arquivo) em formato Markdown. A organização interna pode seguir a numeração dos arquivos (00, 01, 02...) ou ser dividida em subpastas temáticas conforme a documentação crescer.