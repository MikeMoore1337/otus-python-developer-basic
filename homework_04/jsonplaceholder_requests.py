"""
создайте асинхронные функции для выполнения запросов к ресурсам (используйте aiohttp)
"""

import aiohttp

USERS_DATA_URL = "https://jsonplaceholder.typicode.com/users"
POSTS_DATA_URL = "https://jsonplaceholder.typicode.com/posts"


async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()


async def fetch_users_data():
    return await fetch_data(USERS_DATA_URL)


async def fetch_posts_data():
    return await fetch_data(POSTS_DATA_URL)
