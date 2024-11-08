"""В файле base.py мы опишем наш универсальный базовый класс.
Для начала добавим два метода:
 один для добавления одной записи,
 а второй — для массового добавления записей.
 Приготовьтесь, сейчас начнётся настоящая магия!"""

from typing import List, Any, Dict

from sqlalchemy import values, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class BaseDAO:
    model = None

    # Добавить одну запись
    @classmethod
    async def add(cls, session: AsyncSession, **values):
        new_instance = cls.model(**values)
        session.add(new_instance)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance

    @classmethod
    async def add_many(cls, session: AsyncSession, instances: List[dict[str, Any]]):
        new_instances = [cls.model(**values) for values in instances]
        session.add_all(new_instances)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instances

    # Начнем с простого примера получения всех записей из таблицы
    @classmethod
    async def get_all_users(cls, session: AsyncSession):

        # Создаем запрос для выборки всех пользователей
        query = select(cls.model)

        # Выполняем запрос и получаем результат
        result = await session.execute(query)

        # Извлекаем записи как объекты модели
        records = result.scalars().all()

        # Возвращаем список всех пользователей
        return records














