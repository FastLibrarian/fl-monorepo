from uuid import uuid4

from sqlalchemy import UUID, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastlibrarian.db import Base


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
    books = relationship(
        "Book",
        back_populates="series",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
