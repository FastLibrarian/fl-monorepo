from uuid import uuid4

from sqlalchemy import UUID, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastlibrarian.db import Base


class Book(Base):
    """Book model for FastLibrarian API."""

    __tablename__ = "books"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author_id: Mapped[UUID] = mapped_column(
        UUID,
        ForeignKey("authors.id", ondelete="CASCADE"),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    series_id: Mapped[UUID | None] = mapped_column(
        UUID,
        ForeignKey("series.id", ondelete="SET NULL"),
        nullable=True,
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
    author = relationship(
        "Author",
        back_populates="books",
        passive_deletes=True,
    )
    series = relationship(
        "Series",
        back_populates="books",
        passive_deletes=True,
    )
