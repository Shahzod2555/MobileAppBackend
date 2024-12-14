from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

engine = create_async_engine("sqlite+aiosqlite:///./database.db", future=True)

Base = declarative_base()

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.create_all)
            print("База данных успешно создана")
        except Exception as error:
            print("Ошибка при создании базу данных: ", error)
async def drop_db():
    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.drop_all)
            print("База данных успешно очищена")
        except Exception as error:
            print("Ошибка при чистки базы данных: ", error)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]
