from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .utils.hash_pwd import hash_password, verify_password
from .schema import UserRegisterSchema, UserLoginSchema, UserResponse, CurrentUser
from .models import Executor, Customer

# create user
async def create_user(session: AsyncSession, user_data: UserRegisterSchema) -> UserResponse:
    role, model = (True, Customer) if user_data.customer else (False, Executor)
    user_exists = await session.execute(
        select(model).where((model.email == user_data.email) | (model.phone_number == user_data.phone_number))
    )
    if user_exists.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Заказчик с таким email или номером телефона уже существует")

    new_user = model(
        email=user_data.email,
        phone_number=user_data.phone_number,
        hash_password=hash_password(user_data.password),
        first_name=user_data.first_name,
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return UserResponse.model_validate(new_user).model_copy(update={"customer": bool(role)})


# get user
async def get_user(session: AsyncSession, user_data: UserLoginSchema) -> UserResponse:
    role, model = (True, Customer) if user_data.customer else (False, Executor)

    if user_data.email:
        condition = model.email == user_data.email
    elif user_data.phone_number:
        condition = model.phone_number == user_data.phone_number
    else:
        raise HTTPException(status_code=400, detail="Необходимо указать email или номер телефона.")

    result = await session.execute(select(model).where(condition))
    user = result.scalar_one_or_none()

    if not user or not verify_password(user_data.password, user.hash_password):
        raise HTTPException(status_code=400, detail="Неверный номер телефона, email или пароль.")

    return UserResponse.model_validate(user).model_copy(update={"customer": bool(role)})


# get all users
async def get_all_users(session: AsyncSession) -> list[UserResponse]:
    executor_result = await get_users(session=session, user_model=Executor)
    customer_result = await get_users(session=session, user_model=Customer)

    all_users = executor_result + customer_result
    return [UserResponse.model_validate(user) for user in all_users]


# get users
async def get_users(session: AsyncSession, user_model) -> list[UserResponse]:
    result = await session.execute(select(user_model))
    users = result.scalars().all()
    return [UserResponse.model_validate(user) for user in users]


# get current user
async def get_current_user(session: AsyncSession, user_data: CurrentUser) -> UserResponse:
    role, model = (True, Customer) if user_data.customer else (False, Executor)
    result = await session.execute(
        select(model).where((model.email == user_data.email) & (model.phone_number == user_data.phone_number))
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="Пользователь с таким email или номером телефона не существует")
    return UserResponse.model_validate(user).model_copy(update={"customer": bool(role)})
