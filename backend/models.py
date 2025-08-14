from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Numeric, DateTime, text
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Property(Base):
    __tablename__ = "properties"
    # ensure AUTOINCREMENT on SQLite
    __table_args__ = {"sqlite_autoincrement": True}

    # INTEGER PRIMARY KEY works across Postgres + SQLite
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    address: Mapped[str] = mapped_column(String, nullable=False)
    suburb: Mapped[str] = mapped_column(String, nullable=False)
    bedrooms: Mapped[int] = mapped_column(Integer, nullable=False)
    bathrooms: Mapped[int] = mapped_column(Integer, nullable=False)
    floor_area: Mapped[float | None] = mapped_column(Numeric(10, 2))
    rent_weekly: Mapped[float | None] = mapped_column(Numeric(10, 2))
    property_type: Mapped[str | None] = mapped_column(String(30))
    # use a cross-DB default that works in SQLite & Postgres
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
