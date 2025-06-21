---
id: TASK-049
title: "DEV (Fase 2): Criar Estrutura Base do `pdf_processor_service`"
epic: "Fase 2: Infraestrutura de Microserviços"
status: backlog
priority: medium
dependencies: []
assignee: Jules
---

### Descrição

Configurar a estrutura básica de diretórios e arquivos para o novo microserviço `pdf_processor_service`. Este serviço será responsável por receber PDFs, extrair texto e possivelmente outras informações, e armazená-las.

### Critérios de Aceitação

- [ ] Novo diretório criado para o serviço (e.g., `pdf_processor_service/`).
- [ ] `Dockerfile` básico para o serviço criado.
- [ ] `requirements.txt` (ou `pyproject.toml`) inicializado com dependências básicas (e.g., FastAPI, Uvicorn, bibliotecas de extração de PDF).
- [ ] Estrutura de pastas interna básica (e.g., `app/`, `app/main.py`, `app/routers/`, `app/services/`).
- [ ] Configuração básica de um servidor FastAPI dentro do serviço.

### Arquivos Relevantes

* `pdf_processor_service/Dockerfile`
* `pdf_processor_service/requirements.txt`
* `pdf_processor_service/app/main.py`

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
