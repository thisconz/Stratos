from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=getattr(settings, "SQLALCHEMY_ECHO", False),
    future=True,
)

Base = declarative_base()

async_session_maker = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
    future=True,
    autocommit=False,
    autoflush=False,
)

async def get_db():
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()

async def shutdown():
    await engine.dispose()
