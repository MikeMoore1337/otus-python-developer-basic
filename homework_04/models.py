"""
создайте алхимичный engine
добавьте declarative base (свяжите с engine)
создайте объект Session
добавьте модели User и Post, объявите поля:
для модели User обязательными являются name, username, email
для модели Post обязательными являются user_id, title, body
создайте связи relationship между моделями: User.posts и Post.user
"""

import os

from sqlalchemy import Column, ForeignKey, Integer, MetaData, String
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

PG_CONN_URI = (
    os.environ.get("SQLALCHEMY_PG_CONN_URI")
    or "postgresql+asyncpg://postgres:password@localhost/postgres"
)

engine = create_async_engine(PG_CONN_URI, echo=True)
metadata = MetaData()
Base = declarative_base(metadata=metadata)
AsyncSession = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, nullable=False)
    street = Column(String, nullable=False)
    suite = Column(String, nullable=False)
    lat = Column(String, nullable=False)
    lng = Column(String, nullable=False)
    zipcode = Column(String, nullable=False)

    def __init__(self, **kwargs):
        self.geo = {"lat": kwargs.get("lat"), "lng": kwargs.get("lng")}
        super().__init__(**kwargs)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    address_id = Column(Integer, ForeignKey("addresses.id"))

    address = relationship("Address")

    posts = relationship("Post", back_populates="user")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)

    user = relationship("User", back_populates="posts")
