from sqlalchemy import Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import List, Optional
from datetime import datetime

class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    file_hash: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False) # Assuming a reasonable length for hash
    file_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True) # Assuming a reasonable length for filename
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    chunks: Mapped[List["DocumentChunk"]] = relationship("DocumentChunk", back_populates="document")

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    document_id: Mapped[int] = mapped_column(Integer, ForeignKey("documents.id"), nullable=False)
    chunk_text: Mapped[str] = mapped_column(Text, nullable=False)
    chunk_order: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    document: Mapped["Document"] = relationship("Document", back_populates="chunks")
