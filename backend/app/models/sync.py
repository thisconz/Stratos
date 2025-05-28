from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime

from app.core.db import Base

class SyncJob(Base):
    __tablename__ = "sync_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    device_id = Column(UUID(as_uuid=True), ForeignKey("device_info.id"), nullable=False)
    status = Column(String, nullable=False)  # 'pending', 'running', 'completed', 'failed'
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    error_message = Column(String, nullable=True)

    device = relationship("DeviceInfo", back_populates="sync_jobs")


class SyncHistory(Base):
    __tablename__ = "sync_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    sync_job_id = Column(UUID(as_uuid=True), ForeignKey("sync_jobs.id"), nullable=False)
    file_id = Column(UUID(as_uuid=True), nullable=False)
    action = Column(String, nullable=False)  # 'created', 'updated', 'deleted'
    timestamp = Column(DateTime, default=datetime.utcnow)

    sync_job = relationship("SyncJob", back_populates="history_entries")


class DeviceInfo(Base):
    __tablename__ = "device_info"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    device_name = Column(String, nullable=False)
    device_type = Column(String, nullable=True)  # 'desktop', 'mobile', 'tablet', etc.
    os = Column(String, nullable=True)
    last_seen = Column(DateTime, default=datetime.utcnow)

    sync_jobs = relationship("SyncJob", back_populates="device")
