from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError
from jose import JWTError

from ..utils.log import logger

class ExceptionHandler:
    @staticmethod
    def handle_exception(exc):
        if isinstance(exc, HTTPException):
            logger.error(f"HTTP ошибка: {exc.detail}")
            raise exc
        elif isinstance(exc, SQLAlchemyError):
            logger.error(f"Ошибка базы данных: {exc}")
            raise HTTPException(status_code=500, detail="Ошибка работы с базой данных")
        elif isinstance(exc, ValidationError):
            logger.error(f"Ошибка базы данных: {exc}")
            raise HTTPException(status_code=500, detail="Ошибка работы с pydantic данных")
        elif isinstance(exc, JWTError):
            logger.error(f"Ошибка jwt ошибка: {exc}")
            raise HTTPException(status_code=500, detail="Ошибка работы с jwt")
        else:
            logger.error(f"Неизвестная ошибка: {exc}")
            raise HTTPException(status_code=500, detail="Ошибка сервера")
