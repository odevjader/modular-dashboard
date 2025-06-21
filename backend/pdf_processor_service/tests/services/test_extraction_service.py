import pytest
import hashlib
from app.services.extraction_service import (
    generate_file_hash,
    extract_text_from_pdf,
    chunk_text_by_paragraph
)
# Mock pypdfium2 if direct PDF processing is too heavy for unit tests or for error condition simulation
# For now, we'll try with actual pypdfium2 for basic cases, assuming it's fast enough.

@pytest.fixture
def sample_pdf_bytes() -> bytes:
    # A very simple, tiny, valid PDF file in bytes.
    # This is a hex representation of a minimal PDF: %PDF-1.0 %âãÏÓ 1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj 2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj 3 0 obj << /Type /Page /MediaBox [0 0 100 100] /Parent 2 0 R /Resources <<>> /Contents 4 0 R >> endobj 4 0 obj << /Length 0 >> stream endstream endobj trailer << /Root 1 0 R >> %%EOF
    # For simplicity in defining, let's use a text-based content and imagine it's PDF bytes.
    # In a real scenario, load actual minimal PDF bytes here.
    # This is NOT a valid PDF, but will be used to test hashing and simulate text extraction (if pypdfium2 is mocked).
    # For a real test with pypdfium2, a valid minimal PDF byte string is needed.
    # Let's create a placeholder for a REAL minimal PDF's text content for assertion for now.
    # Actual PDF bytes would be like: b'%PDF-1.0\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj ...'
    # For now, to make progress, we will use simple text and mock pypdfium2.
    return b"This is a test PDF content for hashing."

@pytest.fixture
def mock_pypdfium2_pdfdocument(mocker):
    mock_textpage = mocker.MagicMock()
    mock_textpage.get_text_range.return_value = "Page 1 text.\n\nPage 2 text."

    mock_page = mocker.MagicMock()
    mock_page.get_textpage.return_value = mock_textpage

    mock_pdf = mocker.MagicMock()
    mock_pdf.__len__.return_value = 2 # Simulate 2 pages
    mock_pdf.__getitem__.return_value = mock_page # Each page is this mock_page
    mock_pdf.close = mocker.MagicMock()
    mock_page.close = mocker.MagicMock()
    mock_textpage.close = mocker.MagicMock()

    return mocker.patch('app.services.extraction_service.pdfium.PdfDocument', return_value=mock_pdf)

def test_generate_file_hash(sample_pdf_bytes):
    file_bytes = sample_pdf_bytes
    expected_hash = hashlib.sha256(file_bytes).hexdigest()
    actual_hash = generate_file_hash(file_bytes)
    assert actual_hash == expected_hash

def test_generate_file_hash_empty():
    file_bytes = b""
    expected_hash = hashlib.sha256(file_bytes).hexdigest()
    actual_hash = generate_file_hash(file_bytes)
    assert actual_hash == expected_hash

def test_extract_text_from_pdf_mocked(mock_pypdfium2_pdfdocument, sample_pdf_bytes):
    # This test uses the mocked pypdfium2
    extracted_text = extract_text_from_pdf(sample_pdf_bytes) # sample_pdf_bytes content doesn't matter here due to mock
    mock_pypdfium2_pdfdocument.assert_called_once_with(sample_pdf_bytes)
    assert "Page 1 text." in extracted_text
    assert "Page 2 text." in extracted_text
    assert extracted_text.strip() == "Page 1 text.\n\nPage 2 text."

def test_chunk_text_by_paragraph():
    text = "Paragraph 1.\n\nParagraph 2 with some lines.\nStill P2.\n\nParagraph 3."
    expected_chunks = [
        "Paragraph 1.",
        "Paragraph 2 with some lines.\nStill P2.",
        "Paragraph 3."
    ]
    chunks = chunk_text_by_paragraph(text)
    assert chunks == expected_chunks

def test_chunk_text_empty():
    text = ""
    expected_chunks = []
    chunks = chunk_text_by_paragraph(text)
    assert chunks == expected_chunks

def test_chunk_text_no_double_newline():
    text = "Single line of text. Another sentence."
    expected_chunks = ["Single line of text. Another sentence."]
    chunks = chunk_text_by_paragraph(text)
    assert chunks == expected_chunks

def test_chunk_text_with_leading_trailing_whitespace():
    text = "  \n\n  Paragraph 1.  \n\nParagraph 2.  \n\n  "
    expected_chunks = ["Paragraph 1.", "Paragraph 2."]
    chunks = chunk_text_by_paragraph(text)
    assert chunks == expected_chunks
