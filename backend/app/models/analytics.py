from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime

from app.core.db import Base


class StorageStats(Base):
    __tablename__ = "storage_stats"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    total_storage_bytes = Column(Integer, default=0)
    used_storage_bytes = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow)


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    action = Column(String, nullable=False)  # e.g., 'upload', 'download', 'delete'
    target_id = Column(UUID(as_uuid=True), nullable=True)
    target_type = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String, nullable=True)


class BillingRecord(Base):
    __tablename__ = "billing_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), nullable=False)
    billing_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, nullable=False)  # 'paid', 'pending', 'failed'
    transaction_id = Column(String, nullable=True)
