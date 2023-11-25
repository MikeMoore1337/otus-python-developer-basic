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
from models import Base, Post, Session, User, engine


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def add_data_to_db(users_data, posts_data):
    async with Session() as session:
        async with session.begin():
            for user_data in users_data:
                user = User(**user_data)
                session.add(user)

            for post_data in posts_data:
                post = Post(**post_data)
                session.add(post)


async def async_main():
    users_data, posts_data = await asyncio.gather(
        fetch_users_data(),
        fetch_posts_data(),
    )

    await init_db()
    await add_data_to_db(users_data, posts_data)

    print("Data added to the database")


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
