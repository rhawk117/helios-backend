from typing import Optional
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker
from ..config.builds import settings
from sqlalchemy import text
from typing import Dict, Any


class _DBInterface:
    _engine: Optional[AsyncEngine] = None
    _session_factory: Optional[async_sessionmaker] = None

    _PRAGMAS: Dict[str, str | int] = {
        "journal_mode": "WAL",
        "foreign_keys": "ON",
        "busy_timeout": 5000
    }
    _CONNECT_ARGS: Dict[str, Any] = {
        "check_same_thread": False,
        "timeout": 30,
    }

    @classmethod
    def get_engine(cls) -> AsyncEngine:
        if cls._engine is None:
            cls._engine = create_async_engine(
                settings.DATABASE_URL,
                connect_args=cls._CONNECT_ARGS
            )
        return cls._engine

    @classmethod
    async def init_pragmas(cls) -> None:
        async with cls.get_engine().begin() as conn:
            for pragma, value in cls._PRAGMAS.items():
                await conn.execute(text(f"PRAGMA {pragma} = {value}"))

    @classmethod
    def get_session_factory(cls) -> async_sessionmaker:
        if cls._session_factory is None:
            cls._session_factory = async_sessionmaker(
                bind=cls.get_engine(),
                expire_on_commit=False
            )
        return cls._session_factory
