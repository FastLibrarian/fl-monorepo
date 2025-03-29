import httpx


class GoogleBooks:
    """Class for interacting with GBooks API."""

    def __init__(self: "GoogleBooks") -> None:
        """Initialize the Google Books API client."""
        self.base_url = "https://www.googleapis.com/books/v1"
        self.session = httpx.AsyncClient()

    async def search(self: "GoogleBooks", query: str) -> dict:
        """Search for books using a query string."""
        search_url = f"{self.base_url}/volumes?q={query}"
        response = await self.session.get(search_url)
        response.raise_for_status()
        return response.json() if response.status_code == 200 else {}

    # Ref: https://web.archive.org/web/20240619214514/https://stackoverflow.com/questions/66392498/google-books-api-find-exact-author
    async def get_author(self: "GoogleBooks", author: str) -> dict:
        """Get author details using author ID."""
        author = author.replace(" ", "+")
        author_url = f"{self.base_url}q=inauthor:'{author}'"
        response = await self.session.get(author_url)
        response.raise_for_status()
        return response.json() if response.status_code == 200 else {}
