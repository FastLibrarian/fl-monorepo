import os
from dataclasses import dataclass


@dataclass
class Config:
    """Configuration class for Fast Librarian."""

    hc_api_key: str = os.getenv("HC_API_KEY", "")
