---
id: TASK-051
title: "DEV (Fase 2): Implementar Endpoint `POST /process-pdf` no `pdf_processor_service`"
epic: "Fase 2: Infraestrutura de Microserviços"
status: backlog
priority: medium
dependencies: []
assignee: Jules
---

### Descrição

Criar um endpoint HTTP `POST /process-pdf` no `pdf_processor_service` que aceite um arquivo PDF (ou um identificador para ele), orquestre a extração de texto (usando a lógica da TASK-050) e o armazenamento dos chunks.

### Critérios de Aceitação

- [ ] Rota `POST /process-pdf` definida no FastAPI do `pdf_processor_service`.
- [ ] Endpoint aceita um arquivo PDF via upload (`UploadFile`) ou um ID/path para um arquivo já acessível pelo serviço.
- [ ] Endpoint chama a lógica de extração de texto e armazenamento de chunks.
- [ ] Endpoint retorna uma resposta significativa (e.g., ID do documento processado, número de chunks, status).
- [ ] Tratamento básico de erros implementado para falhas no processamento.

### Arquivos Relevantes

* `pdf_processor_service/app/routers/processing.py`
* `pdf_processor_service/app/main.py`

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
