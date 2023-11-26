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

from aiohttp import ClientSession
from jsonplaceholder_requests import POSTS_DATA_URL, USERS_DATA_URL
from models import AsyncSession, Base, Post, User, engine


async def fetch_data(url):
    try:
        async with ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()  # Raises an exception for 4xx and 5xx status codes
                return await response.json()
    except Exception as e:
        print(f"Error fetching data from {url}: {e}")
        return []


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    users_data, posts_data = await asyncio.gather(
        fetch_data(USERS_DATA_URL), fetch_data(POSTS_DATA_URL)
    )

    async with AsyncSession() as session:
        users = [User(**user_data) for user_data in users_data]
        posts = [Post(**post_data) for post_data in posts_data]

        # Batch insert users
        session.bulk_save_objects(users)
        session.commit()

        # Batch insert posts
        session.bulk_save_objects(posts)
        session.commit()


if __name__ == "__main__":
    asyncio.run(async_main())
