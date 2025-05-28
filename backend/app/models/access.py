from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime

from app.core.db import Base

class SharedLink(Base):
    __tablename__ = "shared_links"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    file_id = Column(UUID(as_uuid=True), ForeignKey("file_metadata.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)  # creator/owner
    token = Column(String, unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=True)
    max_downloads = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    file = relationship("FileMetadata")


class FileShare(Base):
    __tablename__ = "file_shares"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    file_id = Column(UUID(as_uuid=True), ForeignKey("file_metadata.id"), nullable=False)
    shared_with_user_id = Column(UUID(as_uuid=True), nullable=False)
    permission = Column(String, nullable=False)  # 'read', 'write', 'owner'
    shared_by_user_id = Column(UUID(as_uuid=True), nullable=False)
    shared_at = Column(DateTime, default=datetime.utcnow)

    file = relationship("FileMetadata")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    action = Column(String, nullable=False)  # 'login', 'file_upload', 'file_delete', etc.
    target_id = Column(UUID(as_uuid=True), nullable=True)
    target_type = Column(String, nullable=True)  # 'file', 'folder', 'shared_link', etc.
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)


class AccessRule(Base):
    __tablename__ = "access_rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    file_id = Column(UUID(as_uuid=True), ForeignKey("file_metadata.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    permission = Column(String, nullable=False)  # 'read', 'write', 'admin'
    created_at = Column(DateTime, default=datetime.utcnow)

    file = relationship("FileMetadata")