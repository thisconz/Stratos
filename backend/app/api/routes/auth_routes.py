from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, EmailStr, validator

from ...models.user import User
from ..auth import create_access_token, verify_password, get_password_hash
from ...core.db import get_db

router = APIRouter()

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

    @classmethod
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        # Add more checks as needed (uppercase, numbers, etc.)
        return value

    _validate_password = validator('password', allow_reuse=True)(validate_password)

@router.post("/register")
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    exists = await db.execute(select(User).where(User.email == data.email))
    if exists.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already in use")
    hashed_password = get_password_hash(data.password)
    user = User(email=data.email, hashed_password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {"message": "Account created"}

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

async def authenticate_user(email: str, password: str, db: AsyncSession):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}