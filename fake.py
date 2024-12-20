from faker import Faker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.models import Customer, Executor, Order
from src.auth.hash_pwd import hash_password
from src.config import settings

engine = create_async_engine(settings.URL_DATABASE, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

fake = Faker()

async def add_fake_users():
    async with async_session() as session:
        # Добавляем фейковых заказчиков
        customers = []
        for _ in range(100):
            fake_customer = Customer(
                email=fake.email(),
                phone_number=fake.phone_number(),
                hash_password=hash_password("password123"),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                middle_name=fake.first_name(),
                role_name="customer"
            )
            session.add(fake_customer)
            customers.append(fake_customer)

        await session.flush()  # Сохраняем, чтобы получить id

        # Добавляем фейковые заказы
        for customer in customers:
            fake_order = Order(
                price=fake.random_int(min=2000, max=10000),
                pickup_location=fake.address(),
                delivery_location=fake.address(),
                phone_number_recipient=fake.phone_number(),
                first_name_recipient=fake.first_name(),
                phone_number_sender=fake.phone_number(),
                first_name_sender=fake.first_name(),
                customer_id=customer.id  # Привязка заказа к заказчику
            )
            session.add(fake_order)

        # Добавляем фейковых исполнителей
        for _ in range(100):
            fake_executor = Executor(
                email=fake.email(),
                phone_number=fake.phone_number(),
                hash_password=hash_password("password123"),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                middle_name=fake.first_name(),
                role_name="executor"
            )
            session.add(fake_executor)

        await session.commit()


# Запуск скрипта
import asyncio
asyncio.run(add_fake_users())
