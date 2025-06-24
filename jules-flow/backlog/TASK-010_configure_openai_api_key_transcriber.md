---
id: TASK-010
title: "Configure OpenAI API Key for Transcriber PDF Service"
epic: "Bugfix - Transcritor PDF Service"
type: "configuration"
status: blocked # Blocked pending user action to set the env var
priority: high
dependencies: []
assignee: Jules
---

### Descrição

The `transcritor-pdf` service fails during PDF processing when attempting to generate embeddings via the OpenAI API. Logs show a `401 Unauthorized` error from `https://api.openai.com/v1/embeddings`. This indicates that the OpenAI API key is missing, incorrect, or not properly configured.

This task involved:
1.  Locating how the OpenAI API key is sourced by the `transcritor-pdf` service.
2.  Confirming the code supports reading the API key from an environment variable.
3.  Providing instructions to the user on how to set this variable.

### Critérios de Aceitação

- [x] The method for OpenAI API key configuration within the `transcritor-pdf` service code (`transcritor-pdf/src/vectorizer/embedding_generator.py`) was identified. It uses `langchain_openai.OpenAIEmbeddings`, which automatically reads the `OPENAI_API_KEY` environment variable.
- [x] Confirmed that no code modification was necessary as the service already supports reading the key from the `OPENAI_API_KEY` environment variable.
- [x] Clear instructions were provided to the user on how to set the `OPENAI_API_KEY` environment variable for the `transcritor-pdf` service (typically in a `.env` file used by Docker Compose).
- [ ] After correct configuration by the user, the `transcritor-pdf` service can successfully generate embeddings without a 401 error from OpenAI. (Pending user action)

### Arquivos Relevantes

* `transcritor-pdf/src/vectorizer/embedding_generator.py` (inspected)

### Relatório de Execução

1.  **Located API Key Usage:** Inspected `transcritor-pdf/src/vectorizer/embedding_generator.py`.
2.  **Confirmed Configuration Method:** The code uses `langchain_openai.OpenAIEmbeddings`, which by default reads the OpenAI API key from the `OPENAI_API_KEY` environment variable. No code changes were needed.
3.  **Provided Instructions:** Instructed the user to set the `OPENAI_API_KEY` environment variable in their environment for the `transcritor-pdf` service, likely in a `.env` file at the project root or specific Docker Compose configuration for that service.
4.  **Next Step:** The user needs to set their OpenAI API key in the environment for the `transcritor-pdf` service and restart the service.

This task is now `blocked` pending the user setting the API key and confirming the resolution of the 401 error. The user then reported a new database-related error, which will be handled in TASK-011.
