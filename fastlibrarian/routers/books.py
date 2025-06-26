from uuid import uuid4

import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastlibrarian.db import get_db
from fastlibrarian.models import authors as author_models
from fastlibrarian.models import books as models
from fastlibrarian.models import series as series_models
from fastlibrarian.models.schemas import BookCreate, BookRead

from .shared import hardcover_headers

router = APIRouter(prefix="/books", tags=["books"])


async def search_hardcover_book(title: str):
    """Search for a book using the Hardcover GraphQL API."""
    url = "https://api.hardcover.app/v1/graphql"

    query = """
    query searchBook($query: String!) {
        search(query: $query, query_type: "Book", per_page: 5, page: 1) {
            results
        }
    }
    """

    variables = {"query": title}
    payload = {"query": query, "variables": variables}
    async with httpx.AsyncClient(headers=hardcover_headers) as client:
        resp = await client.post(url, json=payload)
        print(f"Hardcover API response: {resp.text}")
        if resp.status_code != 200:
            return None

        data = resp.json()
        results = data.get("data", {}).get("search", {}).get("results", {})
        hits = results.get("hits", [])
        # Try to find an exact match (case-insensitive)
        for hit in hits:
            doc = hit.get("document", {})
            if doc.get("title", "").lower() == title.lower():
                # Extract author info
                authors = []
                for c in doc.get("contributions", []):
                    author = c.get("author")
                    if author:
                        authors.append(
                            {
                                "id": author.get("id"),
                                "name": author.get("name"),
                                "bio": author.get("bio"),
                            },
                        )
                if not authors and doc.get("author_names"):
                    authors = [{"name": doc["author_names"][0]}]
                return {
                    "title": doc.get("title"),
                    "description": doc.get("description"),
                    "authors": authors,
                    "series": doc.get("featured_series"),
                }
        if hits:
            doc = hits[0].get("document", {})
            authors = []
            for c in doc.get("contributions", []):
                author = c.get("author")
                if author:
                    authors.append(
                        {
                            "id": author.get("id"),
                            "name": author.get("name"),
                            "bio": author.get("bio"),
                        },
                    )
            if not authors and doc.get("author_names"):
                authors = [{"name": doc["author_names"][0]}]
            return {
                "title": doc.get("title"),
                "description": doc.get("description"),
                "authors": authors,
                "series": doc.get("featured_series"),
            }
        return None


async def get_or_create_author(db: AsyncSession, author_data):
    statement = select(author_models.Author).where(
        author_models.Author.name == author_data["name"],
    )
    result = await db.execute(statement)
    db_author = result.scalars().first()
    if db_author:
        return db_author
    db_author = author_models.Author(
        id=uuid4(),
        name=author_data["name"],
        bio=author_data.get("bio"),
    )
    db.add(db_author)
    await db.commit()
    await db.refresh(db_author)
    return db_author


async def get_or_create_series(db: AsyncSession, series_data):
    statement = select(series_models.Series).where(
        series_models.Series.name == series_data["name"],
    )
    result = await db.execute(statement)
    db_series = result.scalars().first()
    if db_series:
        return db_series
    db_series = series_models.Series(
        id=uuid4(),
        name=series_data["name"],
        description=series_data.get("description"),
    )
    db.add(db_series)
    await db.commit()
    await db.refresh(db_series)
    return db_series


@router.post("/", response_model=BookRead)
async def create_book(data: dict, db: AsyncSession = Depends(get_db)) -> BookRead:
    """Create a new book, searching Hardcover API first."""
    title = data.get("title")
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")
    hc_book = await search_hardcover_book(title)
    if not hc_book:
        raise HTTPException(status_code=404, detail="Book not found on Hardcover")
    # Use Hardcover data
    title = hc_book.get("title")
    description = hc_book.get("description")
    # Handle author
    hc_authors = hc_book.get("authors", [])
    if not hc_authors:
        raise HTTPException(
            status_code=400,
            detail="No author found for book on Hardcover",
        )
    hc_author = hc_authors[0]
    db_author = await get_or_create_author(db, hc_author)
    # Handle series (optional)
    hc_series = hc_book.get("series")
    db_series = None
    if hc_series:
        db_series = await get_or_create_series(db, hc_series)
    db_book = models.Book(
        id=uuid4(),
        title=title,
        author_id=db_author.id,
        description=description,
        series_id=db_series.id if db_series else None,
    )
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return BookRead.model_validate(db_book)


@router.get("/", response_model=list[BookRead])
async def list_books(db: AsyncSession = Depends(get_db)) -> list[BookRead]:
    """List all books."""
    statement = select(models.Book)
    result = await db.execute(statement)
    books = result.scalars().all()
    return [BookRead.model_validate(b) for b in books]


@router.get("/{book_id}", response_model=BookRead)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)) -> BookRead:
    """Get a book by ID."""
    statement = select(models.Book).where(models.Book.id == book_id)
    result = await db.execute(statement)
    book = result.scalars().first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookRead.model_validate(book)


@router.put("/{book_id}", response_model=BookRead)
async def update_book(
    book_id: int,
    book: BookCreate,
    db: AsyncSession = Depends(get_db),
) -> BookRead:
    """Update a book by ID."""
    statement = select(models.Book).where(models.Book.id == book_id)
    result = await db.execute(statement)
    db_book = result.scalars().first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.model_dump().items():
        setattr(db_book, key, value)
    await db.commit()
    await db.refresh(db_book)
    return BookRead.model_validate(db_book)


@router.delete("/{book_id}", response_model=BookRead)
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)) -> BookRead:
    """Delete a book by ID."""
    statement = select(models.Book).where(models.Book.id == book_id)
    result = await db.execute(statement)
    db_book = result.scalars().first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    await db.delete(db_book)
    await db.commit()
    return BookRead.model_validate(db_book)
    return BookRead.model_validate(db_book)


@router.delete("/{book_id}", response_model=BookRead)
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)) -> BookRead:
    """Delete a book by ID."""
    statement = select(models.Book).where(models.Book.id == book_id)
    result = await db.execute(statement)
    db_book = result.scalars().first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    await db.delete(db_book)
    await db.commit()
    return BookRead.model_validate(db_book)
