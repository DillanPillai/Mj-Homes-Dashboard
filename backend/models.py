# backend/models.py
from __future__ import annotations
from datetime import datetime

from sqlalchemy import Integer, String, Numeric, DateTime, UniqueConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Property(Base):
    __tablename__ = "properties"
    __table_args__ = (
        # Ensures idempotent upserts per provider
        UniqueConstraint("source", "external_id", name="uq_properties_source_extid"),
        {"sqlite_autoincrement": True},
    )

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Provenance for deduplication across providers
    source: Mapped[str | None] = mapped_column(String(32))
    external_id: Mapped[str | None] = mapped_column(String(64))

    # Core fields
    address: Mapped[str] = mapped_column(String, nullable=False)
    suburb: Mapped[str] = mapped_column(String, nullable=False)
    bedrooms: Mapped[int] = mapped_column(Integer, nullable=False)
    bathrooms: Mapped[int] = mapped_column(Integer, nullable=False)
    floor_area: Mapped[float | None] = mapped_column(Numeric(10, 2))
    rent_weekly: Mapped[float | None] = mapped_column(Numeric(10, 2))
    property_type: Mapped[str | None] = mapped_column(String(30))

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
