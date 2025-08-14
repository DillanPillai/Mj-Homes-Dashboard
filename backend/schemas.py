from pydantic import BaseModel, Field
from datetime import datetime

class PropertyOut(BaseModel):
    id: int
    address: str = Field(..., description="Street address")
    suburb: str
    bedrooms: int
    bathrooms: int
    floor_area: float | None = None
    rent_weekly: float | None = Field(None, description="Weekly rent (price)")
    property_type: str | None = Field(None, description="House/Apartment/etc.")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # pydantic v2
