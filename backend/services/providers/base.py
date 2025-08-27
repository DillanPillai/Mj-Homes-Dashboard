from __future__ import annotations
from typing import Protocol, List, TypedDict, Optional


class ListingRecord(TypedDict, total=False):
    """
    Standardised listing payload every provider must return.
    - external_id: provider-unique ID for the listing
    - address: street address
    - suburb: suburb name (e.g., 'Manurewa')
    - bedrooms: integer > 0
    - bathrooms: integer > 0
    - floor_area: square meters, may be None
    - rent_weekly: weekly rent price, may be None
    - property_type: e.g., 'House', 'Apartment', may be None
    """
    external_id: str
    address: str
    suburb: str
    bedrooms: int
    bathrooms: int
    floor_area: Optional[float]
    rent_weekly: Optional[float]
    property_type: Optional[str]


class PropertyProvider(Protocol):
    """
    Provider interface. Implementations must expose:
    - name: short provider key (e.g., 'mock', 'realestate_nz')
    - fetch_listings(): return a list of ListingRecord dicts
    """
    name: str

    def fetch_listings(self) -> List[ListingRecord]:
        ...
