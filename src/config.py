from pydantic_settings import BaseSettings
from typing import ClassVar

class Config(BaseSettings):
    URL_DATABASE: str = "sqlite+aiosqlite:///./database.db"
    ALGORITHM: ClassVar[str] = "HS256"
    SECRET_KEY: ClassVar[str] = 'ОРГК94%$#@#f%$#u&^$UH632C4TWF0Т3492043-9ВЧ11ЬЧ-321ТЬ9-№к№2К3223r$#t@$%yt#t@4317СТ65-1'

settings = Config()
