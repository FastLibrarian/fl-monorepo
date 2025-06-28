"""Book model for FastLibrarian API."""

from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import UUID, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastlibrarian.db import Base
from fastlibrarian.models.schemas import BookStatus
from fastlibrarian.models.shared import Tags, author_books, series_books

if TYPE_CHECKING:
    from fastlibrarian.models.shared import Tags


class Book(Base):
    """Book model for FastLibrarian API."""

    __tablename__ = "books"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[BookStatus] = mapped_column(
        SQLEnum(BookStatus, name="book_status"),
        nullable=False,
        default=BookStatus.Wanted,
        server_default=BookStatus.Wanted.value,
    )
    a_status: Mapped[BookStatus] = mapped_column(
        SQLEnum(BookStatus, name="book_a_status"),
        nullable=False,
        default=BookStatus.Wanted,
        server_default=BookStatus.Wanted.value,
    )
    p_status: Mapped[BookStatus] = mapped_column(
        SQLEnum(BookStatus, name="book_p_status"),
        nullable=True,
        default=BookStatus.Wanted,
        server_default=BookStatus.Wanted.value,
    )

    external_refs: Mapped[JSONB] = mapped_column(
        JSONB,
        nullable=True,
        default=dict,
    )
    editions: Mapped[JSONB] = mapped_column(
        JSONB,
        nullable=True,
        default=dict,
    )
    authors = relationship(
        "Author",
        secondary=author_books,
        back_populates="books",
        passive_deletes=True,
        lazy="selectin",
    )
    series = relationship(
        "Series",
        secondary=series_books,
        back_populates="books",
        passive_deletes=True,
        lazy="selectin",
    )
    tags: Mapped[list["Tags"]] = relationship(
        "Tags",
        secondary="book_tags",
        back_populates="books",
        passive_deletes=True,
        lazy="selectin",
    )
