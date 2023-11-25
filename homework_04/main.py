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


async def add_data_to_db(session, model, data):
    # Извлечение только нужных полей
    valid_keys = [key for key in data.keys() if key in model.__table__.columns]

    # Создание объекта модели, но без добавления в сеанс
    instance = model(**{key: data[key] for key in valid_keys})

    # Добавление user в базу данных, если это User модель
    if model == User:
        session.add(instance)
        await session.flush()  # Гарантирует, что пользователь получает ID
    elif model == Post:
        # Получение user_id из переданных данных или выбор существующего пользователя
        user_id = data.get('user_id')
        user = await session.get(User, user_id)

        if not user:
            # Создание нового пользователя, если его нет в базе данных
            user = User(**{key: data[key] for key in valid_keys if key != 'user_id'})
            session.add(user)
            await session.flush()  # Гарантирует, что пользователь получает ID

        # Установка user_id для поста и добавление в сеанс
        instance.user_id = user.id
        session.add(instance)

    await session.flush()  # Гарантирует, что запись добавлена в базу данных


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

        # Закрытие соединения с базой данных
        await session.commit()


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
