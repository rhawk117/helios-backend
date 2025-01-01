from src.db import init_db
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator
from fastapi import FastAPI


@asynccontextmanager
async def life_span(app: FastAPI) -> AsyncGenerator:
    print("Starting Application...")
    await init_db()
    yield
    print("Shutting Down Application...")


def register_routes(app: FastAPI) -> None:
    from src.user.routes import user_router
    app.include_router(user_router)
