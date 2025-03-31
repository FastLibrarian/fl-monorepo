"""Author schema models."""

from pydantic import BaseModel

from .book import Book


class AuthorBase(BaseModel):
    """Base author schema."""

    name: str


class AuthorCreate(AuthorBase):
    """Schema for creating a new author."""


class Author(AuthorBase):
    """Schema for author responses."""

    id: int
    book_count: int | None = None
    biography: str | None = None
    books: list[Book] | None = None

    class Config:
        """Pydantic config."""

        from_attributes = True
