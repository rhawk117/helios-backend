from config import settings
from config.logging import configure_logger, LogLevels
from fastapi import FastAPI

'''
work in progress, definitely not finished 
'''

configure_logger(
    console_level=LogLevels.DEBUG,
    traceback_level=LogLevels.ERROR
)

app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    debug=settings.DEBUG
)
