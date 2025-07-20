from typing import Any

import httpx


class Bookshop:
    """Bookshop API client for searching books."""

    BASE_URL = "https://bookshop.org/api/next/instantsearch/multi-search"

    # Query body for a simple search (single query)
    SIMPLE_QUERY_BODY = lambda self, query: {
        "queries": [
            {
                "indexUid": "products",
                "q": query,
                "facets": [
                    "format_category",
                    "is_drm_free",
                    "is_primary",
                ],
                "filter": [
                    [
                        '"is_primary"="true"',
                    ],
                ],
                "attributesToHighlight": [
                    "*",
                ],
                "highlightPreTag": "__ais-highlight__",
                "highlightPostTag": "__/ais-highlight__",
                "limit": 21,
                "offset": 0,
                "matchingStrategy": "frequency",
                "attributesToSearchOn": [
                    "title",
                    "subtitle",
                    "ean",
                    "primary_contributor",
                    "contributors",
                ],
            },
        ],
    }

    # Query body for a more complex search (multiple queries)
    COMPLEX_QUERY_BODY = lambda self, query, format: {
        "queries": [
            {
                "indexUid": "products",
                "q": query,
                "facets": [
                    "format_category",
                    "is_drm_free",
                    "is_primary",
                ],
                "filter": [
                    [
                        f'"format_category"={format}',
                    ],
                ],
                "attributesToHighlight": [
                    "*",
                ],
                "highlightPreTag": "__ais-highlight__",
                "highlightPostTag": "__/ais-highlight__",
                "limit": 21,
                "offset": 0,
                "matchingStrategy": "frequency",
                "attributesToSearchOn": [
                    "title",
                    "subtitle",
                    "ean",
                    "primary_contributor",
                    "contributors",
                ],
            },
            {
                "indexUid": "products",
                "q": query,
                "facets": [
                    "format_category",
                ],
                "attributesToHighlight": [
                    "*",
                ],
                "highlightPreTag": "__ais-highlight__",
                "highlightPostTag": "__/ais-highlight__",
                "limit": 1,
                "offset": 0,
                "matchingStrategy": "frequency",
                "attributesToSearchOn": [
                    "title",
                    "subtitle",
                    "ean",
                    "primary_contributor",
                    "contributors",
                ],
            },
        ],
    }

    def __init__(self):
        self.client = httpx.AsyncClient()

    async def search(
        self,
        query: str,
        format: str = "paperback",
        use_complex: bool = False,
    ) -> dict[str, Any] | None:
        """Search for books using the Bookshop API.

        Args:
            query (str): The search query.
            use_complex (bool): Whether to use the complex query body.

        Returns:
            Optional[Dict[str, Any]]: The API response JSON, or None on error.
        """
        body = (
            self.COMPLEX_QUERY_BODY(query, format)
            if use_complex
            else self.SIMPLE_QUERY_BODY(query)
        )
        try:
            resp = await self.client.post(self.BASE_URL, json=body)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPError:
            return None

    async def aclose(self):
        await self.client.aclose()
