import time
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import JWTError, jwt
from typing import Optional, List

from ..core.db import async_session_maker
from ..models.user import User
from ..core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

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
    allowed_algorithms = {"HS256", "RS256"}
    if settings.ALGORITHM not in allowed_algorithms:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Invalid JWT algorithm configuration"
        )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        exp = payload.get("exp")
        if username is None or exp is None or exp < time.time():
            raise_credentials_exception()
    except JWTError:
        raise_credentials_exception()

    result = await db.execute(
        select(User).filter_by(email=username).limit(1)
    )
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