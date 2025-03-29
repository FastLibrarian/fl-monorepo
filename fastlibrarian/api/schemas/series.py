"""Series schema models."""

from pydantic import BaseModel


class SeriesBase(BaseModel):
    """Base series schema."""

    name: str


class SeriesCreate(SeriesBase):
    """Schema for creating a new series."""


class Series(SeriesBase):
    """Schema for series responses."""

    id: int
    book_count: int | None = None

    class Config:
        """Pydantic config."""

        from_attributes = True


from .book import Book  # noqa: E402

Series.model_rebuild()
