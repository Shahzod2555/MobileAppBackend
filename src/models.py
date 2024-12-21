from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

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

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

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

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

