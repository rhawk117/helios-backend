from .config.builds import settings
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .db.main import init_db
from typing import Any, AsyncGenerator



@asynccontextmanager
async def life_span(app: FastAPI) -> AsyncGenerator:
    print("Starting Application...")
    await init_db()
    yield
    print("Shutting Down Application...")

'''
work in progress, definitely not finished 
'''

app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    debug=settings.DEBUG,
    lifespan=life_span
)
