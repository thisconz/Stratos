from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from ..models.user import User
from ..models.file_metadata import FileMetadata

async def get_system_stats(db: AsyncSession) -> dict:
    try:
        total_users = (await db.execute(select(func.count(User.id)))).scalar_one() or 0
        total_files = (await db.execute(select(func.count(FileMetadata.id)))).scalar_one() or 0
        deleted_files = (await db.execute(
            select(func.count()).select_from(FileMetadata).where(FileMetadata.deleted.is_(True))
        )).scalar_one() or 0

        return {
            "total_users": total_users,
            "total_files": total_files,
            "deleted_files": deleted_files,
        }
    except Exception as e:
        # Log the error as needed
        return {
            "total_users": 0,
            "total_files": 0,
            "deleted_files": 0,
            "error": str(e)
        }
