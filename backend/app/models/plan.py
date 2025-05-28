from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from app.core.db import Base

class Plan(Base):
    __tablename__ = "plans"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    price_cents = Column(Integer, nullable=False)
    description = Column(String)
