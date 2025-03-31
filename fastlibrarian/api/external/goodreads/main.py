"""Module for interacting with Goodreads web interface."""

import httpx
from bs4 import BeautifulSoup as bs


class Goodreads:
    """Class to pull data from GR web interface, and serialize as JSON."""

    def __init__(self: "Goodreads") -> None:
        """Initialize Goodreads client with httpx async client."""
        self.client = httpx.AsyncClient()
        self.base_url = "https://www.goodreads.com"

    async def search_author(self: "Goodreads", author: str):
        """Search for an author."""
        url_params = "&search_type=books&search%5Bfield%5D=author"
        url = f"{self.base_url}/search?utf8=✓&q={author}{url_params}"

        response = await self.client.get(url)
        response.raise_for_status()
        return response.text

    def _strip_html(self: "Goodreads", html: str) -> str:
        """Strip HTML tags from a string."""
        soup = bs(html, "html.parser")
        return soup.get_text(strip=True)


gr = Goodreads()


async def main() -> None:
    """Run the main async function."""
    result1 = await gr.search_author("Stephen King")
    result = gr._strip_html(result1)
    print(result)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
