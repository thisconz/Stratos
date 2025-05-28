from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta, datetime
from pydantic import EmailStr

from app.core.config import settings
from app.core.db import get_db
from app.core.security import create_access_token, generate_reset_token, get_token_expiry
from app.api.deps import get_current_user, require_role
from app.services.user import get_user_by_username, get_user_by_email, verify_password, create_user, get_password_hash
from app.schemas.user import UserOut, UserCreate
from app.models.user import User, UserRole

router = APIRouter()

# -- Login --
@router.post("/token", response_model=dict)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: UserOut = Depends(get_db)):
    return current_user

# -- Register --
@router.post("/register", response_model=UserOut)
async def register_user(
    user_in: UserCreate, db: AsyncSession = Depends(get_db)
):
    existing_user = await get_user_by_username(db, user_in.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    new_user = await create_user(db, user_in)
    return new_user

@router.get("/verify-email")
async def verify_email(token: str, db: AsyncSession = Depends(get_db)):
    query = await db.execute(select(User).where(User.verification_token == token))
    user = query.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid verification token")

    user.is_verified = True
    user.verification_token = None
    await db.commit()
    return {"message": "Email successfully verified"}

@router.post("/forgot-password")
async def forgot_password(email: EmailStr, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.reset_token = generate_reset_token()
    user.reset_token_expiry = get_token_expiry(15)
    await db.commit()
    # TODO: Send reset email
    return {"msg": "Password reset link sent"}

@router.post("/reset-password")
async def reset_password(token: str, new_password: str, db: AsyncSession = Depends(get_db)):
    now = datetime.utcnow()
    query = await db.execute(
        select(User).where(User.reset_token == token, User.reset_token_expiry > now)
    )
    user = query.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user.hashed_password = get_password_hash(new_password)
    user.reset_token = None
    user.reset_token_expiry = None
    await db.commit()
    return {"msg": "Password successfully reset"}

# -- Admin --
@router.get("/admin-only")
async def admin_data(user: UserOut = Depends(require_role(UserRole.ADMIN))):
    return {"msg": "You are an Admin", "user": user.username}
