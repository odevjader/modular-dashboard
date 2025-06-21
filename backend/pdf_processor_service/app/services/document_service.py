from sqlalchemy.orm import Session
from .. import models # Assuming models are in pdf_processor_service/app/models/
from .extraction_service import extract_text_from_pdf, chunk_text_by_paragraph, generate_file_hash

def create_document_and_chunks(
    db: Session,
    file_contents: bytes,
    original_file_name: str | None = None
) -> models.Document:
    file_hash = generate_file_hash(file_contents)

    db_document = db.query(models.Document).filter(models.Document.file_hash == file_hash).first()

    if not db_document:
        db_document = models.Document(
            file_hash=file_hash,
            file_name=original_file_name
        )
        db.add(db_document)
        # Commit here to get the document ID if the DB is configured for autoincrement ID before chunking
        # However, if there's a chance of failure during chunking, might want to commit at the very end.
        # For now, let's commit after adding document to simplify ID retrieval if needed by other parts before chunks are added.
        db.commit()
        db.refresh(db_document)
    else:
        # If document exists, clear old chunks before adding new ones.
        # This is a simple overwrite strategy.
        db.query(models.DocumentChunk).filter(models.DocumentChunk.document_id == db_document.id).delete()
        # Potentially update file_name if it has changed, or other metadata
        if original_file_name and db_document.file_name != original_file_name:
            db_document.file_name = original_file_name
        db.commit() # Commit deletion and any updates to document metadata
        db.refresh(db_document)

    full_text = extract_text_from_pdf(file_contents)
    text_chunks = chunk_text_by_paragraph(full_text)

    for i, chunk_content in enumerate(text_chunks):
        db_chunk = models.DocumentChunk(
            document_id=db_document.id,
            chunk_text=chunk_content,
            chunk_order=i
        )
        db.add(db_chunk)

    db.commit() # Commit all new chunks and document updates
    db.refresh(db_document)
    return db_document
