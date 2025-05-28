from pydantic import BaseModel, EmailStr
from enum import Enum as PyEnum
from typing import Optional
from uuid import UUID

class UserRole(str, PyEnum):
    USER = "user"
    ADMIN = "admin"
    SUPERUSER = "superuser"

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    is_verified: bool
    role: UserRole

    class Config:
        orm_mode = True