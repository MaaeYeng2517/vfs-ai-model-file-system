from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends
from app.services.db import get_db

router = APIRouter(prefix="/api/chat", tags=["chat"])

@router.post("/")
def chat(payload: dict, db: Session = Depends(get_db)):
    q = payload.get("message", "")
    # simple retrieval over files
    from sqlalchemy import text
    rows = db.execute(text("SELECT name,path FROM files WHERE name ILIKE :q OR path ILIKE :q"), {"q": f"%{q}%"}).fetchall()
    sources = [{"name": r.name, "path": r.path} for r in rows]
    return {"answer": f"Found {len(sources)} related files for: {q}", "sources": sources}
