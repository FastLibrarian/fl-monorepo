from uuid import uuid4

from sqlalchemy import UUID, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastlibrarian.db import Base


class Author(Base):
    """Author model for FastLibrarian API."""

    __tablename__ = "authors"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    books = relationship(
        "Book",
        back_populates="author",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    external_refs: Mapped[JSONB] = mapped_column(JSONB, nullable=True, default=dict)
