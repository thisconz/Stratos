from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime

from app.core.db import Base


class ExternalCloudAccount(Base):
    __tablename__ = "external_cloud_accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    provider = Column(String, nullable=False)  # 'google_drive', 'dropbox', 'onedrive', etc.
    external_user_id = Column(String, nullable=False)
    access_token = Column(Text, nullable=False)
    refresh_token = Column(Text, nullable=True)
    token_expiry = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    linked_at = Column(DateTime, default=datetime.utcnow)
    last_sync_at = Column(DateTime, nullable=True)

    # Optional: relationship to SyncJobs if syncing across providers


class ExternalFileMapping(Base):
    __tablename__ = "external_file_mappings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    external_cloud_account_id = Column(UUID(as_uuid=True), ForeignKey("external_cloud_accounts.id"), nullable=False)
    external_file_id = Column(String, nullable=False)
    stratos_file_id = Column(UUID(as_uuid=True), ForeignKey("file_metadata.id"), nullable=False)
    synced_at = Column(DateTime, default=datetime.utcnow)

    external_account = relationship("ExternalCloudAccount")
    file_metadata = relationship("FileMetadata")
