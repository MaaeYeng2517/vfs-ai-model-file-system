import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.services.db import get_db
from app.models.qa import Memory

router = APIRouter(prefix="/api/memory", tags=["memory"])

@router.post("")
def create(memory_type: str=Query(...), content: str=Query(...), tenant_id: str=Query(None), db: Session=Depends(get_db)):
    m=Memory(memory_type=memory_type,content=content,tenant_id=tenant_id)
    db.add(m); db.commit(); db.refresh(m)
    return {"memory_id":str(m.id)}

@router.get("")
def list_memories(db: Session=Depends(get_db)):
    return [{"id":str(m.id),"type":m.memory_type,"content":m.content} for m in db.query(Memory).all()]
