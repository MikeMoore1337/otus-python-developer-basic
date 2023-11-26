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
from models import Address, AsyncSession, Base, Geo, Post, User, engine


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    users_data, posts_data = await asyncio.gather(
        fetch_users_data(),
        fetch_posts_data(),
    )

    async with AsyncSession(bind=engine) as session:
        for user_data in users_data:
            user = User(
                id=user_data["id"],
                name=user_data["name"],
                username=user_data["username"],
                email=user_data["email"],
                phone=user_data.get("phone"),
                website=user_data.get("website"),
                company_id=user_data["company"]["id"],
                address_id=user_data["address"]["id"],
            )
            session.add(user)

            address_data = user_data["address"]
            geo_data = address_data["geo"]

            geo = Geo(id=geo_data["id"], lat=geo_data["lat"], lng=geo_data["lng"])
            session.add(geo)

            address = Address(
                id=address_data["id"],
                street=address_data["street"],
                suite=address_data["suite"],
                city=address_data["city"],
                zipcode=address_data["zipcode"],
                geo_id=geo_data["id"],
            )
            session.add(address)

        for post_data in posts_data:
            post = Post(
                id=post_data["id"],
                user_id=post_data["userId"],
                title=post_data["title"],
                body=post_data["body"],
            )
            session.add(post)

        await session.commit()


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
