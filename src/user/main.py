from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from ..auth.jtw_ import decode_jwt
from ..auth.schema import CurrentUser, UserResponse
from ..models import Executor, Customer
from ..auth.crud import (
    get_user as get_user_crud,
    get_all_users as get_all_users_crud,
    get_users as get_users_crud
)
from ..database import get_session

user = APIRouter()


@user.post('/me')
async def get_current_user_data(authorization: Annotated[str, Header()], session: AsyncSession = Depends(get_session)) -> UserResponse:
    decode_jwt_token = decode_jwt(token=authorization)
    get_user_data = CurrentUser(email=decode_jwt_token['email'], phone_number=decode_jwt_token['phone_number'])
    current_user_data = await get_user_crud(session=session, user_data=get_user_data)
    return UserResponse.model_validate(current_user_data)


@user.get('/get-users-all')
async def get_all_users(session: AsyncSession = Depends(get_session)) -> list[UserResponse]:
    users = await get_all_users_crud(session=session)
    return [UserResponse.model_validate(user_) for user_ in users]

@user.get('/get-users-executors')
async def get_all_executors(session: AsyncSession = Depends(get_session)) -> list[UserResponse]:
    users = await get_users_crud(session=session, user_model=Executor)
    return [UserResponse.model_validate(user_) for user_ in users]


@user.get('/get-users-customers')
async def get_all_customers(session: AsyncSession = Depends(get_session)) -> list[UserResponse]:
    users = await get_users_crud(session=session, user_model=Customer)
    return [UserResponse.model_validate(user_) for user_ in users]