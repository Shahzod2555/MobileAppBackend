from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..utils.jtw_ import decode_jwt
from ..schema import CurrentUser, UserResponse
from ..models import Executor, Customer
from ..crud import get_current_user, get_all_users as get_all_users_crud, get_users
from ..database import get_session

user = APIRouter()

# current user
@user.post('/me')
async def current_user(authorization: str = Header(), session: AsyncSession = Depends(get_session)) -> UserResponse:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Неверный формат токена. Используйте Bearer токен.")

    decode_jwt_token = decode_jwt(token=authorization[7:])

    get_user_data = CurrentUser(
        email=decode_jwt_token['email'],
        phone_number=decode_jwt_token['phone_number'],
        customer=decode_jwt_token['customer']
    )
    current_user_data = await get_current_user(session=session, user_data=get_user_data)
    return current_user_data


# get all users
@user.get('/get-users-all')
async def get_all_users(session: AsyncSession = Depends(get_session)) -> list[UserResponse]:
    return await get_all_users_crud(session=session)


# get all executors
@user.get('/get-users-executors')
async def get_all_executors(session: AsyncSession = Depends(get_session)) -> list[UserResponse]:
    return await get_users(session=session, user_model=Executor)


# get all customers
@user.get('/get-users-customers')
async def get_all_customers(session: AsyncSession = Depends(get_session)) -> list[UserResponse]:
    return await get_users(session=session, user_model=Customer)
