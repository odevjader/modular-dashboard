---
id: TASK-018
title: "DOC-SEARCH: Pesquisar Documentação (pgvector, LLM Client)"
epic: "Fase 3: Habilitando a Interação e Diálogo com Documentos (Backend do Transcritor-PDF)"
status: done
priority: medium
dependencies: ["TASK-017"] # Fase 3 inicia após conclusão da Fase 2
assignee: Jules
---

### Descrição

Pesquisar documentação sobre `pgvector` (consultas de similaridade) e a biblioteca/API usada para interagir com o LLM (conforme `transcritor-pdf/src/extractor/llm_client.py`).

### Critérios de Aceitação

- [ ] URLs e informações chave sobre consultas de similaridade com `pgvector` coletadas.
- [ ] Detalhes da API do cliente LLM (autenticação, formato de request/response) compreendidos.

### Arquivos Relevantes

* (Nenhum arquivo de código, pesquisa externa)

### Relatório de Execução

Research on `pgvector` similarity queries and the LLM client API (`transcritor-pdf/src/extractor/llm_client.py`) has been completed.

**1. LLM Client Analysis (`transcritor-pdf/src/extractor/llm_client.py`)**

*   **Provider Interaction**: Uses `langchain_openai.ChatOpenAI`, targeting OpenAI-compatible APIs. OpenRouter (`https://openrouter.ai/api/v1`) is the default base URL.
*   **Authentication**: Uses an API Key provided via the `OPENAI_API_KEY` environment variable.
*   **API Endpoint & Model**: Configurable via `OPENAI_BASE_URL`, `OPENAI_MODEL_NAME`/`OPENROUTER_MODEL_NAME` environment variables. Defaults to OpenRouter and `google/gemini-flash` model.
*   **Core Library**: `langchain-openai` for client, `langchain_core` for prompts/messages.
*   **Request/Response**: Abstracted by Langchain. Requests are typically lists of messages processed via `ChatPromptTemplate` and `.invoke()`. Responses are message objects with content accessible via `.content`.
*   **Features**: Loads configuration from `.env` files and uses a singleton pattern for the client instance.

**2. `pgvector` Similarity Queries**

*   **Primary Documentation Source**: `https://github.com/pgvector/pgvector`
*   **Functionality**: Extends PostgreSQL with a `vector` data type for similarity searches.
*   **Key Distance Operators for KNN Search (used in `ORDER BY`)**:
    *   `vector <-> query_vector`: L2 distance (Euclidean).
    *   `vector <#> query_vector`: Negative inner product (ordering ASC by this is equivalent to ordering DESC by actual inner product).
    *   `vector <=> query_vector`: Cosine distance (calculated as `1 - cosine_similarity`).
*   **Calculating Similarity/Distance Explicitly**:
    *   Actual Inner Product: `(embedding <#> query_vector) * -1`
    *   Actual Cosine Similarity: `1 - (embedding <=> query_vector)`
*   **Example KNN Query (using Cosine Distance)**:
    ```sql
    SELECT id, embedding, embedding <=> '[q1,q2,q3]' AS distance
    FROM items
    ORDER BY embedding <=> '[q1,q2,q3]'
    LIMIT N;
    ```
*   **Example KNN Query (using Inner Product for normalized vectors)**:
    ```sql
    SELECT id, embedding, (embedding <#> '[q1,q2,q3]') * -1 AS similarity
    FROM items
    ORDER BY embedding <#> '[q1,q2,q3]' -- ASC order
    LIMIT N;
    ```
*   **Filtering**: Can use `WHERE (embedding <=> query_vector) < threshold_distance`.
*   **Indexing**: Crucial for performance. Supports HNSW and IVFFlat indexes. Requires specific operator classes (e.g., `vector_cosine_ops` for cosine distance) during index creation.

This research fulfills the requirements of the task.
