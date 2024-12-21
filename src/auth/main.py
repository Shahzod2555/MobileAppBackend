from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..utils.jtw_ import create_access_token
from ..database import get_session
from ..crud import get_user, create_user
from ..schema import UserLoginSchema, UserRegisterSchema

auth = APIRouter()

# login auth
@auth.post("/login")
async def login_auth(user_data: UserLoginSchema, session: AsyncSession = Depends(get_session)):
    user = await get_user(session=session, user_data=user_data)
    return {"access_token": create_access_token(data=user.model_dump())}

# register auth
@auth.post("/register")
async def register_auth(user_data: UserRegisterSchema, session: AsyncSession = Depends(get_session)):
    user = await create_user(session=session, user_data=user_data)
    return {"access_token": create_access_token(data=user.model_dump())}
