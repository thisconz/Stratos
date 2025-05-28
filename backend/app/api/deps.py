import time
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from jose import JWTError, jwt, ExpiredSignatureError
from typing import Optional, List
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime, timedelta

from ..core.db import async_session_maker
from ..models.user import User
from ..core.config import settings
from ..core.db import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
serializer = URLSafeTimedSerializer(settings.SECRET_KEY)

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

async def get_db() -> AsyncSession: # type: ignore
    async with async_session_maker() as session:
        yield session

def raise_credentials_exception():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise_credentials_exception()
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise_credentials_exception()

    result = await db.execute(select(User).filter_by(id=user_id).limit(1))
    user = result.scalars().first()
    if user is None or not user.is_active:
        raise_credentials_exception()
    return user

def get_current_admin(required_scopes: Optional[List[str]] = None):
    async def _verify_admin(current_user: User = Depends(get_current_user)) -> User:
        if not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Not enough permissions")

        # Optional scope check from JWT payload
        if required_scopes:
            token_scopes = current_user.scopes if hasattr(current_user, "scopes") else []
            missing = [scope for scope in required_scopes if scope not in token_scopes]
            if missing:
                raise HTTPException(
                    status_code=403,
                    detail=f"Missing required scopes: {', '.join(missing)}"
                )

        return current_user
    return _verify_admin

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def generate_email_verification_token(email: str) -> str:
    return serializer.dumps(email, salt="email-confirm")

def verify_email_token(token: str, max_age: int = 3600) -> str:
    try:
        return serializer.loads(token, salt="email-confirm", max_age=max_age)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if "sub" not in to_encode:
        raise ValueError("Token payload must include 'sub' claim")
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> int:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return int(user_id)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")