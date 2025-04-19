# backend/tests/test_gerador_quesitos.py
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock # Import AsyncMock for async methods
import sys
from pathlib import Path
import pytest
from io import BytesIO

# Add application root directory to path
app_root_dir = str(Path(__file__).parent.parent / "app")
if app_root_dir not in sys.path:
    sys.path.insert(0, app_root_dir)

# Import app and settings
from main import app
from core.config import settings
# Import the response schema using Portuguese name
from modules.gerador_quesitos.v1.esquemas import RespostaQuesitos

# Create Test Client
client = TestClient(app)

# Define targets for mocking
LLM_MOCK_TARGET = "modules.gerador_quesitos.v1.endpoints.llm"
# Target the DoclingLoader class within the endpoints module where it's imported/used
LOADER_MOCK_TARGET = "modules.gerador_quesitos.v1.endpoints.DoclingLoader"
# Target tempfile.NamedTemporaryFile if needed, or mock os.remove
TEMPFILE_MOCK_TARGET = "modules.gerador_quesitos.v1.endpoints.tempfile.NamedTemporaryFile"
OS_REMOVE_MOCK_TARGET = "modules.gerador_quesitos.v1.endpoints.os.remove"
OS_PATH_EXISTS_MOCK_TARGET = "modules.gerador_quesitos.v1.endpoints.os.path.exists"


# Helper function to create mock AI message
def create_mock_ai_message(content: str):
    mock_msg = MagicMock()
    mock_msg.content = content
    return mock_msg

# Helper function to create mock Langchain Document
def create_mock_langchain_doc(page_content: str):
    mock_doc = MagicMock()
    mock_doc.page_content = page_content
    return mock_doc

# --- Test Cases ---

# Use patch decorators in the correct order (bottom up)
@patch(OS_PATH_EXISTS_MOCK_TARGET, return_value=False) # Assume temp file doesn't exist after for cleanup check
@patch(OS_REMOVE_MOCK_TARGET) # Mock os.remove to avoid errors on temp file cleanup
@patch(TEMPFILE_MOCK_TARGET) # Mock NamedTemporaryFile
@patch(LOADER_MOCK_TARGET) # Mock DoclingLoader class
@patch(LLM_MOCK_TARGET) # Mock llm object
def test_gerar_quesitos_success(mock_llm, mock_DoclingLoader, mock_NamedTemporaryFile, mock_os_remove, mock_os_path_exists):
    """ Test successful quesitos generation with mocked AI and Loader. """

    # --- Mock Setup ---
    # Mock LLM
    if mock_llm is None:
        pytest.skip("Skipping test: LLM mock target None (check API key?)")
        return
    mock_response_content = "1. Quesito Mock A?\n2. Quesito Mock B?"
    # Use AsyncMock for await llm.ainvoke
    mock_llm.ainvoke = AsyncMock(return_value=create_mock_ai_message(mock_response_content))

    # Mock DoclingLoader instance and its load/aload method
    mock_loader_instance = MagicMock()
    # Assuming DoclingLoader has an async 'aload' method, mock it
    mock_loader_instance.aload = AsyncMock(return_value=[
        create_mock_langchain_doc("Texto extraído do PDF mockado.")
    ])
    # Configure the DoclingLoader class mock to return our instance mock
    mock_DoclingLoader.return_value = mock_loader_instance

    # Mock tempfile context manager
    mock_temp_file = MagicMock()
    mock_temp_file.__enter__.return_value.name = "/tmp/fake_pdf_path.pdf" # Provide a fake path
    mock_temp_file.__enter__.return_value.write.return_value = None # Mock write method
    mock_NamedTemporaryFile.return_value = mock_temp_file

    # --- Request ---
    url = f"{settings.API_PREFIX}/gerador_quesitos/v1/gerar"
    dummy_pdf_content = b"%PDF..."
    files = {'file': ('test.pdf', BytesIO(dummy_pdf_content), 'application/pdf')}

    response = client.post(url, files=files) # No 'data' needed as inputs are removed for V1

    # --- Assertions ---
    assert response.status_code == 200
    response_data = RespostaQuesitos(**response.json())
    assert response_data.quesitos_texto == mock_response_content

    # Verify mocks were called (optional but good)
    mock_NamedTemporaryFile.assert_called_once() # Check temp file was used
    mock_DoclingLoader.assert_called_once_with(file_path="/tmp/fake_pdf_path.pdf")
    mock_loader_instance.aload.assert_called_once()
    mock_llm.ainvoke.assert_called_once() # Check LLM was called
    # mock_os_remove.assert_called_once_with("/tmp/fake_pdf_path.pdf") # Check cleanup


@patch(LLM_MOCK_TARGET, None) # Simulate LLM not being initialized
def test_gerar_quesitos_no_llm():
    """ Test endpoint when LLM is not available. """
    url = f"{settings.API_PREFIX}/gerador_quesitos/v1/gerar"
    files = {'file': ('test.pdf', BytesIO(b'pdf'), 'application/pdf')}
    response = client.post(url, files=files)
    assert response.status_code == 503

@patch(OS_PATH_EXISTS_MOCK_TARGET, return_value=False)
@patch(OS_REMOVE_MOCK_TARGET)
@patch(TEMPFILE_MOCK_TARGET)
@patch(LOADER_MOCK_TARGET)
@patch(LLM_MOCK_TARGET)
def test_gerar_quesitos_llm_error(mock_llm, mock_DoclingLoader, mock_NamedTemporaryFile, mock_os_remove, mock_os_path_exists):
    """ Test endpoint when the LLM call raises an exception. """
    if mock_llm is None:
        pytest.skip("Skipping test: LLM mock target None")
        return

    # Mock Loader to return some data
    mock_loader_instance = MagicMock()
    mock_loader_instance.aload = AsyncMock(return_value=[create_mock_langchain_doc("Text")])
    mock_DoclingLoader.return_value = mock_loader_instance
    # Mock temp file
    mock_temp_file = MagicMock()
    mock_temp_file.__enter__.return_value.name = "/tmp/fake_pdf_path.pdf"
    mock_NamedTemporaryFile.return_value = mock_temp_file

    # Configure mock LLM to raise error
    mock_llm.ainvoke = AsyncMock(side_effect=Exception("Simulated Google API Error"))

    url = f"{settings.API_PREFIX}/gerador_quesitos/v1/gerar"
    files = {'file': ('test.pdf', BytesIO(b'pdf'), 'application/pdf')}
    response = client.post(url, files=files)
    assert response.status_code == 500
    assert "Erro ao processar documento" in response.json().get("detail", "")

def test_gerar_quesitos_invalid_file_type():
    """ Test sending a non-PDF file. """
    url = f"{settings.API_PREFIX}/gerador_quesitos/v1/gerar"
    files = {'file': ('test.txt', BytesIO(b'text content'), 'text/plain')}
    response = client.post(url, files=files)
    assert response.status_code == 400
    assert "Tipo de arquivo inválido" in response.json().get("detail", "")

@patch(OS_PATH_EXISTS_MOCK_TARGET, return_value=False)
@patch(OS_REMOVE_MOCK_TARGET)
@patch(TEMPFILE_MOCK_TARGET)
@patch(LOADER_MOCK_TARGET) # Mock DoclingLoader only
@patch(LLM_MOCK_TARGET) # Mock LLM just to prevent None error if key exists
def test_gerar_quesitos_loader_error(mock_llm, mock_DoclingLoader, mock_NamedTemporaryFile, mock_os_remove, mock_os_path_exists):
    """ Test endpoint when the DoclingLoader call raises an exception. """

    # Mock temp file
    mock_temp_file = MagicMock()
    mock_temp_file.__enter__.return_value.name = "/tmp/fake_pdf_path.pdf"
    mock_NamedTemporaryFile.return_value = mock_temp_file

    # Configure mock Loader to raise error
    mock_loader_instance = MagicMock()
    mock_loader_instance.aload = AsyncMock(side_effect=Exception("Simulated Loader Error"))
    mock_DoclingLoader.return_value = mock_loader_instance

    url = f"{settings.API_PREFIX}/gerador_quesitos/v1/gerar"
    files = {'file': ('test.pdf', BytesIO(b'pdf'), 'application/pdf')}
    response = client.post(url, files=files)
    assert response.status_code == 500 # Should be caught by general exception handler
    assert "Erro ao processar documento" in response.json().get("detail", "") # Check if detail includes loader error