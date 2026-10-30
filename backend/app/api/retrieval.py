import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.services.db import get_db
from app.models.qa import RetrievalRun, RetrievalCandidate, DocumentChunk

router = APIRouter(prefix="/api/retrieval", tags=["retrieval"])

@router.post("/search")
def search(question_id: str = Query(...), query: str = Query(...), top_k: int = Query(10), db: Session = Depends(get_db)):
    try: qid=uuid.UUID(question_id)
    except ValueError: raise HTTPException(400,"invalid question_id")
    run=RetrievalRun(question_id=qid,search_method="keyword",query=query,top_k=top_k,status="completed")
    db.add(run); db.commit(); db.refresh(run)
    chunks=db.query(DocumentChunk).filter(DocumentChunk.content.ilike(f"%{query}%")).limit(top_k).all()
    for i,c in enumerate(chunks,1):
        db.add(RetrievalCandidate(retrieval_id=run.id,chunk_id=c.id,rank=i,score=1.0,selected=True))
    db.commit()
    return {"retrieval_id":str(run.id),"candidates":[str(c.id) for c in chunks]}
