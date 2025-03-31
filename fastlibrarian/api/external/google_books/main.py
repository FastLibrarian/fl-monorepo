import httpx
from loguru import logger

from .models import GoogleBooksResponse


class GoogleBooks:
    """Class for interacting with GBooks API."""

    def __init__(self: "GoogleBooks") -> None:
        """Initialize the Google Books API client."""
        self.base_url = "https://www.googleapis.com/books/v1"
        self.session = httpx.AsyncClient()

    async def search(self: "GoogleBooks", query: str) -> GoogleBooksResponse:
        """Search for books using a query string."""
        search_url = f"{self.base_url}/volumes?q='{query}'"
        logger.debug(f"Query passed to Google: {search_url}")
        response = await self.session.get(search_url)
        logger.debug(response.text)
        response.raise_for_status()
        raw_response = response.json() if response.status_code == 200 else {}
        return GoogleBooksResponse.model_validate(raw_response)

    # Ref: https://web.archive.org/web/20240619214514/https://stackoverflow.com/questions/66392498/google-books-api-find-exact-author
    async def get_author(self: "GoogleBooks", author: str) -> GoogleBooksResponse:
        """Get author details using author name."""
        author_url = f"{self.base_url}/volumes?q=inauthor:{author}&projection=lite&printType=books"
        response = await self.session.get(author_url)
        response.raise_for_status()
        raw_response = response.json() if response.status_code == 200 else {}
        return GoogleBooksResponse.model_validate(raw_response)
