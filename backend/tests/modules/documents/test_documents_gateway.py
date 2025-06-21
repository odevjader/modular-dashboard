import pytest
import httpx # For Response object in mock
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock # Added MagicMock

# Assuming main FastAPI app is in app.main for the main backend
# from app.main import app # Main backend's FastAPI app - MOVED TO FIXTURE TO DELAY IMPORT
# Assuming User model and a way to get a valid token for testing
# This part might need adjustment based on how auth testing is typically handled in this project


# A fixture to get a valid auth token would be ideal here.
# For now, we'll assume a way to bypass or mock auth if direct token generation is complex,
# or focus on tests where auth has already been handled by other means (e.g., if TestClient can be authed).
# Let's assume we can get a token or the TestClient handles auth for certain users.
# We will need a mock user and a way to get a token for that user.
# This is highly project-specific. For now, we'll define a placeholder for headers.

# Import User model for creating a dummy user for dependency override
from app.models.user import User as UserModel # Assuming this is your SQLAlchemy User model
from app.core.dependencies import get_current_active_user # To override this

@pytest.fixture
def client():
    # This ensures 'app' and its settings are loaded after conftest monkeypatching for env vars for each test function
    from app.main import app
    return TestClient(app)

# Dummy user for dependency override
def get_override_get_current_active_user():
    # Return a mock or a simple object that quacks like your User model
    # For example, if your User model has an 'id' and 'role':
    dummy_user = UserModel(id="testuser", email="test@example.com", hashed_password="fake", role="admin", is_active=True)
    # If it's just a Pydantic model or dict elsewhere, adjust accordingly
    return dummy_user

# This fixture will apply the override for tests that use it, or can be applied globally in client fixture
# For now, let's apply it directly in tests that need auth.

# def get_auth_headers(user_id: str = "testuser"): # Placeholder - NO LONGER NEEDED if dependency is overridden
#     # In a real setup, this would generate or fetch a valid JWT token
#     return {"Authorization": f"Bearer fake-token-for-{user_id}"}

@patch('app.modules.documents.endpoints.httpx.AsyncClient') # Corrected patch target
def test_upload_and_process_success(mock_async_client, client: TestClient):
    client.app.dependency_overrides[get_current_active_user] = get_override_get_current_active_user

    # Configure the mock response from the pdf_processor_service
    mock_request = MagicMock(spec=httpx.Request)
    mock_request.url = "http://testurl/processing/process-pdf" # Dummy URL
    mock_response_content = {"id": 1, "file_hash": "mock_hash", "file_name": "test.pdf"}
    mock_http_response = httpx.Response(200, json=mock_response_content, request=mock_request)

    # Configure the behavior of the mocked AsyncClient instance
    mock_instance = mock_async_client.return_value.__aenter__.return_value # This gets the client instance from async with
    mock_instance.post = AsyncMock(return_value=mock_http_response) # Mock the post method

    dummy_pdf_content = b"%PDF-1.0...gateway test"
    files = {'file': ('test.pdf', dummy_pdf_content, 'application/pdf')}

    response = client.post("/api/documents/upload-and-process", files=files) # No headers needed if auth is overridden

    if response.status_code != 200:
        print("Response content for 500 error (success case):", response.json())
    assert response.status_code == 200
    assert response.json() == mock_response_content
    mock_instance.post.assert_called_once()
    # Can add more assertions on the call_args of mock_instance.post if needed
    client.app.dependency_overrides.clear() # Clear overrides after test

def test_upload_and_process_no_auth(client: TestClient):
    client.app.dependency_overrides.clear() # Ensure no overrides from other tests
    dummy_pdf_content = b"%PDF-1.0...gateway test"
    files = {'file': ('test.pdf', dummy_pdf_content, 'application/pdf')}
    response = client.post("/api/documents/upload-and-process", files=files) # No headers
    assert response.status_code == 401 # Or 403 depending on actual auth middleware

@patch('app.modules.documents.endpoints.httpx.AsyncClient') # Corrected patch target
def test_upload_and_process_invalid_file_type_at_gateway(mock_async_client, client: TestClient):
    client.app.dependency_overrides[get_current_active_user] = get_override_get_current_active_user
    files = {'file': ('test.txt', b"not a pdf", 'text/plain')}
    response = client.post("/api/documents/upload-and-process", files=files) # No headers needed
    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]
    mock_async_client.return_value.__aenter__.return_value.post.assert_not_called()
    client.app.dependency_overrides.clear()

@patch('app.modules.documents.endpoints.httpx.AsyncClient') # Corrected patch target
def test_upload_and_process_microservice_returns_error(mock_async_client, client: TestClient):
    client.app.dependency_overrides[get_current_active_user] = get_override_get_current_active_user
    mock_error_content = {"detail": "Microservice processing error"}
    mock_request = MagicMock(spec=httpx.Request)
    mock_request.url = "http://testurl/processing/process-pdf" # Dummy URL
    mock_http_response = httpx.Response(422, json=mock_error_content, request=mock_request)

    mock_instance = mock_async_client.return_value.__aenter__.return_value
    mock_instance.post = AsyncMock(return_value=mock_http_response)

    dummy_pdf_content = b"%PDF-1.0...gateway test"
    files = {'file': ('test.pdf', dummy_pdf_content, 'application/pdf')}

    response = client.post("/api/documents/upload-and-process", files=files) # No headers needed

    if response.status_code != 422:
        print("Response content for 500 error (microservice error case):", response.json())
    assert response.status_code == 422
    assert response.json() == mock_error_content
    client.app.dependency_overrides.clear()

@patch('app.modules.documents.endpoints.httpx.AsyncClient') # Corrected patch target
def test_upload_and_process_microservice_unavailable(mock_async_client, client: TestClient):
    client.app.dependency_overrides[get_current_active_user] = get_override_get_current_active_user
    mock_instance = mock_async_client.return_value.__aenter__.return_value
    mock_instance.post = AsyncMock(side_effect=httpx.ConnectError("Connection refused"))

    dummy_pdf_content = b"%PDF-1.0...gateway test"
    files = {'file': ('test.pdf', dummy_pdf_content, 'application/pdf')}

    response = client.post("/api/documents/upload-and-process", files=files) # No headers needed

    assert response.status_code == 503
    assert "Service unavailable" in response.json()["detail"]
    client.app.dependency_overrides.clear()
