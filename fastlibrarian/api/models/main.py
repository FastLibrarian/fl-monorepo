"""Setup models for the database."""

from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from fastlibrarian.api.database import Base


class BookModel(Base):
    """Book model for the database."""

    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    published_date = Column(Date)
    isbn = Column(String, unique=True)
    pages = Column(Integer)
    cover_image = Column(String)
    language = Column(String)
    series_id = Column(Integer, ForeignKey("series.id"))
    series = relationship("SeriesModel", back_populates="books")


class AuthorModel(Base):
    """Author model for the database."""

    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    books = relationship("BookModel", back_populates="author")


class UserModel(Base):
    """User model for the database."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    books = relationship("BookModel", back_populates="user")


class SeriesModel(Base):
    """Series model for the database."""

    __tablename__ = "series"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    books = relationship("BookModel", back_populates="series")
