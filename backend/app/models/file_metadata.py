from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import relationship

from ..core.db import Base

class FileMetadata(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)
    object_key = Column(String, unique=True, index=True)
    bucket = Column(String)
    size = Column(Integer)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    file_metadata = Column(JSON)
    deleted = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="files")