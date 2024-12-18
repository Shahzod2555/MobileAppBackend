import time
from contextlib import asynccontextmanager
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request

from .log import logger
from .database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("создание базы данных")
    await init_db()
    logger.info("базы данных создана")
    yield


class RequestLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        logger.info(f"Request: {request.method} {request.url}")

        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(f"Request failed: {request.method} {request.url} | Error: {str(e)}")
            raise e

        if response.status_code == 200:
            logger.info(f"Response: {response.status_code} - {time.time() - start_time:.4f}s")
        else:
            logger.error(f"Response: {response.status_code} - {time.time() - start_time:.4f}s")

        return response