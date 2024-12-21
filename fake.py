from faker import Faker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.models import Customer, Executor
from src.config import settings
import asyncio


engine = create_async_engine(settings.URL_DATABASE, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

fake = Faker()

async def add_fake_users():
    async with async_session() as session:
        for _ in range(50):
            session.add(
                Customer(
                    email=fake.email(), phone_number=fake.phone_number(),
                    hash_password="password123",
                    first_name=fake.first_name(), last_name=fake.last_name(),
                    middle_name=fake.first_name(), role_name="customer"
                )
            )

        for _ in range(50):
            session.add(
                Executor(
                    email=fake.email(), phone_number=fake.phone_number(),
                    hash_password="password123",
                    first_name=fake.first_name(), last_name=fake.last_name(),
                    middle_name=fake.first_name(), role_name="executor"
                )
            )

        await session.commit()


asyncio.run(add_fake_users())
