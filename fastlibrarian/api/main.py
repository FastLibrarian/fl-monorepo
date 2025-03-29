"""FastAPI application initialization and configuration."""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from fastlibrarian.api.routers import authors, books

app = FastAPI(title="FastLibrarian API")

# Include routers
app.include_router(books.router)
app.include_router(authors.router)


@app.get("/", response_class=JSONResponse)
async def read_root() -> dict[str, str]:
    """Return welcome message."""
    return {"message": "Welcome to FastLibrarian API"}
