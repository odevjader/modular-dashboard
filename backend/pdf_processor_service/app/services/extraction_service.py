import pypdfium2 as pdfium
import hashlib

def generate_file_hash(file_bytes: bytes) -> str:
    """Generates a SHA256 hash for the given file bytes."""
    sha256_hash = hashlib.sha256()
    sha256_hash.update(file_bytes)
    return sha256_hash.hexdigest()

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    pdf = pdfium.PdfDocument(pdf_bytes)
    full_text = ""
    for i in range(len(pdf)):
        page = pdf[i]
        textpage = page.get_textpage()
        full_text += textpage.get_text_range() + "\n\n" # Add double newline between pages
        textpage.close()
        page.close()
    pdf.close()
    return full_text.strip()

def chunk_text_by_paragraph(text: str) -> list[str]:
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()] # Split by double newline, then strip
    return paragraphs # Keep it simple for now
