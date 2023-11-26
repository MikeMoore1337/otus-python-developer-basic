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


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    users_data, posts_data = await asyncio.gather(
        fetch_users_data(),
        fetch_posts_data(),
    )

    async with Session() as session:
        # Создание пользователей
        users_mapping = {}
        for user_data in users_data:
            user = User(
                id=user_data.get("id"),
                name=user_data.get("name"),
                username=user_data.get("username"),
                email=user_data.get("email"),
                phone=user_data.get("phone"),
                website=user_data.get("website"),
            )
            session.add(user)
            users_mapping[user.id] = user

        # Создание постов
        for post_data in posts_data:
            post = Post(
                id=post_data.get("id"),
                user_id=post_data.get("userId"),
                title=post_data.get("title"),
                body=post_data.get("body"),
            )
            user_id = post_data.get("userId")
            if user_id in users_mapping:
                post.user = users_mapping[user_id]
            session.add(post)

        session.commit()


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
