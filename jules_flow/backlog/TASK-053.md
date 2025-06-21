---
id: TASK-053
title: "DEV (Fase 2): Implementar Endpoint Gateway `/api/v1/documents/upload-and-process` na API Principal"
epic: "Fase 2: Infraestrutura de Microserviços"
status: backlog
priority: medium
dependencies: []
assignee: Jules
---

### Descrição

Implementar um novo endpoint na API Principal (`backend`) que atuará como gateway para o `pdf_processor_service`. Este endpoint receberá um upload de arquivo PDF, o encaminhará para o `pdf_processor_service` (chamando o endpoint `POST /process-pdf` da TASK-051) e retornará a resposta ao cliente.

### Critérios de Aceitação

- [ ] Nova rota `POST /api/v1/documents/upload-and-process` definida no módulo `documents` (ou um novo módulo apropriado) da API Principal.
- [ ] Endpoint protegido por autenticação.
- [ ] Endpoint aceita upload de arquivo PDF.
- [ ] Endpoint faz uma requisição HTTP interna para o endpoint `POST /process-pdf` do `pdf_processor_service`, encaminhando o arquivo ou seus dados.
- [ ] Endpoint retorna a resposta do `pdf_processor_service` ao cliente.
- [ ] Tratamento de erros para falhas na comunicação com o `pdf_processor_service`.

### Arquivos Relevantes

* `backend/app/modules/documents/router.py`
* `backend/app/modules/documents/services.py`

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
