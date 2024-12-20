from sqlalchemy.ext.asyncio import AsyncSession

from .schema import CreateOrder, OrderResponse
from ..models import Order

async def create_order(session: AsyncSession, order_data: CreateOrder) -> OrderResponse:
    if not order_data.phone_number_recipient or not order_data.first_name_recipient:
        new_order = Order(
            price=order_data.price,
            pickup_location=order_data.pickup_location,
            delivery_location=order_data.delivery_location,
            phone_number_recipient=order_data.phone_number_recipient,
            first_name_recipient=order_data.first_name_recipient,
            phone_number_sender=order_data.phone_number_sender,
            first_name_sender=order_data.first_name_sender,
        )
        session.add(new_order)
        await session.commit()
        await session.refresh(new_order)
        return new_order
