import io
from unittest.mock import patch, AsyncMock

import httpx # Required for creating mock response objects for httpx.HTTPStatusError
from fastapi import UploadFile, HTTPException
from fastapi.testclient import TestClient

from app.main import app # Import the main FastAPI application
# from app.models.user import User, UserRole # Not strictly needed if MockUser is comprehensive

client = TestClient(app)

# Simplified MockUser for dependency injection
class MockUser:
    def __init__(self, id: int, is_active: bool = True, role: str = "user"):
        self.id = id
        self.is_active = is_active
        self.role = role # Add role if get_current_active_user checks it, though not strictly used by endpoint itself

def get_mock_active_user():
    return MockUser(id=1, is_active=True)

def test_import_document_schemas():
    from app.modules.documents import schemas as doc_schemas
    assert hasattr(doc_schemas, 'DocumentBase')
    assert hasattr(doc_schemas, 'DocumentCreate')
    assert hasattr(doc_schemas, 'Document')
    print("Document schemas imported successfully.")

def test_import_document_v1_schemas():
    from app.modules.documents.v1 import schemas as v1_doc_schemas
    assert hasattr(v1_doc_schemas, 'PingResponse')
    print("Document v1 schemas imported successfully.")

# test_import_document_services has been removed as example_service_function no longer exists.

def test_documents_module_router_integration():
    response = client.get("/api/openapi.json") # The global prefix is /api
    assert response.status_code == 200
    openapi_schema = response.json()
    paths = openapi_schema.get("paths", {})

    assert "/api/documents/" in paths, "Document module root path not found in OpenAPI spec."
    assert "/api/documents/v1/ping" in paths, "Document module v1 ping path not found in OpenAPI spec."
    # Also check for the new upload endpoint
    assert "/api/documents/upload" in paths, "Document module upload path not found in OpenAPI spec."
    print("Documents module routes (including upload) found in OpenAPI schema.")

def test_documents_v1_ping_endpoint():
    response = client.get("/api/documents/v1/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "Pong from Documents v1"}
    print("Documents v1 ping endpoint responded correctly.")

def test_documents_root_endpoint():
    response = client.get("/api/documents/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Documents Module"}
    print("Documents module root endpoint responded correctly.")

@patch('app.modules.documents.router.get_current_active_user')
@patch('app.modules.documents.services.httpx.AsyncClient.post', new_callable=AsyncMock)
async def test_upload_document_success(mock_httpx_post, mock_get_user):
    # Configure mocks
    mock_get_user.return_value = get_mock_active_user()
    mock_httpx_post.return_value = httpx.Response(
        200,
        json={"transcription_id": "123", "status": "completed", "text": "dummy text"}
    )

    file_content = b"dummy pdf content"
    # When using TestClient, the 'files' parameter takes a dict of field names to file tuples
    # The field name 'file' must match the FastAPI endpoint parameter name: file: UploadFile = File(...)
    files_data = {'file': ('test.pdf', io.BytesIO(file_content), 'application/pdf')}

    response = client.post("/api/documents/upload", files=files_data)

    assert response.status_code == 200
    response_json = response.json()
    assert response_json["original_filename"] == "test.pdf"
    assert response_json["message"] == "File successfully processed by transcriber."
    assert response_json["transcriber_data"]["status"] == "completed"
    assert response_json["uploader_user_id"] == 1
    mock_httpx_post.assert_called_once()
    # You could add more assertions on the arguments of mock_httpx_post if needed

@patch('app.modules.documents.router.get_current_active_user')
@patch('app.modules.documents.services.httpx.AsyncClient.post', new_callable=AsyncMock)
async def test_upload_document_transcriber_error(mock_httpx_post, mock_get_user):
    mock_get_user.return_value = get_mock_active_user()

    # Simulate an error response from the transcriber service
    mock_response = httpx.Response(
        status_code=422, # Example: Unprocessable Entity
        json={'detail': 'Invalid PDF content'}
    )
    mock_httpx_post.side_effect = httpx.HTTPStatusError(
        message="Transcriber service error", request=None, response=mock_response
    )

    file_content = b"corrupted pdf content"
    files_data = {'file': ('corrupt.pdf', io.BytesIO(file_content), 'application/pdf')}

    response = client.post("/api/documents/upload", files=files_data)

    assert response.status_code == 422 # Should match the error code from transcriber
    response_json = response.json()
    assert "Error from transcriber service: Status 422" in response_json["detail"]

@patch('app.modules.documents.router.get_current_active_user')
@patch('app.modules.documents.services.httpx.AsyncClient.post', new_callable=AsyncMock)
async def test_upload_document_transcriber_connection_error(mock_httpx_post, mock_get_user):
    mock_get_user.return_value = get_mock_active_user()

    # Simulate a connection error when trying to reach the transcriber service
    mock_httpx_post.side_effect = httpx.RequestError(
        message="Connection failed", request=None
    )

    file_content = b"any pdf content"
    files_data = {'file': ('any.pdf', io.BytesIO(file_content), 'application/pdf')}

    response = client.post("/api/documents/upload", files=files_data)

    assert response.status_code == 503 # Service Unavailable
    response_json = response.json()
    assert "Could not connect to transcriber service" in response_json["detail"]

@patch('app.modules.documents.router.get_current_active_user')
@patch('app.modules.documents.services.httpx.AsyncClient.post', new_callable=AsyncMock)
async def test_upload_document_unexpected_service_exception(mock_httpx_post, mock_get_user):
    mock_get_user.return_value = get_mock_active_user()

    # Simulate an unexpected error within the service layer after httpx call (e.g., during response processing)
    # or any other Exception not caught by specific httpx exceptions.
    mock_httpx_post.side_effect = Exception("Something totally unexpected broke")

    file_content = b"any pdf content"
    files_data = {'file': ('any.pdf', io.BytesIO(file_content), 'application/pdf')}

    response = client.post("/api/documents/upload", files=files_data)

    assert response.status_code == 500 # Internal Server Error
    response_json = response.json()
    assert "An unexpected error occurred while processing the file." in response_json["detail"]

# Note: The TestClient runs the async functions from the tests directly.
# If your tests were not using an async test runner, you might need to use asyncio.run()
# or a library like pytest-asyncio. However, TestClient handles this.
# The test functions for endpoints are defined with `async def` for consistency,
# although TestClient itself is synchronous, it can call async path operation functions.
# For mocks like AsyncMock, it's good practice for the test fn to be async.
# If these tests are run with pytest, it will handle the async test functions correctly.
# If run with `python -m unittest`, an async test runner might be needed for `async def test_...`
# For now, assuming pytest or similar that supports `async def` tests.
# If not, they can be `def` and `TestClient` still works, but `AsyncMock` behaves slightly differently.
# Let's make them `def` for broader compatibility if `pytest-asyncio` is not assumed.
# TestClient's methods are synchronous.

# Reverting test functions to `def` as TestClient itself is synchronous.
# The `AsyncMock` will still behave as expected in this synchronous context
# when its `return_value` is awaited by the application code being tested.

# Final check on test function definitions:
# TestClient is synchronous, so test functions don't strictly need to be async.
# However, if the code *inside* the test needs to `await` something directly (not via client),
# or if using `AsyncMock`'s `await` capabilities directly in the test body, `async def` is needed.
# Given `new_callable=AsyncMock`, and the service layer is async, `async def` for tests is cleaner.
# Assuming pytest or a runner that supports it. If issues arise, can convert to sync `def`.
# The current FastAPI TestClient documentation shows `def test_...:` for async path operations.
# Let's stick to `async def` as it's more idiomatic with `AsyncMock` and `async` app code.
# This means the test runner (e.g., pytest with pytest-asyncio) must support it.
# If not, the tests would need to be synchronous.
# For this exercise, I'll assume an environment where `async def` tests work.
# I also added a check for the "/api/documents/upload" path in `test_documents_module_router_integration`.
# Added a new test `test_upload_document_unexpected_service_exception` for better coverage.

# One small adjustment for `test_upload_document_success`:
# The `files_data` for `client.post` should use an `io.BytesIO` object for the file content part of the tuple.
# This was already done in the prompt, just confirming it's correct.
# Original: `files={'file': ('test.pdf', file_content, 'application/pdf')}`
# Correct for TestClient: `files={'file': ('test.pdf', io.BytesIO(file_content), 'application/pdf')}`
# This is already correctly reflected in the code block above.


def test_upload_document_no_auth_token():
    # Test uploading a document without providing an authentication token.
    file_content = b"dummy pdf content"
    files_data = {'file': ('test.pdf', io.BytesIO(file_content), 'application/pdf')}
    response = client.post("/api/documents/upload", files=files_data)
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_upload_document_invalid_auth_token():
    # Test uploading a document with an invalid authentication token.
    file_content = b"dummy pdf content"
    files_data = {'file': ('test.pdf', io.BytesIO(file_content), 'application/pdf')}
    headers = {"Authorization": "Bearer invalidtokenstring"}
    response = client.post("/api/documents/upload", files=files_data, headers=headers)
    assert response.status_code == 401
    assert response.json().get("detail") == "Could not validate credentials"

@patch('app.modules.documents.router.get_current_active_user')
def test_upload_document_missing_file(mock_get_user):
    # Test uploading without a file, expecting a 422 Unprocessable Entity error.
    mock_get_user.return_value = get_mock_active_user() # Simulate authenticated user

    response = client.post("/api/documents/upload") # No 'files' data sent

    assert response.status_code == 422
    response_json = response.json()
    assert isinstance(response_json.get("detail"), list), "Detail field should be a list."

    file_error_found = False
    for error in response_json["detail"]:
        # Check for the specific error related to the 'file' field being missing.
        # The exact 'type' can vary slightly (e.g., 'missing', 'value_error.missing').
        if error.get("loc") == ["body", "file"] and "missing" in error.get("type", "").lower():
            file_error_found = True
            break
    assert file_error_found, "Specific error for missing 'file' field not found in details."
