from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from .auth.main import auth
from .order.main import order
from .user.main import user

from .utils import lifespan, RequestLoggerMiddleware


def create_app():
    app = FastAPI(lifespan=lifespan)
    app.add_middleware(RequestLoggerMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(auth, tags=['auth'], prefix='/auth')
    app.include_router(order, tags=['order'], prefix='/order')
    app.include_router(user, tags=['user'], prefix='/user')



    return app

