from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from src.config.builds import settings
from sqlmodel import SQLModel
from typing import AsyncGenerator
from src.config.logging import logger

engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO
)


async def init_db() -> None:
    logger.info("Creating database tables")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    logger.info("Database tables created")


async def get_session() -> AsyncGenerator:
    async with AsyncSession(bind=engine) as session:
        yield session


async def drop_db() -> None:
    logger.warning("Dropping database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
