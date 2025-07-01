"""Pydantic schemas for FastLibrarian API models."""

from enum import Enum
from functools import cached_property
from uuid import UUID

from pydantic import BaseModel, ConfigDict, computed_field


class FastLibrarianConfig(BaseModel):
    """Configuration schema for FastLibrarian API (legacy compatibility)."""

    app_name: str = "FastLibrarian"
    version: str = "1.0.0"
    description: str = "A fast and efficient librarian API."

    @classmethod
    def from_app_config(cls, app_config) -> "FastLibrarianConfig":
        """Create from AppConfig for backward compatibility."""
        return cls(
            app_name=app_config.app_name,
            version=app_config.api.version,
            description=app_config.api.description,
        )


class AuthorShort(BaseModel):
    id: UUID
    name: str

    model_config = ConfigDict(from_attributes=True)


class SeriesShort(BaseModel):
    id: UUID
    name: str

    model_config = ConfigDict(from_attributes=True)


class BookShort(BaseModel):
    id: UUID
    title: str


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
    books: list[BookShort] = []  # Optionally include nested book objects

    class Config:
        """Pydantic config for ORM mode."""

        orm_mode = True


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
    books: list[BookShort] = []  # Optionally include nested book objects

    class Config:
        """Pydantic config for ORM mode."""

        from_attributes = True
        orm_mode = True


class BookStatus(str, Enum):
    """Book status enum."""

    Wanted = "Wanted"
    Have = "Have"
    Ignored = "Ignored"
    Delete = "Delete"


class BookBase(BaseModel):
    """Base schema for Book."""

    title: str
    description: str | None = None
    editions: list[dict] | None = None
    external_refs: dict | None = None
    status: BookStatus = BookStatus.Ignored
    a_status: BookStatus = BookStatus.Ignored
    p_status: BookStatus | None = None


class BookCreate(BookBase):
    """Schema for creating a Book."""

    author_ids: list[UUID]
    series_ids: list[UUID] = []


class BookRead(BookBase):
    """Schema for reading a Book."""

    id: UUID
    authors: list[AuthorShort] = []  # Optionally include nested author objects
    series: list[SeriesShort] = []  # Optionally include nested series objects

    @computed_field
    @cached_property
    def author_ids(self) -> list[UUID]:
        """Return list of author UUIDs for this book."""
        return [a.id for a in self.authors] if self.authors else []

    @computed_field
    @cached_property
    def series_ids(self) -> list[UUID]:
        """Return list of series UUIDs for this book."""
        return [s.id for s in self.series] if self.series else []

    class Config:
        """Pydantic config for ORM mode."""

        from_attributes = True
        orm_mode = True


AuthorRead.model_rebuild()
SeriesRead.model_rebuild()
BookRead.model_rebuild()
