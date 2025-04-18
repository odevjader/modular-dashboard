# backend/tests/test_ai_test.py
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path
import pytest

# Add application root directory to path
app_root_dir = str(Path(__file__).parent.parent)
if app_root_dir not in sys.path:
    sys.path.insert(0, app_root_dir)

# Import app and settings
from main import app
from core.config import settings
from modules.ai_test.v1.schemas import TextInput, AIResponse

# Create Test Client
client = TestClient(app)

# Define the target for mocking
LLM_MOCK_TARGET = "modules.ai_test.v1.endpoints.llm"

# Helper function to create mock AI message
def create_mock_ai_message(content: str):
    mock_msg = MagicMock()
    mock_msg.content = content
    return mock_msg

# Test successful ping
@patch(LLM_MOCK_TARGET)
def test_ping_ai_model_success(mock_llm):
    """ Test success with mocked AI response. """
    if mock_llm is None:
        pytest.skip("Skipping test: LLM mock target None (check API key?)")
        return

    mock_response_content = "This is a mocked AI response to ping."
    async def mock_ainvoke(*args, **kwargs):
        return create_mock_ai_message(mock_response_content)
    mock_llm.ainvoke = mock_ainvoke

    test_payload = TextInput(text="Test ping")
    ping_url = f"{settings.API_PREFIX}/ai_test/v1/ping"
    response = client.post(ping_url, json=test_payload.model_dump())

    assert response.status_code == 200
    response_data = AIResponse(**response.json())
    assert response_data.response == mock_response_content

# Test case for when LLM is not initialized
@patch(LLM_MOCK_TARGET, None)
# REMOVED the argument from the function definition below
def test_ping_ai_model_no_llm():
    """ Test when LLM is not initialized (mocked as None). """
    test_payload = TextInput(text="Test ping")
    ping_url = f"{settings.API_PREFIX}/ai_test/v1/ping"

    response = client.post(ping_url, json=test_payload.model_dump())

    assert response.status_code == 503
    assert "AI model is not configured" in response.json().get("detail", "")

# Test case for when the LLM call itself fails
@patch(LLM_MOCK_TARGET)
def test_ping_ai_model_llm_error(mock_llm):
    """ Test when llm.ainvoke raises an exception. """
    if mock_llm is None:
        pytest.skip("Skipping test: LLM mock target None (check API key?)")
        return

    async def mock_ainvoke_error(*args, **kwargs):
        raise Exception("Simulated LLM API error")
    mock_llm.ainvoke = mock_ainvoke_error

    test_payload = TextInput(text="Test ping causing error")
    ping_url = f"{settings.API_PREFIX}/ai_test/v1/ping"

    response = client.post(ping_url, json=test_payload.model_dump())

    assert response.status_code == 500
    assert "An error occurred while processing" in response.json().get("detail", "")