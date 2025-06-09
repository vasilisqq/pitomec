from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from config import settings


# Ссылка на базу данных
DATABASE_URL = settings.DB_URL.get_secret_value()

# создаем движок для передачи ссылки в базы данных в sqlalchemy(создание движка)
engine = create_async_engine(DATABASE_URL)

# генератор сессий (транзакций)   (движок         класс, который будем ждать     при завершении транзакции не отключаться от базы данных) 
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# класс, который используется для миграций
class Base(DeclarativeBase):
    pass