from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastlibrarian.routers import authors_router, books_router, series_router

app = FastAPI(
    title="FastLibrarian API",
    version="1.0.0",
)

# Allow frontend (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authors_router)
app.include_router(books_router)
app.include_router(series_router)
