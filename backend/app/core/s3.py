import re
import botocore.exceptions
import boto3
from botocore.config import Config
from .config import settings
from tempfile import SpooledTemporaryFile
from sqlalchemy import select
from ..models.file_metadata import FileMetadata
from sqlalchemy.ext.asyncio import AsyncSession

s3 = boto3.client(
    "s3",
    endpoint_url=settings.S3_ENDPOINT,
    aws_access_key_id=settings.S3_ACCESS_KEY,
    aws_secret_access_key=settings.S3_SECRET_KEY,
    config=Config(signature_version='s3v4'),
    region_name="us-east-1",
)

BUCKET_NAME = settings.S3_BUCKET

def sanitize_filename(filename):
    # Only allow alphanumeric, dash, underscore, and dot
    return re.sub(r'[^A-Za-z0-9._-]', '_', filename)

async def upload_to_s3(file, max_size=10 * 1024 * 1024):  # 10 MB limit
    try:
        content = await file.read()
        if len(content) > max_size:
            raise ValueError("File too large")
        safe_filename = sanitize_filename(file.filename)
        s3.put_object(Bucket=BUCKET_NAME, Key=safe_filename, Body=content)
        return safe_filename
    except botocore.exceptions.BotoCoreError as e:
        # Log error and return a safe error message
        raise RuntimeError("Failed to upload file to S3") from e

async def download_from_s3(filename):
    try:
        safe_filename = sanitize_filename(filename)
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=safe_filename)
        stream = SpooledTemporaryFile()
        stream.write(obj['Body'].read())
        stream.seek(0)
        return stream
    except botocore.exceptions.BotoCoreError as e:
        raise RuntimeError("Failed to download file from S3") from e

async def get_next_version(object_key: str, db: AsyncSession):
    try:
        result = await db.execute(
            select(FileMetadata)
            .where(FileMetadata.object_key == object_key)
            .order_by(FileMetadata.version_number.desc())
        )
        last_entry = result.scalars().first()
        return (last_entry.version_number + 1) if last_entry else 1
    except Exception as e:
        raise RuntimeError("Failed to get next version from database") from e

def get_presigned_url(key: str, expires_in: int = 600):
    try:
        safe_key = sanitize_filename(key)
        return s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": BUCKET_NAME, "Key": safe_key},
            ExpiresIn=expires_in
        )
    except botocore.exceptions.BotoCoreError as e:
        raise RuntimeError("Failed to generate presigned URL") from e

