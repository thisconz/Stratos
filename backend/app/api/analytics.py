from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from ..models.user import User
from ..models.file_metadata import FileMetadata

async def get_system_stats(db: AsyncSession) -> dict:
    stmt = select(
        func.count(User.id),
        func.count(FileMetadata.id),
        func.count().filter(FileMetadata.deleted.is_(True))
    )
    result = await db.execute(stmt)
    total_users, total_files, deleted_files = result.one()

    return {
        "total_users": total_users or 0,
        "total_files": total_files or 0,
        "deleted_files": deleted_files or 0,
    }
