import jwt
from jwt import PyJWTError
import secrets
from datetime import datetime, timezone, timedelta

from app.core.config import settings

class CredentialsException(Exception):
    pass

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False}
        )
        
        exp = payload.get("exp")
        if exp is not None:
            expire_time = datetime.fromtimestamp(exp, tz=timezone.utc)
            if expire_time < datetime.now(tz=timezone.utc):
                raise CredentialsException("Token expired")
        
        return payload

    except PyJWTError as e:
        raise CredentialsException(f"Could not validate credentials: {str(e)}")

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()

    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# -- Generate Verification Token --
def generate_verification_token() -> str:
    return secrets.token_urlsafe(32)

# -- Reset token generator --
def generate_reset_token() -> str:
    return secrets.token_urlsafe(32)

def get_token_expiry(minutes: int = 15):
    return datetime.utcnow() + timedelta(minutes=minutes)
