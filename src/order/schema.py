from pydantic import BaseModel, PastDate


class CreateOrder(BaseModel):
    id: int
    price: int
    pickup_location: str
    delivery_location: str
    phone_number_recipient: str
    first_name_recipient: str
    phone_number_sender: str
    first_name_sender: str
    customer_id: int
    executor_id: int
    created_at: PastDate
    updated_at: PastDate


class OrderResponse(BaseModel):
    price: int
    pickup_location: str
    delivery_location: str
    phone_number_recipient: str
    first_name_recipient: str
    phone_number_sender: str
    first_name_sender: str
