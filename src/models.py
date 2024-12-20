from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


# Заказчик
class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)

    email = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(12), unique=True, nullable=False)
    hash_password = Column(String(128), nullable=False)

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50))
    middle_name = Column(String(50))

    role_name = Column(String(50))

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    orders = relationship("Order", back_populates="customer")


# Исполнитель
class Executor(Base):
    __tablename__ = "executors"

    id = Column(Integer, primary_key=True, autoincrement=True)

    email = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(12), unique=True, nullable=False)
    hash_password = Column(String(128), nullable=False)

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50))
    middle_name = Column(String(50))

    role_name = Column(String(50))

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    orders = relationship("Order", back_populates="executor")


# Заказ
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(Integer, nullable=False)

    pickup_location  = Column(String(255), nullable=False)  # откуда
    delivery_location = Column(String(255), nullable=False)  # куда

    phone_number_recipient = Column(String(12), nullable=False)  # получателя
    first_name_recipient = Column(String(50), nullable=False)  # получателя

    phone_number_sender = Column(String(12), nullable=False)  # отправителя
    first_name_sender = Column(String(50), nullable=False)  # отправителя

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    customer_id = Column(ForeignKey("customers.id"), nullable=False, index=True)
    executor_id = Column(ForeignKey("executors.id"), index=True)

    customer = relationship("Customer", back_populates="orders")
    executor = relationship("Executor", back_populates="orders")
