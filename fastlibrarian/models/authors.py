"""Author model for FastLibrarian API."""

from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import UUID, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastlibrarian.db import Base
from fastlibrarian.models.shared import Tags, author_books

if TYPE_CHECKING:
    from fastlibrarian.models.shared import Tags


class Author(Base):
    """Author model for FastLibrarian API."""

    __tablename__ = "authors"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    books = relationship(
        "Book",
        secondary=author_books,
        back_populates="authors",
        passive_deletes=True,
        lazy="selectin",
    )
    external_refs: Mapped[JSONB] = mapped_column(JSONB, nullable=True, default=dict)
    tags: Mapped[list["Tags"]] = relationship(
        "Tags",
        secondary="author_tags",
        back_populates="authors",
        passive_deletes=True,
        lazy="selectin",
    )
