from fastapi import FastAPI
from .config.builds import settings


app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    debug=settings.DEBUG
)



