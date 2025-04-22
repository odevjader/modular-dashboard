# Arquitetura do Modular Dashboard

Este documento descreve a arquitetura de alto nível do projeto Modular Dashboard, seus principais componentes, o fluxo de dados, as decisões de design fundamentais, o mecanismo de modularidade e a estratégia de configuração.

*(Última atualização: 22 de Abril de 2025, aprox. 08:20 -03)*

## Visão Geral

O Modular Dashboard adota uma arquitetura de **Monorepo** contendo:
* Uma aplicação **Frontend SPA (Single Page Application)** responsável pela interface do usuário (React/TypeScript/Vite).
* Um **Backend API RESTful Assíncrono** que expõe os endpoints e contém a lógica de negócio (FastAPI/Python/SQLAlchemy).
* Um **Banco de Dados Relacional** para persistência (PostgreSQL/pgvector).
O ambiente é orquestrado via **Docker e Docker Compose**, e a arquitetura é projetada para ser uma **plataforma base versátil e extensível**.

## Componentes Principais

1.  **Frontend (React SPA):** Responsável pela interface do usuário (UI), interação com o usuário, gerenciamento de estado da UI (local e global com Zustand), e chamadas para a API Backend. Atua como o "shell" ou "casca" onde as UIs dos diferentes módulos são carregadas e apresentadas de forma integrada.
2.  **Backend (FastAPI API):** Expõe endpoints RESTful para o frontend e potencialmente para outros serviços. Lida com a lógica de negócios do Core da plataforma (Autenticação, Gerenciamento de Usuários, Configurações Globais) e também expõe as funcionalidades específicas de cada módulo carregado. Realiza validação de dados, interage com o banco de dados de forma assíncrona, integra com serviços de IA (via Langchain) e gerencia a segurança.
3.  **Banco de Dados (PostgreSQL + pgvector):** Armazena os dados persistentes da aplicação. Isso inclui dados do Core (tabelas `users`, `configuracoes_aplicacao`, `user_preferences`) e potencialmente tabelas específicas criadas e gerenciadas por módulos individuais (requer definição de estratégia de migração e nomes). A extensão `pgvector` habilita capacidades de busca semântica.
4.  **Docker / Docker Compose:** Containeriza os serviços principais (Backend API, Banco de Dados e, futuramente, o serviço de processamento de PDF/OCR) para garantir um ambiente de desenvolvimento consistente, portátil e facilmente replicável. Gerencia a rede interna, volumes de dados e variáveis de ambiente. (Nota: Considera-se mover o processamento pesado de PDF/OCR para um container dedicado no futuro - ver `ROADMAP.md`).
5.  **Roo (Ferramenta Externa):** Utilizada exclusivamente durante o fluxo de desenvolvimento AI-assistido para permitir que as IAs (Maestro ou Coder, via Usuário Humano) apliquem mudanças (criação, sobrescrita, adição de linhas) aos arquivos no sistema de arquivos local do desenvolvedor.

## Mecanismo de Modularidade (Abordagem Inicial Planejada)

A capacidade de "plugar" módulos independentes é central para a visão do projeto. A abordagem inicial planejada busca um equilíbrio entre flexibilidade e simplicidade:

### Backend (FastAPI)

* **Carregamento Dinâmico de Roteadores via Configuração:** Em vez de registrar rotas de módulos estaticamente no código (`app.include_router(...)` hardcoded), a aplicação Core lerá um arquivo de configuração central na inicialização (ex: `backend/app/modules.yaml`).
* **`modules.yaml` (Exemplo):**
    ```yaml
    # backend/app/modules.yaml
    # Lista de módulos backend ativos e suas configurações de roteamento
    active_modules:
      - name: auth_user # Identificador do módulo
        # Caminho Python para importar o objeto APIRouter do módulo
        router_path: app.modules.auth.v1.endpoints.router
        prefix: /api/auth/v1 # Prefixo da URL para as rotas deste módulo
        tags: ["Core", "Autenticação", "Usuários"] # Tags para agrupar no Swagger/ReDoc
      - name: gerador_quesitos
        router_path: app.modules.gerador_quesitos.v1.endpoints.router
        prefix: /api/gerador_quesitos/v1
        tags: ["Módulo Exemplo", "IA", "Jurídico"]
      # Novos módulos são adicionados/removidos aqui
    ```
* **Processo de Inicialização:** O Core FastAPI itera sobre `active_modules`, importa dinamicamente o `router_path` especificado e chama `app.include_router()` com os metadados (`prefix`, `tags`) fornecidos.
* **Vantagens:** Flexibilidade para ativar/desativar módulos e configurar seus pontos de montagem via configuração, sem alterar o código do Core. Mantém a simplicidade da estrutura de `APIRouter` por módulo.
* **Dependências Core:** Módulos podem acessar serviços Core (sessão DB, usuário atual) através do sistema de injeção de dependências padrão do FastAPI. Dependências Python específicas de módulos precisam ser gerenciadas no ambiente compartilhado (ex: `requirements.txt` ou `pyproject.toml` principal).

### Frontend (React)

* **Code Splitting Baseado em Rota:** Utilizaremos o padrão `React.lazy()` e `import()` dinâmico do JavaScript para carregar o código de um módulo apenas quando o usuário navegar para uma rota pertencente àquele módulo.
* **Registro de Módulos:** Um arquivo central (ex: `frontend/src/config/moduleRegistry.ts`) definirá o mapeamento entre uma chave de identificação de módulo (string) e o carregamento dinâmico do seu componente principal (página ou layout do módulo).
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
* **Roteamento:** O roteador principal (`react-router-dom`, configurado em `App.tsx` ou similar) usará esse registro para definir as rotas. Ao navegar para uma rota de módulo, apenas o código (JavaScript/CSS) daquele módulo será baixado pelo navegador.
* `React.Suspense` será usado para mostrar um indicador de carregamento enquanto o módulo é baixado.
* **Vantagens:** Otimiza o carregamento inicial (bundle menor). Abordagem padrão e bem suportada no ecossistema React/Vite. Permite que módulos compartilhem estado global (Zustand) e componentes/temas (MUI) definidos no Core facilmente.

## Estratégia de Configuração Geral

A gestão de configurações segue uma abordagem em camadas para equilibrar segurança, flexibilidade e versionamento:

1.  **Arquivos `.env` (Não Versionados):**
    * **Uso:** Exclusivamente para segredos (chaves de API, `SECRET_KEY` JWT), URLs de serviços externos (DB) e configurações que **variam por ambiente** (desenvolvimento, teste, produção).
    * **Localização:** `backend/.env` (lido por Pydantic Settings), `frontend/.env` (variáveis devem começar com `VITE_`, lidas no build e expostas publicamente no JS final).
    * **Versionamento:** **NUNCA** commitados no Git (devem estar no `.gitignore`). Cada ambiente/desenvolvedor tem o seu.

2.  **Arquivos de Configuração Versionados (YAML/JSON no Backend, TS/JSON no Frontend):**
    * **Uso:** Para configurações **estruturais** da aplicação que *não são secretas* e que definem como a aplicação se monta ou se comporta por padrão. Devem ser versionadas com o código.
    * **Exemplos:** `backend/app/modules.yaml` (lista de módulos backend ativos), `frontend/src/config/navigation.ts` (estrutura de menu), `frontend/src/config/moduleRegistry.ts` (registro de módulos UI).
    * **Leitura:** Backend lê na inicialização (YAML/JSON). Frontend importa durante o build (TS/JSON).
    * **Versionamento:** **DEVEM** ser commitados no Git.

3.  **Banco de Dados:**
    * **Uso:** Para configurações que precisam ser **alteradas dinamicamente em runtime sem novo deploy** por usuários autorizados (Admins) ou que são **preferências específicas por entidade** (usuário, tenant futuro, etc.).
    * **Exemplos:**
        * *Configurações Globais/Admin:* Modelo de IA padrão, limites de uso, feature flags dinâmicas (`configuracoes_aplicacao` table).
        * *Preferências do Usuário:* Tema de cores, séries favoritas, configurações de notificação por usuário (`user_preferences` table ou colunas em `users`).
    * **Leitura:** Backend lê dinamicamente (com cache se necessário). Frontend obtém via chamadas API.
    * **Versionamento:** O *schema* das tabelas (`users`, `configuracoes_aplicacao`, etc.) é versionado via Alembic, mas os *dados* (os valores das configurações/preferências) não ficam no Git.

*(Esta estratégia busca equilibrar flexibilidade, segurança e manutenibilidade).*

## Fluxo de Dados Típico (Alto Nível)

O fluxo geral de uma requisição de usuário normalmente segue este padrão:

1.  Usuário interage com o **Frontend** (React SPA) no navegador.
2.  O Frontend envia uma requisição HTTP (usando `Workspace`) para o **Backend** (API FastAPI), possivelmente incluindo um token JWT no cabeçalho para rotas protegidas.
3.  O Backend processa a requisição: valida dados de entrada (Pydantic), verifica autenticação/autorização (FastAPI Dependencies com JWT/Security Utils), executa a lógica de negócio específica do endpoint (seja do Core ou de um módulo carregado).
4.  Se necessário, o Backend interage com o **Banco de Dados** (PostgreSQL via SQLAlchemy async) para ler ou escrever dados.
5.  Se a requisição envolve IA (ex: em um módulo como `gerador_quesitos`), o Backend interage com serviços externos (Google Gemini API via Langchain) ou bibliotecas de processamento (futuro container de PDF/OCR).
6.  O Backend formula e retorna uma resposta JSON para o Frontend.
7.  O Frontend recebe a resposta, atualiza seu estado (se necessário, via Zustand ou estado local) e re-renderiza a interface do usuário para refletir o resultado.

**Diagrama Simplificado:**

```text
 [Frontend: React SPA] <--(HTTP/REST + JWT)--> [Backend: FastAPI Core + Módulos] <--(SQLAlchemy/asyncpg)--> [PostgreSQL + pgvector]
         ^                                                    |
         |                                                    | (LangChain / Outras Libs)
         +--------------------------------------------------- V
                                                       [APIs Externas (Ex: Google AI)]
                                                       [Futuro: Serviço PDF/OCR Dedicado]