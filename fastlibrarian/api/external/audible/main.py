import httpx


class Audible:
    """Class to interface with Audible API"""

    def __init__(self: "Audible") -> None:
        self.base_url = "https://api.audible.com/1.0/catalog"
        self.client = httpx.AsyncClient()

    async def __del__(self: "Audible") -> None:
        await self.client.aclose()

    async def search_audible(self: "Audible", query: str):
        """Search audible for query string."""
        url = f"{self.base_url}/products?{query}"
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()
