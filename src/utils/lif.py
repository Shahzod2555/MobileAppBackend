from contextlib import asynccontextmanager
from fastapi import FastAPI

from .log import logger
from ..database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("создание базы данных")
    await init_db()
    logger.info("базы данных создана")
    yield
