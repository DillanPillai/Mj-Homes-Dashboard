# backend/schemas.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict


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


# --- Upload summary for dataset uploads ---
class UploadSummary(BaseModel):
    total_rows: int = Field(..., description="Total rows processed from the uploaded dataset")
    rows_inserted: int = Field(..., description="Number of new rows successfully inserted into the database")
    rows_skipped: int = Field(..., description="Number of duplicate rows skipped (already existed in DB)")
    message: str = Field(..., description="Status message about the upload")
    cleaned_file_name: str = Field(..., description="Name of the cleaned CSV file saved on the server")
    download_url: str = Field(..., description="API endpoint to download the cleaned CSV/XLSX file")


# --- NEW: pipeline run summary ---
class PipelineRunSummary(BaseModel):
    stage_counts: Dict[str, int] = Field(
        ..., description="Number of rows at each stage (ingested, validated_ok, rejected, duplicates, transformed_ok, stored)"
    )
    report_csv: Optional[str] = Field(
        None, description="Relative path to CSV issues report (if issues found)"
    )
    duration_seconds: float = Field(..., description="Pipeline execution time in seconds")
    mode: str = Field(..., description="'append' (default) or 'replace' mode for DB storage")
