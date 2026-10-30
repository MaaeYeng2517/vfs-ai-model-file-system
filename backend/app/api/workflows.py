from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.services.db import get_db
from sqlalchemy import text
import uuid

router = APIRouter(prefix="/workflows", tags=["workflows"])

class WIn(BaseModel):
    name: str
    definition: dict | None = None

@router.get("")
def list_workflows(db: Session = Depends(get_db)):
    rows = db.execute(text("SELECT id,name,created_at,updated_at FROM workflows ORDER BY created_at DESC")).fetchall()
    return [{"id": str(r.id), "name": r.name, "created_at": str(r.created_at)} for r in rows]

@router.post("")
def create_workflow(body: WIn, db: Session = Depends(get_db)):
    wid = str(uuid.uuid4())
    db.execute(text("INSERT INTO workflows (id,name,created_at,updated_at) VALUES (:id,:n,now(),now())"), {"id": wid, "n": body.name})
    db.commit()
    return {"id": wid}

@router.post("/{wid}/execute")
def execute(wid: str, db: Session = Depends(get_db)):
    eid = str(uuid.uuid4())
    db.execute(text("INSERT INTO workflow_executions (id,workflow_version_id,status,started_at) VALUES (:id,:wv,'running',now())"),
               {"id": eid, "wv": wid})
    db.commit()
    return {"execution_id": eid, "status": "running"}
