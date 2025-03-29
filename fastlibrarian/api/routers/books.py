"""Book router module."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from fastlibrarian.api.database import get_session
from fastlibrarian.api.modules import books
from fastlibrarian.api.schemas.book import Book, BookCreate

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/{book_id}", response_model=Book)
async def read_book(book_id: int, db: AsyncSession = Depends(get_session)):
    """Get a book by ID."""
    db_book = await books.get_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@router.get("/", response_model=List[Book])
async def read_books(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_session)
):
    """Get list of books."""
    return await books.get_books(db, skip=skip, limit=limit)


@router.post("/", response_model=Book)
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_session)):
    """Create a new book."""
    try:
        return await books.create_book(db, book)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
