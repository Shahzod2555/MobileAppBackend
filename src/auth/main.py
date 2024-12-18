from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .jtw_ import create_access_token
from ..database import get_session
from .crud import get_user_by_email_or_phone, create_user
from .schema import UserLoginSchema, UserRegisterSchema
from ..errors import ExceptionHandler

auth = APIRouter()


@auth.post("/login")
async def login_auth(user_data: UserLoginSchema, session: AsyncSession = Depends(get_session)):
    try:
        user = await get_user_by_email_or_phone(session=session, user_data=user_data)
        return {"access_token": create_access_token(data=user)}
    except Exception as e:
        ExceptionHandler.handle_exception(e)


@auth.post("/register")
async def register_auth(
        user_data: UserRegisterSchema,
        session: AsyncSession = Depends(get_session)):
    try:
        user = await create_user(session=session, user_data=user_data)
        return {"access_token": create_access_token(data=user)}
    except Exception as e:
        ExceptionHandler.handle_exception(e)
