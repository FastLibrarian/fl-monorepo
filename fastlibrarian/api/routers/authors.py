"""Author router module."""

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from fastlibrarian.api.database import get_session
from fastlibrarian.api.external.audible.main import Audible
from fastlibrarian.api.external.google_books import (
    GoogleBooks,
    GoogleBooksResponse,
)
from fastlibrarian.api.external.openlibrary import OpenLibrary
from fastlibrarian.api.external.utils.conversions import GBooksConversions as gbc
from fastlibrarian.api.modules import authors
from fastlibrarian.api.schemas.author import Author, AuthorCreate

router = APIRouter(prefix="/authors", tags=["authors"])


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


@router.get("/findauthor", response_model=list[Author])
async def find_author(
    name: str,
    db: AsyncSession = Depends(get_session),
) -> list[Author]:
    """Find an author by name."""
    results = []

    # Try Google Books first
    google_results = await find_from_google(name)
    logger.debug("Google Results:")
    logger.debug(google_results)
    # db_results = await authors.search(db, name)
    openlibrary_results = await find_from_openlibrary(name)
    logger.debug("OpenLibrary Results:")
    logger.debug(openlibrary_results)
    audible_results = await find_from_audible(name)
    print(audible_results)
    # Deduplicate results based on name
    seen_names = set()
    unique_results = []
    for author in results:
        if author.name not in seen_names:
            seen_names.add(author.name)
            unique_results.append(author)

    if not unique_results:
        raise HTTPException(status_code=404, detail="No results found")
    return unique_results


@router.post("/gbooks_create/{term}", response_model=Author)
async def create_author_from_gbooks(author: str):
    """Create an author from Google Books API."""
    gbooks = GoogleBooks()
    result: GoogleBooksResponse = await gbooks.get_author(author)

    if not gbooks:
        raise HTTPException(status_code=404, detail="Author not found in Google Books")
    fl_author = gbc.volume_to_author(result.items[0])
    if not fl_author:
        raise HTTPException(status_code=404, detail="Author not found in Google Books")
    author = await create_author(fl_author, db=Depends(get_session))


@router.get("audible_search/{term}", response_model=list[Author])
async def find_from_audible(term: str) -> list[Author]:
    """Search for authors using Audible API."""
    audible = Audible()
    result = await audible.search_audible(term)
    if not result:
        raise HTTPException(status_code=404, detail="No results found")
    return result

    raise HTTPException(status_code=404, detail="No results found")


@router.get("/gbooks_search/{term}", response_model=list[Author])
async def find_from_google(term: str) -> list[Author]:
    """Search for authors, books, etc using Google Books API."""
    gbooks = GoogleBooks()
    result: GoogleBooksResponse = await gbooks.get_author(term)
    authors = []
    books = []
    for item in result.items:
        author = gbc.volume_to_author(item)
        if author:
            authors.append(author)
            print(authors)
            return authors


@router.get("/openlibrary_search/{term}", response_model=list[Author])
async def find_from_openlibrary(term: str) -> list[Author]:
    """Search for authors using OpenLibrary API."""
    ol = OpenLibrary()

    result = await ol.author_search(term)
    if not result:
        raise HTTPException(status_code=404, detail="No results found")
    return result


@router.get("/{author_id}", response_model=Author)
async def read_author(author_id: int, db: AsyncSession = Depends(get_session)):
    """Get an author by ID."""
    db_author = await authors.get_author(db, author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


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
        updated_author = await authors.update_author_from_external_api(db, author_id)
        return updated_author
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
