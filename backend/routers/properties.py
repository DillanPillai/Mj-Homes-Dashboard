from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

from db import get_db
from models import Property
from schemas import PropertyOut

router = APIRouter(prefix="/properties", tags=["Properties"])

@router.get("", response_model=List[PropertyOut], summary="List property listings")
def list_properties(
    limit: int = Query(100, ge=1, le=500, description="Max rows to return"),
    offset: int = Query(0, ge=0, description="Rows to skip"),
    db: Session = Depends(get_db),
):
    try:
        stmt = (
            select(Property)
            .order_by(Property.updated_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return db.execute(stmt).scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e.__class__.__name__}")
