from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, EmailStr, constr

from app.core.db import get_db
from app.schemas.auth import SignInRequest, SignUpRequest, OAuthProvider
from app.api.deps import get_current_user, verify_password, create_access_token
from app.models.user import User

router = APIRouter()

class SignupRequest(BaseModel):
    email: EmailStr
    password: constr(min_length=8)
    accept_terms: bool
    plan: str  # "free", "pro", "enterprise"

@router.post("/signup", status_code=201)
async def signup(data: SignupRequest, db: AsyncSession = Depends(get_db)):
    if not data.accept_terms:
        raise HTTPException(status_code=400, detail="Terms and conditions must be accepted.")

    result = await db.execute(select(User).filter_by(email=data.email).limit(1))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered.")

    hashed_pw = get_password_hash(data.password)
    user = User(
        email=data.email,
        hashed_password=hashed_pw,
        is_active=True,
        plan=data.plan.lower(),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    # Optionally: Send verification email here

    return {"message": "User created successfully", "user_id": user.id}

@router.post("/signup")
async def sign_up(data: SignUpRequest):
    return {"message": "Sign up with email/password and T&C"}

@router.post("/oauth/{provider}")
async def oauth_sign_in(provider: OAuthProvider):
    return {"message": f"OAuth sign-in with {provider}"}

@router.get("/me", response_model=User)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    # form_data.username = email in your case
    result = await db.execute(
        select(User).filter_by(email=form_data.username).limit(1)
    )
    user = result.scalars().first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}