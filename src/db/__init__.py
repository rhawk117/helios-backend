from typing import AsyncGenerator
from sqlalchemy.orm import DeclarativeBase
from ..config.app_config import settings
import os
from ._db_internals import _DBInterface
from sqlalchemy.ext.asyncio import AsyncSession
from .crud import CRUDService

__all__ = ["Base", "init_db", "get_session", "CRUDService"]


class Base(DeclarativeBase):
    pass

    
async def init_db() -> None:
    """Initialize the database and create tables."""
    tables_exist = os.path.exists("instance")
    os.makedirs("instance", exist_ok=True)
    await _DBInterface.init_pragmas()
    engine = _DBInterface.get_engine()
    async with engine.begin() as connection:
        from src.models import User
        await connection.run_sync(Base.metadata.create_all)
    if not tables_exist:
        await _init_db_defaults()

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    '''gets a async_sessionmaker from _DBInterface'''
    async_sess = _DBInterface.get_session_factory()
    async with async_sess() as session:
        async with session.begin():
            yield session

async def drop_tables() -> None:
    '''drops all tables in the database'''
    if settings.DEBUG == False:
        raise Exception("Cannot drop tables when DEBUG is 'False'")
    engine = _DBInterface.get_engine()
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
