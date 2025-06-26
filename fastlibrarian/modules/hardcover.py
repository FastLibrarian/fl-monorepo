import httpx
from loguru import logger

from fastlibrarian.config import Config


class HardcoverAPI:
    """A class to interact with the Hardcover API for book-related operations."""

    def __init__(self):
        url = "https://api.hardcover.app/v1/graphql"
        self.headers = {
            "authorization": f"Bearer {Config.hc_api_key}",
        }
        self.client = httpx.AsyncClient(headers=self.headers, base_url=url)

    async def search_author(self, author: str):
        """Search for an author using the Hardcover GraphQL API."""
        url = ""
        query = f"""
        {{
          search(
            query: "{author}",
            query_type: "Author",
            per_page: 5,
            page: 1
          )
          {{
            results
          }}
        }}
        """
        payload = {"query": query}

        resp = await self.client.post(url=url, json=payload)
        logger.debug(f"Hardcover API response: {resp.text}")
        if resp.status_code != 200:
            return None
        data = resp.json()
        # Adjust parsing to match the actual API response structure
        results = data.get("data", {}).get("search", {}).get("results", {})
        hits = results.get("hits", [])
        for hit in hits:
            doc = hit.get("document", {})
            if doc.get("name", "").lower() == author.lower():
                return {
                    "name": doc.get("name"),
                    "bio": doc.get("bio"),
                    "id": doc.get("id"),
                }
        if hits:
            doc = hits[0].get("document", {})
            return {"name": doc.get("name"), "bio": doc.get("bio"), "id": doc.get("id")}
        return None

    async def get_works(self, id: str):
        """Extract and return works for an author from Hardcover, structured for db."""
        query = f"""{{
        contributions(where: {{author_id: {{_eq: {id}}}}}) {{
                    book {{
                        id
                        title
                        description
                        editions {{
                            asin
                            isbn_10
                            isbn_13
                        }}
                        book_series {{
                            position
                            series {{
                                name
                                id
                                }}
                        }}
                    }}

                }}
        }}
        """
        payload = {"query": query}
        url = ""
        resp = await self.client.post(url=url, json=payload)
        logger.debug(f"Hardcover API response: {resp.text}")
        if resp.status_code != 200:
            return None
        data = resp.json()
        results = data.get("data", {}).get("contributions", [])
        books = []
        for result in results:
            book = result.get("book")
            if not book:
                continue

            editions = book.get("editions", [])

            book_series = [
                {
                    "position": bs.get("position"),
                    "series_id": bs.get("series", {}).get("id"),
                    "name": bs.get("series", {}).get("name"),
                }
                for bs in book.get("book_series", [])
            ]
            books.append(
                {
                    "id": book.get("id"),
                    "title": book.get("title"),
                    "description": book.get("description"),
                    "editions": editions,
                    "book_series": book_series,
                },
            )
        return books
