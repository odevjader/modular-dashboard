# Test Plan: Unit Tests for Query Processor Orchestrator

## 1. Introduction

*   **1.1. Purpose**: To define the unit testing strategy for the `get_llm_answer_with_context` function located in `transcritor-pdf/src/query_processor.py`.
*   **1.2. Scope**:
    *   Unit testing of the `get_llm_answer_with_context` function in isolation.
    *   Focus on verifying the function's orchestration logic: calling vector search, formatting context, constructing prompts, interacting with the LLM client (mocked), processing responses, and error handling.
*   **1.3. Document Version**: 1.0
*   **1.4. References**:
    *   TASK-026: DEV: Construir Orquestrador de Respostas com LLM (Transcritor-PDF)
    *   TASK-027: TEST-PLAN: Planejar Testes para Orquestrador de Respostas (Transcritor-PDF)
    *   `transcritor-pdf/src/query_processor.py`
    *   `transcritor-pdf/src/vectorizer/vector_store_handler.py`
    *   `transcritor-pdf/src/extractor/llm_client.py`
    *   `langchain_core.messages` (for `SystemMessage`, `HumanMessage`)

## 2. Test Environment and Setup (Unit Testing)

*   **2.1. Frameworks/Libraries**:
    *   `pytest` (for test discovery and execution).
    *   `unittest.mock` (for creating mocks and patches: `patch`, `MagicMock`, `AsyncMock`).
    *   `asyncio` (native support in pytest for `async def` tests, often via `pytest-asyncio` plugin).
    *   `langchain_core.messages` (types used in prompt construction).
*   **2.2. Target Module**: `transcritor-pdf.src.query_processor`

## 3. Mocking Strategy

*   **3.1. `vector_store_handler.search_similar_chunks()`**:
    *   Mocked using `unittest.mock.patch('src.query_processor.vector_store_handler.search_similar_chunks')`.
    *   As this is an `async` function, its mock should be an `AsyncMock`.
    *   Configured to:
        *   Return a predefined list of chunk dictionaries (e.g., `[{'text_content': 'context 1', 'chunk_id': 'id1', 'metadata': {}, 'similarity_score': 0.9}]`).
        *   Return an empty list `[]` for "no context found" scenarios.
        *   Raise `ConnectionError` for context retrieval failure tests.
*   **3.2. `llm_client.get_llm_client()`**:
    *   Mocked using `unittest.mock.patch('src.query_processor.llm_client.get_llm_client')`.
    *   Configured to return a mock LLM client object (`mock_llm = MagicMock()`).
    *   Can also be configured to raise `ValueError` (simulating `load_api_config` failure from `llm_client`) for testing LLM client initialization errors.
*   **3.3. Mock LLM Client's `invoke()` Method**:
    *   The `mock_llm` object (returned by the mocked `get_llm_client`) will have its `invoke` method mocked (e.g., `mock_llm.invoke = MagicMock()`).
    *   Configured to:
        *   Return a `MagicMock` instance simulating an LLM response, with a `content` attribute (e.g., `MagicMock(content="LLM's answer")`).
        *   Return a `MagicMock` instance *without* a `content` attribute for testing malformed LLM response.
        *   Raise `Exception` for LLM API call failure tests.
*   **3.4. `logging`**:
    *   The `logger` object within `query_processor.py` (i.e., `src.query_processor.logger`) can be patched using `unittest.mock.patch.object` or the `caplog` fixture from `pytest` can be used to capture and assert log messages (e.g., `info`, `warning`, `error`).
*   **3.5. `langchain_core.messages.SystemMessage` and `langchain_core.messages.HumanMessage`**:
    *   These are typically not mocked directly. Instead, tests will assert that the `content` passed to their constructors (when forming the `messages` list for the LLM) is correct, effectively testing the prompt construction logic.

## 4. Test Cases

Detailed test cases correspond to the scenarios defined in TASK-027, Step 2.

*   **4.1. Scenario: Successful Query with Context Found**
    *   **TC_QP_001: Successful query with context**
        *   **Description**: Tests the end-to-end happy path where context is found and LLM provides an answer.
        *   **Inputs**: `user_query = "What is X?"`, `document_filename = None`, `top_k_context_chunks = 1`.
        *   **Mocked Behavior**:
            *   `search_similar_chunks` returns `[{'chunk_id': 'c1', 'text_content': 'X is a variable.', 'metadata': {}, 'similarity_score': 0.9}]`.
            *   `mock_llm.invoke(messages)` returns `MagicMock(content="X is indeed a variable according to the context.")`.
        *   **Assertions**:
            *   `search_similar_chunks` called with `user_query="What is X?"`, `top_k=1`, `document_filename=None`.
            *   The `messages` list passed to `mock_llm.invoke` contains `SystemMessage` and `HumanMessage` with correctly formatted content (context "X is a variable." and question "What is X?").
            *   The function returns `{"answer": "X is indeed a variable according to the context.", "retrieved_context": [{'chunk_id': 'c1', ...}], "error": None}`.

*   **4.2. Scenario: Query with No Context Found**
    *   **TC_QP_002: Query results in no context found**
        *   **Description**: Tests behavior when vector search returns no relevant context.
        *   **Inputs**: `user_query = "What is Y?"`.
        *   **Mocked Behavior**:
            *   `search_similar_chunks` returns `[]`.
            *   `mock_llm.invoke(messages)` returns `MagicMock(content="Com base nas informações fornecidas, não posso responder à pergunta sobre Y.")`.
        *   **Assertions**:
            *   `mock_llm.invoke` called with `messages` where context string indicates "Nenhum contexto fornecido.".
            *   Returns `{"answer": "Com base nas informações fornecidas, não posso responder à pergunta sobre Y.", "retrieved_context": [], "error": None}`.

*   **4.3. Scenario: Error during Context Retrieval**
    *   **TC_QP_003: Failure in context retrieval**
        *   **Description**: Tests error handling when `search_similar_chunks` fails.
        *   **Inputs**: `user_query = "DB error test"`.
        *   **Mocked Behavior**: `search_similar_chunks` raises `ConnectionError("Simulated DB error")`.
        *   **Assertions**:
            *   `mock_llm.invoke` is NOT called.
            *   Returns `{"answer": "Erro ao buscar contexto no banco de dados. Por favor, tente novamente mais tarde.", "retrieved_context": [], "error": "Erro de conexão com o banco de dados ao buscar contexto: Simulated DB error"}`.
            *   `logger.error` called with relevant message.

*   **4.4. Scenario: Error during LLM Call**
    *   **TC_QP_004: Failure in LLM invocation**
        *   **Description**: Tests error handling when `llm.invoke()` fails.
        *   **Inputs**: `user_query = "LLM error test"`.
        *   **Mocked Behavior**:
            *   `search_similar_chunks` returns `[{'text_content': 'Some context'}]`.
            *   `mock_llm.invoke(messages)` raises `Exception("Simulated LLM API error")`.
        *   **Assertions**:
            *   Returns `{"answer": "Ocorreu um erro inesperado ao processar sua pergunta. Por favor, tente novamente mais tarde.", "retrieved_context": [{'text_content': 'Some context'}], "error": "Erro inesperado: Simulated LLM API error"}`.
            *   `logger.error` called.

*   **4.5. Scenario: Error during LLM Client Initialization**
    *   **TC_QP_005: Failure in LLM client initialization**
        *   **Description**: Tests error handling if `get_llm_client` fails.
        *   **Inputs**: `user_query = "LLM init error"`.
        *   **Mocked Behavior**:
            *   `search_similar_chunks` returns context.
            *   `llm_client.get_llm_client` raises `ValueError("Missing API Key")` (as if from `load_api_config`).
        *   **Assertions**:
            *   Returns `{"answer": "Erro na configuração do serviço de linguagem. Verifique as credenciais.", "retrieved_context": [...], "error": "Erro de configuração do LLM: Missing API Key"}`.
            *   `logger.error` called.

*   **4.6. Scenario: LLM Response Malformed**
    *   **TC_QP_006: Malformed response from LLM**
        *   **Description**: Tests handling of an unexpected LLM response format (e.g., missing `content` attribute).
        *   **Inputs**: `user_query = "Malformed LLM response"`.
        *   **Mocked Behavior**:
            *   `search_similar_chunks` returns context.
            *   `mock_llm.invoke(messages)` returns `MagicMock(some_other_attribute="No content here")`.
        *   **Assertions**:
            *   Returns `{"answer": "Formato de resposta inesperado do LLM.", "retrieved_context": [...], "error": "Formato de resposta inesperado do LLM."}`.
            *   `logger.error` called.

*   **4.7. Scenario: Context Chunks with Empty `text_content`**
    *   **TC_QP_007: Handling of empty text in context chunks**
        *   **Description**: Tests how empty `text_content` from retrieved chunks is handled during prompt construction.
        *   **Inputs**: `user_query = "Empty context content"`.
        *   **Mocked Behavior**:
            *   `search_similar_chunks` returns `[{'text_content': ''}, {'text_content': None}, {'text_content': 'Valid context'}]`.
            *   `mock_llm.invoke(messages)` returns `MagicMock(content="Answer based on valid context.")`.
        *   **Assertions**:
            *   The `context_string` within the prompt passed to `mock_llm.invoke` should only contain "Valid context" (or be "Nenhum contexto fornecido." if all are empty).
            *   Returns `{"answer": "Answer based on valid context.", "retrieved_context": [...], "error": None}`.
            *   `logger.info` or `logger.warning` called regarding empty text content.

## 5. Success Criteria

*   All defined unit test cases pass when executed with `pytest`.
*   Code coverage for the `get_llm_answer_with_context` function is high (e.g., >90%).
*   Dependencies are correctly mocked, and interactions (arguments to mocks, call counts) are verified as expected.

## 6. Out of Scope

*   Integration testing with a real vector database or a live LLM API.
*   Testing of the internal logic of `vector_store_handler.search_similar_chunks` or `llm_client.get_llm_client` (these should have their own separate unit tests).
*   Performance or load testing.

## 7. Test Reporting (Placeholder)

*   *(This section would be filled in upon actual test execution and reporting.)*
