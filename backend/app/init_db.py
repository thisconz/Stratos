import logging
from app.core.db import engine
from .models.user import Base
from .models.file_metadata import Base
import asyncio

async def init():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        logging.error(f"Database initialization failed: {e}")

if __name__ == "__main__":
    asyncio.run(init())
