import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock # For mocking the service call

# Assuming your FastAPI app instance is in app.main
from app.main import app
from app.schemas.document_schemas import DocumentResponse # For asserting response structure
from app.models.document import Document as DocumentModel # For service mock return type hint
from datetime import datetime

client = TestClient(app)

@pytest.fixture
def mock_create_document_and_chunks(mocker):
    # This mock will represent the services.create_document_and_chunks function
    # It's being patched in the context of where the router imports it from.
    # Assuming processing_router.py does: from .. import services (or from ..services import create_document_and_chunks)
    # Adjust the patch target string if the import path is different in processing_router.py
    mock_service = mocker.patch('app.routers.processing_router.services.create_document_and_chunks')
    return mock_service

def test_process_pdf_endpoint_success(mock_create_document_and_chunks):
    # Mock the service function to return a sample Document object (SQLAlchemy model instance)
    # The endpoint should then convert this to a DocumentResponse schema
    mock_document_model = DocumentModel(
        id=1,
        file_hash="testhash123",
        file_name="test.pdf",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    mock_create_document_and_chunks.return_value = mock_document_model

    # Create a dummy PDF file for upload
    dummy_pdf_content = b"%PDF-1.0...dummy content"
    files = {'file': ('test.pdf', dummy_pdf_content, 'application/pdf')}

    response = client.post("/processing/process-pdf", files=files)

    assert response.status_code == 200
    # Check if the response matches the DocumentResponse schema based on mock_document_model
    response_data = response.json()
    assert response_data["id"] == mock_document_model.id
    assert response_data["file_hash"] == mock_document_model.file_hash
    assert response_data["file_name"] == mock_document_model.file_name
    mock_create_document_and_chunks.assert_called_once()

def test_process_pdf_endpoint_invalid_file_type():
    files = {'file': ('test.txt', b"not a pdf", 'text/plain')}
    response = client.post("/processing/process-pdf", files=files)
    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]

def test_process_pdf_endpoint_empty_file():
    files = {'file': ('empty.pdf', b"", 'application/pdf')}
    response = client.post("/processing/process-pdf", files=files)
    assert response.status_code == 400
    assert "Empty file uploaded" in response.json()["detail"]

def test_process_pdf_endpoint_service_exception(mock_create_document_and_chunks):
    mock_create_document_and_chunks.side_effect = Exception("Service layer boom!")

    dummy_pdf_content = b"%PDF-1.0...dummy content"
    files = {'file': ('test.pdf', dummy_pdf_content, 'application/pdf')}

    response = client.post("/processing/process-pdf", files=files)
    assert response.status_code == 500
    assert "Error processing PDF: Service layer boom!" in response.json()["detail"]

# Placeholder for more nuanced service error handling tests if developed
# def test_process_pdf_endpoint_service_http_exception_forwarding(mock_create_document_and_chunks):
#     pass
