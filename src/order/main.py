from fastapi import APIRouter, Depends

from .crud import create_order
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Order
from .schema import OrderResponse, CreateOrder

from ..database import get_session

order = APIRouter()


@order.get('/get-orders')
async def get_orders(session: AsyncSession = Depends(get_session)) -> list[OrderResponse]:
    result = await session.execute(select(Order))
    orders = result.scalars().all()
    return [order for order in orders]



@order.post("/create-order")
async def create_item(order_data: CreateOrder, session: AsyncSession = Depends(get_session)):
    try:
        order = await create_order(session=session, user_data=user_data)
        return order
    except Exception as e:
        ExceptionHandler.handle_exception(e)