"""Conversion functions for Google Books API models to FastLibrarian models."""

from datetime import datetime

from fastlibrarian.api.external.google_books.models import Volume
from fastlibrarian.api.schemas.author import AuthorCreate
from fastlibrarian.api.schemas.book import BookCreate


class GBooksConversions:
    """Class for staticmethods used in GBooks conversions."""

    @staticmethod
    def convert_date(date_str: str | None) -> datetime | None:
        """Convert Google Books date string to datetime object."""
        if not date_str:
            return None

        # Handle different date formats from Google Books
        formats = ["%Y-%m-%d", "%Y-%m", "%Y"]
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        return None

    @staticmethod
    def volume_to_book(volume: Volume) -> BookCreate:
        """Convert Google Books Volume to FastLibrarian BookCreate model."""
        info = volume.volumeInfo

        # Get ISBN if available
        isbn = next(
            (
                i.identifier
                for i in (info.industryIdentifiers or [])
                if i.type in ("ISBN_13", "ISBN_10")
            ),
            "",
        )

        return BookCreate(
            title=info.title,
            author=info.authors[0] if info.authors else "Unknown Author",
            published_date=convert_date(info.publishedDate) or datetime.now().date(),
            isbn=isbn,
            pages=info.pageCount or 0,
            cover_image=str(info.imageLinks.thumbnail) if info.imageLinks else None,
            language=info.language,
            description=info.description,
        )

    @staticmethod
    def volume_to_author(volume: Volume) -> AuthorCreate:
        """Convert Google Books Volume author information to FastLibrarian AuthorCreate model."""
        info = volume.volumeInfo
        return AuthorCreate(
            name=info.authors[0] if info.authors else "Unknown Author",
        )


class OpenLibraryConversions:
    """Class for staticmethods used in OpenLibrary conversions."""
