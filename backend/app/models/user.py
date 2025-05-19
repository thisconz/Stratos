from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, DateTime, Integer, String, func

from ..core.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, server_default=func.now())
    is_admin = Column(Boolean, default=False)

    files = relationship("FileMetadata", back_populates="owner")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', is_admin={self.is_admin})>"

    def __str__(self):
        return f"User {self.email} (ID: {self.id})"