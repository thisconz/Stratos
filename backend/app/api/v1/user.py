from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api.deps import get_current_user, get_db
from app.schemas.user import UserOut
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[UserOut])
async def list_users(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute("SELECT id, username FROM users")
    users = result.all()
    return [{"id": u.id, "username": u.username} for u in users]