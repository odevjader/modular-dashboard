---
id: TASK-011
title: "Fix UndefinedColumnError (chunk_id) in Transcritor PDF Service"
epic: "Bugfix - Transcritor PDF Service Database"
type: "bug"
status: blocked # Blocked pending user action (migrations, processing.py update)
priority: high
dependencies: ["TASK-010"]
assignee: Jules
---

### Descrição

The `transcritor-pdf` service encountered an `asyncpg.exceptions.UndefinedColumnError: column "chunk_id" of relation "documents" does not exist` when `vector_store_handler.py` attempted to save PDF chunks and embeddings. This indicated a schema mismatch. Investigation revealed the service was trying to write chunk data into the `documents` table, while the schema (managed by `backend/app/models/` and Alembic) designates `documents` for parent document metadata and `document_chunks` for chunk-specific data.

### Critérios de Aceitação

- [x] The database connection configuration for the `transcritor-pdf` service was understood (`transcritor-pdf/src/db_config.py`).
- [x] The code in `vector_store_handler.py` was analyzed.
- [x] Schema definition from `backend/app/models/document.py` was reviewed; no separate schema for `transcritor-pdf` was found, confirming shared DB schema.
- [x] Cause of schema mismatch identified: `vector_store_handler.py` targeted `documents` table for chunk data instead of `document_chunks`, and `document_chunks` was missing `embedding` and `logical_chunk_id` columns.
- [x] Solution implemented/guided:
    - Modified `backend/app/models/document.py` to add `embedding: TEXT` and `logical_chunk_id: String` to `DocumentChunk` model.
    - Provided modified code for `transcritor-pdf/src/vectorizer/vector_store_handler.py` to target `document_chunks` table and use the new schema.
    - Instructed user to:
        1. Generate and run Alembic migrations for the schema changes in `backend/`.
        2. Update `transcritor-pdf/src/processing.py` to pass `parent_document_id` to `add_chunks_to_vector_store`.
- [ ] The `transcritor-pdf` service can successfully write to its `document_chunks` table without the `UndefinedColumnError`. (Pending user implementation of migrations and `processing.py` changes, and testing)

### Arquivos Relevantes

* `transcritor-pdf/src/vectorizer/vector_store_handler.py` (guidance for modification provided)
* `transcritor-pdf/src/db_config.py` (reviewed)
* `backend/app/models/document.py` (modified)
* `backend/alembic/` (user needs to generate and run new migration)
* `transcritor-pdf/src/processing.py` (user needs to modify to pass `parent_document_id`)

### Relatório de Execução

1.  **Analyzed Error & Code:** Confirmed `vector_store_handler.py` was trying to insert `chunk_id` into the `documents` table.
2.  **Reviewed Schema Source:** Based on user confirmation, established that `backend/app/models/document.py` and its Alembic migrations are the source of truth for the shared database schema. This model showed `documents` table does not have `chunk_id`, but `document_chunks` table is intended for chunk data.
3.  **Schema Modification:** Added `embedding: Mapped[Optional[str]] = mapped_column(Text, nullable=True)` and `logical_chunk_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)` to the `DocumentChunk` class in `backend/app/models/document.py`.
4.  **Guidance for `vector_store_handler.py`:** Provided a refactored version of the script to:
    *   Target the `document_chunks` table.
    *   Accept `parent_document_id` as a parameter.
    *   Use new columns: `document_id`, `logical_chunk_id`, `chunk_text`, `embedding`.
    *   Adjust `ON CONFLICT` for the new structure (requires a unique constraint like `(document_id, logical_chunk_id)` to be added by user via migration).
5.  **User Actions Required:**
    *   Generate and apply Alembic migration for the changes to `document_chunks` table in the `backend/` service context.
    *   Modify `transcritor-pdf/src/processing.py` to correctly obtain and pass `parent_document_id` to `add_chunks_to_vector_store`.
    *   Test the end-to-end PDF processing flow.

Task is now `blocked` pending these user actions. The necessary changes within my scope (model update and guidance for handler script) are complete.
