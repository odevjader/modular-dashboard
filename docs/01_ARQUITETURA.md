# Arquitetura do Modular Dashboard

Este documento descreve a arquitetura de alto nível do projeto Modular Dashboard, seus principais componentes, o fluxo de dados e as decisões de design fundamentais.

## Visão Geral

O Modular Dashboard adota uma arquitetura de **Monorepo** (implícito, com código fonte do frontend e backend no mesmo repositório Git) contendo:

* Uma aplicação **Frontend SPA (Single Page Application)** responsável pela interface do usuário.
* Um **Backend API RESTful Assíncrono** que expõe os endpoints e contém a lógica de negócio.
* Um **Banco de Dados Relacional** para persistência.

O ambiente de desenvolvimento e a orquestração dos serviços (backend e banco de dados) são gerenciados via **Docker e Docker Compose**.

## Componentes Principais

1.  **Frontend:**
    * **Tecnologias:** React, TypeScript, Vite, Material UI (MUI), Zustand, react-router-dom.
    * **Responsabilidades:** Renderizar a interface do usuário, gerenciar o estado da UI, lidar com a interação do usuário, realizar chamadas HTTP para a API Backend (`Workspace`), e gerenciar o fluxo de autenticação no lado do cliente.

2.  **Backend:**
    * **Tecnologias:** Python, FastAPI, SQLAlchemy (com `asyncpg` para modo assíncrono), Pydantic, Alembic, Langchain, Uvicorn (`uvloop`).
    * **Responsabilidades:** Expor endpoints RESTful, processar requisições HTTP, validar dados de entrada (Pydantic), aplicar a lógica de negócio, interagir com o banco de dados de forma assíncrona (SQLAlchemy), gerenciar autenticação (JWT) e autorização (roles), integrar com serviços de IA (Google Gemini via Langchain) e processar arquivos (Docling).

3.  **Banco de Dados:**
    * **Tecnologias:** PostgreSQL (v16+), pgvector.
    * **Responsabilidades:** Persistir os dados da aplicação (usuários, histórico futuro, configurações, etc.). A extensão `pgvector` permite o armazenamento e consulta de embeddings vetoriais, habilitando futuras funcionalidades de busca semântica ou RAG (Retrieval-Augmented Generation).

4.  **Docker / Docker Compose:**
    * **Responsabilidades:** Containerizar os serviços de Backend (`api`) e Banco de Dados (`db`), definir a rede interna para comunicação entre eles, gerenciar volumes para persistência de dados (DB) e live-reloading (código do backend), e carregar variáveis de ambiente, proporcionando um ambiente de desenvolvimento consistente e portátil.

## Fluxo de Dados Típico (Alto Nível)

O fluxo geral de uma requisição de usuário normalmente segue este padrão:

1.  Usuário interage com o **Frontend** (React SPA) no navegador.
2.  O Frontend envia uma requisição HTTP (usando `Workspace`) para o **Backend** (API FastAPI), possivelmente incluindo um token JWT no cabeçalho para rotas protegidas.
3.  O Backend processa a requisição: valida dados de entrada (Pydantic), verifica autenticação/autorização (FastAPI Dependencies com JWT/Security Utils), executa a lógica de negócio específica do endpoint.
4.  Se necessário, o Backend interage com o **Banco de Dados** (PostgreSQL via SQLAlchemy async) para ler ou escrever dados.
5.  Se a requisição envolve IA (ex: `/gerador_quesitos`), o Backend interage com serviços externos (Google Gemini API via Langchain) ou bibliotecas de processamento (Docling).
6.  O Backend formula e retorna uma resposta JSON para o Frontend.
7.  O Frontend recebe a resposta, atualiza seu estado (se necessário, via Zustand ou estado local) e re-renderiza a interface do usuário para refletir o resultado.

**Diagrama Simplificado:**

```text
 [Frontend: React SPA] <--(HTTP/REST + JWT)--> [Backend: FastAPI] <--(SQLAlchemy/asyncpg)--> [PostgreSQL + pgvector]
         ^                                            |
         |                                            | (LangChain/Docling)
         +------------------------------------------- V
                                               [Google Gemini API]