from passlib.context import CryptContext
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, DateTime, Integer, String, func

from ..core.db import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, server_default=func.now())
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    files = relationship(
        "FileMetadata",
        back_populates="owner",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def set_password(self, password: str):
        self.hashed_password = pwd_context.hash(password)

    def verify_password(self, password: str):
        return pwd_context.verify(password, self.hashed_password)

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', is_admin={self.is_admin})>"

    def __str__(self):
        return f"User {self.email} (ID: {self.id})"