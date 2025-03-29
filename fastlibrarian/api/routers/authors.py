"""Author router module."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from fastlibrarian.api.database import get_session
from fastlibrarian.api.modules import authors
from fastlibrarian.api.schemas.author import Author, AuthorCreate

router = APIRouter(prefix="/authors", tags=["authors"])


@router.get("/{author_id}", response_model=Author)
async def read_author(author_id: int, db: AsyncSession = Depends(get_session)):
    """Get an author by ID."""
    db_author = await authors.get_author(db, author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@router.get("/", response_model=list[Author])
async def read_authors(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_session),
):
    """Get list of authors."""
    return await authors.get_authors(db, skip=skip, limit=limit)


@router.post("/", response_model=Author)
async def create_author(author: AuthorCreate, db: AsyncSession = Depends(get_session)):
    """Create a new author."""
    return await authors.create_author(db, author)


@router.patch("/{author_id}", response_model=Author)
async def update_author(
    author_id: int,
    db: AsyncSession = Depends(get_session),
):
    """Update author details from external API."""
    # First check if author exists
    db_author = await authors.get_author(db, author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    try:
        # You'll need to implement this function in the authors module
        updated_author = await authors.update_author_from_external_api(db, author_id)
        return updated_author
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
