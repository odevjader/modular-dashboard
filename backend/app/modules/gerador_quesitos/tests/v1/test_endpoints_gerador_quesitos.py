# backend/app/modules/gerador_quesitos/tests/v1/test_endpoints_gerador_quesitos.py
import pytest
import os
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi import status # HTTPException might not be needed for direct assertion

# Deliberately not importing app-specific modules at the top level
# to ensure conftest.py runs first and sets up the environment.

# Client for testing - Initialize it here so it picks up env vars from conftest.py
# This requires conftest.py to be in a location Pytest can find, typically at the root of the tests directory
# or a higher-level directory that's part of pythonpath.
# For `python -m pytest ...`, if `backend` is the current dir, `app/tests/conftest.py` is fine.
# However, if `backend/app` is added to sys.path by tests, then `backend/conftest.py` or `backend/app/conftest.py` might be better.
# Let's assume `app.tests.conftest` is correctly loaded due to `PYTHONPATH=.` or similar pytest config.

# It's often safer to initialize the client *inside* tests or fixtures that depend on environment variables,
# especially if those env vars are dynamically set by other fixtures (like our autouse session fixture).
# For now, let's try initializing it globally and see if conftest.py's autouse fixture for env vars works as expected.
# If not, we'll move client initialization into a fixture.

# To ensure env vars from conftest are applied before app is imported and settings are instantiated:
# We can define a fixture that provides the client.
@pytest.fixture(scope="module")
def test_app_client(set_test_environment_variables_session_auto, test_db_async_engine_and_tables):
    from app.core import config
    config._settings_instance = None # Crucial: force reload of settings in app.main

    from fastapi.testclient import TestClient
    from app.main import app # Import app after settings are forced to reload
    from app.core.database import get_db as real_get_db, async_session_local as app_async_session_local
    from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

    # Ensure the app's global async_session_local is also rebound to the test engine
    # This is vital if get_db in the actual app code uses a globally defined async_session_local
    # which might have been initialized with a non-test engine before this fixture runs.
    if app_async_session_local is None or app_async_session_local.kw['bind'] != test_db_async_engine_and_tables:
        # print("Rebinding app's global async_session_local to test engine.")
        new_testing_session_local = async_sessionmaker(
            bind=test_db_async_engine_and_tables, # This is the engine from the fixture
            class_=AsyncSession,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False
        )
        # Patch the actual async_session_local used by the app's get_db
        # This requires careful handling if database.py is structured to prevent this.
        # A cleaner way would be for database.py's get_db to always create session from current app.state.engine or similar.
        # For now, let's try overriding the dependency.
        async def override_get_db() -> AsyncSession:
            async with new_testing_session_local() as session:
                yield session
        app.dependency_overrides[real_get_db] = override_get_db

    # print("\nRegistered routes at test_app_client setup (after DB init and get_db override):")
    # for route in app.routes:
    #     if hasattr(route, "path"):
    #         print(f"  Path: {route.path}, Name: {route.name if hasattr(route, 'name') else 'N/A'}")
    #     if hasattr(route, "methods"):
    #          print(f"    Methods: {route.methods}")

    client = TestClient(app)
    yield client

    app.dependency_overrides.pop(real_get_db, None)


# --- Testes para /gerar_com_referencia_documento ---

# Use fixtures from conftest.py by just listing their names as arguments
@patch("app.modules.gerador_quesitos.v1.endpoints.get_db")
@patch("app.modules.gerador_quesitos.v1.endpoints.ChatGoogleGenerativeAI")
@patch("app.modules.gerador_quesitos.v1.endpoints.prompt_template_string", "Conteúdo do PDF: {pdf_content}\nBenefício: {beneficio}\nProfissão: {profissao}")
def test_gq_be_001_gerar_quesitos_com_referencia_sucesso(
    mock_chat_google_gen_ai, mock_get_db,
    mock_db_session_fixture,
    mock_llm_fixture,
    valid_token_header_fixture,
    test_app_client
):
    import os
    from app.models.document import DocumentChunk

    # Configure mock_db_session_fixture for async operations
    # Mock `execute` and the chain `scalars().all()`
    mock_result = MagicMock()

    mock_chunk1 = DocumentChunk(id=1, document_id=123, chunk_text="Texto do chunk 1.", chunk_order=1)
    mock_chunk2 = DocumentChunk(id=2, document_id=123, chunk_text="Texto do chunk 2.", chunk_order=2)
    mock_result.scalars.return_value.all.return_value = [mock_chunk1, mock_chunk2]

    # db.execute should be an AsyncMock if db itself is async, but here get_db provides the session
    # and the session object (mock_db_session_fixture) is what needs to have execute mocked.
    # If get_db itself is async and yields an async session, then the mock setup is fine.
    # Let's assume mock_db_session_fixture is an AsyncMock or MagicMock configured for await.
    if not isinstance(mock_db_session_fixture.execute, AsyncMock): # Ensure execute is awaitable if it's not already an AsyncMock
        mock_db_session_fixture.execute = AsyncMock(return_value=mock_result)
    else:
        mock_db_session_fixture.execute.return_value = mock_result


    mock_get_db.return_value = mock_db_session_fixture # This mock is for the dependency injection
    mock_chat_google_gen_ai.return_value = mock_llm_fixture

    # Use os.environ for values that were set in conftest.py
    payload = {
        "document_id": 123,
        "beneficio": "Auxílio Doença",
        "profissao": "Desenvolvedor",
        "modelo_nome": os.environ.get("GEMINI_MODEL_NAME")
    }
    response = test_app_client.post("/api/gerador_quesitos/v1/gerar_com_referencia_documento", json=payload, headers=valid_token_header_fixture)

    assert response.status_code == 200
    data = response.json()
    assert "quesitos_texto" in data
    assert "Quesito gerado mockado 1." in data["quesitos_texto"]

    expected_combined_text = "Texto do chunk 1.\n\nTexto do chunk 2."
    expected_prompt_content = f"Conteúdo do PDF: {expected_combined_text}\nBenefício: Auxílio Doença\nProfissão: Desenvolvedor"

    mock_llm_fixture.ainvoke.assert_called_once()
    called_messages = mock_llm_fixture.ainvoke.call_args[0][0]
    assert len(called_messages) == 1
    assert called_messages[0].content == expected_prompt_content
    # Ensure ChatGoogleGenerativeAI is called with the API key from the (mocked) environment
    mock_chat_google_gen_ai.assert_called_with(
        model=os.environ.get("GEMINI_MODEL_NAME"),
        google_api_key=os.environ.get("GOOGLE_API_KEY")
    )


@patch("app.modules.gerador_quesitos.v1.endpoints.get_db")
@patch("app.modules.gerador_quesitos.v1.endpoints.ChatGoogleGenerativeAI")
@patch("app.modules.gerador_quesitos.v1.endpoints.prompt_template_string", "Prompt: {pdf_content}, {beneficio}, {profissao}")
def test_gq_be_002_document_id_inexistente(
    mock_chat_google_gen_ai, mock_get_db,
    mock_db_session_fixture,
    valid_token_header_fixture,
    test_app_client
):
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [] # No chunks found
    if not isinstance(mock_db_session_fixture.execute, AsyncMock):
        mock_db_session_fixture.execute = AsyncMock(return_value=mock_result)
    else:
        mock_db_session_fixture.execute.return_value = mock_result

    mock_get_db.return_value = mock_db_session_fixture

    payload = {
        "document_id": 999,
        "beneficio": "Aposentadoria",
        "profissao": "Engenheiro",
        "modelo_nome": "<Modelo Padrão>"
    }
    response = test_app_client.post("/api/gerador_quesitos/v1/gerar_com_referencia_documento", json=payload, headers=valid_token_header_fixture)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    # Detail message might vary slightly depending on how FastAPI handles it,
    # but the core idea is that the document ID is not found.
    # For a more robust check, one might check for key error if detail is not uniform.
    # For now, let's assume the endpoint correctly signals a document not found.
    # The previous "não encontrado ou não possui conteúdo processado" was specific to the endpoint's previous logic.
    # A generic 404 from the routing layer might just be "Not Found".
    # Let's check if the endpoint is reached by seeing if get_db was called.
    # If get_db was called, it means routing worked, and the 404 is from the endpoint logic.
    # If get_db was NOT called, it means routing itself failed (e.g. path truly not found).
    # Based on logs, the path IS registered, so the 404 should be from endpoint logic.
    assert "não encontrado ou não possui conteúdo processado" in response.json().get("detail", "")
    mock_chat_google_gen_ai.return_value.ainvoke.assert_not_called()


@patch("app.modules.gerador_quesitos.v1.endpoints.get_db")
@patch("app.modules.gerador_quesitos.v1.endpoints.ChatGoogleGenerativeAI")
@patch("app.modules.gerador_quesitos.v1.endpoints.prompt_template_string", "Prompt: {pdf_content}, {beneficio}, {profissao}")
def test_gq_be_003_texto_documento_vazio_ou_inadequado(
    mock_chat_google_gen_ai, mock_get_db,
    mock_db_session_fixture,
    mock_llm_fixture,
    valid_token_header_fixture,
    test_app_client
):
    from app.models.document import DocumentChunk # Import locally

    mock_result = MagicMock()
    mock_chunk_empty = DocumentChunk(id=1, document_id=789, chunk_text="", chunk_order=1)
    mock_result.scalars.return_value.all.return_value = [mock_chunk_empty]
    if not isinstance(mock_db_session_fixture.execute, AsyncMock):
        mock_db_session_fixture.execute = AsyncMock(return_value=mock_result)
    else:
        mock_db_session_fixture.execute.return_value = mock_result

    mock_get_db.return_value = mock_db_session_fixture
    mock_chat_google_gen_ai.return_value = mock_llm_fixture

    ai_message_empty_mock = MagicMock()
    ai_message_empty_mock.content = "Não foi possível gerar quesitos com o conteúdo fornecido."
    mock_llm_fixture.ainvoke.return_value = ai_message_empty_mock

    payload = {
        "document_id": 789,
        "beneficio": "Pensão",
        "profissao": "Professor",
        "modelo_nome": "<Modelo Padrão>"
    }
    response = test_app_client.post("/api/gerador_quesitos/v1/gerar_com_referencia_documento", json=payload, headers=valid_token_header_fixture)

    assert response.status_code == 200
    data = response.json()
    assert "Não foi possível gerar quesitos com o conteúdo fornecido." in data["quesitos_texto"]

    mock_llm_fixture.ainvoke.assert_called_once()
    called_messages = mock_llm_fixture.ainvoke.call_args[0][0]
    assert called_messages[0].content == "Prompt: , Pensão, Professor"


def test_gq_be_004_sem_document_id(valid_token_header_fixture, test_app_client):
    payload = {
        "beneficio": "Auxílio Acidente",
        "profissao": "Motorista",
        "modelo_nome": "<Modelo Padrão>"
    }
    response = test_app_client.post("/api/gerador_quesitos/v1/gerar_com_referencia_documento", json=payload, headers=valid_token_header_fixture)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert any("Field required" in err["msg"] or "Input should be a valid integer" in err["msg"] for err in response.json()["detail"])


def test_gq_be_005_sem_tema_beneficio_profissao(valid_token_header_fixture, test_app_client):
    payload_no_beneficio = {
        "document_id": 123,
        "profissao": "Motorista",
        "modelo_nome": "<Modelo Padrão>"
    }
    response = test_app_client.post("/api/gerador_quesitos/v1/gerar_com_referencia_documento", json=payload_no_beneficio, headers=valid_token_header_fixture)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert any("Field required" in err["msg"] for err in response.json()["detail"] if err['loc'][1] == 'beneficio')

    payload_no_profissao = {
        "document_id": 123,
        "beneficio": "Auxílio Acidente",
        "modelo_nome": "<Modelo Padrão>"
    }
    response = test_app_client.post("/api/gerador_quesitos/v1/gerar_com_referencia_documento", json=payload_no_profissao, headers=valid_token_header_fixture)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert any("Field required" in err["msg"] for err in response.json()["detail"] if err['loc'][1] == 'profissao')


@patch("app.modules.gerador_quesitos.v1.endpoints.get_db")
@patch("app.modules.gerador_quesitos.v1.endpoints.ChatGoogleGenerativeAI")
@patch("app.modules.gerador_quesitos.v1.endpoints.prompt_template_string", "Prompt: {pdf_content}, {beneficio}, {profissao}")
def test_gq_be_006_erro_interno_llm(
    mock_chat_google_gen_ai, mock_get_db,
    mock_db_session_fixture,
    mock_llm_fixture,
    valid_token_header_fixture,
    test_app_client
):
    from app.models.document import DocumentChunk # Import locally

    mock_result = MagicMock()
    mock_chunk = DocumentChunk(id=1, document_id=101, chunk_text="Conteúdo válido.", chunk_order=1)
    mock_result.scalars.return_value.all.return_value = [mock_chunk]
    if not isinstance(mock_db_session_fixture.execute, AsyncMock):
        mock_db_session_fixture.execute = AsyncMock(return_value=mock_result)
    else:
        mock_db_session_fixture.execute.return_value = mock_result

    mock_get_db.return_value = mock_db_session_fixture
    mock_chat_google_gen_ai.return_value = mock_llm_fixture
    mock_llm_fixture.ainvoke.side_effect = Exception("LLM Service Unavailable")

    payload = {
        "document_id": 101,
        "beneficio": "Salário Maternidade",
        "profissao": "Autônoma",
        "modelo_nome": "<Modelo Padrão>"
    }
    response = test_app_client.post("/api/gerador_quesitos/v1/gerar_com_referencia_documento", json=payload, headers=valid_token_header_fixture)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Erro ao contatar o serviço de IA: LLM Service Unavailable" in response.json()["detail"]


@patch("app.modules.gerador_quesitos.v1.endpoints.get_db")
@patch("app.modules.gerador_quesitos.v1.endpoints.ChatGoogleGenerativeAI")
@patch("app.modules.gerador_quesitos.v1.endpoints.default_llm", None)
@patch("app.modules.gerador_quesitos.v1.endpoints.settings") # Patch settings object in endpoints module
@patch("app.modules.gerador_quesitos.v1.endpoints.prompt_template_string", "Prompt: {pdf_content}, {beneficio}, {profissao}")
def test_gq_be_llm_nao_configurado_sem_api_key(
    mock_settings, # Add mock_settings from the new patch
    mock_chat_google_gen_ai_class, mock_get_db,
    mock_db_session_fixture,
    valid_token_header_fixture,
    test_app_client
):
    from app.models.document import DocumentChunk # Import locally
    # Configure the settings mock to simulate GOOGLE_API_KEY being None
    mock_settings.GOOGLE_API_KEY = None

    mock_result = MagicMock()
    mock_chunk = DocumentChunk(id=1, document_id=202, chunk_text="Algum texto.", chunk_order=1)
    mock_result.scalars.return_value.all.return_value = [mock_chunk]
    if not isinstance(mock_db_session_fixture.execute, AsyncMock):
        mock_db_session_fixture.execute = AsyncMock(return_value=mock_result)
    else:
        mock_db_session_fixture.execute.return_value = mock_result

    mock_get_db.return_value = mock_db_session_fixture

    payload_default_model = {
        "document_id": 202,
        "beneficio": "BPC",
        "profissao": "Estudante",
        "modelo_nome": "<Modelo Padrão>"
    }
    response_default = test_app_client.post("/api/gerador_quesitos/v1/gerar_com_referencia_documento", json=payload_default_model, headers=valid_token_header_fixture)
    assert response_default.status_code == 200
    assert "Placeholder: LLM indisponível" in response_default.json()["quesitos_texto"]
    mock_chat_google_gen_ai_class.assert_not_called()

    payload_specific_model = {
        "document_id": 202,
        "beneficio": "BPC",
        "profissao": "Estudante",
        "modelo_nome": "gemini-pro"
    }
    response_specific = test_app_client.post("/api/gerador_quesitos/v1/gerar_com_referencia_documento", json=payload_specific_model, headers=valid_token_header_fixture)
    assert response_specific.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert "chave API ausente" in response_specific.json()["detail"]
    mock_chat_google_gen_ai_class.assert_not_called()


@patch("app.modules.gerador_quesitos.v1.endpoints.get_db")
@patch("app.modules.gerador_quesitos.v1.endpoints.ChatGoogleGenerativeAI")
@patch("app.modules.gerador_quesitos.v1.endpoints.prompt_template_string", "")
def test_gq_be_prompt_template_nao_carregado(
    mock_chat_google_gen_ai, mock_get_db,
    mock_db_session_fixture,
    valid_token_header_fixture,
    test_app_client
):
    mock_get_db.return_value = mock_db_session_fixture

    payload = {
        "document_id": 303,
        "beneficio": "LOAS",
        "profissao": "Doméstica",
        "modelo_nome": "<Modelo Padrão>"
    }
    response = test_app_client.post("/api/gerador_quesitos/v1/gerar_com_referencia_documento", json=payload, headers=valid_token_header_fixture)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Template de prompt não disponível" in response.json()["detail"]
    mock_chat_google_gen_ai.return_value.ainvoke.assert_not_called()


def test_gerar_quesitos_endpoint_desativado(valid_token_header_fixture, test_app_client):
    from io import BytesIO
    file_content = b"dummy pdf content"
    file_obj = BytesIO(file_content)
    file_obj.name = "test.pdf"

    response = test_app_client.post(
        "/api/gerador_quesitos/v1/gerar", # Corrected path based on logged routes
        files={"files": ("test.pdf", file_obj, "application/pdf")},
        data={
            "beneficio": "Teste Beneficio",
            "profissao": "Teste Profissao",
            "modelo_nome": "<Modelo Padrão>"
        },
        headers=valid_token_header_fixture
    )

    assert response.status_code == 200
    data = response.json()
    assert "quesitos_texto" in data
    assert "Funcionalidade de geração de quesitos via IA desativada temporariamente." in data["quesitos_texto"]
