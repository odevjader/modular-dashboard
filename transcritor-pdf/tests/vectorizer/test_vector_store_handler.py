# -*- coding: utf-8 -*-
"""
Unit tests for the src.vectorizer.vector_store_handler module using asyncpg mocks.
"""

import pytest
import json
import asyncio
import logging # Added for caplog
from unittest.mock import MagicMock, AsyncMock, patch
from src.vectorizer.vector_store_handler import add_chunks_to_vector_store, load_db_config, search_similar_chunks # Added search_similar_chunks
try:
    import asyncpg # Import asyncpg to reference its exceptions
    ASYNC_PG_AVAILABLE = True
except ImportError:
    ASYNC_PG_AVAILABLE = False

pytestmark = pytest.mark.asyncio

@pytest.fixture
def mock_db_config(mocker):
    dummy_config = {"host": "mockhost", "port": 5432, "database": "mockdb", "user": "mockuser", "password": "mockpassword"}
    mocker.patch('src.vectorizer.vector_store_handler.load_db_config', return_value=dummy_config)
    return dummy_config

@pytest.fixture
def mock_asyncpg_connect(mocker):
    if not ASYNC_PG_AVAILABLE: pytest.skip("asyncpg not installed")
    mock_conn = AsyncMock(spec=asyncpg.Connection)
    # Mock the transaction context manager
    mock_tx = AsyncMock()
    # __aexit__ needs to handle exception propagation correctly for the test
    # If side_effect is set on execute, __aexit__ will receive exception info
    async def mock_aexit(exc_type, exc_val, exc_tb):
        # Simulate default behavior: re-raise if exception occurred
        # print(f"DEBUG: __aexit__ called with exc_type={exc_type}") # Debug print
        if exc_type:
            return False # Indicates exception should be re-raised
        return True # Indicates exception was handled (suppressed)

    mock_conn.transaction.return_value = mocker.AsyncMock(
        __aenter__=AsyncMock(return_value=mock_tx),
        __aexit__=AsyncMock(side_effect=mock_aexit) # Use side_effect for async func
    )
    mock_conn.execute = AsyncMock()
    mock_conn.close = AsyncMock()
    mock_conn.is_closed.return_value = False
    mock_connect = mocker.patch('asyncpg.connect', new_callable=AsyncMock, return_value=mock_conn)
    return mock_connect, mock_conn

@pytest.mark.skipif(not ASYNC_PG_AVAILABLE, reason="asyncpg not installed.")
async def test_add_chunks_success(mock_db_config, mock_asyncpg_connect):
    mock_connect, mock_conn = mock_asyncpg_connect
    embedding_dim = 1536
    sample_chunks = [
        {"chunk_id": "ok_chunk_1", "text_content": "Text 1.", "metadata": {"p": 1}, "embedding": [0.1] * embedding_dim},
        {"chunk_id": "ok_chunk_2", "text_content": "Text 2.", "metadata": {"p": 2}, "embedding": [0.2] * embedding_dim},
    ]
    await add_chunks_to_vector_store(sample_chunks)
    mock_connect.assert_awaited_once_with(**mock_db_config)
    mock_conn.transaction.assert_called_once()
    assert mock_conn.execute.await_count == 2
    mock_conn.close.assert_awaited_once()

@pytest.mark.skipif(not ASYNC_PG_AVAILABLE, reason="asyncpg not installed.")
async def test_add_chunks_skips_invalid(mock_db_config, mock_asyncpg_connect):
    mock_connect, mock_conn = mock_asyncpg_connect
    embedding_dim = 1536
    sample_chunks = [
        {"chunk_id": "valid_1", "text_content": "Valid text.", "metadata": {}, "embedding": [0.1] * embedding_dim},
        {"chunk_id": "invalid_1", "text_content": "Missing embedding.", "metadata": {}},
        {"chunk_id": "valid_2", "text_content": "Another valid.", "metadata": {}, "embedding": [0.2] * embedding_dim},
        {"chunk_id": "invalid_2", "text_content": None, "metadata": {}, "embedding": [0.3] * embedding_dim},
    ]
    await add_chunks_to_vector_store(sample_chunks)
    mock_connect.assert_awaited_once()
    mock_conn.transaction.assert_called_once()
    assert mock_conn.execute.await_count == 2
    mock_conn.close.assert_awaited_once()

@pytest.mark.skipif(not ASYNC_PG_AVAILABLE, reason="asyncpg not installed.")
async def test_add_chunks_connection_error(mock_db_config, mocker):
    mock_connect = mocker.patch('asyncpg.connect', new_callable=AsyncMock)
    mock_connect.side_effect = OSError("Simulated connection refused")
    sample_chunks = [{"chunk_id": "c1", "text_content": "t", "metadata": {}, "embedding": [0.1]}]
    # Expect ConnectionError because the outer except block catches OSError
    with pytest.raises(ConnectionError):
        await add_chunks_to_vector_store(sample_chunks)
    mock_connect.assert_awaited_once_with(**mock_db_config)

@pytest.mark.skipif(not ASYNC_PG_AVAILABLE, reason="asyncpg not installed.")
async def test_add_chunks_execute_error(mock_db_config, mock_asyncpg_connect):
    """
    Tests that ConnectionError is raised if conn.execute fails internally,
    due to the outer exception handling wrapping the original asyncpg error.
    """
    mock_connect, mock_conn = mock_asyncpg_connect
    embedding_dim = 1536
    sample_chunks = [{"chunk_id": "c1", "text_content": "t", "metadata": {}, "embedding": [0.1] * embedding_dim}]

    # Simulate asyncpg error during execute
    db_error = asyncpg.PostgresError("Simulated unique constraint violation")
    mock_conn.execute.side_effect = db_error

    # --- Expect ConnectionError, as the original error is caught and wrapped ---
    with pytest.raises(ConnectionError):
        await add_chunks_to_vector_store(sample_chunks)
    # --- End Correction ---

    # Assertions
    mock_connect.assert_awaited_once()
    mock_conn.transaction.assert_called_once()
    mock_conn.execute.assert_awaited_once() # Should be called once before failing
    mock_conn.close.assert_awaited_once() # Finally block should still close

async def test_add_chunks_empty_list():
    """Tests that the function handles an empty input list gracefully."""
    await add_chunks_to_vector_store([])

# --- Unit Tests for search_similar_chunks ---

@pytest.mark.skipif(not ASYNC_PG_AVAILABLE, reason="asyncpg not installed.")
@patch('src.vectorizer.vector_store_handler.embedding_generator')
async def test_search_successful_no_filter(mock_embedding_gen, mock_db_config, mock_asyncpg_connect, caplog):
    mock_connect, mock_conn = mock_asyncpg_connect

    # Configure mock embedding generator
    mock_embed_client = MagicMock()
    mock_embed_client.embed_query.return_value = [0.1, 0.2, 0.3]
    mock_embedding_gen.get_embedding_client.return_value = mock_embed_client

    # Configure mock_conn.fetch to return mock records
    def make_mock_record(data):
        record = MagicMock(spec=asyncpg.Record)
        # Make the mock record behave like a dictionary for __getitem__
        def getitem_side_effect(key):
            return data[key]
        record.__getitem__.side_effect = getitem_side_effect
        # Also allow accessing items as attributes if your code does that (though spec=Record implies dict-like)
        for key, value in data.items():
            setattr(record, key, value)
        return record

    mock_records_data = [
        {'chunk_id': 'id1', 'text_content': 'text1', 'metadata': {'filename': 'docA.pdf', 'page_number': 1}, 'distance': 0.1},
        {'chunk_id': 'id2', 'text_content': 'text2', 'metadata': {'filename': 'docB.pdf', 'page_number': 1}, 'distance': 0.2},
    ]
    mock_conn.fetch.return_value = [make_mock_record(data) for data in mock_records_data]

    query_text = "test query"
    top_k = 2

    caplog.set_level(logging.INFO)
    results = await search_similar_chunks(query_text, top_k=top_k)

    mock_embedding_gen.get_embedding_client.assert_called_once()
    mock_embed_client.embed_query.assert_called_once_with(query_text)

    mock_connect.assert_awaited_once_with(**mock_db_config)

    called_args = mock_conn.fetch.call_args
    assert called_args is not None
    sql_query = called_args[0][0]
    params = called_args[0][1:] # Correctly slice all positional args after the query string

    assert "SELECT chunk_id, text_content, metadata, embedding <=> $1 AS distance FROM documents" in sql_query
    assert "ORDER BY distance ASC LIMIT $2" in sql_query
    assert "WHERE" not in sql_query
    assert params[0] == [0.1, 0.2, 0.3] # embedding is the first param
    assert params[1] == top_k          # top_k is the second param

    assert len(results) == 2
    assert results[0]['chunk_id'] == 'id1'
    assert results[0]['similarity_score'] == pytest.approx(1 - 0.1)
    assert results[0]['metadata']['filename'] == 'docA.pdf'
    assert results[1]['chunk_id'] == 'id2'
    assert results[1]['similarity_score'] == pytest.approx(1 - 0.2)

    mock_conn.close.assert_awaited_once()
    assert "Generated embedding for query" in caplog.text
    assert "Executing search query" in caplog.text
    assert f"Found {len(results)} similar chunks." in caplog.text

@pytest.mark.skipif(not ASYNC_PG_AVAILABLE, reason="asyncpg not installed.")
@patch('src.vectorizer.vector_store_handler.embedding_generator')
async def test_search_successful_with_filename_filter(mock_embedding_gen, mock_db_config, mock_asyncpg_connect):
    mock_connect, mock_conn = mock_asyncpg_connect

    mock_embed_client = MagicMock()
    mock_embed_client.embed_query.return_value = [0.4, 0.5, 0.6]
    mock_embedding_gen.get_embedding_client.return_value = mock_embed_client

    def make_mock_record(data):
        record = MagicMock(spec=asyncpg.Record)
        def getitem_side_effect(key):
            return data[key]
        record.__getitem__.side_effect = getitem_side_effect
        for key, value in data.items(): # Allow attribute access if used
            setattr(record, key, value)
        return record

    mock_records_data = [
        {'chunk_id': 'id3', 'text_content': 'text3 from docX', 'metadata': {'filename': 'docX.pdf'}, 'distance': 0.3},
    ]
    mock_conn.fetch.return_value = [make_mock_record(data) for data in mock_records_data]

    query_text = "filter query"
    top_k = 1
    document_filename = "docX.pdf"
    results = await search_similar_chunks(query_text, top_k=top_k, document_filename=document_filename)

    mock_embed_client.embed_query.assert_called_once_with(query_text)

    called_args = mock_conn.fetch.call_args
    assert called_args is not None
    sql_query = called_args[0][0]
    params = called_args[0][1:]

    assert "WHERE metadata->>'filename' = $2" in sql_query
    assert "ORDER BY distance ASC LIMIT $3" in sql_query
    assert params[0] == [0.4, 0.5, 0.6]    # embedding
    assert params[1] == document_filename # filename filter
    assert params[2] == top_k             # limit

    assert len(results) == 1
    assert results[0]['chunk_id'] == 'id3'
    assert results[0]['metadata']['filename'] == 'docX.pdf'
    assert results[0]['similarity_score'] == pytest.approx(1 - 0.3)

    mock_conn.close.assert_awaited_once()

@pytest.mark.skipif(not ASYNC_PG_AVAILABLE, reason="asyncpg not installed.")
@patch('src.vectorizer.vector_store_handler.embedding_generator')
async def test_search_returns_no_results(mock_embedding_gen, mock_db_config, mock_asyncpg_connect):
    mock_connect, mock_conn = mock_asyncpg_connect

    mock_embed_client = MagicMock()
    mock_embed_client.embed_query.return_value = [0.7, 0.8, 0.9]
    mock_embedding_gen.get_embedding_client.return_value = mock_embed_client

    mock_conn.fetch.return_value = [] # Simulate no records found

    results = await search_similar_chunks("no match query", top_k=5)

    assert results == []
    mock_conn.fetch.assert_awaited_once()
    mock_conn.close.assert_awaited_once()

@pytest.mark.skipif(not ASYNC_PG_AVAILABLE, reason="asyncpg not installed.")
@patch('src.vectorizer.vector_store_handler.logger')
@patch('src.vectorizer.vector_store_handler.embedding_generator')
async def test_search_invalid_top_k(mock_embedding_gen_unused, mock_logger_vsh, mock_db_config_fixture_unused, mock_asyncpg_connect_fixture_unused, caplog):
    # caplog can also be used if preferred over patching logger directly
    # mock_db_config_fixture_unused and mock_asyncpg_connect_fixture_unused are just to match signature if all fixtures are auto-used

    # For top_k = 0
    results_zero = await search_similar_chunks("any query", top_k=0)
    assert results_zero == []
    # Check if the logger associated with vector_store_handler was called
    assert any("top_k must be positive" in record.message for record in mock_logger_vsh.warning.call_args_list)

    mock_logger_vsh.reset_mock()

    # For top_k = -1
    results_negative = await search_similar_chunks("any query", top_k=-1)
    assert results_negative == []
    assert any("top_k must be positive" in record.message for record in mock_logger_vsh.warning.call_args_list)

    mock_embedding_gen_unused.get_embedding_client.assert_not_called()
    # mock_asyncpg_connect_fixture_unused[0] is mock_connect if this fixture were actually used and passed
    # Since we expect an early return, these deeper mocks might not be needed or might not be called.
    # If the fixtures are auto-used, ensure they don't interfere.
    # If not auto-used, they are not passed and this check is not applicable.
    # For this test, it's better to assert that the patched asyncpg.connect was NOT called.
    with patch('asyncpg.connect') as mock_connect_call_check: # Check if asyncpg.connect was called
        await search_similar_chunks("any query", top_k=0) # Call again to check connect
        mock_connect_call_check.assert_not_called()

# --- Helper for mock records, define at module scope if used by multiple tests ---
def make_mock_pg_record_global(data): # Renamed to avoid conflict if already defined locally
    record = MagicMock(spec=asyncpg.Record)
    def getitem_side_effect(key):
        return data[key]
    record.__getitem__.side_effect = getitem_side_effect
    for key, value in data.items():
        setattr(record, key, value)
    return record

@pytest.mark.skipif(not ASYNC_PG_AVAILABLE, reason="asyncpg not installed.")
@patch('src.vectorizer.vector_store_handler.embedding_generator')
async def test_search_embedding_generation_error(mock_embedding_gen, mock_db_config, caplog):
    # mock_db_config fixture ensures load_db_config is patched and returns valid config
    mock_embed_client = MagicMock()
    mock_embed_client.embed_query.side_effect = RuntimeError("Simulated embedding error")
    mock_embedding_gen.get_embedding_client.return_value = mock_embed_client

    caplog.set_level(logging.ERROR)
    results = await search_similar_chunks("error query")

    assert results == []
    mock_embedding_gen.get_embedding_client.assert_called_once()
    mock_embed_client.embed_query.assert_called_once_with("error query")
    assert "Error generating query embedding: Simulated embedding error" in caplog.text

@pytest.mark.skipif(not ASYNC_PG_AVAILABLE, reason="asyncpg not installed.")
@patch('src.vectorizer.vector_store_handler.embedding_generator')
@patch('asyncpg.connect', new_callable=AsyncMock) # Patch asyncpg.connect directly
async def test_search_db_connection_error(mock_asyncpg_connect_method, mock_embedding_gen, mock_db_config):
    # mock_db_config fixture patches load_db_config to return a valid config

    mock_embed_client = MagicMock()
    mock_embed_client.embed_query.return_value = [0.1, 0.2, 0.3]
    mock_embedding_gen.get_embedding_client.return_value = mock_embed_client

    mock_asyncpg_connect_method.side_effect = OSError("Simulated connection refused")

    with pytest.raises(ConnectionError) as excinfo:
        await search_similar_chunks("db connect error query")

    assert "Database connection or query failed during search: Simulated connection refused" in str(excinfo.value)
    mock_embedding_gen.get_embedding_client.assert_called_once()
    # load_db_config is called inside SUT, patched by mock_db_config fixture
    # asyncpg.connect was called
    mock_asyncpg_connect_method.assert_awaited_once()


@pytest.mark.skipif(not ASYNC_PG_AVAILABLE, reason="asyncpg not installed.")
@patch('src.vectorizer.vector_store_handler.embedding_generator')
async def test_search_db_query_execution_error(mock_embedding_gen, mock_db_config, mock_asyncpg_connect, caplog):
    # mock_asyncpg_connect is a fixture providing (mock_connect_patch, mock_connection_instance)
    mock_connect_patch, mock_conn_instance = mock_asyncpg_connect

    mock_embed_client = MagicMock()
    mock_embed_client.embed_query.return_value = [0.1, 0.2, 0.3]
    mock_embedding_gen.get_embedding_client.return_value = mock_embed_client

    db_error_message = "Simulated query syntax error"
    mock_conn_instance.fetch.side_effect = asyncpg.PostgresError(db_error_message)

    caplog.set_level(logging.CRITICAL)
    with pytest.raises(ConnectionError) as excinfo:
        await search_similar_chunks("db query error query")

    assert f"Database connection or query failed during search: {db_error_message}" in str(excinfo.value)

    mock_connect_patch.assert_awaited_once_with(**mock_db_config)
    mock_conn_instance.fetch.assert_awaited_once()
    mock_conn_instance.close.assert_awaited_once()
    assert f"Database connection or query error during search: {db_error_message}" in caplog.text


@pytest.mark.skipif(not ASYNC_PG_AVAILABLE, reason="asyncpg not installed.")
@patch('src.vectorizer.vector_store_handler.embedding_generator')
async def test_search_malformed_json_metadata(mock_embedding_gen, mock_db_config, mock_asyncpg_connect, caplog):
    mock_connect_patch, mock_conn_instance = mock_asyncpg_connect

    mock_embed_client = MagicMock()
    mock_embed_client.embed_query.return_value = [0.1, 0.2, 0.3]
    mock_embedding_gen.get_embedding_client.return_value = mock_embed_client

    malformed_metadata_str = "this is not json{"
    # Use the globally defined helper for mock records
    mock_records_data = [
        {'chunk_id': 'id_malformed', 'text_content': 'text_meta_error', 'metadata': malformed_metadata_str, 'distance': 0.4},
    ]
    mock_conn_instance.fetch.return_value = [make_mock_pg_record_global(data) for data in mock_records_data]

    caplog.set_level(logging.WARNING)
    results = await search_similar_chunks("metadata error query")

    assert len(results) == 1
    assert results[0]['chunk_id'] == 'id_malformed'
    # The function currently tries json.loads, if it fails, it should keep the original.
    # However, the current implementation of search_similar_chunks does not include this try-except for json.loads
    # It was in the draft but not in the final applied code for search_similar_chunks.
    # Assuming the metadata is passed as is if it's not a dict already.
    # If asyncpg returns a string for a JSONB field that's malformed, it would be passed as a string.
    # The test should reflect the actual implementation.
    # Current implementation of search_similar_chunks:
    # metadata_content = row['metadata']
    # if isinstance(metadata_content, str): <--- This block was in the thought process but not in the final code for search_similar_chunks
    # So, if row['metadata'] is a string, it will be passed as is.
    assert results[0]['metadata'] == malformed_metadata_str
    assert results[0]['similarity_score'] == pytest.approx(1 - 0.4)
    # The warning for JSON parsing is only logged if json.loads is attempted and fails.
    # Based on current code of search_similar_chunks, this warning won't be logged.
    # I will add the json.loads block to search_similar_chunks as it was intended.
    # For now, this assertion will fail if the warning is not logged.
    # To make test pass with current code: remove the log check or expect no such log.
    # For now, I will assume the json.loads block IS in search_similar_chunks as it was planned.
    assert f"Failed to parse metadata JSON for chunk_id id_malformed" in caplog.text
    mock_conn_instance.close.assert_awaited_once()

@pytest.mark.skipif(not ASYNC_PG_AVAILABLE, reason="asyncpg not installed.")
@patch('src.vectorizer.vector_store_handler.embedding_generator')
@patch('src.vectorizer.vector_store_handler.load_db_config') # Patch load_db_config where it's used
async def test_search_db_config_missing_error(mock_load_db_config_vsh, mock_embedding_gen, caplog):
    mock_embed_client = MagicMock()
    mock_embed_client.embed_query.return_value = [0.1, 0.2, 0.3]
    mock_embedding_gen.get_embedding_client.return_value = mock_embed_client

    mock_load_db_config_vsh.return_value = {"host": "mockhost", "port": 5432, "database": None, "user": "mockuser", "password": "mockpassword"}

    caplog.set_level(logging.CRITICAL)
    with pytest.raises(ConnectionError) as excinfo:
        await search_similar_chunks("any query")

    assert "Database connection details missing in .env (DB_NAME, DB_USER, DB_PASSWORD) for search." in str(excinfo.value)
    assert "Database connection details missing in .env" in caplog.text
    mock_load_db_config_vsh.assert_called_once()
    mock_embedding_gen.get_embedding_client.assert_called_once()
