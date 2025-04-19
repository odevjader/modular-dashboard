# backend/tests/test_gerador_quesitos.py
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
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
from modules.gerador_quesitos.v1.esquemas import RespostaQuesitos

# Create Test Client
client = TestClient(app)

# Define mock targets
DEFAULT_LLM_MOCK_TARGET = "modules.gerador_quesitos.v1.endpoints.default_llm"
PROCESSOR_MOCK_TARGET = "modules.gerador_quesitos.v1.endpoints.processar_pdfs_upload"
PROMPT_LOAD_TARGET = "modules.gerador_quesitos.v1.endpoints.prompt_template_string"
DYNAMIC_LLM_INIT_TARGET = "modules.gerador_quesitos.v1.endpoints.ChatGoogleGenerativeAI"

# Helper function to create mock AI message
def create_mock_ai_message(content: str):
    mock_msg = MagicMock()
    mock_msg.content = content
    return mock_msg

# --- Test Cases ---

@patch(PROMPT_LOAD_TARGET, "Prompt: {pdf_content}, Ben: {beneficio}, Prof: {profissao}")
@patch(PROCESSOR_MOCK_TARGET)
@patch(DEFAULT_LLM_MOCK_TARGET)
def test_gerar_quesitos_success_default_model(mock_llm, mock_processar_pdfs):
    """ Test successful generation using the default model setting. """
    if mock_llm is None: pytest.skip("Skipping test: Default LLM mock target None"); return
    mock_extracted_text = "Texto extraído mockado."
    mock_processar_pdfs.return_value = mock_extracted_text
    mock_response_content = "1. Quesito Gerado A?"
    mock_llm.ainvoke = AsyncMock(return_value=create_mock_ai_message(mock_response_content))
    url = f"{settings.API_PREFIX}/gerador_quesitos/v1/gerar"
    form_data = {"beneficio": "Auxílio-Doença", "profissao": "Pedreiro", "modelo_nome": "<Modelo Padrão>"}
    files = {'files': ('test.pdf', BytesIO(b'pdf'), 'application/pdf')}
    response = client.post(url, files=files, data=form_data)
    assert response.status_code == 200
    response_data = RespostaQuesitos(**response.json())
    assert response_data.quesitos_texto == mock_response_content
    mock_processar_pdfs.assert_called_once()
    mock_llm.ainvoke.assert_called_once()

@patch(PROMPT_LOAD_TARGET, "Prompt: {pdf_content}, Ben: {beneficio}, Prof: {profissao}")
@patch(DYNAMIC_LLM_INIT_TARGET)
@patch(PROCESSOR_MOCK_TARGET)
@patch(DEFAULT_LLM_MOCK_TARGET)
def test_gerar_quesitos_success_specific_model(mock_default_llm, mock_processar_pdfs, mock_dynamic_llm_init):
    """ Test successful generation requesting a specific model. """
    mock_extracted_text = "Texto extraído mockado."
    mock_processar_pdfs.return_value = mock_extracted_text
    mock_response_content = "1. Quesito Gerado B?"
    mock_dynamic_instance = MagicMock()
    mock_dynamic_instance.ainvoke = AsyncMock(return_value=create_mock_ai_message(mock_response_content))
    mock_dynamic_llm_init.return_value = mock_dynamic_instance
    url = f"{settings.API_PREFIX}/gerador_quesitos/v1/gerar"
    specific_model = "gemini-1.5-pro-latest"
    form_data = {"beneficio": "BPC-LOAS", "profissao": "Do Lar", "modelo_nome": specific_model}
    files = {'files': ('test2.pdf', BytesIO(b'pdf2'), 'application/pdf')}
    response = client.post(url, files=files, data=form_data)
    assert response.status_code == 200
    response_data = RespostaQuesitos(**response.json())
    assert response_data.quesitos_texto == mock_response_content
    mock_processar_pdfs.assert_called_once()
    mock_dynamic_llm_init.assert_called_once_with(model=specific_model, google_api_key=settings.GOOGLE_API_KEY)
    mock_dynamic_instance.ainvoke.assert_called_once()
    if mock_default_llm: mock_default_llm.ainvoke.assert_not_called()

@patch(DEFAULT_LLM_MOCK_TARGET, None)
# REMOVED mock_default_llm_is_none argument
def test_gerar_quesitos_no_default_llm():
    """ Test endpoint when default LLM is not available and default model is requested. """
    url = f"{settings.API_PREFIX}/gerador_quesitos/v1/gerar"
    form_data = {"beneficio": "BPC", "profissao": "Do Lar", "modelo_nome": "<Modelo Padrão>"}
    files = {'files': ('test.pdf', BytesIO(b'pdf'), 'application/pdf')}
    response = client.post(url, files=files, data=form_data)
    assert response.status_code == 503

@patch(PROMPT_LOAD_TARGET, "Prompt: {pdf_content}, Ben: {beneficio}, Prof: {profissao}")
@patch(PROCESSOR_MOCK_TARGET)
@patch(DEFAULT_LLM_MOCK_TARGET)
def test_gerar_quesitos_llm_error(mock_llm, mock_processar_pdfs):
    """ Test endpoint when the default LLM call raises an exception. """
    if mock_llm is None: pytest.skip("Skipping test: Default LLM mock target None"); return
    mock_processar_pdfs.return_value = "Texto extraído."
    mock_llm.ainvoke = AsyncMock(side_effect=Exception("Simulated Google API Error"))
    url = f"{settings.API_PREFIX}/gerador_quesitos/v1/gerar"
    form_data = {"beneficio": "BPC", "profissao": "Do Lar", "modelo_nome": "<Modelo Padrão>"}
    files = {'files': ('test.pdf', BytesIO(b'pdf'), 'application/pdf')}
    response = client.post(url, files=files, data=form_data)
    assert response.status_code == 500
    assert "Erro inesperado" in response.json().get("detail", "")

@patch(PROMPT_LOAD_TARGET, "Prompt: {pdf_content}, Ben: {beneficio}, Prof: {profissao}")
@patch(PROCESSOR_MOCK_TARGET)
@patch(DEFAULT_LLM_MOCK_TARGET)
def test_gerar_quesitos_processor_error(mock_llm, mock_processar_pdfs):
    """ Test endpoint when the PDF processor utility raises an exception. """
    mock_processar_pdfs.side_effect = Exception("Simulated PDF Processing Error")
    url = f"{settings.API_PREFIX}/gerador_quesitos/v1/gerar"
    form_data = {"beneficio": "BPC", "profissao": "Do Lar", "modelo_nome": "<Modelo Padrão>"}
    files = {'files': ('test.pdf', BytesIO(b'pdf'), 'application/pdf')}
    response = client.post(url, files=files, data=form_data)
    assert response.status_code == 500
    assert "Erro inesperado" in response.json().get("detail", "")

@patch(PROMPT_LOAD_TARGET, "Prompt: {pdf_content}, Ben: {beneficio}, Prof: {profissao}")
@patch(PROCESSOR_MOCK_TARGET)
@patch(DEFAULT_LLM_MOCK_TARGET)
def test_gerar_quesitos_processor_returns_empty(mock_llm, mock_processar_pdfs):
    """ Test endpoint when the PDF processor returns empty text. """
    mock_processar_pdfs.return_value = ""
    url = f"{settings.API_PREFIX}/gerador_quesitos/v1/gerar"
    form_data = {"beneficio": "BPC", "profissao": "Do Lar", "modelo_nome": "<Modelo Padrão>"}
    files = {'files': ('test.pdf', BytesIO(b'pdf'), 'application/pdf')}
    response = client.post(url, files=files, data=form_data)
    assert response.status_code == 422
    assert "Não foi possível extrair conteúdo" in response.json().get("detail", "")

def test_gerar_quesitos_no_files():
    """ Test sending request with no files attached. """
    url = f"{settings.API_PREFIX}/gerador_quesitos/v1/gerar"
    form_data = {"beneficio": "BPC", "profissao": "Do Lar", "modelo_nome": "<Modelo Padrão>"}
    response = client.post(url, data=form_data)
    assert response.status_code == 422

def test_gerar_quesitos_missing_form_data():
    """ Test sending request with missing form data. """
    url = f"{settings.API_PREFIX}/gerador_quesitos/v1/gerar"
    files = {'files': ('test.pdf', BytesIO(b'pdf'), 'application/pdf')}
    # Missing beneficio, profissao, but including model_nome
    response = client.post(url, files=files, data={"modelo_nome": "<Modelo Padrão>"})
    assert response.status_code == 422