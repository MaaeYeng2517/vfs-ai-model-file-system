from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.db import get_db
from sqlalchemy import text

router = APIRouter(prefix="/monitoring", tags=["monitoring"])

@router.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "ok"}

@router.get("/metrics")
def metrics():
    return {"requests": 0, "errors": 0}

@router.get("/jobs")
def jobs():
    return []
