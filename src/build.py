from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from src.db.main import init_db


@asynccontextmanager
async def life_span(app: FastAPI) -> AsyncGenerator:
    print("Starting Application...")
    await init_db()
    yield
    print("Shutting Down Application...")

def register_routes(app: FastAPI) -> None:
    from src.user.routes import user_router
    app.include_router(user_router)
