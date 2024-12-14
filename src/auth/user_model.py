from sqlalchemy import Column, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.hash_pwd import hash_password
from src.auth.schema import UserRegisterSchema, GetUser
from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    hash_password = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    middle_name = Column(String)

async def add_user(session: AsyncSession | AsyncSession, user_data: UserRegisterSchema) -> User:
    existing_user = await session.execute(
        select(User).where(
            (User.email == user_data.email) |
            (User.phone_number == user_data.phone_number)
        )
    )
    if existing_user.scalar_one_or_none():
        raise UserRegisterSchema

    new_user = User(email=user_data.email, phone_number=user_data.phone_number, hash_password=hash_password(user_data.password))
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user

async def get_user(session: AsyncSession, user_data=GetUser) -> User | None:
    if user_data.email:
        condition = User.email == user_data.email
    elif user_data.phone_number:
        condition = User.phone_number == user_data.phone_number
    elif user_data.id:
        condition = User.id == user_data.id
    else:
        return None
    result = await session.execute(select(User).where(condition))
    user = result.scalar_one_or_none()
    return user

async def get_users_db(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User))
    return list(result.scalars().all())

