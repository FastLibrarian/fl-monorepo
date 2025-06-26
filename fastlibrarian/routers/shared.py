import os

HARD_COVER_API_KEY = os.getenv("HARD_COVER_API_KEY")

hardcover_headers = {
    "authorization": f"Bearer {HARD_COVER_API_KEY}",
}
