import pytest
import httpx # For Response object in mock
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

# Assuming main FastAPI app is in app.main for the main backend
from app.main import app # Main backend's FastAPI app
# Assuming User model and a way to get a valid token for testing
# This part might need adjustment based on how auth testing is typically handled in this project

client = TestClient(app)

# A fixture to get a valid auth token would be ideal here.
# For now, we'll assume a way to bypass or mock auth if direct token generation is complex,
# or focus on tests where auth has already been handled by other means (e.g., if TestClient can be authed).
# Let's assume we can get a token or the TestClient handles auth for certain users.
# We will need a mock user and a way to get a token for that user.
# This is highly project-specific. For now, we'll define a placeholder for headers.

def get_auth_headers(user_id: str = "testuser"): # Placeholder
    # In a real setup, this would generate or fetch a valid JWT token
    return {"Authorization": f"Bearer fake-token-for-{user_id}"}

@patch('app.modules.documents.router.httpx.AsyncClient') # Target where AsyncClient is used
def test_upload_and_process_success(mock_async_client):
    # Configure the mock response from the pdf_processor_service
    mock_response_content = {"id": 1, "file_hash": "mock_hash", "file_name": "test.pdf"}
    mock_http_response = httpx.Response(200, json=mock_response_content)

    # Configure the behavior of the mocked AsyncClient instance
    mock_instance = mock_async_client.return_value.__aenter__.return_value # This gets the client instance from async with
    mock_instance.post = AsyncMock(return_value=mock_http_response) # Mock the post method

    dummy_pdf_content = b"%PDF-1.0...gateway test"
    files = {'file': ('test.pdf', dummy_pdf_content, 'application/pdf')}

    response = client.post("/api/v1/documents/upload-and-process", files=files, headers=get_auth_headers())

    assert response.status_code == 200
    assert response.json() == mock_response_content
    mock_instance.post.assert_called_once()
    # Can add more assertions on the call_args of mock_instance.post if needed

def test_upload_and_process_no_auth():
    dummy_pdf_content = b"%PDF-1.0...gateway test"
    files = {'file': ('test.pdf', dummy_pdf_content, 'application/pdf')}
    response = client.post("/api/v1/documents/upload-and-process", files=files)
    assert response.status_code == 401 # Or 403 depending on actual auth middleware

@patch('app.modules.documents.router.httpx.AsyncClient')
def test_upload_and_process_invalid_file_type_at_gateway(mock_async_client):
    files = {'file': ('test.txt', b"not a pdf", 'text/plain')}
    response = client.post("/api/v1/documents/upload-and-process", files=files, headers=get_auth_headers())
    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]
    mock_async_client.return_value.__aenter__.return_value.post.assert_not_called()

@patch('app.modules.documents.router.httpx.AsyncClient')
def test_upload_and_process_microservice_returns_error(mock_async_client):
    mock_error_content = {"detail": "Microservice processing error"}
    mock_http_response = httpx.Response(422, json=mock_error_content) # e.g., Unprocessable Entity

    mock_instance = mock_async_client.return_value.__aenter__.return_value
    mock_instance.post = AsyncMock(return_value=mock_http_response)

    dummy_pdf_content = b"%PDF-1.0...gateway test"
    files = {'file': ('test.pdf', dummy_pdf_content, 'application/pdf')}

    response = client.post("/api/v1/documents/upload-and-process", files=files, headers=get_auth_headers())

    assert response.status_code == 422
    assert response.json() == mock_error_content

@patch('app.modules.documents.router.httpx.AsyncClient')
def test_upload_and_process_microservice_unavailable(mock_async_client):
    mock_instance = mock_async_client.return_value.__aenter__.return_value
    mock_instance.post = AsyncMock(side_effect=httpx.ConnectError("Connection refused"))

    dummy_pdf_content = b"%PDF-1.0...gateway test"
    files = {'file': ('test.pdf', dummy_pdf_content, 'application/pdf')}

    response = client.post("/api/v1/documents/upload-and-process", files=files, headers=get_auth_headers())

    assert response.status_code == 503
    assert "Service unavailable" in response.json()["detail"]
