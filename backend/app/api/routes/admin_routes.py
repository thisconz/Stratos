from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from ...models.user import User
from ...models.file_metadata import FileMetadata
from ...core.db import get_db
from ..dependencies import get_current_admin
from ..schemas.user import UserOut
from ..schemas.stats import StatsResponse
from ..analytics import get_system_stats

router = APIRouter()

@router.get("/users", response_model=list[UserOut])
async def list_users(
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin),
    skip: int = 0,
    limit: int = 100
):
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()

@router.get("/stats", response_model=StatsResponse)
async def system_stats(db: AsyncSession = Depends(get_db), admin=Depends(get_current_admin)):
    stats = await get_system_stats(db)
    return StatsResponse(**stats)
