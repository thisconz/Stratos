from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from ..models.user import User
from ..models.file_metadata import FileMetadata

async def get_system_stats(db: AsyncSession) -> dict:
    total_users = await db.scalar(select(func.count(User.id)))
    total_files = await db.scalar(select(func.count(FileMetadata.id)))
    deleted_files = await db.scalar(select(func.count(FileMetadata.id)).where(FileMetadata.deleted == True))

    return {
        "total_users": total_users or 0,
        "total_files": total_files or 0,
        "deleted_files": deleted_files or 0,
    }
