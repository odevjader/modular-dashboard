# backend/tests/test_pdf_processor.py
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi import UploadFile as FastAPIUploadFile # Keep for type hints
from io import BytesIO
import sys
from pathlib import Path

# Add application root directory to path
app_root_dir = str(Path(__file__).parent.parent / "app")
if app_root_dir not in sys.path:
    sys.path.insert(0, app_root_dir)

# Import the function to test
from utils.pdf_processor import processar_pdfs_upload

# Define mock target for DoclingLoader within the utility module
LOADER_MOCK_TARGET = "utils.pdf_processor.DoclingLoader"
TEMPFILE_MOCK_TARGET = "utils.pdf_processor.tempfile.NamedTemporaryFile"
OS_REMOVE_MOCK_TARGET = "utils.pdf_processor.os.remove"
OS_PATH_EXISTS_MOCK_TARGET = "utils.pdf_processor.os.path.exists"

# Helper function to create mock Langchain Document
def create_mock_langchain_doc(page_content: str):
    mock_doc = MagicMock()
    mock_doc.page_content = page_content
    return mock_doc

# Helper function to create mock UploadFile using MagicMock
def create_mock_upload_file(filename: str, content_type: str, content: bytes) -> FastAPIUploadFile:
    # Create a MagicMock simulating UploadFile
    mock_file_object = MagicMock(spec=FastAPIUploadFile)
    mock_file_object.filename = filename
    mock_file_object.content_type = content_type

    # Simulate the file-like object stored internally
    file_like = BytesIO(content)
    mock_file_object.file = file_like # Assign the BytesIO object

    # Mock the async read method to return the content
    # Needs to be an awaitable that returns bytes
    async def mock_read():
        return content # Return the original bytes
    mock_file_object.read = AsyncMock(side_effect=mock_read)

    # Mock the async close method
    mock_file_object.close = AsyncMock(return_value=None)

    # Mock seek if necessary (less likely needed for read-only)
    mock_file_object.seek = MagicMock(return_value=None)

    return mock_file_object

# --- Test Cases ---

@pytest.mark.asyncio
@patch(OS_PATH_EXISTS_MOCK_TARGET, return_value=False)
@patch(OS_REMOVE_MOCK_TARGET)
@patch(TEMPFILE_MOCK_TARGET)
@patch(LOADER_MOCK_TARGET)
async def test_processar_pdfs_success_single(mock_DoclingLoader, mock_NamedTemporaryFile, mock_os_remove, mock_os_path_exists):
    """ Test processing a single valid PDF successfully. """
    mock_loader_instance = MagicMock()
    mock_loader_instance.load = MagicMock(return_value=[create_mock_langchain_doc("Texto do PDF 1.")])
    mock_DoclingLoader.return_value = mock_loader_instance
    mock_temp_file = MagicMock()
    mock_temp_file.__enter__.return_value.name = "/tmp/fake1.pdf"
    mock_NamedTemporaryFile.return_value = mock_temp_file
    dummy_file = create_mock_upload_file("doc1.pdf", "application/pdf", b"pdf1_content")
    result_text = await processar_pdfs_upload([dummy_file])
    expected_text = "--- CONTEÚDO DO ARQUIVO: doc1.pdf ---\n\nTexto do PDF 1."
    assert result_text == expected_text
    mock_DoclingLoader.assert_called_once_with(file_path="/tmp/fake1.pdf")
    mock_loader_instance.load.assert_called_once()
    # Check if close was awaited on the mock
    dummy_file.close.assert_awaited_once()

@pytest.mark.asyncio
@patch(OS_PATH_EXISTS_MOCK_TARGET, return_value=False)
@patch(OS_REMOVE_MOCK_TARGET)
@patch(TEMPFILE_MOCK_TARGET)
@patch(LOADER_MOCK_TARGET)
async def test_processar_pdfs_success_multiple(mock_DoclingLoader, mock_NamedTemporaryFile, mock_os_remove, mock_os_path_exists):
    """ Test processing multiple valid PDFs successfully. """
    mock_loader_instance1 = MagicMock()
    mock_loader_instance1.load = MagicMock(return_value=[create_mock_langchain_doc("Texto PDF 1.")])
    mock_loader_instance2 = MagicMock()
    mock_loader_instance2.load = MagicMock(return_value=[create_mock_langchain_doc("Texto PDF 2.")])
    mock_DoclingLoader.side_effect = [mock_loader_instance1, mock_loader_instance2]
    mock_temp_file1 = MagicMock()
    mock_temp_file1.__enter__.return_value.name = "/tmp/fake1.pdf"
    mock_temp_file2 = MagicMock()
    mock_temp_file2.__enter__.return_value.name = "/tmp/fake2.pdf"
    mock_NamedTemporaryFile.side_effect = [mock_temp_file1, mock_temp_file2]
    file1 = create_mock_upload_file("doc1.pdf", "application/pdf", b"pdf1")
    file2 = create_mock_upload_file("doc2.pdf", "application/pdf", b"pdf2")
    result_text = await processar_pdfs_upload([file1, file2])
    expected_text = "--- CONTEÚDO DO ARQUIVO: doc1.pdf ---\n\nTexto PDF 1.\n\n--- CONTEÚDO DO ARQUIVO: doc2.pdf ---\n\nTexto PDF 2."
    assert result_text == expected_text
    assert mock_DoclingLoader.call_count == 2
    mock_loader_instance1.load.assert_called_once()
    mock_loader_instance2.load.assert_called_once()
    file1.close.assert_awaited_once()
    file2.close.assert_awaited_once()


@pytest.mark.asyncio
@patch(OS_PATH_EXISTS_MOCK_TARGET, return_value=False)
@patch(OS_REMOVE_MOCK_TARGET)
@patch(TEMPFILE_MOCK_TARGET)
@patch(LOADER_MOCK_TARGET)
async def test_processar_pdfs_skip_non_pdf(mock_DoclingLoader, mock_NamedTemporaryFile, mock_os_remove, mock_os_path_exists):
    """ Test skipping non-PDF files. """
    mock_loader_instance = MagicMock()
    mock_loader_instance.load = MagicMock(return_value=[create_mock_langchain_doc("Texto PDF valido.")])
    mock_DoclingLoader.return_value = mock_loader_instance
    mock_temp_file = MagicMock()
    mock_temp_file.__enter__.return_value.name = "/tmp/fake_valid.pdf"
    mock_NamedTemporaryFile.return_value = mock_temp_file
    file_pdf = create_mock_upload_file("doc_ok.pdf", "application/pdf", b"pdf")
    file_txt = create_mock_upload_file("doc_bad.txt", "text/plain", b"txt") # Non-PDF
    result_text = await processar_pdfs_upload([file_pdf, file_txt])
    expected_text = "--- CONTEÚDO DO ARQUIVO: doc_ok.pdf ---\n\nTexto PDF valido."
    assert result_text == expected_text
    mock_DoclingLoader.assert_called_once_with(file_path="/tmp/fake_valid.pdf")
    # Ensure close was called even for the skipped file
    file_pdf.close.assert_awaited_once()
    file_txt.close.assert_awaited_once()


@pytest.mark.asyncio
@patch(OS_PATH_EXISTS_MOCK_TARGET, return_value=False)
@patch(OS_REMOVE_MOCK_TARGET)
@patch(TEMPFILE_MOCK_TARGET)
@patch(LOADER_MOCK_TARGET)
async def test_processar_pdfs_loader_error_continues(mock_DoclingLoader, mock_NamedTemporaryFile, mock_os_remove, mock_os_path_exists):
    """ Test that processing continues if one file fails to load. """
    mock_loader_instance1 = MagicMock()
    mock_loader_instance1.load = MagicMock(return_value=[create_mock_langchain_doc("Texto PDF 1.")])
    mock_loader_instance2 = MagicMock()
    mock_loader_instance2.load = MagicMock(side_effect=Exception("Docling Load Error"))
    mock_DoclingLoader.side_effect = [mock_loader_instance1, mock_loader_instance2]
    mock_temp_file1 = MagicMock()
    mock_temp_file1.__enter__.return_value.name = "/tmp/fake1.pdf"
    mock_temp_file2 = MagicMock()
    mock_temp_file2.__enter__.return_value.name = "/tmp/fake2.pdf"
    mock_NamedTemporaryFile.side_effect = [mock_temp_file1, mock_temp_file2]
    file1 = create_mock_upload_file("doc1.pdf", "application/pdf", b"pdf1")
    file2 = create_mock_upload_file("doc2_fails.pdf", "application/pdf", b"pdf2")
    result_text = await processar_pdfs_upload([file1, file2])
    expected_text = "--- CONTEÚDO DO ARQUIVO: doc1.pdf ---\n\nTexto PDF 1."
    assert result_text == expected_text
    assert mock_DoclingLoader.call_count == 2
    file1.close.assert_awaited_once()
    file2.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_processar_pdfs_empty_list():
    """ Test processing an empty list of files. """
    result_text = await processar_pdfs_upload([])
    assert result_text == ""