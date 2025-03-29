"""Book operations module."""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastlibrarian.api.models.main import BookModel
from fastlibrarian.api.schemas.book import BookCreate


async def get_book(db: AsyncSession, book_id: int) -> Optional[BookModel]:
    """Get a book by ID.

    Args:
        db: Database session
        book_id: Book ID

    Returns:
        Optional[BookModel]: Book if found
    """
    result = await db.execute(select(BookModel).filter(BookModel.id == book_id))
    return result.scalar_one_or_none()


async def get_books(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> List[BookModel]:
    """Get list of books.

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List[BookModel]: List of books
    """
    result = await db.execute(select(BookModel).offset(skip).limit(limit))
    return result.scalars().all()


async def create_book(db: AsyncSession, book: BookCreate) -> BookModel:
    """Create a new book.

    Args:
        db: Database session
        book: Book data

    Returns:
        BookModel: Created book
    """
    db_book = BookModel(**book.model_dump())
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book
