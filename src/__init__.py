from src.config.app_config import settings
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db import init_db
from typing import Any, AsyncGenerator
import src.build as build_tools 

'''
work in progress, definitely not finished 
'''
app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    debug=settings.DEBUG,
    lifespan=build_tools.life_span
)
build_tools.register_routes(app)

