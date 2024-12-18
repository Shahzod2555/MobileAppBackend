from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.config import settings
from src.log import logger

engine = create_async_engine(settings.URL_DATABASE, future=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    ...

async def init_db():
    logger.info("База данных успешно создана")
    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("База данных успешно создана")
        except Exception as error:
            logger.error("Ошибка при создании базу данных: ", error)

async def drop_db():
    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.drop_all)
            logger.info("База данных успешно очищена")
        except Exception as error:
            logger.error("Ошибка при чистки базы данных: ", error)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
