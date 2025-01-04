import os
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import text
from .crud import CRUDService
from src.config.app_config import settings
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    async_sessionmaker
)
from sqlalchemy.ext.asyncio import AsyncSession


async_engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    connect_args={
        "check_same_thread": False,
        "timeout": 30
    }
)

SessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    pass

async def init_db() -> None:
    db_exists = os.path.exists("instance")
    os.makedirs("instance", exist_ok=True)
    async with async_engine.begin() as conn:
        from src.models.user import User
        await conn.run_sync(Base.metadata.create_all)
    if not db_exists:
        await seed_db()


async def get_db() -> AsyncSession:  # type: ignore
    async with SessionLocal() as session:
        yield session  # type: ignore


async def seed_db() -> None:
    from src.models.user import User, Permissions
    from src.utils.security import PasswordUtils
    async with SessionLocal() as conn:
        admin = User(
            username="admin",
            email="admin@localhost.com",
            password=PasswordUtils.hash_password(settings.ADMIN_SEED_PWD),
            permission=Permissions.admin.value
        )
        conn.add(admin)
        await conn.commit()
