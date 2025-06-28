from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import UUID, Column, ForeignKey, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastlibrarian.db import Base

if TYPE_CHECKING:
    from fastlibrarian.models.authors import Author
    from fastlibrarian.models.books import Book
    from fastlibrarian.models.series import Series


class Tags(Base):
    """Tags model for FastLibrarian API."""

    __tablename__ = "tags"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    books: Mapped[list["Book"]] = relationship(
        "Book",
        secondary="book_tags",
        back_populates="tags",
        passive_deletes=True,
    )

    series: Mapped[list["Series"]] = relationship(
        "Series",
        secondary="series_tags",
        back_populates="tags",
        passive_deletes=True,
    )
    authors: Mapped[list["Author"]] = relationship(
        "Author",
        secondary="author_tags",
        back_populates="tags",
        passive_deletes=True,
    )


book_tags = Table(
    "book_tags",
    Base.metadata,
    Column(
        "book_id",
        UUID(as_uuid=True),
        ForeignKey("books.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tag_id",
        UUID(as_uuid=True),
        ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

author_tags = Table(
    "author_tags",
    Base.metadata,
    Column(
        "author_id",
        UUID(as_uuid=True),
        ForeignKey("authors.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tag_id",
        UUID(as_uuid=True),
        ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

series_tags = Table(
    "series_tags",
    Base.metadata,
    Column(
        "series_id",
        UUID(as_uuid=True),
        ForeignKey("series.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tag_id",
        UUID(as_uuid=True),
        ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

author_books = Table(
    "author_books",
    Base.metadata,
    Column(
        "author_id",
        UUID(as_uuid=True),
        ForeignKey("authors.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "book_id",
        UUID(as_uuid=True),
        ForeignKey("books.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

series_books = Table(
    "series_books",
    Base.metadata,
    Column(
        "series_id",
        UUID(as_uuid=True),
        ForeignKey("series.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "book_id",
        UUID(as_uuid=True),
        ForeignKey("books.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
