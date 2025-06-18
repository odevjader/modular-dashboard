# Test Plan: Unit Tests for Vector Search Functionality

## 1. Introduction

*   **1.1. Purpose**: To define the unit testing strategy for the `search_similar_chunks` function located in `transcritor-pdf/src/vectorizer/vector_store_handler.py`.
*   **1.2. Scope**:
    *   Unit testing of the `search_similar_chunks` function in isolation.
    *   Focus on verifying the function's internal logic, SQL query construction, interaction with mocked dependencies (embedding generator, database connection), data transformation, and error handling.
*   **1.3. Document Version**: 1.0
*   **1.4. References**:
    *   TASK-023: DEV: Desenvolver Inteligência de Busca Vetorial (Transcritor-PDF)
    *   TASK-024: TEST-PLAN: Planejar Testes para Busca Vetorial (Transcritor-PDF)
    *   `transcritor-pdf/src/vectorizer/vector_store_handler.py`
    *   `transcritor-pdf/src/vectorizer/embedding_generator.py`

## 2. Test Environment and Setup (Unit Testing)

*   **2.1. Frameworks/Libraries**:
    *   `pytest` (for test discovery and execution).
    *   `unittest.mock` (for creating mocks and patches).
    *   `asyncio` (native support in pytest for `async def` tests, or `pytest-asyncio` plugin).
    *   `asyncpg` (for type hints like `asyncpg.Record`, though actual connections are mocked).
*   **2.2. Target Module**: `transcritor-pdf.src.vectorizer.vector_store_handler`

## 3. Mocking Strategy

*   **3.1. `embedding_generator.get_embedding_client().embed_query()`**:
    *   Mocked using `unittest.mock.patch` on `src.vectorizer.vector_store_handler.embedding_generator.get_embedding_client` (or more specifically, its `embed_query` method if preferred).
    *   The mock client's `embed_query` method will be configured to return a predefined vector (e.g., `[0.1, 0.2, 0.3]`) or raise specific exceptions for error case testing.
*   **3.2. `asyncpg.connect()`**:
    *   Mocked using `unittest.mock.patch` on `asyncpg.connect` (as imported and used within `vector_store_handler.py`).
    *   Will be configured to return a mock `asyncpg.Connection` object or raise connection-related exceptions (e.g., `OSError`).
*   **3.3. Mock `asyncpg.Connection` Object**:
    *   The returned mock connection object will itself have its methods mocked, primarily:
        *   `fetch(query_string, *params)`: This will be the primary interaction point. Mocked to:
            *   Return a list of mock `asyncpg.Record` objects. These can be `MagicMock` instances configured with `spec=asyncpg.Record` and a `__getitem__` side effect to return values for keys like `chunk_id`, `text_content`, `metadata`, `distance`.
            *   Return an empty list for "no results" scenarios.
            *   Raise `asyncpg.PostgresError` for query failure scenarios.
        *   `close()`: Mocked to allow assertion that it was called.
*   **3.4. `load_db_config()` (within `vector_store_handler.py`)**:
    *   Mocked using `unittest.mock.patch` on `src.vectorizer.vector_store_handler.load_db_config`.
    *   Configured to return specific dictionary outputs, especially for testing missing DB credentials or different connection parameters if needed.
*   **3.5. `logging`**:
    *   The `logger` object within `vector_store_handler.py` (e.g., `src.vectorizer.vector_store_handler.logger`) can be patched using `unittest.mock.patch.object` to capture log messages (e.g., with `caplog` fixture in pytest, or by asserting calls on a mock logger's methods like `warning()`, `error()`).

## 4. Test Cases

Detailed test cases correspond to the scenarios defined in TASK-024, Step 2.

*   **4.1. Scenario: Successful Search - No Filename Filter**
    *   **TC_VS_001: Search without filename filter returns correct data**
        *   **Description**: Test a standard similarity search without filtering by filename.
        *   **Inputs**: `query_text = "test query"`, `top_k = 3`.
        *   **Mocked Behavior**:
            *   `embedding_generator.embed_query("test query")` returns `[0.1, 0.2, 0.3]`.
            *   `asyncpg.connect` returns a mock connection (`mock_conn`).
            *   `mock_conn.fetch(sql, [0.1, 0.2, 0.3], 3)` returns `[Record1, Record2, Record3]` with predefined content and distances (e.g., 0.1, 0.2, 0.3).
        *   **Assertions**:
            *   Verify the SQL query string passed to `mock_conn.fetch` is `SELECT chunk_id, text_content, metadata, embedding <=> $1 AS distance FROM documents ORDER BY distance ASC LIMIT $2` (or its parameterized equivalent).
            *   Verify parameters passed to `mock_conn.fetch` are `([0.1, 0.2, 0.3], 3)`.
            *   Verify the function returns a list of 3 dictionaries.
            *   Verify each dictionary contains `chunk_id`, `text_content`, `metadata`, and correctly calculated `similarity_score` (1 - distance).
            *   Verify `mock_conn.close()` was called.

*   **4.2. Scenario: Successful Search - With Filename Filter**
    *   **TC_VS_002: Search with filename filter returns correct data**
        *   **Description**: Test similarity search filtered by a specific document filename.
        *   **Inputs**: `query_text = "filter query"`, `top_k = 2`, `document_filename = "docX.pdf"`.
        *   **Mocked Behavior**:
            *   `embedding_generator.embed_query("filter query")` returns `[0.4, 0.5, 0.6]`.
            *   `mock_conn.fetch(sql, [0.4, 0.5, 0.6], "docX.pdf", 2)` returns 2 mock records matching the filename.
        *   **Assertions**:
            *   Verify SQL query includes `WHERE metadata->>'filename' = $2` (or equivalent for the specific parameter index used).
            *   Verify parameters include `"docX.pdf"`.
            *   Verify returned list has 2 dictionaries, all from `"docX.pdf"`.

*   **4.3. Scenario: Search Returns No Results (Empty Fetch)**
    *   **TC_VS_003: Search with no matching results**
        *   **Description**: Test behavior when the database query finds no matching chunks.
        *   **Inputs**: `query_text = "no match query"`, `top_k = 5`.
        *   **Mocked Behavior**: `mock_conn.fetch` returns `[]`.
        *   **Assertions**: Verify the function returns `[]`.

*   **4.4. Scenario: `top_k` Validation (Invalid `top_k`)**
    *   **TC_VS_004: Invalid `top_k` value (zero or negative)**
        *   **Description**: Test the input validation for `top_k`.
        *   **Inputs**: `query_text = "any query"`, `top_k = 0` (and another test for `top_k = -1`).
        *   **Assertions**: Verify the function returns `[]`. Verify `logger.warning` was called with an appropriate message.

*   **4.5. Scenario: Error in Query Embedding Generation**
    *   **TC_VS_005: Embedding generation failure**
        *   **Description**: Test behavior when `embedding_generator.embed_query` fails.
        *   **Inputs**: `query_text = "embedding error query"`.
        *   **Mocked Behavior**: `embedding_generator.embed_query` raises `RuntimeError("Embedding API failed")`.
        *   **Assertions**: Verify the function returns `[]`. Verify `logger.error` was called.

*   **4.6. Scenario: Database Connection Error (`asyncpg.connect` fails)**
    *   **TC_VS_006: Database connection failure**
        *   **Description**: Test behavior when the database connection cannot be established.
        *   **Inputs**: `query_text = "db connect error query"`.
        *   **Mocked Behavior**: `asyncpg.connect` raises `OSError("Connection refused")`.
        *   **Assertions**: Verify that `ConnectionError` is raised by `search_similar_chunks`.

*   **4.7. Scenario: Database Query Execution Error (`conn.fetch` fails)**
    *   **TC_VS_007: Database query execution failure**
        *   **Description**: Test behavior when the database query execution fails.
        *   **Inputs**: `query_text = "db query error query"`.
        *   **Mocked Behavior**: `mock_conn.fetch` raises `asyncpg.PostgresError("Syntax error")`.
        *   **Assertions**: Verify that `ConnectionError` is raised by `search_similar_chunks`.

*   **4.8. Scenario: Malformed JSON Metadata in DB Record**
    *   **TC_VS_008: Malformed JSON metadata from database**
        *   **Description**: Test graceful handling if metadata from DB is not valid JSON.
        *   **Inputs**: `query_text = "metadata error query"`.
        *   **Mocked Behavior**: `mock_conn.fetch` returns a record where `row['metadata']` is the string `"this is not json"`.
        *   **Assertions**: Verify the function returns a result for that chunk. Verify `metadata` field for that chunk is `"this is not json"`. Verify `logger.warning` was called.

*   **4.9. Scenario: DB Config Missing**
    *   **TC_VS_009: Missing essential DB configuration**
        *   **Description**: Test behavior if essential DB configuration (e.g., DB_NAME) is missing.
        *   **Inputs**: `query_text = "any query"`.
        *   **Mocked Behavior**: `load_db_config` (mocked) returns `{"host": "localhost", "port": 5432, "database": None, "user": "user", "password": "pass"}`.
        *   **Assertions**: Verify that `ConnectionError` is raised by `search_similar_chunks` before attempting to connect.

## 5. Success Criteria

*   All defined unit test cases pass when executed with `pytest`.
*   Code coverage for the `search_similar_chunks` function (as reported by a coverage tool like `pytest-cov`) is high (e.g., >90%).
*   Tests effectively mock external dependencies and isolate the function's logic for verification.

## 6. Out of Scope

*   Integration testing involving a real PostgreSQL database or a live embedding service API.
*   Performance or load testing of the search function.
*   Testing of the `src.vectorizer.embedding_generator` module itself (which should have its own unit tests).
*   Testing of other functions within `vector_store_handler.py` (e.g., `add_chunks_to_vector_store`).

## 7. Test Reporting (Placeholder)

*   *(This section would be filled in upon actual test execution and reporting, typically by CI/CD systems or manual test runs.)*
