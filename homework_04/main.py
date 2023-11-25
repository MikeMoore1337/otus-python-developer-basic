"""
Домашнее задание №4
Асинхронная работа с сетью и бд

доработайте функцию main, по вызову которой будет выполняться полный цикл программы
(добавьте туда выполнение асинхронной функции async_main):
- создание таблиц (инициализация)
- загрузка пользователей и постов
    - загрузка пользователей и постов должна выполняться конкурентно (параллельно)
      при помощи asyncio.gather (https://docs.python.org/3/library/asyncio-task.html#running-tasks-concurrently)
- добавление пользователей и постов в базу данных
  (используйте полученные из запроса данные, передайте их в функцию для добавления в БД)
- закрытие соединения с БД
"""

import asyncio

from jsonplaceholder_requests import fetch_posts_data, fetch_users_data

from homework_04.models import (
    Address,
    AsyncSession,
    Base,
    Post,
    User,
    async_session,
    engine,
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def fetch_data_and_add_to_db(session, users_data, posts_data):
    user_instances = []
    post_instances = []

    for user_data in users_data:
        # Извлекаем вложенные данные из user_data
        address_data = user_data.pop("address", None)

        # Создаем объект Address, если есть данные
        if address_data:
            address_instance = Address(**address_data)
        else:
            address_instance = None

        # Создаем объект User, передавая в него address_instance
        user_instance = User(address=address_instance, **user_data)
        user_instances.append(user_instance)

    for post_data in posts_data:
        # Извлекаем user_id из данных поста
        user_id = post_data.pop("userId", None)

        # Если user_id есть, пытаемся получить пользователя из базы данных
        if user_id is not None:
            user_instance = await session.get(User, user_id)
        else:
            user_instance = None

        # Если пользователя нет, создаем нового
        if user_instance is None:
            user_instance = User(**user_data)
            session.add(user_instance)

        # Создаем пост и устанавливаем связь с пользователем
        post_instance = Post(**post_data, user=user_instance)
        post_instances.append(post_instance)

    session.add_all(user_instances + post_instances)
    await session.commit()


async def add_users_to_db(users_data):
    for user_data in users_data:
        user = User(
            id=user_data["id"],
            name=user_data["name"],
            username=user_data["username"],
            email=user_data["email"],
        )
        async_session.add(user)

    await async_session.commit()


async def add_posts_to_db(posts_data):
    for post_data in posts_data:
        post = Post(
            id=post_data["id"],
            user_id=post_data["userId"],
            title=post_data["title"],
            body=post_data["body"],
        )
        async_session.add(post)

    await async_session.commit()


async def async_main():
    async with AsyncSession() as session:
        # Инициализация базы данных
        await init_db()

        # Загрузка данных и добавление их в базу данных
        users_data, posts_data = await asyncio.gather(
            fetch_users_data(), fetch_posts_data()
        )
        await fetch_data_and_add_to_db(session, users_data, posts_data)

    # Закрытие соединения с БД
    await async_session.close()


def main():
    # Запуск асинхронного цикла
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
