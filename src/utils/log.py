import logging
from fastapi import Request
import time
from starlette.middleware.base import BaseHTTPMiddleware
from colorlog import ColoredFormatter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = ColoredFormatter(
    "%(log_color)s%(levelname)-8s %(asctime)s %(reset)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors={"INFO": "green", "ERROR": "red"},
)
handler.setFormatter(formatter)
logger.addHandler(handler)


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
