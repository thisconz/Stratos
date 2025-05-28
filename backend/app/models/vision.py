from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime

from app.core.db import Base

class DocumentOCR(Base):
    __tablename__ = "document_ocr"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    file_id = Column(UUID(as_uuid=True), ForeignKey("file_metadata.id"), nullable=False)
    ocr_text = Column(Text, nullable=False)
    language = Column(String, nullable=True)
    processed_at = Column(DateTime, default=datetime.utcnow)

    blocks = relationship("OCRBlock", back_populates="document", cascade="all, delete-orphan")
    file = relationship("FileMetadata")


class OCRBlock(Base):
    __tablename__ = "ocr_blocks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("document_ocr.id"), nullable=False)
    block_text = Column(Text, nullable=False)
    block_order = Column(Integer, nullable=False)

    document = relationship("DocumentOCR", back_populates="blocks")


class SmartTag(Base):
    __tablename__ = "smart_tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    file_id = Column(UUID(as_uuid=True), ForeignKey("file_metadata.id"), nullable=False)
    tag = Column(String, nullable=False)
    confidence = Column(Integer, nullable=True)  # 0-100 scale
    created_at = Column(DateTime, default=datetime.utcnow)

    file = relationship("FileMetadata")


class SearchIndex(Base):
    __tablename__ = "search_indexes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    file_id = Column(UUID(as_uuid=True), ForeignKey("file_metadata.id"), nullable=False)
    index_data = Column(Text, nullable=False)  # JSON or serialized data
    updated_at = Column(DateTime, default=datetime.utcnow)

    file = relationship("FileMetadata")
