---
id: TASK-020
title: "DEV: Implementar Endpoint de Processamento de PDF no Transcritor-PDF"
epic: "Fase 3: Habilitando a Interação e Diálogo com Documentos (Backend do Transcritor-PDF)"
status: backlog
priority: medium
dependencies: ["TASK-004", "TASK-019"] # Depende de Celery/Redis config e docs de pgvector/LLM
assignee: Jules
---

### Descrição

Criar rota `POST /process-pdf` no `transcritor-pdf/src/main.py`. Recebe arquivo, enfileira tarefa Celery para extração, vetorização e armazenamento.

### Critérios de Aceitação

- [ ] Rota `POST /process-pdf` implementada em `transcritor-pdf/src/main.py`.
- [ ] Aceita `UploadFile`.
- [ ] Enfileira uma tarefa Celery (e.g., `src.tasks.process_pdf_task`) com o conteúdo do arquivo ou caminho.
- [ ] Retorna um ID de job ou confirmação.
- [ ] (A tarefa Celery `process_pdf_task` em `src.tasks.py` precisará ser definida/verificada para realizar a lógica de processamento e armazenamento no DB com pgvector.)

### Arquivos Relevantes

* `transcritor-pdf/src/main.py`
* `transcritor-pdf/src/tasks.py`

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
