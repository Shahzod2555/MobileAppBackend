from sqlalchemy import Column, Integer, String

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    hash_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String)
    middle_name = Column(String)
