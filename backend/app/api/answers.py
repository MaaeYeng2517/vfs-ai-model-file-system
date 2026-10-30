import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.services.db import get_db
from app.models.qa import AIAnswer

router = APIRouter(prefix="/api/answers", tags=["answers"])

@router.post("/generate")
def generate(question_id: str=Query(...), answer_text: str=Query(...), model_name: str=Query("local"), db: Session=Depends(get_db)):
    try: qid=uuid.UUID(question_id)
    except ValueError: raise HTTPException(400,"invalid question_id")
    ans=AIAnswer(question_id=qid,answer_text=answer_text,model_name=model_name,verification_status="unverified")
    db.add(ans); db.commit(); db.refresh(ans)
    return {"answer_id":str(ans.id)}
