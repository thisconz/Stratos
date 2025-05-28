from minio import Minio
import asyncio
from concurrent.futures import ThreadPoolExecutor

from app.core.config import settings

executor = ThreadPoolExecutor()

client = Minio(
    settings.S3_ENDPOINT,
    access_key=settings.S3_ACCESS_KEY,
    secret_key=settings.S3_SECRET_KEY,
    secure=False
)

async def init_bucket():
    def _check_create():
        if not client.bucket_exists(settings.S3_BUCKET):
            client.make_bucket(settings.S3_BUCKET)

    await asyncio.get_event_loop().run_in_executor(executor, _check_create)

async def generate_presigned_upload_url(object_name: str, expires: int = 3600):
    return await asyncio.get_event_loop().run_in_executor(
        executor,
        lambda: client.presigned_put_object(settings.S3_BUCKET, object_name, expires)
    )

async def generate_presigned_download_url(object_name: str, expires: int = 3600):
    return await asyncio.get_event_loop().run_in_executor(
        executor,
        lambda: client.presigned_get_object(settings.S3_BUCKET, object_name, expires)
    )