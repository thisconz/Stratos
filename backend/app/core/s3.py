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

async def upload_to_s3(file):
    content = await file.read()
    s3.put_object(Bucket=BUCKET_NAME, Key=file.filename, Body=content)
    return file.filename

async def download_from_s3(filename):
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=filename)
    stream = SpooledTemporaryFile()
    stream.write(obj['Body'].read())
    stream.seek(0)
    return stream

async def get_next_version(object_key: str, db: AsyncSession):
    result = await db.execute(
        select(FileMetadata)
        .where(FileMetadata.object_key == object_key)
        .order_by(FileMetadata.version_number.desc())
    )
    last_entry = result.scalars().first()
    return (last_entry.version_number + 1) if last_entry else 1

def get_presigned_url(key: str, expires_in: int = 600):
    return s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": BUCKET_NAME, "Key": key},
        ExpiresIn=expires_in
    )
