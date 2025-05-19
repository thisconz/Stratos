from fastapi import APIRouter, UploadFile, File, Depends, Body, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from tempfile import SpooledTemporaryFile
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

from ..auth import get_current_user
from ...core.db import get_db
from ..schemas.file import MetadataSearchQuery
from ...core.s3 import s3, BUCKET_NAME, get_presigned_url
from ...models.user import User
from ...models.file_metadata import FileMetadata

router = APIRouter()

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

async def get_next_version(object_key: str, db: AsyncSession):
    result = await db.execute(
        select(FileMetadata)
        .where(FileMetadata.object_key == object_key)
        .order_by(FileMetadata.version_number.desc())
    )
    last_entry = result.scalars().first()
    return (last_entry.version_number + 1) if last_entry else 1

class UploadMetadata(BaseModel):
    metadata: Optional[dict] = None

@router.post("/upload/{object_key}")
async def upload_file(
    object_key: str,
    file: UploadFile = File(...),
    meta: Optional[UploadMetadata] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Get next version number
    version = await get_next_version(object_key, db)
    versioned_filename = f"{object_key}_v{version}"

    # Read file content
    content = await file.read()

    # Upload to S3
    s3.put_object(Bucket=BUCKET_NAME, Key=versioned_filename, Body=content)

    metadata_dict = meta.metadata if meta else {}

    metadata = FileMetadata(
        object_key=object_key,
        filename=versioned_filename,
        version_number=version,
        size=len(content),
        uploaded_at=datetime.utcnow(),
        metadata=metadata_dict
    )
    db.add(metadata)
    await db.commit()

    return {
        "status": "uploaded",
        "object_key": object_key,
        "filename": versioned_filename,
        "version": version,
        "metadata": metadata_dict,
    }

@router.get("/download/{object_key}")
async def download_file(object_key: str, db: AsyncSession = Depends(get_db)):
    # Get latest version
    result = await db.execute(
        select(FileMetadata)
        .where(FileMetadata.object_key == object_key)
        .order_by(FileMetadata.version_number.desc())
    )
    metadata = result.scalars().first()

    if not metadata:
        return {"error": "File not found"}

    obj = s3.get_object(Bucket=BUCKET_NAME, Key=metadata.filename)
    stream = SpooledTemporaryFile()
    stream.write(obj["Body"].read())
    stream.seek(0)

    return StreamingResponse(stream, media_type="application/octet-stream", headers={
        "Content-Disposition": f"attachment; filename={metadata.filename}"
    })

@router.get("/files")
async def list_files(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(FileMetadata).where(FileMetadata.deleted == False))
    return result.scalars().all()

@router.get("/versions/{object_key}")
async def get_versions(object_key: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(FileMetadata)
        .where(FileMetadata.object_key == object_key)
        .order_by(FileMetadata.version_number.desc())
    )
    return result.scalars().all()

@router.get("/presigned/{object_key}")
async def get_presigned_download_url(
    object_key: str,
    version: int = Query(default=None),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(FileMetadata).where(FileMetadata.object_key == object_key)

    if version:
        stmt = stmt.where(FileMetadata.version_number == version)
    else:
        stmt = stmt.order_by(FileMetadata.version_number.desc())

    result = await db.execute(stmt)
    metadata = result.scalars().first()

    if not metadata:
        return {"error": "File/version not found"}

    url = get_presigned_url(metadata.filename)
    return {"url": url, "expires_in": 600}

@router.delete("/delete/{object_key}")
async def soft_delete_file(
    object_key: str,
    version: int = Query(default=None),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(FileMetadata).where(FileMetadata.object_key == object_key)

    if version:
        stmt = stmt.where(FileMetadata.version_number == version)
    else:
        stmt = stmt.order_by(FileMetadata.version_number.desc())

    result = await db.execute(stmt)
    file = result.scalars().first()

    if not file:
        return {"error": "File/version not found"}

    file.deleted = True
    await db.commit()
    return {"status": "soft_deleted", "filename": file.filename}

@router.delete("/purge/{object_key}")
async def purge_file(
    object_key: str,
    version: int = Query(default=None),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(FileMetadata).where(FileMetadata.object_key == object_key)

    if version:
        stmt = stmt.where(FileMetadata.version_number == version)
    else:
        stmt = stmt.order_by(FileMetadata.version_number.desc())

    result = await db.execute(stmt)
    file = result.scalars().first()

    if not file:
        return {"error": "File/version not found"}

    try:
        s3.delete_object(Bucket=BUCKET_NAME, Key=file.filename)
    except Exception as e:
        return {"error": f"Failed to delete from S3: {str(e)}"}

    await db.delete(file)
    await db.commit()
    return {"status": "purged", "filename": file.filename}

@router.post("/search/metadata")
async def search_by_metadata(
    metadata_filter: dict = Body(...),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(FileMetadata).where(FileMetadata.deleted == False)

    for key, value in metadata_filter.items():
        stmt = stmt.where(FileMetadata.file_metadata[key].astext == str(value))

    result = await db.execute(stmt)
    return result.scalars().all()

@router.post("/search/advanced")
async def advanced_search(
    query: MetadataSearchQuery,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(FileMetadata).where(FileMetadata.deleted == False)

    if query.exact:
        for key, value in query.exact.items():
            stmt = stmt.where(FileMetadata.file_metadata[key].astext == str(value))

    if query.partial:
        for key, value in query.partial.items():
            stmt = stmt.where(
                FileMetadata.file_metadata[key].astext.ilike(f"%{value}%")
            )

    if query.date_from:
        stmt = stmt.where(FileMetadata.uploaded_at >= query.date_from)

    if query.date_to:
        stmt = stmt.where(FileMetadata.uploaded_at <= query.date_to)

    stmt = stmt.order_by(FileMetadata.uploaded_at.desc())
    stmt = stmt.offset((query.page - 1) * query.page_size).limit(query.page_size)

    result = await db.execute(stmt)
    return result.scalars().all()

from sqlalchemy.dialects.postgresql import JSONB

@router.get("/tags/frequency")
async def get_tag_frequencies(
    key: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    if key:
        # Most frequent values for a given metadata key
        stmt = select(
            FileMetadata.file_metadata[key].astext.label("tag"),
            func.count().label("count")
        ).group_by("tag").order_by(func.count().desc()).limit(10)
    else:
        # Top-level keys frequency
        stmt = select(
            func.jsonb_object_keys(FileMetadata.file_metadata).label("tag")
        )

    result = await db.execute(stmt)
    rows = result.fetchall()

    if key:
        return [{"value": r.tag, "count": r.count} for r in rows]
    else:
        # Aggregate keys
        from collections import Counter
        counts = Counter([r.tag for r in rows])
        return [{"key": k, "count": v} for k, v in counts.most_common(10)]

@router.get("/files/suggested", response_model=List[FileOut])
def get_suggested_files(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Suggest top 5 most accessed or recent files by the user
    return (
        db.query(FileMetadata)
        .filter(FileMetadata.owner_id == current_user.id)
        .order_by(FileMetadata.access_count.desc(), FileMetadata.uploaded_at.desc())
        .limit(5)
        .all()
    )

@router.get("/files/recent", response_model=List[FileOut])
def get_recent_files(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return (
        db.query(FileMetadata)
        .filter(FileMetadata.owner_id == current_user.id)
        .order_by(FileMetadata.uploaded_at.desc())
        .limit(10)
        .all()
    )