import sys
import os
import asyncio

sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

from app.core.db import Base, engine
from app.models import user, object, document  # Ensure all models are loaded

async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Tables created.")

if __name__ == "__main__":
    asyncio.run(init())
    