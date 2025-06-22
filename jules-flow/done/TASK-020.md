---
id: TASK-020
title: "DEV: Implementar Endpoint de Processamento de PDF no Transcritor-PDF"
epic: "Fase 3: Habilitando a Interação e Diálogo com Documentos (Backend do Transcritor-PDF)"
status: done
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

- **Endpoint Verification**: Confirmed that the FastAPI endpoint `POST /process-pdf` in `transcritor-pdf/src/main.py` and the Celery task `process_pdf_task` in `transcritor-pdf/src/tasks.py` were already largely implemented and correctly structured to call each other.
- **Pipeline Implementation**: The primary effort was focused on `transcritor-pdf/src/processing.py`.
    - Replaced all placeholder functions within `process_pdf_pipeline`.
    - Implemented PDF loading from in-memory bytes using `pypdfium2`.
    - Implemented direct text extraction from PDF pages using `pypdfium2` methods (e.g., `page.get_textpage().get_text_range()`).
    - Added a new helper function `chunk_text` for splitting extracted text into manageable, overlapping chunks.
    - Integrated `src.vectorizer.embedding_generator.generate_embeddings_for_chunks` to create vector embeddings for these text chunks.
    - Integrated `src.vectorizer.vector_store_handler.add_chunks_to_vector_store` to persist the processed chunks (including text, metadata, and embeddings) into the PostgreSQL `documents` table.
    - Included error handling for various stages of the pipeline.
- **Dependency Noted**: `pypdfium2` was identified and used as a new core dependency for PDF processing.
- **Criteria Met**:
    - The route `POST /process-pdf` was verified as implemented.
    - It accepts `UploadFile`.
    - It enqueues the Celery task `src.tasks.process_pdf_task`.
    - It returns a `task_id`.
    - The Celery task `process_pdf_task` now executes a fully implemented pipeline for PDF processing, text extraction, chunking, embedding generation, and storage in the database with pgvector support.
