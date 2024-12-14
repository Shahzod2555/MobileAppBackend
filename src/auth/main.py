from fastapi import APIRouter, HTTPException, Form
from typing import Annotated

from .hash_pwd import verify_password
from .jtw_ import create_access_token
from ..database import SessionDep
from ..errors import InvalidCredentialsError, UserAlreadyExistsError
from ..auth.user_model import get_user, add_user
from .schema import UserLoginSchema, GetUser, UserRegisterSchema

auth = APIRouter()

@auth.post("/login")
async def login(user_data: Annotated[UserLoginSchema, Form()], session: SessionDep):
    try:
        get_user_data = GetUser(email=user_data.email, phone_number=user_data.phone_number)
        user = await get_user(session=session, user_data=get_user_data)
        if not user or not verify_password(user_data.password, user.hash_password):
            raise InvalidCredentialsError()
        user_ = {"id": str(user.id), "email": str(user.email), "phone_number": str(user.phone_number)}
        access_token = create_access_token(data=user_)
        return {"access_token": access_token, "token_type": "bearer"}
    except InvalidCredentialsError as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ошибка сервера")

@auth.post("/register")
async def register(user_data: Annotated[UserRegisterSchema, Form()], session: SessionDep):
    try:
        add_user_data = UserRegisterSchema(email=user_data.email, phone_number=user_data.phone_number, first_name=user_data.first_name, password=user_data.password)
        user = await add_user(session=session, user_data=add_user_data)
        user_ = {"id": str(user.id), "email": str(user.email), "phone_number": str(user.phone_number)}
        access_token = create_access_token(data=user_)
        return {"access_token": access_token, "token_type": "bearer"}
    except UserAlreadyExistsError as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ошибка сервера")
