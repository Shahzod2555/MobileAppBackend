from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from ..log import logger
from ..auth.jtw_ import decode_jwt
from ..auth.schema import CurrentUser, UserResponse
from ..auth.crud import get_all_users, validate_user_by_email_and_phone
from ..database import get_session

current_user = APIRouter()

@current_user.get('/users')
async def get_users(session: AsyncSession = Depends(get_session)):
    users = await get_all_users(session)
    return [{"email": i.email, "phone_number": i.phone_number} for i in users]


@current_user.post('/me')
async def get_current_user_data(authorization: Annotated[str, Header()], session: AsyncSession = Depends(get_session)):
    logger.info(authorization)
    decode_jwt_token = decode_jwt(token=authorization)
    get_user_data = CurrentUser(email=decode_jwt_token['email'], phone_number=decode_jwt_token['phone_number'])
    user = await validate_user_by_email_and_phone(session=session, user_data=get_user_data)
    return UserResponse.model_validate(user)
