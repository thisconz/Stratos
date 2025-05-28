from sqlalchemy import Boolean, Column, Integer, String, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
import enum
import uuid

from app.core.db import Base

class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"
    SUPERUSER = "superuser"

class User(Base):
    __tablename__ = "users"

    # -- Core --
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # -- Email verification --
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String, nullable=True)

    # -- Admin --
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)

    # -- Password reset token --
    reset_token = Column(String, nullable=True)
    reset_token_expiry = Column(DateTime, nullable=True)