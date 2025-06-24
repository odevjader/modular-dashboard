---
id: TASK-011
title: "Fix UndefinedColumnError (chunk_id) in Transcritor PDF Service"
epic: "Bugfix - Transcritor PDF Service Database"
type: "bug"
status: backlog
priority: high
dependencies: ["TASK-010"] # Assumes OpenAI key config is a prerequisite for reaching this db error
assignee: Jules
---

### Descrição

The `transcritor-pdf` service encounters an `asyncpg.exceptions.UndefinedColumnError: column "chunk_id" of relation "documents" does not exist` when attempting to save processed PDF data (specifically, chunks and their embeddings) to its PostgreSQL database. This error occurs in `transcritor-pdf/src/vectorizer/vector_store_handler.py`.

This indicates a mismatch between the database schema the application code expects and the actual schema present in the database connected to the `transcritor-pdf` service.

This task involves:
1.  Investigating the database schema definition (models, migrations) within the `transcritor-pdf` service codebase.
2.  Understanding how the service connects to its database.
3.  Determining if the `chunk_id` column is missing from the `documents` table definition or if migrations are not being applied correctly.
4.  Proposing and, if possible, implementing a fix (e.g., correcting schema definitions, advising on migration execution).

### Critérios de Aceitação

- [ ] The database connection configuration for the `transcritor-pdf` service is understood.
- [ ] The code responsible for database interaction in `vector_store_handler.py` is analyzed.
- [ ] The schema definition (models/migrations) for the `documents` table within the `transcritor-pdf` service is found and reviewed.
- [ ] The cause of the schema mismatch is identified (e.g., missing column in model/migration, migrations not run, incorrect table usage).
- [ ] A solution is implemented (e.g., model/migration updated) or clear guidance is provided to the user if external actions like running migrations are needed.
- [ ] The `transcritor-pdf` service can successfully write to its `documents` table without the `UndefinedColumnError`.

### Arquivos Relevantes

* `transcritor-pdf/src/vectorizer/vector_store_handler.py` (where the error occurs)
* `transcritor-pdf/src/db_config.py` (for database connection setup)
* Any model definition files (e.g., `models.py`) or migration scripts (e.g., Alembic) within `transcritor-pdf/`.

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
