from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.services.db import get_db
from sqlalchemy import text
import uuid

router = APIRouter(prefix="/questions", tags=["questions"])

class QIn(BaseModel):
    original_text: str
    tenant_id: str | None = None

@router.post("")
def create_question(body: QIn, db: Session = Depends(get_db)):
    qid = str(uuid.uuid4())
    db.execute(text("INSERT INTO questions (id,original_text,created_at,updated_at) VALUES (:id,:c,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"), {"id": qid, "c": body.original_text})
    db.commit()
    return {"id": qid}

@router.get("")
def list_questions(db: Session = Depends(get_db)):
    rows = db.execute(text("SELECT id,original_text,classification,created_at FROM questions ORDER BY created_at DESC")).fetchall()
    return [{"id": str(r.id), "normalized_text": r.normalized_text, "classification": r.classification, "created_at": str(r.created_at)} for r in rows]

@router.get("/{qid}")
def get_question(qid: str, db: Session = Depends(get_db)):
    row = db.execute(text("SELECT id,original_text,classification,created_at FROM questions WHERE id=:id"), {"id": qid}).first()
    if not row: raise HTTPException(404)
    return {"id": str(row.id), "original_text": row.original_text, "classification": row.classification, "created_at": str(row.created_at)}

@router.get("/{qid}/history")
def history(qid: str, db: Session = Depends(get_db)):
    rows = db.execute(text("SELECT version,normalized_text,created_at FROM question_versions WHERE question_id=:id ORDER BY version"), {"id": qid}).fetchall()
    return [{"version": r.version, "normalized_text": r.normalized_text, "created_at": str(r.created_at)} for r in rows]

@router.put("/{qid}")
def update_question(qid: str, body: QIn, db: Session = Depends(get_db)):
    db.execute(text("UPDATE questions SET original_text=:c WHERE id=:id"), {"id": qid, "c": body.original_text})
    db.commit()
    return {"id": qid, "updated": True}

@router.delete("/{qid}")
def delete_question(qid: str, db: Session = Depends(get_db)):
    db.execute(text("DELETE FROM questions WHERE id=:id"), {"id": qid})
    db.commit()
    return {"deleted": qid}
