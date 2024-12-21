from jose import jwt

from ..config import settings

ALGORITHM = settings.ALGORITHM
SECRET_KEY = settings.SECRET_KEY

def create_access_token(data) -> str:
    return jwt.encode(data,  SECRET_KEY, algorithm=ALGORITHM)

def decode_jwt(token: str):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
