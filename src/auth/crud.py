from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .hash_pwd import hash_password, verify_password
from .schema import UserRegisterSchema, UserLoginSchema, CurrentUser, UserResponse
from ..models import User


async def create_user(session: AsyncSession, user_data: UserRegisterSchema) -> User:
    user_exists = await session.execute(
        select(User).where(
            (User.email == user_data.email) | (User.phone_number == user_data.phone_number)
        )
    )
    if user_exists.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Пользователь с таким email или номером телефона уже существует")

    new_user = User(
        email=user_data.email,
        phone_number=user_data.phone_number,
        hash_password=hash_password(user_data.password),
        first_name=user_data.first_name
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user

async def get_user_by_email_or_phone(user_data: UserLoginSchema, session: AsyncSession) -> User | None:
    if user_data.email:
        condition = User.email == user_data.email
    elif user_data.phone_number:
        condition = User.phone_number == user_data.phone_number
    else:
        raise HTTPException(status_code=400, detail="Необходимо указать email или номер телефона.")

    result = await session.execute(select(User).where(condition))
    user = result.scalar_one_or_none()
    if not user or not verify_password(user_data.password, user.hash_password):
        raise HTTPException(status_code=400, detail="Неверный номер телефона, email или пароль.")
    return user

async def validate_user_by_email_and_phone(user_data: CurrentUser, session: AsyncSession) -> User | None:
    user = await session.execute(
        select(User).where((User.email == user_data.email) & (User.phone_number == user_data.phone_number))
    )
    user_one_or_none = user.scalar_one_or_none()
    if not user_one_or_none:
        raise HTTPException(status_code=400, detail="Неверный номер телефона или email.")
    return user_one_or_none

async def get_all_users(session: AsyncSession) -> list[UserResponse]:
    result = await session.execute(select(User))
    users = result.scalars().all()
    return [UserResponse.from_orm(user) for user in users]
