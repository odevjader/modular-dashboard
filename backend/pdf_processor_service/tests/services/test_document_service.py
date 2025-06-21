import pytest
from unittest.mock import MagicMock, patch # patch can be used as an alternative to mocker fixture for specific imports
from sqlalchemy.orm import Session

# Assuming your models are in app.models and services in app.services
from app.models.document import Document, DocumentChunk # Import your actual models
from app.services.document_service import create_document_and_chunks
# We will mock generate_file_hash, extract_text_from_pdf, chunk_text_by_paragraph

@pytest.fixture
def mock_db_session():
    db = MagicMock(spec=Session)
    db.query.return_value.filter.return_value.first.return_value = None # Default: document not found
    db.query.return_value.filter.return_value.delete = MagicMock() # For deleting old chunks
    return db

@pytest.fixture
def mock_extraction_services(mocker):
    mocker.patch('app.services.document_service.generate_file_hash', return_value="test_hash_123")
    mocker.patch('app.services.document_service.extract_text_from_pdf', return_value="Extracted text for testing.")
    mocker.patch('app.services.document_service.chunk_text_by_paragraph', return_value=["Chunk 1", "Chunk 2"])

def test_create_document_and_chunks_new_document(
    mock_db_session: MagicMock,
    mock_extraction_services # This fixture applies the mocks
):
    file_contents = b"sample pdf content"
    original_file_name = "test.pdf"

    # Ensure document is reported as not existing initially
    mock_db_session.query(Document).filter(Document.file_hash == "test_hash_123").first.return_value = None

    created_document = create_document_and_chunks(mock_db_session, file_contents, original_file_name)

    # Assertions for document creation
    # Check if Document was instantiated correctly and added
    args, kwargs = mock_db_session.add.call_args_list[0] # First call to add should be the Document
    added_object = args[0]
    assert isinstance(added_object, Document)
    assert added_object.file_hash == "test_hash_123"
    assert added_object.file_name == original_file_name

    # Assertions for chunk creation
    # Second and third calls to add should be DocumentChunk instances
    assert mock_db_session.add.call_count >= 3 # Document + 2 chunks
    first_chunk_args, _ = mock_db_session.add.call_args_list[1]
    assert isinstance(first_chunk_args[0], DocumentChunk)
    assert first_chunk_args[0].chunk_text == "Chunk 1"
    assert first_chunk_args[0].chunk_order == 0
    # assert first_chunk_args[0].document_id == created_document.id # This needs actual ID or more complex mocking

    second_chunk_args, _ = mock_db_session.add.call_args_list[2]
    assert isinstance(second_chunk_args[0], DocumentChunk)
    assert second_chunk_args[0].chunk_text == "Chunk 2"
    assert second_chunk_args[0].chunk_order == 1

    # Verify commits
    assert mock_db_session.commit.call_count >= 2 # At least after doc creation and after chunk creation
    assert mock_db_session.refresh.call_count >= 1 # At least for the document

    assert created_document is not None
    assert created_document.file_hash == "test_hash_123"

def test_create_document_and_chunks_existing_document(
    mock_db_session: MagicMock,
    mock_extraction_services
):
    file_contents = b"sample pdf content"
    original_file_name = "updated_test.pdf"

    # Simulate existing document
    existing_document_mock = Document(id=1, file_hash="test_hash_123", file_name="test.pdf")
    mock_db_session.query(Document).filter(Document.file_hash == "test_hash_123").first.return_value = existing_document_mock

    updated_document = create_document_and_chunks(mock_db_session, file_contents, original_file_name)

    # Verify old chunks were deleted
    mock_db_session.query(DocumentChunk).filter(DocumentChunk.document_id == existing_document_mock.id).delete.assert_called_once()

    # Assertions for new chunk creation (similar to the new document test)
    assert mock_db_session.add.call_count >= 2 # 2 chunks (document itself is not 'add'ed again, but updated)
    first_chunk_args, _ = mock_db_session.add.call_args_list[0] # Chunks are added first in this path after delete
    assert isinstance(first_chunk_args[0], DocumentChunk)
    assert first_chunk_args[0].chunk_text == "Chunk 1"

    # Verify document filename update
    assert existing_document_mock.file_name == original_file_name # Check if the instance was modified

    assert mock_db_session.commit.call_count >= 2 # After delete, after chunks
    assert mock_db_session.refresh.call_count >= 1

    assert updated_document.id == existing_document_mock.id
    assert updated_document.file_name == original_file_name
