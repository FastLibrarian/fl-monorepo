"""Book schema models."""

from datetime import date

from pydantic import BaseModel


class BookBase(BaseModel):
    """Base book schema."""

    title: str
    author: str
    published_date: date
    isbn: str
    pages: int
    cover_image: str | None = None
    language: str
    series_id: int | None = None
    description: str | None = None


class BookCreate(BookBase):
    """Schema for creating a new book."""


class Book(BookBase):
    """Schema for book responses."""

    id: int
    author_id: int
    series_id: int | None = None

    class Config:
        """Pydantic config."""

        from_attributes = True
