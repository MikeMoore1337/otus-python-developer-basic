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

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base, relationship

PG_CONN_URI = (
    os.environ.get("SQLALCHEMY_PG_CONN_URI")
    or "postgresql+asyncpg://postgres:password@localhost/postgres"
)

Base = declarative_base()
engine = create_async_engine(PG_CONN_URI, echo=True, future=True)

# Создание сессии для взаимодействия с базой данных
AsyncSession = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
async_session = AsyncSession()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    website = Column(String, nullable=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    address_id = Column(Integer, ForeignKey('addresses.id'), nullable=False)

    address = relationship('Address', back_populates='user')
    company = relationship('Company', back_populates='user')
    posts = relationship("Post", back_populates="user")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)

    user = relationship("User", back_populates="posts")


class Geo(Base):
    __tablename__ = "geos"

    id = Column(Integer, primary_key=True, index=True)
    lat = Column(String, nullable=False)
    lng = Column(String, nullable=False)


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    street = Column(String, nullable=False)
    suite = Column(String, nullable=False)
    city = Column(String, nullable=False)
    zipcode = Column(String, nullable=False)
    geo_id = Column(Integer, ForeignKey("geos.id"), nullable=False)

    geo = relationship("Geo", back_populates="address")
    user = relationship("User", back_populates="address")


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    catch_phrase = Column(String, nullable=False)
    bs = Column(String, nullable=False)
