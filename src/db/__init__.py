from typing import AsyncGenerator
from sqlalchemy.orm import DeclarativeBase
from ..config.builds import settings
import os
from ._db_internals import _DBInterface
from sqlalchemy.ext.asyncio import AsyncSession
from .crud import CRUDService

__all__ = ["Base", "init_db", "get_session", "CRUDService"]


class Base(DeclarativeBase):
    pass


def _register_models() -> None:
    '''imports all of the models to be registered to the database'''
    from src.models import User


async def init_db() -> None:
    """Initialize the database and create tables."""
    os.makedirs("instance", exist_ok=True)
    await _DBInterface.init_pragmas()
    engine = _DBInterface.get_engine()
    async with engine.begin() as connection:
        _register_models()
        await connection.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    '''gets a async_sessionmaker from _DBInterface'''
    async_sess = _DBInterface.get_session_factory()
    async with async_sess() as session:
        yield session
