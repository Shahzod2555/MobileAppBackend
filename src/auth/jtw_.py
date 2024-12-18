from fastapi import HTTPException
from jose import jwt, JWTError

from ..config import settings

ALGORITHM = settings.ALGORITHM
SECRET_KEY = settings.SECRET_KEY

def create_access_token(data) -> str:
    user_data = {
        "id": str(data.id),
        "email": data.email,
        "phone_number": data.phone_number
    }
    return jwt.encode(user_data,  SECRET_KEY, algorithm=ALGORITHM)


def decode_jwt(token: str):
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Неверный токен или токен истек")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Ошибка при декодировании токена")
