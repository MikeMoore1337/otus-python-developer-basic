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
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

PG_CONN_URI = (
    os.environ.get("SQLALCHEMY_PG_CONN_URI")
    or "postgresql+asyncpg://postgres:password@localhost/postgres"
)

Base = declarative_base()
engine = create_async_engine(PG_CONN_URI, echo=True, future=True)
Session = sessionmaker(engine, class_=AsyncSession)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    website = Column(String, nullable=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    address_id = Column(Integer, ForeignKey("addresses.id"), nullable=False)

    address = relationship("Address", back_populates="user")
    company = relationship("Company", back_populates="user")
    posts = relationship("Post", back_populates="user")

    def __init__(self, name, username, email, phone, website, company_id, address_id):
        self.name = name
        self.username = username
        self.email = email
        self.phone = phone
        self.website = website
        self.company_id = company_id
        self.address_id = address_id


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

    address = relationship("Address", back_populates="geo")


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

    user = relationship("User", back_populates="company")
