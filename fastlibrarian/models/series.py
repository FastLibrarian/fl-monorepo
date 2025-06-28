"""Series model for FastLibrarian API."""

from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import UUID, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastlibrarian.db import Base
from fastlibrarian.models.shared import series_books

if TYPE_CHECKING:
    from fastlibrarian.models.shared import Tags


class Series(Base):
    """Series model for FastLibrarian API."""

    __tablename__ = "series"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    external_refs: Mapped[JSONB] = mapped_column(
        JSONB,
        nullable=True,
        default=dict,
    )

    tags: Mapped[list["Tags"]] = relationship(
        "Tags",
        secondary="series_tags",
        back_populates="series",
        passive_deletes=True,
        lazy="selectin",
    )
    books = relationship(
        "Book",
        secondary=series_books,
        back_populates="series",
        passive_deletes=True,
        lazy="selectin",
    )
