from __future__ import annotations
from typing import Dict, Any, List, Tuple
import logging
import math

from sqlalchemy.orm import Session
from sqlalchemy import select

from models import Property
from services.providers.mock_provider import MockPropertyProvider
try:
    from services.providers.realestate_template import RealEstateNZProvider  # optional, may not exist yet
except Exception:
    RealEstateNZProvider = None  # type: ignore

logger = logging.getLogger(__name__)


def get_provider(provider_name: str):
    """
    Return a provider instance by name.
    """
    key = (provider_name or "mock").lower()
    if key == "mock":
        return MockPropertyProvider()
    if key in ("realestate_nz", "realestate", "re_nz") and RealEstateNZProvider:
        return RealEstateNZProvider()
    raise ValueError(f"Unknown provider: {provider_name}")


def _normalize(rec: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalise and validate a single record.
    """
    def S(v):
        return (v or "").strip() if isinstance(v, str) else v

    def F(v):
        if v is None or v == "":
            return None
        try:
            f = float(v)
            return None if math.isnan(f) or math.isinf(f) else f
        except Exception:
            return None

    out = {
        "external_id": S(rec.get("external_id")),
        "address": S(rec.get("address")),
        "suburb": S(rec.get("suburb")),
        "bedrooms": int(rec.get("bedrooms") or 0),
        "bathrooms": int(rec.get("bathrooms") or 0),
        "floor_area": F(rec.get("floor_area")),
        "rent_weekly": F(rec.get("rent_weekly")),
        "property_type": S(rec.get("property_type")),
    }

    if not out["external_id"] or not out["address"] or not out["suburb"]:
        raise ValueError("Missing external_id/address/suburb")
    if out["bedrooms"] <= 0 or out["bathrooms"] <= 0:
        raise ValueError("Bedrooms and bathrooms must be greater than 0")

    return out


def _prepare_rows(provider_name: str, raw: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], int]:
    """
    Prepare rows for DB insertion. Returns (valid_rows, skipped_count).
    """
    rows, skipped = [], 0
    for rec in raw:
        try:
            norm = _normalize(rec)
            norm["source"] = provider_name
            rows.append(norm)
        except Exception as ex:
            logger.warning("[INGEST] Skipping invalid record: %s", ex)
            skipped += 1
    return rows, skipped


def _upsert_any_db(db: Session, rows: List[Dict[str, Any]]) -> Tuple[int, int]:
    """
    Insert or update rows by (source, external_id).
    Returns (inserted_count, updated_count).
    """
    inserted = updated = 0
    for r in rows:
        existing = db.execute(
            select(Property).where(
                Property.source == r["source"],
                Property.external_id == r["external_id"]
            )
        ).scalar_one_or_none()

        if existing:
            existing.address = r["address"]
            existing.suburb = r["suburb"]
            existing.bedrooms = r["bedrooms"]
            existing.bathrooms = r["bathrooms"]
            existing.floor_area = r["floor_area"]
            existing.rent_weekly = r["rent_weekly"]
            existing.property_type = r["property_type"]
            updated += 1
        else:
            db.add(Property(**r))
            inserted += 1

    db.commit()
    return inserted, updated


def run_ingestion(db: Session, provider_name: str = "mock") -> Dict[str, Any]:
    """
    Run ingestion for a given provider.
    """
    provider = get_provider(provider_name)
    raw = provider.fetch_listings()
    rows, skipped = _prepare_rows(provider.name, raw)
    inserted, updated = _upsert_any_db(db, rows)
    summary = {
        "provider": provider.name,
        "fetched": len(raw),
        "inserted": inserted,
        "updated": updated,
        "skipped_invalid": skipped,
    }
    logger.info("[INGEST] %s", summary)
    return summary
