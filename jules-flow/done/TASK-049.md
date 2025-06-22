---
id: TASK-049
title: "DEV (Fase 2): Criar Estrutura Base do `pdf_processor_service`"
epic: "Fase 2: Infraestrutura de Microserviços"
status: done
priority: medium
dependencies: []
assignee: Jules
---

### Descrição

Configurar a estrutura básica de diretórios e arquivos para o novo microserviço `pdf_processor_service`. Este serviço será responsável por receber PDFs, extrair texto e possivelmente outras informações, e armazená-las.

### Critérios de Aceitação

- [x] Novo diretório criado para o serviço (e.g., `pdf_processor_service/`).
- [x] `Dockerfile` básico para o serviço criado.
- [x] `requirements.txt` (ou `pyproject.toml`) inicializado com dependências básicas (e.g., FastAPI, Uvicorn, bibliotecas de extração de PDF).
- [x] Estrutura de pastas interna básica (e.g., `app/`, `app/main.py`, `app/routers/`, `app/services/`).
- [x] Configuração básica de um servidor FastAPI dentro do serviço.

### Arquivos Relevantes

* `pdf_processor_service/Dockerfile`
* `pdf_processor_service/requirements.txt`
* `pdf_processor_service/app/main.py`

### Relatório de Execução
### Relatório de Execução

1.  **Diretório Principal do Serviço**:
    *   Criado o diretório `backend/pdf_processor_service/` para abrigar o novo microserviço.
2.  **Estrutura Interna `app/`**:
    *   Criado o subdiretório `backend/pdf_processor_service/app/`.
    *   Adicionado `backend/pdf_processor_service/app/__init__.py`.
    *   Criado `backend/pdf_processor_service/app/main.py` com uma aplicação FastAPI mínima, incluindo um endpoint de health check (`/health`).
3.  **Arquivos de Configuração e Suporte**:
    *   `backend/pdf_processor_service/requirements.txt`: Criado com `fastapi` and `uvicorn[standard]` como dependências iniciais.
    *   `backend/pdf_processor_service/Dockerfile`: Criado com uma configuração básica usando `python:3.9-slim`, que copia os arquivos da aplicação, instala as dependências e executa o Uvicorn.
    *   `backend/pdf_processor_service/.env.example`: Criado com um placeholder para variáveis de ambiente futuras.
4.  **Subdiretórios Adicionais para Desenvolvimento Futuro**:
    *   As seguintes pastas foram criadas dentro de `backend/pdf_processor_service/app/` (com um arquivo `.gitkeep` em cada para garantir que sejam rastreadas pelo Git, se vazias):
        *   `core/`
        *   `routers/`
        *   `services/`
        *   `models/`
        *   `schemas/`
    *   Uma pasta `backend/pdf_processor_service/tests/` também foi criada com um `.gitkeep`.

Todos os critérios de aceitação para a estrutura base do serviço foram atendidos.
