# Arquitetura do Modular Dashboard

Este documento descreve a arquitetura de alto nível do projeto Modular Dashboard, seus principais componentes, o fluxo de dados, as decisões de design fundamentais, o mecanismo de modularidade e a estratégia de configuração.

*(Última atualização: 22 de Abril de 2025, aprox. 08:32 -03)*

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

## Diagrama de Arquitetura (Containers C4)

O diagrama abaixo ilustra os principais containers (componentes de alto nível) do sistema e suas interações primárias:

```mermaid
C4Container
  title Diagrama de Containers - Modular Dashboard

  Person(user, "Usuário Humano", "Admin, User, etc.")

  System_Boundary(platform, "Modular Dashboard") {
    Container(frontend, "Frontend SPA", "React, TypeScript, Vite", "Interface com o usuário (Shell + UIs dos Módulos)")
    Container(backend, "Backend API", "FastAPI, Python", "Core (Auth, User), Endpoints dos Módulos, Lógica, Orquestração IA")
    ContainerDb(db, "Banco de Dados", "PostgreSQL, pgvector", "Armazena dados da plataforma e módulos")
    Container(ocr_service, "Serviço PDF/OCR", "Python/Tesseract (TBD)", "Processamento pesado de PDFs/OCR (Futuro, container separado)")
  }

  System_Ext(google_ai, "Google AI API", "Serviço Externo (Gemini/Gemma)")

  Rel(user, frontend, "Usa (Navegador)", "HTTPS")
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