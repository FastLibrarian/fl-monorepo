from uuid import uuid4

import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastlibrarian.db import get_db
from fastlibrarian.models import series as models
from fastlibrarian.models.schemas import SeriesCreate, SeriesRead

from .shared import hardcover_headers  # Import the headers for Hardcover API

router = APIRouter(prefix="/series", tags=["series"])


async def search_hardcover_series(name: str):
    """Search for a series using the Hardcover GraphQL API."""
    url = "https://api.hardcover.app/v1/graphql"
    query = """
    query SearchSeries($query: String!) {
      search(
        query: $query,
        query_type: "Series",
        per_page: 5,
        page: 1
      ) {
        results {
          ... on SeriesSearchResult {
            id
            name
            description
          }
        }
      }
    }
    """
    variables = {"query": name}
    payload = {"query": query, "variables": variables}
    async with httpx.AsyncClient(headers=hardcover_headers) as client:
        resp = await client.post(url, json=payload)
        if resp.status_code != 200:
            return None
        data = resp.json()
        results = data.get("data", {}).get("search", {}).get("results", [])
        for series in results:
            if series.get("name", "").lower() == name.lower():
                return series
        if results:
            return results[0]
        return None


@router.post("/", response_model=SeriesRead)
async def create_series(
    data: dict,
    db: AsyncSession = Depends(get_db),
) -> SeriesRead:
    """Create a new series, searching Hardcover API first."""
    name = data.get("name")
    if not name:
        raise HTTPException(status_code=400, detail="Name is required")
    hc_series = await search_hardcover_series(name)
    if not hc_series:
        raise HTTPException(status_code=404, detail="Series not found on Hardcover")
    name = hc_series.get("name")
    description = hc_series.get("description")
    db_series = models.Series(
        id=uuid4(),
        name=name,
        description=description,
    )
    db.add(db_series)
    await db.commit()
    await db.refresh(db_series)
    return SeriesRead.model_validate(db_series)


@router.get("/", response_model=list[SeriesRead])
async def list_series(db: AsyncSession = Depends(get_db)) -> list[SeriesRead]:
    """List all series."""
    statement = select(models.Series)
    result = await db.execute(statement)
    series_list = result.scalars().all()
    return [SeriesRead.model_validate(s) for s in series_list]


@router.get("/{series_id}", response_model=SeriesRead)
async def get_series(series_id: int, db: AsyncSession = Depends(get_db)) -> SeriesRead:
    """Get a series by ID."""
    statement = select(models.Series).where(models.Series.id == series_id)
    result = await db.execute(statement)
    series = result.scalars().first()
    if not series:
        raise HTTPException(status_code=404, detail="Series not found")
    return SeriesRead.model_validate(series)


@router.put("/{series_id}", response_model=SeriesRead)
async def update_series(
    series_id: int,
    series: SeriesCreate,
    db: AsyncSession = Depends(get_db),
) -> SeriesRead:
    """Update a series by ID."""
    statement = select(models.Series).where(models.Series.id == series_id)
    result = await db.execute(statement)
    db_series = result.scalars().first()
    if not db_series:
        raise HTTPException(status_code=404, detail="Series not found")
    for key, value in series.model_dump().items():
        setattr(db_series, key, value)
    await db.commit()
    await db.refresh(db_series)
    return SeriesRead.model_validate(db_series)


@router.delete("/{series_id}", response_model=SeriesRead)
async def delete_series(
    series_id: int,
    db: AsyncSession = Depends(get_db),
) -> SeriesRead:
    """Delete a series by ID."""
    statement = select(models.Series).where(models.Series.id == series_id)
    result = await db.execute(statement)
    db_series = result.scalars().first()
    if not db_series:
        raise HTTPException(status_code=404, detail="Series not found")
    await db.delete(db_series)
    await db.commit()
    return SeriesRead.model_validate(db_series)
