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
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from testing.test_homework_04.test_main import check_data_match


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
        await session.execute(User.__table__.insert().values(users))

        # Batch insert posts
        await session.execute(Post.__table__.insert().values(posts))


async def test_main(users_data, posts_data):
    await async_main()

    stmt_query_users = select(User).options(selectinload(User.posts))
    stmt_query_posts = select(Post).options(joinedload(Post.user))

    users = []
    posts = []

    async with AsyncSession() as session:
        res_users = await session.execute(stmt_query_users)
        res_posts = await session.execute(stmt_query_posts)

        users.extend(res_users.scalars())
        posts.extend(res_posts.scalars())

    assert len(posts) == len(posts_data)

    check_data_match(
        users,
        users_data,
        args_mapping=dict(
            name="name",
            username="username",
            email="email",
        ),
    )
    check_data_match(
        posts,
        posts_data,
        args_mapping=dict(
            user_id="userId",
            title="title",
            body="body",
        ),
    )

    for post in posts:
        # check relationships
        assert post.user in users
        assert post in post.user.posts


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
