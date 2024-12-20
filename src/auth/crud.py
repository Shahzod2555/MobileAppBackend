from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..auth.hash_pwd import hash_password, verify_password
from ..auth.schema import UserRegisterSchema, UserLoginSchema, UserResponse
from ..models import Executor, Customer


async def create_user(session: AsyncSession, user_data: UserRegisterSchema):
    if user_data.executor_or_customer:
        user = await create_executor(session=session, executor_data=user_data)
    else:
        user = await create_customer(session=session, customer_data=user_data)
    return user


async def create_customer(session: AsyncSession, customer_data: UserRegisterSchema) -> Customer:
    customer_exists = await session.execute(
        select(Customer).where(
            (Customer.email == customer_data.email) | (Customer.phone_number == customer_data.phone_number)
        )
    )
    if customer_exists.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Заказчик с таким email или номером телефона уже существует")

    new_customer = Customer(
        email=customer_data.email,
        phone_number=customer_data.phone_number,
        hash_password=hash_password(customer_data.password),
        first_name=customer_data.first_name,
        last_name=customer_data.last_name,
        middle_name=customer_data.middle_name,
    )
    session.add(new_customer)
    await session.commit()
    await session.refresh(new_customer)
    return new_customer


async def create_executor(session: AsyncSession, executor_data: UserRegisterSchema) -> Executor:
    executor_exists = await session.execute(
        select(Executor).where(
            (Executor.email == executor_data.email) | (Executor.phone_number == executor_data.phone_number)
        )
    )
    if executor_exists.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Исполнитель с таким email или номером телефона уже существует")

    new_executor = Executor(
        email=executor_data.email,
        phone_number=executor_data.phone_number,
        hash_password=hash_password(executor_data.password),
        first_name=executor_data.first_name,
        last_name=executor_data.last_name,
        middle_name=executor_data.middle_name,
    )
    session.add(new_executor)
    await session.commit()
    await session.refresh(new_executor)
    return new_executor


async def get_user(session: AsyncSession, user_data: UserLoginSchema):
    user_model = Executor if user_data.executor_or_customer else Customer

    if user_data.email:
        condition = user_model.email == user_data.email
    elif user_data.phone_number:
        condition = user_model.phone_number == user_data.phone_number
    else:
        raise HTTPException(status_code=400, detail="Необходимо указать email или номер телефона.")

    result = await session.execute(select(user_model).where(condition))
    user = result.scalar_one_or_none()

    if not user or not verify_password(user_data.password, user.hash_password):
        raise HTTPException(status_code=400, detail="Неверный номер телефона, email или пароль.")
    return user



async def get_current_user(user_data: CurrentUser, session: AsyncSession):
    decode_jwt_token = decode_jwt(token=authorization)
    get_user_data = CurrentUser(
        email=decode_jwt_token['email'], phone_number=decode_jwt_token['phone_number']
        )
    current_user_data = await get_user(session=session, user_data=get_user_data)
    return UserResponse.model_validate(current_user_data)






async def get_all_users(session: AsyncSession) -> list[UserResponse]:
    executor_result = await session.execute(select(Executor))
    customer_result = await session.execute(select(Customer))

    executors = executor_result.scalars().all()  # Преобразуем в список
    customers = customer_result.scalars().all()  # Преобразуем в список

    all_users = executors + customers
    return [UserResponse.model_validate(user) for user in all_users]


async def get_users(session: AsyncSession, user_model) -> list[UserResponse]:
    result = await session.execute(select(user_model))
    users = result.scalars().all()
    return [UserResponse.model_validate(user) for user in users]