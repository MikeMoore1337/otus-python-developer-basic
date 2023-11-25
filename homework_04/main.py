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
from models import AsyncSession, Base, Post, User, engine


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def fetch_data_and_add_to_db(session, users_data, posts_data):
    tasks = [
                add_data_to_db(session, User, user_data)
                for user_data in users_data
            ] + [
                add_data_to_db(session, Post, post_data)
                for post_data in posts_data
            ]
    await asyncio.gather(*tasks)


async def fetch_data_and_add_to_db(session, users_data, posts_data):
    user_instances = []
    post_instances = []

    for user_data in users_data:
        user_instance = User(**user_data)
        user_instances.append(user_instance)

    for post_data in posts_data:
        # Извлекаем user_id из данных поста
        user_id = post_data.pop('user_id', None)

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


async def async_main():
    async with AsyncSession() as session:
        # Инициализация базы данных
        await init_db()

        # Загрузка данных и добавление их в базу данных
        users_data, posts_data = await asyncio.gather(
            fetch_users_data(),
            fetch_posts_data()
        )
        await fetch_data_and_add_to_db(session, users_data, posts_data)


# async def async_main():
#     async with AsyncSession() as session:
#         # Инициализация базы данных
#         await init_db()
#
#         # Загрузка данных и добавление их в базу данных
#         users_data, posts_data = await asyncio.gather(
#             fetch_users_data(),
#             fetch_posts_data()
#         )
#         await fetch_data_and_add_to_db(session, users_data, posts_data)
#
#         # Закрытие соединения с базой данных
#         await session.commit()


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
