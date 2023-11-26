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

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import configure_mappers, relationship

PG_CONN_URI = (
    os.environ.get("SQLALCHEMY_PG_CONN_URI")
    or "postgresql+asyncpg://postgres:password@localhost/postgres"
)

engine = create_async_engine(PG_CONN_URI, echo=True)

# Создание базового класса для декларативных моделей
Base = declarative_base()

# Создание сессии для взаимодействия с базой данных
AsyncSession = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
async_session = AsyncSession()

association_table = Table(
    "user_address_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("address_id", Integer, ForeignKey("addresses.id")),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)

    posts = relationship("Post", secondary=association_table, back_populates="users")
    addresses = relationship(
        "Address", secondary=association_table, back_populates="users"
    )
    company_id = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company", uselist=False, back_populates="user")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)

    user = relationship("User", secondary=association_table, back_populates="posts")


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    street = Column(String, nullable=False)
    suite = Column(String, nullable=False)
    city = Column(String, nullable=False)
    zipcode = Column(String, nullable=False)
    geo = relationship("Geo", uselist=False, back_populates="address")

    users = relationship(
        "User", secondary=association_table, back_populates="addresses"
    )


class Geo(Base):
    __tablename__ = "geo"

    id = Column(Integer, primary_key=True, index=True)
    lat = Column(String, nullable=False)
    lng = Column(String, nullable=False)

    address = relationship("Address", back_populates="geo")


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    catch_phrase = Column(String, nullable=False)
    bs = Column(String, nullable=False)

    user = relationship("User", back_populates="company")


configure_mappers()
