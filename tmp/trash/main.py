import asyncio

from tmp.trash.jsonplaceholder_requests import fetch_posts_data, fetch_users_data
from tmp.trash.models import AsyncSession, Base, Post, User, engine


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    users_data, posts_data = await asyncio.gather(
        fetch_users_data(),
        fetch_posts_data(),
    )

    async with AsyncSession(bind=engine) as session:
        users = [
            User(
                id=user_data["id"],
                name=user_data["name"],
                username=user_data["username"],
                email=user_data["email"],
            )
            for user_data in users_data
        ]

        posts = [
            Post(
                id=post_data["id"],
                user_id=post_data["userId"],
                title=post_data["title"],
                body=post_data["body"],
            )
            for post_data in posts_data
        ]

        session.add_all(users)
        session.add_all(posts)
        await session.commit()


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
