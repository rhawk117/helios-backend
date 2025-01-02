from fastapi import FastAPI

import src.build as build_tools
from src.config.app_config import settings

app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    debug=settings.DEBUG,
    lifespan=build_tools.life_span
)
build_tools.register_routes(app)
