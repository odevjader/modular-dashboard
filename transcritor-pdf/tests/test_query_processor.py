# -*- coding: utf-8 -*-
"""Unit tests for the Query Processor module.

Tests the `get_llm_answer_with_context` function's orchestration logic,
including interaction with mocked vector search and LLM client.
"""
import pytest
import asyncio
import logging # For caplog
from unittest.mock import patch, MagicMock, AsyncMock

# Import the function to be tested
from src.query_processor import get_llm_answer_with_context, DEFAULT_TOP_K_CONTEXT_CHUNKS

# Import types for mocking and assertion clarity
from langchain_core.messages import SystemMessage, HumanMessage

# For asserting specific custom exceptions if any, or standard ones
# from src.custom_exceptions import SomeCustomException # Example
# Standard ConnectionError is used by the SUT based on previous tasks.

pytestmark = pytest.mark.asyncio

# --- Test Case TC_QP_001: Successful Query with Context Found ---
@patch('src.query_processor.vector_store_handler.search_similar_chunks', new_callable=AsyncMock)
@patch('src.query_processor.llm_client.get_llm_client')
async def test_successful_query_with_context(mock_get_llm_client, mock_search_chunks, caplog):
    caplog.set_level(logging.INFO)

    # 1. Configure Mocks
    mock_retrieved_chunk_data = {'chunk_id': 'c1', 'text_content': 'X is a variable.', 'metadata': {'file': 'test.pdf'}, 'similarity_score': 0.9}
    mock_search_chunks.return_value = [mock_retrieved_chunk_data]

    mock_llm_instance = MagicMock()
    mock_llm_response_content = "X is indeed a variable according to the context."
    mock_llm_instance.invoke.return_value = MagicMock(content=mock_llm_response_content)
    mock_get_llm_client.return_value = mock_llm_instance

    # 2. Call the function
    user_query = "What is X?"
    top_k = 1
    result = await get_llm_answer_with_context(user_query, top_k_context_chunks=top_k)

    # 3. Assertions
    mock_search_chunks.assert_called_once_with(
        query_text=user_query,
        top_k=top_k,
        document_filename=None
    )

    mock_get_llm_client.assert_called_once()
    mock_llm_instance.invoke.assert_called_once()

    # Assert prompt construction (inspecting messages passed to invoke)
    called_messages = mock_llm_instance.invoke.call_args[0][0]
    assert len(called_messages) == 2
    assert isinstance(called_messages[0], SystemMessage)
    assert "Você é um assistente de IA prestativo" in called_messages[0].content
    assert isinstance(called_messages[1], HumanMessage)
    assert "Contexto Fornecido:" in called_messages[1].content
    assert mock_retrieved_chunk_data['text_content'] in called_messages[1].content
    assert user_query in called_messages[1].content

    assert result == {
        "answer": mock_llm_response_content,
        "retrieved_context": [mock_retrieved_chunk_data],
        "error": None
    }
    assert "Nenhum chunk de contexto encontrado" not in caplog.text
    assert "Resposta recebida do LLM." in caplog.text

# --- Test Case TC_QP_002: Query with No Context Found ---
@patch('src.query_processor.vector_store_handler.search_similar_chunks', new_callable=AsyncMock)
@patch('src.query_processor.llm_client.get_llm_client')
async def test_query_no_context_found(mock_get_llm_client, mock_search_chunks, caplog):
    caplog.set_level(logging.INFO)

    mock_search_chunks.return_value = [] # No context found

    mock_llm_instance = MagicMock()
    mock_llm_response_content = "Com base nas informações fornecidas, não posso responder à pergunta sobre Y."
    mock_llm_instance.invoke.return_value = MagicMock(content=mock_llm_response_content)
    mock_get_llm_client.return_value = mock_llm_instance

    user_query = "What is Y?"
    result = await get_llm_answer_with_context(user_query)

    mock_search_chunks.assert_called_once_with(
        query_text=user_query,
        top_k=DEFAULT_TOP_K_CONTEXT_CHUNKS, # Using default
        document_filename=None
    )

    called_messages = mock_llm_instance.invoke.call_args[0][0]
    assert "Nenhum contexto fornecido." in called_messages[1].content # Check that prompt reflects no context

    assert result == {
        "answer": mock_llm_response_content,
        "retrieved_context": [],
        "error": None
    }
    assert f"Nenhum chunk de contexto encontrado para a query: '{user_query[:100]}...'" in caplog.text

# --- Test Case TC_QP_003: Error during Context Retrieval ---
@patch('src.query_processor.vector_store_handler.search_similar_chunks', new_callable=AsyncMock)
@patch('src.query_processor.llm_client.get_llm_client')
async def test_error_during_context_retrieval(mock_get_llm_client, mock_search_chunks, caplog):
    caplog.set_level(logging.ERROR)

    db_error_message = "Simulated DB error"
    mock_search_chunks.side_effect = ConnectionError(db_error_message)

    mock_llm_instance = MagicMock() # To ensure get_llm_client is not the cause of error
    mock_get_llm_client.return_value = mock_llm_instance

    user_query = "DB error test"
    result = await get_llm_answer_with_context(user_query)

    mock_get_llm_client.assert_not_called() # Should not be called if context retrieval fails
    mock_llm_instance.invoke.assert_not_called()

    assert result == {
        "answer": "Erro ao buscar contexto no banco de dados. Por favor, tente novamente mais tarde.",
        "retrieved_context": [],
        "error": f"Erro de conexão com o banco de dados ao buscar contexto: {db_error_message}"
    }
    assert f"Erro de conexão ao buscar chunks de contexto: {db_error_message}" in caplog.text

# --- Test Case TC_QP_004: Error during LLM Call ---
@patch('src.query_processor.vector_store_handler.search_similar_chunks', new_callable=AsyncMock)
@patch('src.query_processor.llm_client.get_llm_client')
async def test_error_during_llm_call(mock_get_llm_client, mock_search_chunks, caplog):
    caplog.set_level(logging.ERROR)

    mock_retrieved_chunk_data = [{'text_content': 'Some context'}]
    mock_search_chunks.return_value = mock_retrieved_chunk_data

    mock_llm_instance = MagicMock()
    llm_api_error_message = "Simulated LLM API error"
    mock_llm_instance.invoke.side_effect = Exception(llm_api_error_message)
    mock_get_llm_client.return_value = mock_llm_instance

    user_query = "LLM error test"
    result = await get_llm_answer_with_context(user_query)

    assert result == {
        "answer": "Ocorreu um erro inesperado ao processar sua pergunta. Por favor, tente novamente mais tarde.",
        "retrieved_context": mock_retrieved_chunk_data,
        "error": f"Erro inesperado: {llm_api_error_message}"
    }
    assert f"Erro inesperado durante o processamento da query: {llm_api_error_message}" in caplog.text

# --- Test Case TC_QP_005: Error during LLM Client Initialization ---
@patch('src.query_processor.vector_store_handler.search_similar_chunks', new_callable=AsyncMock)
@patch('src.query_processor.llm_client.get_llm_client')
async def test_error_llm_client_initialization(mock_get_llm_client, mock_search_chunks, caplog):
    caplog.set_level(logging.ERROR)

    mock_retrieved_chunk_data = [{'text_content': 'Context for LLM init error'}]
    mock_search_chunks.return_value = mock_retrieved_chunk_data

    llm_init_error_message = "Missing API Key"
    # Assuming get_llm_client itself (or load_api_config within it) raises ValueError for this
    mock_get_llm_client.side_effect = ValueError(llm_init_error_message)

    user_query = "LLM init error"
    result = await get_llm_answer_with_context(user_query)

    # Check that the error message from the SUT matches the expected format
    # The SUT catches `llm_client.ValueError` which is `ValueError` from `llm_client.py`
    # If `llm_client.ValueError` is not specifically defined and imported, it's standard ValueError.
    assert result == {
        "answer": "Erro na configuração do serviço de linguagem. Verifique as credenciais.",
        "retrieved_context": mock_retrieved_chunk_data, # Context was retrieved before LLM client init attempt
        "error": f"Erro de configuração do LLM: {llm_init_error_message}"
    }
    assert f"Erro de configuração do cliente LLM: {llm_init_error_message}" in caplog.text

# --- Test Case TC_QP_006: LLM Response Malformed ---
@patch('src.query_processor.vector_store_handler.search_similar_chunks', new_callable=AsyncMock)
@patch('src.query_processor.llm_client.get_llm_client')
async def test_llm_response_malformed(mock_get_llm_client, mock_search_chunks, caplog):
    caplog.set_level(logging.ERROR)

    mock_retrieved_chunk_data = [{'text_content': 'Context for malformed response'}]
    mock_search_chunks.return_value = mock_retrieved_chunk_data

    mock_llm_instance = MagicMock()
    # Simulate LLM response without 'content' attribute
    malformed_response = MagicMock()
    del malformed_response.content # Ensure 'content' attribute is missing
    mock_llm_instance.invoke.return_value = malformed_response
    mock_get_llm_client.return_value = mock_llm_instance

    user_query = "Malformed LLM response"
    result = await get_llm_answer_with_context(user_query)

    assert result == {
        "answer": "Formato de resposta inesperado do LLM.",
        "retrieved_context": mock_retrieved_chunk_data,
        "error": "Formato de resposta inesperado do LLM."
    }
    assert "Resposta do LLM não possui atributo 'content'." in caplog.text

# --- Test Case TC_QP_007: Context Chunks with Empty `text_content` ---
@patch('src.query_processor.vector_store_handler.search_similar_chunks', new_callable=AsyncMock)
@patch('src.query_processor.llm_client.get_llm_client')
async def test_context_chunks_with_empty_text_content(mock_get_llm_client, mock_search_chunks, caplog):
    caplog.set_level(logging.INFO)

    mock_chunks_with_empty = [
        {'text_content': '', 'chunk_id': 'c_empty1', 'metadata': {}, 'similarity_score': 0.95},
        {'text_content': None, 'chunk_id': 'c_none', 'metadata': {}, 'similarity_score': 0.92}, # None should be handled by .get('text_content', '')
        {'text_content': 'Valid context here.', 'chunk_id': 'c_valid', 'metadata': {}, 'similarity_score': 0.9}
    ]
    mock_search_chunks.return_value = mock_chunks_with_empty

    mock_llm_instance = MagicMock()
    mock_llm_response_content = "Answer based on valid context."
    mock_llm_instance.invoke.return_value = MagicMock(content=mock_llm_response_content)
    mock_get_llm_client.return_value = mock_llm_instance

    user_query = "Empty context content test"
    result = await get_llm_answer_with_context(user_query)

    # Assert that the context string passed to LLM only contains 'Valid context here.'
    called_messages = mock_llm_instance.invoke.call_args[0][0]
    human_message_content = called_messages[1].content

    # Expected context string in prompt: "Valid context here."
    # (The joiner "\n\n---\n\n" will not be present if only one valid item)
    assert "Valid context here." in human_message_content
    assert "''" not in human_message_content # Check that empty string from first chunk is not directly in context
    assert "None" not in human_message_content # Check that None from second chunk is not directly in context
    # Check if it correctly states "Nenhum contexto fornecido." if *all* are empty/None.
    # This specific test has one valid context.

    assert result == {
        "answer": mock_llm_response_content,
        "retrieved_context": mock_chunks_with_empty,
        "error": None
    }
    # Check for logs related to empty context string processing
    assert "Context string is empty even after retrieving chunks" not in caplog.text # Because one is valid
    # No specific log for individual empty chunks, but the context_string formatting handles it.
    # The "Nenhum conteúdo de contexto para enviar ao LLM." log appears if context_string is ultimately empty.
    # If all chunks were empty:
    # assert "Nenhum conteúdo de contexto para enviar ao LLM." in caplog.text
    # assert "Nenhum contexto fornecido." in human_message_content

    # Test case where ALL chunks are empty
    mock_search_chunks.return_value = [{'text_content': ''}, {'text_content': None}]
    caplog.clear()
    await get_llm_answer_with_context("all empty context")
    all_empty_called_messages = mock_llm_instance.invoke.call_args[0][0]
    all_empty_human_content = all_empty_called_messages[1].content
    assert "Nenhum contexto fornecido." in all_empty_human_content
    assert "Context string is empty even after retrieving chunks" in caplog.text # if retrieved_chunks is not empty
    assert "Nenhum conteúdo de contexto para enviar ao LLM." in caplog.text # if context_string is empty
