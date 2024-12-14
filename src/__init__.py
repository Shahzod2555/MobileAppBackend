from contextlib import asynccontextmanager
from fastapi import FastAPI


from .auth.main import auth
from .user.main import user
from .database import init_db, drop_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

def create_app():
    app = FastAPI()
    app.include_router(auth, tags=['auth'], prefix='/auth')
    app.include_router(user, tags=['user'], prefix='/user')

    return app
