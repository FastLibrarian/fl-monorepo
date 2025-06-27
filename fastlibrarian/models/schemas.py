"""Pydantic schemas for FastLibrarian API models."""

from uuid import UUID

from pydantic import BaseModel


class AuthorBase(BaseModel):
    """Base schema for Author."""

    name: str
    bio: str | None = None
    external_refs: dict | None = None


class AuthorCreate(AuthorBase):
    """Schema for creating an Author."""


class AuthorRead(AuthorBase):
    """Schema for reading an Author."""

    id: UUID

    class Config:
        """Pydantic config for ORM mode."""

        from_attributes = True
        orm_mode = True


class BookBase(BaseModel):
    """Base schema for Book."""

    title: str
    author_id: UUID
    description: str | None = None
    series_id: UUID | None = None
    editions: list[dict] | None = None
    external_refs: dict | None = None


class BookCreate(BookBase):
    """Schema for creating a Book."""


class BookRead(BookBase):
    """Schema for reading a Book."""

    id: UUID

    class Config:
        """Pydantic config for ORM mode."""

        from_attributes = True
        orm_mode = True


class SeriesBase(BaseModel):
    """Base schema for Series."""

    name: str
    description: str | None = None
    external_refs: dict | None = None


class SeriesCreate(SeriesBase):
    """Schema for creating a Series."""


class SeriesRead(SeriesBase):
    """Schema for reading a Series."""

    id: UUID

    class Config:
        """Pydantic config for ORM mode."""

        orm_mode = True
