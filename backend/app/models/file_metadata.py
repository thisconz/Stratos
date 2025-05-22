from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, JSON, func
from sqlalchemy.types import TypeDecorator, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression
import os
import json
from datetime import datetime
from cryptography.fernet import Fernet

from ..core.db import Base

class EncryptedJSON(TypeDecorator):
    """
    SQLAlchemy custom type for storing encrypted JSON data as a string.
    Uses Fernet symmetric encryption.
    """
    impl = VARCHAR
    cache_ok = True

    def __init__(self, *args, **kwargs):
        fernet_key = os.environ.get("FERNET_KEY")
        if not fernet_key:
            raise RuntimeError("FERNET_KEY environment variable not set")
        self.fernet = Fernet(fernet_key.encode())
        super().__init__(*args, **kwargs)

    def process_bind_param(self, value, dialect):
        if value is not None:
            try:
                json_str = json.dumps(value)
                encrypted = self.fernet.encrypt(json_str.encode()).decode()
                return encrypted
            except Exception as e:
                raise ValueError(f"Failed to encrypt JSON: {e}")
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            try:
                decrypted = self.fernet.decrypt(value.encode()).decode()
                return json.loads(decrypted)
            except Exception as e:
                raise ValueError(f"Failed to decrypt JSON: {e}")
        return value

class FileMetadata(Base):
    """
    SQLAlchemy model for file metadata.
    """
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)
    object_key = Column(String(255), unique=True, index=True, nullable=False)
    bucket = Column(String(128), nullable=False)
    size = Column(Integer, nullable=False)
    uploaded_at = Column(DateTime, server_default=func.now(), nullable=False)
    file_metadata = Column(EncryptedJSON, nullable=True)
    deleted = Column(Boolean, server_default=expression.false(), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User", back_populates="files")
