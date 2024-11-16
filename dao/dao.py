"""Теперь, для того, чтоб это все работало,
нам необходимо создать дочерний класс под каждую таблицу.
Для этого, в корне пакета dao, давайте создадим файл dao.py и опишем дочерние классы."""

from sqlalchemy import values, select
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession

from dao.base import BaseDAO
from models import Profile, User, Post, Comment

class UserDAO(BaseDAO):
    model = User

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

    @classmethod
    async def add_user_with_profile(cls, session: AsyncSession, user_data: dict) -> User:

        """
                Добавляет пользователя и привязанный к нему профиль.

                Аргументы:
                - session: AsyncSession - асинхронная сессия базы данных
                - user_data: dict - словарь с данными пользователя и профиля

                Возвращает:
                - User - объект пользователя
        """
        # Создаем пользователя из переданных данных
        user = cls.model(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
        )
        session.add(user)
        await session.flush()  # Чтобы получить user.id для профиля

        """user_data — это словарь,
        и у словарей в Python действительно есть метод .get().
        Этот метод используется для получения значения по заданному ключу. 
        Преимущество dict.get() в том, что если ключ отсутствует, 
        он возвращает None 
        (или любое другое значение по умолчанию, если вы его укажете) 
        вместо генерации ошибки KeyError, 
        как это происходит при использовании стандартной индексации."""

        # Создаем профиль, привязанный к пользователю
        profile = Profile(
            user_id=user.id,
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            age=user_data.get('age'),
            gender=user_data.get('gender'),
            profession=user_data.get('profession'),
            interests=user_data.get('interests'),
            contacts=user_data.get('contacts')
        )
        session.add(profile)

        # Один коммит для обеих операций
        await session.commit()

        return user  # Возвращаем объект пользователя

class ProfileDAO(BaseDAO):
    model = Profile


class PostDAO(BaseDAO):
    model = Post


class CommentDAO(BaseDAO):
    model = Comment
