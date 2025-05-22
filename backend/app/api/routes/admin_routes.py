from fastapi import APIRouter, Depends, Query, Security 
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from ...models.user import User
from ...models.file_metadata import FileMetadata
from ...core.db import get_db
from ..dependencies import get_current_admin
from ..schemas.user import UserOut, PaginatedUsers
from ..schemas.stats import StatsResponse
from ..analytics import get_system_stats

router = APIRouter()

@router.get(
    "/users",
    response_model=PaginatedUsers,
    description="Retrieve a paginated list of users. Requires admin privileges.",
    response_description="A paginated response containing user objects and pagination metadata."
)
async def list_users(
    db: AsyncSession = Depends(get_db),
    admin=Security(get_current_admin, scopes=["users:read"]),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of users to return (max 100)")
):
    """
    List users with pagination and metadata.
    """
    MAX_LIMIT = 100
    if skip < 0:
        skip = 0
    if limit < 1 or limit > MAX_LIMIT:
        limit = MAX_LIMIT
    try:
        total = await db.scalar(select(func.count()).select_from(User))
        result = await db.execute(select(User).offset(skip).limit(limit))
        users = result.scalars().all()
        return PaginatedUsers(
            total=total,
            skip=skip,
            limit=limit,
            users=[UserOut.from_orm(u) for u in users]
        )
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error occurred.")

@router.get(
    "/stats",
    response_model=StatsResponse,
    description="Retrieve system statistics. Requires admin privileges.",
    response_description="A response containing system statistics."
)
async def system_stats(
    db: AsyncSession = Depends(get_db),
    admin=Security(get_current_admin, scopes=["stats:read"])
):
    """
    Get system statistics.
    """
    try:
        stats = await get_system_stats(db)
        return StatsResponse(**stats)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error occurred.")
