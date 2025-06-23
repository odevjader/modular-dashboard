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
# PROCESSOR_MOCK_TARGET foi removido pois a função processar_pdfs_upload foi removida.
# Os testes que o utilizavam foram atualizados ou serão removidos se a funcionalidade
# de upload direto para este endpoint for completamente descontinuada em favor do transcritor_pdf.
PROMPT_LOAD_TARGET = "modules.gerador_quesitos.v1.endpoints.prompt_template_string"
DYNAMIC_LLM_INIT_TARGET = "modules.gerador_quesitos.v1.endpoints.ChatGoogleGenerativeAI"

# Mock para a nova forma de obter texto do documento (via DB)
DB_EXECUTE_MOCK_TARGET = "sqlalchemy.ext.asyncio.engine.AsyncConnection.execute"


# Helper function to create mock AI message
def create_mock_ai_message(content: str):
    mock_msg = MagicMock()
    mock_msg.content = content
    return mock_msg

# --- Test Cases ---

# Os testes para o endpoint /gerar que dependiam de processar_pdfs_upload
# foram removidos ou comentados, pois essa funcionalidade foi desativada no endpoint.
# O endpoint /gerar agora retorna uma resposta placeholder.
# Novos testes devem focar no endpoint /gerar_com_referencia_documento.

def test_gerar_quesitos_endpoint_placeholder_response():
    """
    Testa se o endpoint /gerar (que fazia upload direto) agora retorna
    a resposta placeholder indicando que a funcionalidade está desativada.
    """
    url = f"{settings.API_PREFIX}/gerador_quesitos/v1/gerar"
    form_data = {"beneficio": "Auxílio-Doença", "profissao": "Pedreiro", "modelo_nome": "<Modelo Padrão>"}
    files = {'files': ('test.pdf', BytesIO(b'pdf'), 'application/pdf')}
    response = client.post(url, files=files, data=form_data)
    assert response.status_code == 200
    response_data = RespostaQuesitos(**response.json())
    assert "Funcionalidade de geração de quesitos via IA desativada temporariamente." in response_data.quesitos_texto

# Testes para o endpoint /gerar_com_referencia_documento
@patch(PROMPT_LOAD_TARGET, "Prompt: {pdf_content}, Ben: {beneficio}, Prof: {profissao}")
@patch(DB_EXECUTE_MOCK_TARGET) # Mocka a execução da query no banco
@patch(DEFAULT_LLM_MOCK_TARGET) # Mocka o LLM padrão
def test_gerar_quesitos_com_referencia_success_default_model(mock_default_llm, mock_db_execute):
    """
    Testa a geração bem-sucedida usando o endpoint /gerar_com_referencia_documento
    com o modelo de LLM padrão.
    """
    if mock_default_llm is None:
        pytest.skip("Skipping test: Default LLM mock target None")
        return

    # Configura o mock do resultado da query do banco
    mock_cursor_result = MagicMock()
    mock_cursor_result.fetchall.return_value = [("Texto do chunk 1.",), ("Texto do chunk 2.",)]
    mock_db_execute.return_value = mock_cursor_result

    mock_response_content = "1. Quesito Gerado Referenciado A?"
    mock_default_llm.ainvoke = AsyncMock(return_value=create_mock_ai_message(mock_response_content))

    url = f"{settings.API_PREFIX}/gerador_quesitos/v1/gerar_com_referencia_documento"
    payload = {
        "document_filename": "documento_teste.pdf",
        "beneficio": "Auxílio-Doença",
        "profissao": "Pedreiro",
        "modelo_nome": "<Modelo Padrão>"
    }
    response = client.post(url, json=payload)

    assert response.status_code == 200
    response_data = RespostaQuesitos(**response.json())
    assert response_data.quesitos_texto == mock_response_content
    mock_db_execute.assert_called_once()
    mock_default_llm.ainvoke.assert_called_once()


@patch(PROMPT_LOAD_TARGET, "Prompt: {pdf_content}, Ben: {beneficio}, Prof: {profissao}")
@patch(DB_EXECUTE_MOCK_TARGET)
@patch(DYNAMIC_LLM_INIT_TARGET) # Mocka a inicialização dinâmica de LLM
@patch(DEFAULT_LLM_MOCK_TARGET) # Mocka o LLM padrão (para garantir que não seja chamado)
def test_gerar_quesitos_com_referencia_success_specific_model(mock_default_llm, mock_dynamic_llm_init, mock_db_execute):
    """
    Testa a geração bem-sucedida usando o endpoint /gerar_com_referencia_documento
    com um modelo de LLM específico.
    """
    # Configura o mock do resultado da query do banco
    mock_cursor_result = MagicMock()
    mock_cursor_result.fetchall.return_value = [("Texto do chunk referenciado.",)]
    mock_db_execute.return_value = mock_cursor_result

    mock_response_content = "1. Quesito Gerado Referenciado B?"
    mock_dynamic_instance = MagicMock()
    mock_dynamic_instance.ainvoke = AsyncMock(return_value=create_mock_ai_message(mock_response_content))
    mock_dynamic_llm_init.return_value = mock_dynamic_instance

    specific_model = "gemini-1.5-pro-latest"
    url = f"{settings.API_PREFIX}/gerador_quesitos/v1/gerar_com_referencia_documento"
    payload = {
        "document_filename": "outro_documento.pdf",
        "beneficio": "BPC-LOAS",
        "profissao": "Do Lar",
        "modelo_nome": specific_model
    }
    response = client.post(url, json=payload)

    assert response.status_code == 200
    response_data = RespostaQuesitos(**response.json())
    assert response_data.quesitos_texto == mock_response_content
    mock_db_execute.assert_called_once()
    mock_dynamic_llm_init.assert_called_once_with(model=specific_model, google_api_key=settings.GOOGLE_API_KEY)
    mock_dynamic_instance.ainvoke.assert_called_once()
    if mock_default_llm: # Garante que o LLM padrão não foi chamado
        mock_default_llm.ainvoke.assert_not_called()


@patch(DB_EXECUTE_MOCK_TARGET)
@patch(DEFAULT_LLM_MOCK_TARGET, None) # Simula LLM padrão não disponível
def test_gerar_quesitos_com_referencia_no_default_llm(mock_db_execute):
    """
    Testa o endpoint /gerar_com_referencia_documento quando o LLM padrão não está
    disponível e é solicitado.
    """
    # Configura o mock do resultado da query do banco
    mock_cursor_result = MagicMock()
    mock_cursor_result.fetchall.return_value = [("Texto qualquer.",)]
    mock_db_execute.return_value = mock_cursor_result

    url = f"{settings.API_PREFIX}/gerador_quesitos/v1/gerar_com_referencia_documento"
    payload = {"document_filename": "doc.pdf", "beneficio": "BPC", "profissao": "Do Lar", "modelo_nome": "<Modelo Padrão>"}

    # Patch settings.GOOGLE_API_KEY to None to ensure re-initialization fails if default_llm is None
    with patch.object(settings, 'GOOGLE_API_KEY', None):
        response = client.post(url, json=payload)

    # Espera-se uma resposta placeholder indicando LLM indisponível, não um 503 direto,
    # pois o endpoint agora tem um fallback para texto placeholder.
    assert response.status_code == 200
    assert "Placeholder: LLM indisponível" in response.json().get("quesitos_texto", "")


@patch(PROMPT_LOAD_TARGET, "Prompt: {pdf_content}, Ben: {beneficio}, Prof: {profissao}")
@patch(DB_EXECUTE_MOCK_TARGET)
@patch(DEFAULT_LLM_MOCK_TARGET)
def test_gerar_quesitos_com_referencia_llm_error(mock_default_llm, mock_db_execute):
    """
    Testa o endpoint /gerar_com_referencia_documento quando a chamada ao LLM padrão falha.
    """
    if mock_default_llm is None:
        pytest.skip("Skipping test: Default LLM mock target None")
        return

    # Configura o mock do resultado da query do banco
    mock_cursor_result = MagicMock()
    mock_cursor_result.fetchall.return_value = [("Texto extraído.",)]
    mock_db_execute.return_value = mock_cursor_result

    mock_default_llm.ainvoke = AsyncMock(side_effect=Exception("Simulated Google API Error"))

    url = f"{settings.API_PREFIX}/gerador_quesitos/v1/gerar_com_referencia_documento"
    payload = {"document_filename": "doc_err.pdf", "beneficio": "BPC", "profissao": "Do Lar", "modelo_nome": "<Modelo Padrão>"}
    response = client.post(url, json=payload)

    assert response.status_code == 500
    assert "Erro ao contatar o serviço de IA" in response.json().get("detail", "")


@patch(PROMPT_LOAD_TARGET, "Prompt: {pdf_content}, Ben: {beneficio}, Prof: {profissao}")
@patch(DB_EXECUTE_MOCK_TARGET)
def test_gerar_quesitos_com_referencia_db_error(mock_db_execute):
    """
    Testa o endpoint /gerar_com_referencia_documento quando ocorre um erro ao buscar
    dados do banco.
    """
    mock_db_execute.side_effect = Exception("Simulated Database Error")

    url = f"{settings.API_PREFIX}/gerador_quesitos/v1/gerar_com_referencia_documento"
    payload = {"document_filename": "doc_db_err.pdf", "beneficio": "BPC", "profissao": "Do Lar", "modelo_nome": "<Modelo Padrão>"}
    response = client.post(url, json=payload)

    assert response.status_code == 500
    assert "Erro ao buscar conteúdo do documento" in response.json().get("detail", "")


@patch(PROMPT_LOAD_TARGET, "Prompt: {pdf_content}, Ben: {beneficio}, Prof: {profissao}")
@patch(DB_EXECUTE_MOCK_TARGET)
def test_gerar_quesitos_com_referencia_doc_not_found(mock_db_execute):
    """
    Testa o endpoint /gerar_com_referencia_documento quando o documento (chunks)
    não é encontrado no banco.
    """
    # Configura o mock do resultado da query do banco para retornar lista vazia
    mock_cursor_result = MagicMock()
    mock_cursor_result.fetchall.return_value = [] # Nenhum chunk encontrado
    mock_db_execute.return_value = mock_cursor_result

    url = f"{settings.API_PREFIX}/gerador_quesitos/v1/gerar_com_referencia_documento"
    payload = {"document_filename": "doc_nao_existe.pdf", "beneficio": "BPC", "profissao": "Do Lar", "modelo_nome": "<Modelo Padrão>"}
    response = client.post(url, json=payload)

    assert response.status_code == 404 # Not Found
    assert "não encontrado ou não possui conteúdo processado" in response.json().get("detail", "")


def test_gerar_quesitos_com_referencia_missing_payload_fields():
    """
    Testa o endpoint /gerar_com_referencia_documento com campos faltando no payload.
    """
    url = f"{settings.API_PREFIX}/gerador_quesitos/v1/gerar_com_referencia_documento"
    # Payload faltando 'document_filename'
    payload = {"beneficio": "BPC", "profissao": "Do Lar", "modelo_nome": "<Modelo Padrão>"}
    response = client.post(url, json=payload)
    assert response.status_code == 422 # Unprocessable Entity

    # Payload faltando 'beneficio'
    payload_sem_beneficio = {"document_filename": "doc.pdf", "profissao": "Do Lar", "modelo_nome": "<Modelo Padrão>"}
    response_sem_beneficio = client.post(url, json=payload_sem_beneficio)
    assert response_sem_beneficio.status_code == 422


# O teste test_gerar_quesitos_no_files não se aplica ao novo endpoint,
# pois ele não recebe 'files' diretamente.

def test_gerar_quesitos_no_files(): # Este teste se refere ao endpoint /gerar original
    """ Test sending request with no files attached to /gerar. """
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