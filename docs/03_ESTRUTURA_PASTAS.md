# Estrutura de Pastas - Modular Dashboard

Este documento descreve a organização das pastas e arquivos principais do projeto Modular Dashboard, ajudando a navegar pela base de código.

## Estrutura Raiz

A raiz do projeto Modular Dashboard contém os seguintes arquivos e diretórios principais:

*   **`.gitignore`**: Especifica arquivos e pastas intencionalmente não rastreados pelo Git.
*   **`.prompts/`**: Contém prompts e configurações para interações com modelos de linguagem grande (LLMs).
*   **`.roo/`**: (Propósito a ser determinado, possivelmente relacionado a ferramentas específicas de IA).
*   **`README.md`**: Documento principal com a visão geral do projeto, instruções de setup e informações essenciais.
*   **`ROADMAP.md`**: Descreve as fases de desenvolvimento e futuras funcionalidades planejadas.
*   **`backend/`**: Contém o código da aplicação backend (API FastAPI). (Detalhado abaixo)
*   **`docker-compose.yml`**: Define os serviços, redes e volumes para o ambiente Docker.
*   **`docs/`**: Contém a documentação do projeto. (Detalhado abaixo)
*   **`frontend/`**: Contém o código da aplicação frontend (React SPA). (Detalhado abaixo)
*   **`package-lock.json`**: Gerado pelo npm, registra as versões exatas das dependências do projeto.
*   **`pdf-exemplos/`**: Contém arquivos PDF utilizados para exemplos ou testes.

## Estrutura do Backend (`backend/`)

A pasta `backend/` contém a aplicação FastAPI e seus arquivos relacionados:

*   **`app/`**: O diretório principal do código da aplicação FastAPI.
    *   **`main.py`**: Ponto de entrada da aplicação FastAPI, onde a instância da aplicação é criada e configurada.
    *   **`api_router.py`**: Agrega os roteadores principais da aplicação, incluindo os de `core_modules` e os carregados dinamicamente de `modules`.
    *   **`core/`**: Contém a lógica central e configurações compartilhadas pela aplicação.
        *   `config.py`: Gerenciamento de configurações da aplicação (ex: variáveis de ambiente).
        *   `database.py`: Configuração da conexão com o banco de dados e sessões SQLAlchemy.
        *   `security.py`: Funções relacionadas à segurança (ex: hashing de senhas, criação de JWT).
        *   `dependencies.py`: Dependências comuns do FastAPI (ex: obter usuário atual).
        *   `module_loader.py`: Lógica para carregar dinamicamente os módulos plugáveis.
    *   **`core_modules/`**: Contém módulos **essenciais** para o funcionamento base da plataforma. São funcionalidades centrais que não são opcionais.
        *   `auth/`: Módulo de autenticação e gerenciamento de usuários.
            *   `v1/`: Contém endpoints, schemas Pydantic e lógica de serviço para a versão 1 da API de autenticação.
        *   `health/`: Módulo de verificação de saúde da aplicação.
            *   `v1/`: Endpoints para checagem de status.
    *   **`models/`**: Contém os modelos de dados SQLAlchemy que definem a estrutura das tabelas do banco de dados.
        *   `user.py`: Modelo de usuário.
        *   `enums.py`: Definições de tipos enumerados usados nos modelos.
    *   **`modules/`**: Contém módulos **funcionais plugáveis e opcionais**. Cada subdiretório representa um módulo que pode ser ativado ou desativado.
        *   `ai_test/`: Módulo para testes de funcionalidades de IA.
        *   `gerador_quesitos/`: Módulo exemplo para geração de quesitos jurídicos.
        *   `info/`: Módulo para informações do sistema/debug.
        *   *(Novos módulos funcionais são adicionados aqui, seguindo uma estrutura interna similar com `endpoints.py`, `schemas.py`, etc.)*
    *   **`schemas/`**: Contém schemas Pydantic utilizados para validação de dados de entrada/saída da API fora dos módulos específicos (ex: `token.py`, `module_config.py`).
    *   **`utils/`**: Funções utilitárias genéricas (ex: `pdf_processor.py`).
    *   **`create_admin_user.py`**, **`create_test_user.py`**: Scripts para criação de usuários específicos.
    *   **`test_db_connect.py`**: Script para testar a conexão com o banco de dados.
*   **`alembic/`**: Contém a configuração e as versões de migração do Alembic para o banco de dados.
    *   `versions/`: Contém os scripts de migração individuais gerados pelo Alembic.
*   **`alembic.ini`**: Arquivo de configuração principal do Alembic.
*   **`Dockerfile`**: Instruções para construir a imagem Docker do serviço backend.
*   **`.env.example`**: Arquivo de exemplo para as variáveis de ambiente necessárias (copiado para `.env` e preenchido localmente).
*   **`requirements.txt`**: Lista de dependências Python do projeto backend.
*   **`tests/`**: Contém os testes automatizados para o backend.

## Estrutura do Frontend (`frontend/`)

A pasta `frontend/` abriga a aplicação Single Page Application (SPA) construída com React e Vite:

*   **`public/`**: Contém arquivos estáticos que são servidos diretamente (ex: `vite.svg`).
*   **`src/`**: Diretório principal do código fonte da aplicação frontend.
    *   **`main.tsx`**: Ponto de entrada da aplicação React, onde o componente raiz `App` é renderizado.
    *   **`App.tsx`**: Componente raiz que configura o roteamento principal e layouts.
    *   **`assets/`**: Imagens, fontes e outros ativos estáticos importados pelos componentes.
    *   **`components/`**: Componentes React reutilizáveis e genéricos usados em várias partes da aplicação (ex: `ProtectedRoute.tsx`).
    *   **`config/`**: Arquivos de configuração específicos do frontend.
        *   `moduleRegistry.ts`: Define como os módulos frontend são registrados, carregados e roteados.
        *   `opcoesFormulario.ts`, `phrases.ts`: Outras configurações ou constantes da UI.
    *   **`layouts/`**: Componentes responsáveis pela estrutura visual principal das páginas (ex: `MainLayout.tsx` que pode incluir header, sidebar, footer).
    *   **`modules/`**: Contém os componentes e lógica específicos de cada módulo funcional plugável, espelhando a estrutura modular do backend.
        *   `ai_test/`, `gerador_quesitos/`, `info/`, `test_module/`: Subdiretórios para cada módulo frontend.
    *   **`pages/`**: Componentes React que representam páginas completas da aplicação, geralmente combinando layouts e componentes específicos.
    *   **`services/`**: Funções e lógica para interagir com a API backend (ex: `api.ts` que pode conter instâncias do cliente HTTP e funções de chamada).
    *   **`stores/`**: Lógica de gerenciamento de estado global ou de features complexas (ex: usando Zustand, como `authStore.ts`).
    *   **`styles/`**: Arquivos de estilização globais ou temas (ex: `theme.ts` para Material UI).
    *   **`utils/`**: Funções utilitárias específicas do frontend.
    *   `index.css`, `App.css`: Arquivos CSS globais ou para o componente App.
    *   `vite-env.d.ts`: Definições de tipo para variáveis de ambiente do Vite.
*   **`Dockerfile`**: Instruções para construir a imagem Docker do serviço frontend (geralmente para servir os arquivos estáticos com Nginx).
*   **`.env.example`**: Arquivo de exemplo para variáveis de ambiente do frontend (usadas pelo Vite, prefixadas com `VITE_`).
*   **`index.html`**: Ponto de entrada HTML para a SPA.
*   **`nginx.default.conf`**: Configuração do Nginx para servir a aplicação em produção dentro do Docker.
*   **`package.json`**: Define metadados do projeto frontend, scripts (ex: `dev`, `build`, `lint`) e dependências.
*   **`package-lock.json`**: Gerado pelo npm, registra as versões exatas das dependências do frontend.
*   **`vite.config.ts`**: Arquivo de configuração do Vite (bundler e servidor de desenvolvimento).
*   **`tsconfig.json`, `tsconfig.app.json`, `tsconfig.node.json`**: Arquivos de configuração do TypeScript.
*   **`eslint.config.js`**: Arquivo de configuração do ESLint para linting do código.
*   **`README.md`**: Documentação específica do frontend, se houver.

## Estrutura da Documentação (`docs/`)

A pasta `docs/` armazena toda a documentação do projeto:

*   **`00_VISAO_GERAL.md`**: Visão geral do projeto, objetivos, público-alvo.
*   **`01_ARQUITETURA.md`**: Detalhes da arquitetura da solução.
*   **`02_CONFIGURACAO_AMBIENTE.md`**: Guia para configurar o ambiente de desenvolvimento.
*   **`03_ESTRUTURA_PASTAS.md`**: Este arquivo, descrevendo a organização do projeto.
*   **`04_BANCO_DE_DADOS.md`**: Informações sobre o banco de dados e schema.
*   **`05_MODULARIDADE.md`**: Explicação do mecanismo de modularidade.
*   **`06_GESTAO_PROJETOS.md`**: Como as tarefas são gerenciadas (Issues, Board).
*   **`07_FLUXO_DESENVOLVIMENTO_E_ONBOARDING.md`**: Fluxo de trabalho de desenvolvimento híbrido IA e guia de onboarding.
*   **`backup/`**: Contém backups de versões anteriores de documentos.
*   **`jules/`**: Pode conter logs ou relatórios gerados por agentes de IA (ex: Jules).
*   **`modules/`**: Documentação específica para cada módulo funcional.
    *   `00_DEVELOPING_MODULES.md`: Guia geral para desenvolvimento de novos módulos.
    *   `01_GERADOR_QUESITOS.md`, `02_AUTH_USER.md`, `03_AI_TEST.md`: Documentação para módulos específicos.

Esta estrutura visa manter o projeto organizado, facilitando a navegação e o desenvolvimento.