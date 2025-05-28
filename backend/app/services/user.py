from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import generate_verification_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -- Hash password --
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# -- Password verify --
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# -- String ID --   
def generate_id() -> str:
    return "usr_" + secrets.token_hex(6)

# -- Get user by username --
async def get_user_by_username(db: AsyncSession, username: str) -> User:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()

# -- Get user by email --
async def get_user_by_email(db: AsyncSession, email: str) -> User:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

# -- Create user --
async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        verification_token=generate_verification_token(),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    # TODO: Send verification email with user.verification_token
    return user