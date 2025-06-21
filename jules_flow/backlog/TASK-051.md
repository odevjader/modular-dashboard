---
id: TASK-051
title: "DEV (Fase 2): Implementar Endpoint `POST /process-pdf` no `pdf_processor_service`"
epic: "Fase 2: Infraestrutura de Microserviços"
status: done
priority: medium
dependencies: []
assignee: Jules
---

### Descrição

Criar um endpoint HTTP `POST /process-pdf` no `pdf_processor_service` que aceite um arquivo PDF (ou um identificador para ele), orquestre a extração de texto (usando a lógica da TASK-050) e o armazenamento dos chunks.

### Critérios de Aceitação

- [x] Rota `POST /process-pdf` definida no FastAPI do `pdf_processor_service`.
- [x] Endpoint aceita um arquivo PDF via upload (`UploadFile`). (ID/path method not implemented in this task)
- [x] Endpoint chama a lógica de extração de texto e armazenamento de chunks.
- [x] Endpoint retorna uma resposta significativa (e.g., ID do documento processado, número de chunks, status).
- [x] Tratamento básico de erros implementado para falhas no processamento.

### Arquivos Relevantes

* `backend/pdf_processor_service/app/routers/processing_router.py`
* `backend/pdf_processor_service/app/schemas/document_schemas.py`
* `backend/pdf_processor_service/app/main.py`
* `backend/pdf_processor_service/app/services/document_service.py`

### Relatório de Execução
### Relatório de Execução

1.  **Pydantic Schemas (`app/schemas/document_schemas.py`)**:
    *   Definidos schemas para request e response, incluindo `DocumentResponse`, `DocumentCreate`, `DocumentChunkBase`, e `DocumentChunkResponse`.
    *   Configurados com `orm_mode = True` (ou `from_attributes = True` para Pydantic V2) para compatibilidade com modelos SQLAlchemy.
    *   Criado `app/schemas/__init__.py` para exportar os schemas.

2.  **Router de Processamento (`app/routers/processing_router.py`)**:
    *   Criado um novo `APIRouter` com o prefixo `/processing`.
    *   Implementado o endpoint `POST /process-pdf`:
        *   Aceita um arquivo PDF via `UploadFile`.
        *   Valida o `content_type` do arquivo para aceitar apenas `application/pdf`.
        *   Lê o conteúdo do arquivo de forma assíncrona.
        *   Chama a função de serviço `services.create_document_and_chunks` (implementada na TASK-050) para realizar a extração de texto, chunking e armazenamento no banco de dados.
        *   Retorna uma resposta usando o schema `schemas.DocumentResponse`, que inclui detalhes do documento processado.
        *   Implementado tratamento de exceções básicas para erros de tipo de arquivo, arquivo vazio e falhas gerais no processamento, retornando códigos de status HTTP apropriados.
    *   Criado `app/routers/__init__.py`.

3.  **Atualização da Aplicação Principal (`app/main.py`)**:
    *   O `processing_router` foi incluído na instância principal do FastAPI no `pdf_processor_service`, tornando o endpoint `/processing/process-pdf` acessível.

O endpoint implementado cumpre os requisitos de aceitar um PDF, processá-lo usando a lógica da TASK-050 e retornar uma resposta estruturada, incluindo tratamento básico de erros.
