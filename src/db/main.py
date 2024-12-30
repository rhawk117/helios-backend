from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool
from typing import AsyncGenerator, Any, Dict
from ..config.builds import settings
from ..config.logging import logger


_ENGINE_OPTIONS: Dict[str, Any] = {
    "echo": settings.DB_ECHO,
    "poolclass": NullPool,  # no benefit from connection pooling -> null pool
    "connect_args": {
        "check_same_thread": False,  # Required for async SQLite connections
        "timeout": 30,
    }
}

_SQLITE_PRAGMAS: Dict[str, Any] = {
    "journal_mode": "WAL",          # write-ahead logging for better concurrency
    "foreign_keys": "ON",           # referential integrity
    "synchronous": "NORMAL",        # Balance safety and performance
    "busy_timeout": 5000,           # Wait up to 5s when database is locked
    "auto_vacuum": "INCREMENTAL",   # Better than FULL for performance
    "cache_size": -2000,            # Use 2MB of memory for cache
    "temp_store": "MEMORY",         # Store temp tables in memory
}

class Base(DeclarativeBase):
    pass

class Database:
    _engine: AsyncEngine = None
    _session_factory: async_sessionmaker = None

    @classmethod
    def get_engine(cls) -> AsyncEngine:
        if cls._engine is None:
            cls._engine = create_async_engine(
                settings.DATABASE_URL,
                **_ENGINE_OPTIONS
            )
        return cls._engine

    @classmethod
    def get_session_factory(cls) -> async_sessionmaker:
        if cls._session_factory is None:
            cls._session_factory = async_sessionmaker(
                bind=cls.get_engine(),
                expire_on_commit=False,  # avoid DetachedInstanceError
                autoflush=False,         # prevent unexpected flushes
                autocommit=False         # explicit transaction management
            )
        return cls._session_factory


async def get_session() -> AsyncSession:
    '''yields an async session; preserves context manager'''
    async_session = Database.get_session_factory()
    async with async_session() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.error(f"Session Error: {str(e)}", exc_info=True)
            raise


async def set_sqlite_pragmas() -> None:
    """configures SQLite with optimal performance and safety settings"""
    try:
        async with Database.get_engine().begin() as conn:
            for pragma, value in _SQLITE_PRAGMAS.items():
                assert isinstance(pragma, str), f"Invalid pragma: {pragma}"
                assert isinstance(value, (str, int)), f"Invalid value for {
                    pragma}: {value}"
                await conn.execute(f"PRAGMA {pragma} = {value};")

            result = await conn.execute("PRAGMA journal_mode;")
            mode = await result.scalar()
            if mode.upper() != "WAL":
                logger.warning(
                    "WAL mode not enabled. This may impact performance."
                )
    except Exception as e:
        logger.error(f"Failed to set SQLite PRAGMAs: {str(e)}", exc_info=True)
        raise


async def init_db() -> None:
    """initializes the database and apply SQLite PRAGMAs."""
    logger.info("Initializing SQLite Database...")
    try:
        await set_sqlite_pragmas()
        async with Database.get_engine().begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Database initialization failed: {
                     str(e)}", exc_info=True)
        raise


async def drop_db() -> None:
    logger.warning("Dropping database tables...")
    try:
        async with Database.get_engine().begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        logger.warning("Database tables dropped successfully.")
    except Exception as e:
        logger.error(f"Failed to drop database: {str(e)}", exc_info=True)
        raise
