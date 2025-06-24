---
id: TASK-010
title: "Configure OpenAI API Key for Transcriber PDF Service"
epic: "Bugfix - Transcritor PDF Service"
type: "bug" # Or "configuration" if that's a valid type
status: backlog
priority: high
dependencies: [] # No direct code dependency, but functionally follows TASK-009
assignee: Jules
---

### Descrição

The `transcritor-pdf` service fails during PDF processing when attempting to generate embeddings via the OpenAI API. Logs show a `401 Unauthorized` error from `https://api.openai.com/v1/embeddings`. This indicates that the OpenAI API key is missing, incorrect, or not properly configured for the `OpenAIEmbeddings` client within the `transcritor-pdf` service.

This task involves:
1.  Locating how the OpenAI API key is sourced within the `transcritor-pdf` service code (located in the `transcritor-pdf/` folder).
2.  Ensuring the code reads the API key from an environment variable (e.g., `OPENAI_API_KEY`). If not, modify the code to do so.
3.  Providing clear instructions to the user on how to set this environment variable for their `transcritor-pdf` service (e.g., in a `.env` file for Docker Compose).

### Critérios de Aceitação

- [ ] The method for OpenAI API key configuration within the `transcritor-pdf` service code is identified.
- [ ] If necessary, the `transcritor-pdf` service code is modified to read the OpenAI API key from a standard environment variable (e.g., `OPENAI_API_KEY`).
- [ ] Clear instructions are provided to the user on how to set this environment variable for the `transcritor-pdf` service.
- [ ] After correct configuration by the user, the `transcritor-pdf` service can successfully generate embeddings without a 401 error from OpenAI.

### Arquivos Relevantes

* `transcritor-pdf/` (directory containing the service code)
* Specifically, files related to OpenAI client initialization or embedding generation.

### Relatório de Execução

(Esta seção deve ser deixada em branco no template)
