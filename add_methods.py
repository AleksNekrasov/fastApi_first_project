from sqlalchemy.ext.asyncio import AsyncSession
from asyncio import run

from models import User, Profile
from database import connection
from sql_enums import GenderEnum, ProfessionEnum


@connection  # Благодаря декоратору @connection сессия(объект session (асинхронная сессия).)
# создаётся автоматически
async def create_user_example_1(username: str, email: str, password: str,
                                session: AsyncSession) -> int:
    """
        Создает нового пользователя с использованием ORM SQLAlchemy.

        Аргументы:
        - username: str - имя пользователя
        - email: str - адрес электронной почты
        - password: str - пароль пользователя
        - session: AsyncSession - асинхронная сессия базы данных

        Возвращает:
        - int - идентификатор созданного пользователя
        """
    user = User(username=username, email=email, password=password)
    session.add(user)
    await session.commit()
    return user.id


"""
Теперь мы готовы к описанию метода, 
который добавит информацию в две смежные таблицы,(Users, Prifiles) 
связанные по типу «Один к одному».
"""


@connection
async def get_user_by_id_example_2(username: str, email: str, password: str,
                                   first_name: str,
                                   last_name: str | None,
                                   age: str | None,
                                   gender: GenderEnum,
                                   profession: ProfessionEnum | None,
                                   interests: list | None,
                                   contacts: dict | None,
                                   session: AsyncSession) -> dict[str, int]:
    user = User(username=username, email=email, password=password)
    session.add(user)
    await session.commit()

    profile1 = Profile(
        user_id=user.id,
        first_name=first_name,
        last_name=last_name,
        age=age,
        gender=gender,
        profession=profession,
        interests=interests,
        contacts=contacts)

    session.add(profile1)
    await session.commit()
    print(f'Создан пользователь с ID {user.id} и ему присвоен профиль с ID {profile1.id}')
    return {'user_id': user.id, 'profile_id': profile1.id}


@connection
async def get_user_by_id_example_3(username: str, email: str, password: str,
                                   first_name: str,
                                   last_name: str | None,
                                   age: str | None,
                                   gender: GenderEnum,
                                   profession: ProfessionEnum | None,
                                   interests: list | None,
                                   contacts: dict | None,
                                   session: AsyncSession) -> dict[str, int]:
    try:
        user = User(username=username, email=email, password=password)
        session.add(user)
        await session.flush()  # Промежуточный шаг для получения user.id без коммита

        profile = Profile(
            user_id=user.id,
            first_name=first_name,
            last_name=last_name,
            age=age,
            gender=gender,
            profession=profession,
            interests=interests,
            contacts=contacts
        )
        session.add(profile)

        # Один коммит для обоих действий
        await session.commit()

        print(f'Создан пользователь с ID {user.id} и ему присвоен профиль с ID {profile.id}')
        return {'user_id': user.id, 'profile_id': profile.id}

    except Exception as e:
        await session.rollback()  # Откатываем транзакцию при ошибке
        raise e


"""Массовое добавление данных в таблицу
Для массового добавления данных в SQLAlchemy существует удобный метод add_all. 
Он работает аналогично методу add, но принимает на вход список экземпляров (инстансов).
 С его помощью мы можем добавить сразу несколько записей за одну операцию. 
 Давайте рассмотрим пример, где добавим пять пользователей с использованием этого метода."""

users = [
    {"username": "michael_brown", "email": "michael.brown@example.com", "password": "pass1234"},
    {"username": "sarah_wilson", "email": "sarah.wilson@example.com", "password": "mysecurepwd"},
    {"username": "david_clark", "email": "david.clark@example.com", "password": "davidsafe123"},
    {"username": "emma_walker", "email": "emma.walker@example.com", "password": "walker987"},
    {"username": "james_martin", "email": "james.martin@example.com", "password": "martinpass001"}
]

@connection
async def create_user_example_4(users_data: list[dict], session: AsyncSession) -> list[int]:
    """
       Создает нескольких пользователей с использованием ORM SQLAlchemy.

       Аргументы:
       - users_data: list[dict] - список словарей, содержащих данные пользователей
         Каждый словарь должен содержать ключи: 'username', 'email', 'password'.
       - session: AsyncSession - асинхронная сессия базы данных

       Возвращает:
       - list[int] - список идентификаторов созданных пользователей
       """
    users_list = [
        User(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password']
        )
        for user_data in users_data
    ]
    session.add_all(users_list)
    await session.commit()
    return [user.id for user in users_list]

run(create_user_example_4(users_data=users))
