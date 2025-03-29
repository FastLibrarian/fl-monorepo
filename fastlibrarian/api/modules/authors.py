"""Author operations module."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastlibrarian.api.models.main import AuthorModel
from fastlibrarian.api.schemas.author import AuthorCreate


async def get_author(db: AsyncSession, author_id: int) -> AuthorModel | None:
    """Get an author by ID."""
    result = await db.execute(select(AuthorModel).filter(AuthorModel.id == author_id))
    return result.scalar_one_or_none()


async def get_authors(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
) -> list[AuthorModel]:
    """Get list of authors."""
    result = await db.execute(select(AuthorModel).offset(skip).limit(limit))
    return result.scalars().all()


async def create_author(db: AsyncSession, author: AuthorCreate) -> AuthorModel:
    """Create a new author."""
    db_author = AuthorModel(**author.model_dump())
    db.add(db_author)
    await db.commit()
    await db.refresh(db_author)
    return db_author

