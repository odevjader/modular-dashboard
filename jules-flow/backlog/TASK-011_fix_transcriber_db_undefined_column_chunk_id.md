---
id: TASK-011
title: "Fix UndefinedColumnError (chunk_id) in Transcritor PDF Service"
epic: "Bugfix - Transcritor PDF Service Database"
type: "bug"
status: blocked # Blocked pending user action (apply migration, test)
priority: high
dependencies: ["TASK-010"]
assignee: Jules
---

### Descrição

The `transcritor-pdf` service encountered an `asyncpg.exceptions.UndefinedColumnError: column "chunk_id" of relation "documents" does not exist`. This was because `vector_store_handler.py` attempted to save chunk data into the `documents` table, which is designed for document-level metadata. The schema (managed by `backend/app/models/` and Alembic) uses a separate `document_chunks` table for chunk-specific data.

### Critérios de Aceitação

- [x] Database connection for `transcritor-pdf` understood (`db_config.py`).
- [x] `vector_store_handler.py` analyzed.
- [x] Schema source (`backend/app/models/document.py`) reviewed.
- [x] Schema mismatch cause identified: incorrect table and missing columns in `document_chunks` for embeddings and logical chunk IDs.
- [x] Solution implemented:
    - Modified `backend/app/models/document.py` to add `embedding: TEXT` and `logical_chunk_id: String` to `DocumentChunk` model.
    - Created Alembic migration script `backend/alembic/versions/c583de4996a7_add_embedding_logical_id_to_chunks.py` for these schema changes.
    - Modified `transcritor-pdf/src/vectorizer/vector_store_handler.py` to target `document_chunks` table, use the new schema, and accept `parent_document_id`. (Applied by user from provided code).
    - Modified `transcritor-pdf/src/tasks.py` and `transcritor-pdf/src/processing.py` to handle and pass `document_id`.
- [ ] The `transcritor-pdf` service can successfully write to its `document_chunks` table without the `UndefinedColumnError`. (Pending user applying migration and testing).
- [ ] The calling service (gateway) correctly passes `document_id` to the Celery task. (User action for gateway code).

### Arquivos Relevantes

* `backend/app/models/document.py` (modified)
* `backend/alembic/versions/c583de4996a7_add_embedding_logical_id_to_chunks.py` (created)
* `transcritor-pdf/src/vectorizer/vector_store_handler.py` (modified by user based on provided code)
* `transcritor-pdf/src/tasks.py` (modified)
* `transcritor-pdf/src/processing.py` (modified)
* `transcritor-pdf/src/db_config.py` (reviewed)

### Relatório de Execução

1.  **Error Analysis:** Confirmed `vector_store_handler.py` targeted `documents` table incorrectly for chunk data.
2.  **Schema Review:** Established `backend/app/models/document.py` and its Alembic migrations as the schema source.
3.  **Model Update:** Added `embedding` (TEXT) and `logical_chunk_id` (String) to `DocumentChunk` in `backend/app/models/document.py`.
4.  **Migration Script Creation:** Created `backend/alembic/versions/c583de4996a7_add_embedding_logical_id_to_chunks.py` with `upgrade` and `downgrade` functions for the new columns and a unique constraint on `(document_id, logical_chunk_id)` for `document_chunks`.
5.  **Transcriber Service Code Update:**
    *   Modified `transcritor-pdf/src/vectorizer/vector_store_handler.py` (via user applying provided code) to use the `document_chunks` table, accept `parent_document_id`, and align with the new schema.
    *   Modified `transcritor-pdf/src/tasks.py` and `transcritor-pdf/src/processing.py` to propagate `document_id` to the vector store handler.
6.  **User Actions Required:**
    *   Apply the Alembic migration: `alembic upgrade head` in the backend service context.
    *   Ensure the gateway service correctly calls the `process_pdf_task` Celery task with the `document_id` argument.
    *   Test the end-to-end PDF processing flow.

Task is `blocked` pending these user actions and final testing. The necessary code changes within this repository are complete.
