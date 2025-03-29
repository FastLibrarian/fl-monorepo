"""Module to interact with OpenLibrary API."""

import httpx


class OpenLibrary:
    """Interact with OpenLibrary API."""

    def __init__(self: "OpenLibrary") -> None:
        """Initialize OpenLibrary API client."""
        self.base_url = "https://openlibrary.org/search"
        self.session = httpx.AsyncClient()

    def author_search(self: "OpenLibrary", author: str) -> dict:
        """Search for books by author."""
        author_url = f"{self.base_url}/authors.json?q={author}"
        response = self.session.get(author_url)
        response.raise_for_status()
        return response.json()

    def book_search(self: "OpenLibrary", title: str) -> dict:
        """Search for books by title."""
        book_url = f"{self.base_url}/books.json?q={title}"
        response = self.session.get(book_url)
        response.raise_for_status()
        return response.json()

    def isbn_search(self: "OpenLibrary", isbn: str) -> dict:
        """Search for books by ISBN."""
        isbn_url = f"{self.base_url}/isbn/{isbn}.json"
        response = self.session.get(isbn_url)
        response.raise_for_status()
        return response.json()

    def close(self: "OpenLibrary") -> None:
        """Close the HTTP session."""
        self.session.close()
