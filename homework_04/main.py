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
        users = []
        posts = []

        # Создание пользователей
        for user_data in users_data:
            user = User(
                id=user_data["id"],
                name=user_data["name"],
                username=user_data["username"],
                email=user_data["email"],
                phone=user_data["phone"],
                website=user_data["website"],
                company_id=user_data["company"]["id"],
                address_id=user_data["address"]["id"],
            )
            users.append(user)

        # Создание постов
        for post_data in posts_data:
            post = Post(
                id=post_data["id"],
                user_id=post_data["userId"],
                title=post_data["title"],
                body=post_data["body"],
            )
            posts.append(post)

        # Установка связей
        for post in posts:
            user_id = post.user_id
            user = next((u for u in users if u.id == user_id), None)
            if user:
                post.user = user

        # Batch insert users
        session.bulk_save_objects(users)
        session.commit()

        # Batch insert posts
        session.bulk_save_objects(posts)
        session.commit()


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
