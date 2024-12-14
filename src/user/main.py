from fastapi import APIRouter

from ..auth.jtw_ import decode_jwt
from ..auth.schema import GetUser
from ..auth.user_model import get_users_db, get_user
from ..database import SessionDep

user = APIRouter()

@user.get('/user')
async def get_users(session: SessionDep):
    users = await get_users_db(session)
    return [{i.email, i.phone_number}  for i in users]


@user.post('/me')
async def get_current_user(session: SessionDep, token: str):
    decode_jwt_token = decode_jwt(token)
    get_user_data = GetUser(id=decode_jwt_token['id'], email=decode_jwt_token['email'], phone_number=decode_jwt_token['phone_number'])
    await get_user(session=session, user_data=get_user_data)
    return decode_jwt_token
