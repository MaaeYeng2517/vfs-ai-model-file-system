import uuid, hashlib
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.services.db import get_db
from app.models.qa import ContextSnapshot

router = APIRouter(prefix="/api/context", tags=["context"])

@router.post("/build")
def build(question_id: str=Query(...), retrieval_id: str=Query(None), token_budget: int=Query(4000), content: str=Query(""), db: Session=Depends(get_db)):
    try: qid=uuid.UUID(question_id)
    except ValueError: raise HTTPException(400,"invalid question_id")
    rid=uuid.UUID(retrieval_id) if retrieval_id else None
    snap=ContextSnapshot(question_id=qid,retrieval_id=rid,token_budget=token_budget,actual_token_count=len(content.split()),context_hash=hashlib.sha256(content.encode()).hexdigest())
    db.add(snap); db.commit(); db.refresh(snap)
    return {"context_id":str(snap.id),"token_count":snap.actual_token_count}
