import os
from typing import List

from .base import ListingRecord


class MockPropertyProvider:
    """
    Mock provider that returns a small, deterministic set of listings.
    This lets you run the ingestion end-to-end without a real API.
    It also demonstrates reading an API key from environment variables.
    """
    name = "mock"

    def __init__(self) -> None:
        # Demonstrates secrets via env vars (no secrets hardcoded)
        # Not required for the mock to function, but kept for acceptance tests.
        self.api_key = os.getenv("API_KEY", "")

    def fetch_listings(self) -> List[ListingRecord]:
        # In a real provider you would perform HTTP requests here.
        # Keep sample data simple, valid, and mapped to your DB schema.
        return [
            {
                "external_id": "mock-1001",
                "address": "12 Example Street",
                "suburb": "Manurewa",
                "bedrooms": 3,
                "bathrooms": 1,
                "floor_area": 90.0,
                "rent_weekly": 650.0,
                "property_type": "House",
            },
            {
                "external_id": "mock-1002",
                "address": "8 Sample Avenue",
                "suburb": "Albany",
                "bedrooms": 2,
                "bathrooms": 1,
                "floor_area": 70.0,
                "rent_weekly": 550.0,
                "property_type": "Apartment",
            },
        ]
