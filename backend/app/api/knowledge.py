import uuid, json
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.services.db import get_db
from app.models.namespace import Namespace
from app.models.knowledge import KnowledgeDocument, KnowledgeChunk

router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])

def _ns(db, slug):
    ns = db.query(Namespace).filter((Namespace.slug==slug)|(Namespace.name==slug)).first()
    if not ns: raise HTTPException(404, "namespace not found")
    return ns

@router.post("/ingest")
def ingest(namespace: str=Query(...), title: str=Query(...), content: str=Query(...), chunk_size: int=Query(500), db: Session=Depends(get_db)):
    ns=_ns(db,namespace)
    doc=KnowledgeDocument(namespace_id=ns.id,title=title,content=content,status="processing")
    db.add(doc); db.commit(); db.refresh(doc)
    words=content.split()
    chunks=[]
    for i in range(0,len(words),chunk_size):
        part=" ".join(words[i:i+chunk_size])
        ch=KnowledgeChunk(document_id=doc.id,chunk_index=i//chunk_size,content=part,token_count=len(part.split()))
        db.add(ch); chunks.append(ch)
    doc.status="ingested"
    db.commit()
    return {"document_id":str(doc.id),"chunks":len(chunks)}

@router.get("/documents")
def list_documents(namespace: str=Query(None), db: Session=Depends(get_db)):
    q=db.query(KnowledgeDocument)
    if namespace:
        ns=_ns(db,namespace); q=q.filter(KnowledgeDocument.namespace_id==ns.id)
    return [{"id":str(d.id),"title":d.title,"status":d.status,"created_at":d.created_at.isoformat()} for d in q.all()]

@router.get("/documents/{doc_id}/chunks")
def list_chunks(doc_id: str, db: Session=Depends(get_db)):
    try: did=uuid.UUID(doc_id)
    except ValueError: raise HTTPException(400,"invalid id")
    chunks=db.query(KnowledgeChunk).filter(KnowledgeChunk.document_id==did).order_by(KnowledgeChunk.chunk_index).all()
    return [{"id":str(c.id),"index":c.chunk_index,"content":c.content,"token_count":c.token_count} for c in chunks]
