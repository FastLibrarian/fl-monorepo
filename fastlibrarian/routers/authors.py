from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastlibrarian.db import get_db
from fastlibrarian.models.authors import Author
from fastlibrarian.models.books import Book
from fastlibrarian.models.schemas import AuthorCreate, AuthorRead, BookShort
from fastlibrarian.models.series import Series
from fastlibrarian.modules.hardcover import HardcoverAPI as hcapi

router = APIRouter(prefix="/authors", tags=["authors"])


async def search_inventaire_author(name: str):
    """Search for author on Inventaire."""
    # TODO: Implement actual search. For now, return None.
    return


async def update_author_books(author_id: UUID, db: AsyncSession):
    """Update books for an author."""
    if not author_id:
        logger.error("Author ID is required for updating books.")
        return
    logger.info(f"Updating books for author {author_id}")
    # Fetch the author from the database
    statement = select(Author).where(Author.id == author_id)
    result = await db.execute(statement)
    author = result.scalars().first()
    if not author:
        logger.error(f"Author with ID {author_id} not found.")
        return
    hc_author_id = author.external_refs.get("hardcover_id")
    if not hc_author_id:
        logger.error(f"No Hardcover ID found for author {author.name}.")
        return
    hc = hcapi()
    works = await hc.get_works(hc_author_id)
    if not works:
        logger.error(f"No works found for author {author.name} on Hardcover.")
        return
    for work in works:
        # --- Check if series exists ---
        series_obj = None
        series_name = None
        series_id = None
        series_description = None
        if work.get("book_series"):
            # Take the first series if present
            first_series = work["book_series"][0]
            series_name = first_series.get("name")
            series_id = first_series.get("series_id")
            # Try to find existing series by name
            if series_name:
                stmt = select(Series).where(Series.name == series_name)
                result = await db.execute(stmt)
                series_obj = result.scalars().first()
            if not series_obj and series_name:
                # If not found, create new series
                series_obj = Series(
                    name=series_name,
                    description=series_description,
                    external_refs={"hardcover_id": series_id} if series_id else {},
                )
                db.add(series_obj)
                await db.flush()  # assign id
        # --- Check if book exists for this author ---
        stmt = select(Book).where(Book.title == work.get("title"))
        result = await db.execute(stmt)
        book_obj = result.scalars().first()
        if book_obj and author in book_obj.authors:
            logger.info(
                f"Book '{work.get('title')}' by author {author.name} already exists, skipping.",
            )
            continue
        # --- Add new book ---
        book = Book(
            title=work.get("title"),
            description=work.get("description"),
            editions=work.get("editions"),
            external_refs={
                "hardcover_id": work.get("id"),
            },
        )
        book.authors.append(author)
        if series_obj:
            book.series.append(series_obj)
        db.add(book)
    await db.commit()
    logger.info(f"Updated {len(works)} books for author {author.name}")


@router.post("/update_single_author_books/{author_id}", response_model=AuthorRead)
async def update_single_author_books(
    author_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> AuthorRead:
    if not author_id:
        raise HTTPException(
            status_code=400,
            detail="Author ID is required for updating books.",
        )
    logger.info(f"Updating books for author {author_id}")
    await update_author_books(author_id, db)
    # Fetch the updated author and return
    statement = select(Author).where(Author.id == author_id)
    result = await db.execute(statement)
    author = result.scalars().first()
    if not author:
        raise HTTPException(
            status_code=404,
            detail="Author not found after update.",
        )
    books_short = [BookShort(id=str(b.id), title=b.title) for b in author.books]
    return AuthorRead(
        id=str(author.id),
        name=author.name,
        bio=author.bio,
        external_refs=dict(author.external_refs) if author.external_refs else None,
        books=books_short,
    )


@router.get("/find_authors", response_model=list[dict])
async def find_authors(
    name: str,
    db: AsyncSession = Depends(get_db),
) -> list[dict]:
    """Find authors by name from local DB and external services, merging results."""
    results = []
    seen_names = set()

    # --- Search local DB (case-insensitive, partial match) ---
    statement = select(Author).where(Author.name.ilike(f"%{name}%"))
    db_result = await db.execute(statement)
    db_authors = db_result.scalars().all()
    for author in db_authors:
        data = AuthorRead.model_validate(author).model_dump()

        seen_names.add(author.name.lower())

    # --- Search Hardcover API ---
    hc_api = hcapi()
    hc_author = await hc_api.search_author(name)
    if hc_author:
        hc_name = hc_author.get("name", "")
        if hc_name and hc_name.lower() not in seen_names:
            results.append(
                {
                    "id": None,
                    "name": hc_author.get("name"),
                    "bio": hc_author.get("bio"),
                    "external_refs": {"hardcover_id": hc_author.get("id")},
                    "in_db": False,
                },
            )
            seen_names.add(hc_name.lower())
        else:
            results.append(
                {
                    "id": None,
                    "name": hc_author.get("name"),
                    "bio": hc_author.get("bio"),
                    "external_refs": {"hardcover_id": hc_author.get("id")},
                    "in_db": True,
                },
            )

    return results


@router.post("/", response_model=AuthorRead)
async def create_author(
    background_tasks: BackgroundTasks,
    author: AuthorCreate,
    db: AsyncSession = Depends(get_db),
) -> AuthorRead:
    hc_api = hcapi()
    hc_author = await hc_api.search_author(author.name)
    if hc_author is not None:
        logger.debug(hc_author)
        name = hc_author.get("name", author.name)
        bio = hc_author.get("bio") or author.bio
        external_refs = {
            "hardcover_id": hc_author.get("id"),
        }
    else:
        await search_inventaire_author(author.name)
        raise HTTPException(status_code=404, detail="Author not found on Hardcover")
    db_author = Author(name=name, bio=bio, external_refs=external_refs)
    db.add(db_author)
    await db.commit()
    await db.refresh(db_author)
    logger.debug(f"Created author: {db_author}")
    logger.info(f"Running update for author {db_author.name}")
    background_tasks.add_task(update_author_books, db_author.id, db)
    books_short = [BookShort(id=str(b.id), title=b.title) for b in db_author.books]
    return AuthorRead(
        id=str(db_author.id),
        name=db_author.name,
        bio=db_author.bio,
        external_refs=dict(db_author.external_refs)
        if db_author.external_refs
        else None,
        books=books_short,
    )


@router.get("/", response_model=list[AuthorRead])
async def list_authors(db: AsyncSession = Depends(get_db)) -> list[AuthorRead]:
    statement = select(Author)
    result = await db.execute(statement)
    authors = result.scalars().all()
    return [
        AuthorRead(
            id=str(a.id),
            name=a.name,
            bio=a.bio,
            external_refs=dict(a.external_refs) if a.external_refs else None,
            books=[BookShort(id=str(b.id), title=b.title) for b in a.books],
        )
        for a in authors
    ]


@router.get("/{author_id}", response_model=AuthorRead)
async def get_author(author_id: UUID, db: AsyncSession = Depends(get_db)) -> AuthorRead:
    statement = select(Author).where(Author.id == author_id)
    result = await db.execute(statement)
    author = result.scalars().first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    books_short = [BookShort(id=str(b.id), title=b.title) for b in author.books]
    return AuthorRead(
        id=str(author.id),
        name=author.name,
        bio=author.bio,
        external_refs=dict(author.external_refs) if author.external_refs else None,
        books=books_short,
    )


@router.put("/{author_id}", response_model=AuthorRead)
async def update_author(
    author_id: UUID,
    author: AuthorCreate,
    db: AsyncSession = Depends(get_db),
) -> AuthorRead:
    statement = select(Author).where(Author.id == author_id)
    result = await db.execute(statement)
    db_author = result.scalars().first()
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    for key, value in author.model_dump().items():
        setattr(db_author, key, value)
    await db.commit()
    await db.refresh(db_author)
    books_short = [BookShort(id=str(b.id), title=b.title) for b in db_author.books]
    return AuthorRead(
        id=str(db_author.id),
        name=db_author.name,
        bio=db_author.bio,
        external_refs=dict(db_author.external_refs)
        if db_author.external_refs
        else None,
        books=books_short,
    )


@router.delete("/{author_id}", response_model=AuthorRead)
async def delete_author(
    author_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> AuthorRead:
    statement = select(Author).where(Author.id == author_id)
    result = await db.execute(statement)
    db_author = result.scalars().first()
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    await db.delete(db_author)
    await db.commit()
    books_short = [BookShort(id=str(b.id), title=b.title) for b in db_author.books]
    return AuthorRead(
        id=str(db_author.id),
        name=db_author.name,
        bio=db_author.bio,
        external_refs=dict(db_author.external_refs)
        if db_author.external_refs
        else None,
        books=books_short,
    )
