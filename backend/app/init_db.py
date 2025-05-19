from app.core.db import engine
from .models.user import Base
from .models.file_metadata import Base
import asyncio

async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init())
