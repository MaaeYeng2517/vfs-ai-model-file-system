import mimetypes, uuid, os, hashlib
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.services.db import get_db, init_db
from app.services.storage import StorageService
from app.models.file import File as FileRecord

router = APIRouter(prefix="/api/vfs", tags=["vfs"])
storage = StorageService()
init_db()

@router.post("/upload")
async def upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
    data = await file.read()
    sha = hashlib.sha256(data).hexdigest()
    key = f"{uuid.uuid4()}/{file.filename}"
    mime = file.content_type or mimetypes.guess_type(file.filename)[0] or "application/octet-stream"
    storage.put(key, data, mime)
    rec = FileRecord(name=file.filename, path=f"/{file.filename}", mime_type=mime, size=len(data), storage_key=key, hash=sha)
    db.add(rec); db.commit(); db.refresh(rec)
    from sqlalchemy import text
    db.execute(text("INSERT INTO file_versions (id,file_id,version,storage_key,size,hash,created_at) VALUES (:id,:fid,1,:sk,:sz,:h,now())"),
               {"id": str(uuid.uuid4()), "fid": str(rec.id), "sk": key, "sz": len(data), "h": sha})
    db.commit()
    return {"id": rec.id, "name": rec.name, "size": rec.size, "mime_type": rec.mime_type, "sha256": sha}

@router.get("/files")
def list_files(db: Session = Depends(get_db)):
    return [{"id": f.id, "name": f.name, "size": f.size, "mime_type": f.mime_type, "path": f.path} for f in db.query(File).all()]

@router.delete("/files/{file_id}")
def delete_file(file_id: str, db: Session = Depends(get_db)):
    rec = db.get(File, file_id)
    if not rec:
        raise HTTPException(404)
    storage.delete(rec.storage_key)
    db.delete(rec); db.commit()
    return {"deleted": file_id}

@router.get("/download/{file_id}")
def download(file_id: str, db: Session = Depends(get_db)):
    rec = db.get(File, file_id)
    if not rec:
        raise HTTPException(404)
    data = storage.get(rec.storage_key)
    return Response(content=data, media_type=rec.mime_type or "application/octet-stream")

_usage = []

@router.post("/usage")
def log_usage(payload: dict):
    _usage.append(payload)
    return {"ok": True}

@router.get("/usage")
def get_usage():
    return _usage


@router.get("/files/{file_id}/versions")
def versions(file_id: str, db: Session = Depends(get_db)):
    from sqlalchemy import text
    rows = db.execute(text("SELECT version,storage_key,size,hash,created_at FROM file_versions WHERE file_id=:fid ORDER BY version"), {"fid": file_id}).fetchall()
    return [{"version": r.version, "storage_key": r.storage_key, "size": r.size, "hash": r.hash, "created_at": str(r.created_at)} for r in rows]


@router.post("/files/{file_id}/blocks")
def build_blocks(file_id: str, db: Session = Depends(get_db)):
    rec = db.get(File, file_id)
    if not rec:
        raise HTTPException(404)
    data = storage.get(rec.storage_key)
    ver = db.execute(text("SELECT id,version_number FROM file_versions WHERE file_id=:fid ORDER BY version_number DESC LIMIT 1"), {"fid": file_id}).fetchone()
    if not ver:
        raise HTTPException(404, "no version")
    from app.services.blocks import store_blocks
    return store_blocks(db, file_id, ver.version_number, data, storage)


@router.post("/files/{file_id}/ingest")
def ingest(file_id: str, db: Session = Depends(get_db)):
    rec = db.get(File, file_id)
    if not rec:
        raise HTTPException(404)
    data = storage.get(rec.storage_key)
    from app.services.knowledge.chunker import extract_text, chunk_text
    from app.services.knowledge.vector import VectorStore
    text = extract_text(data, rec.mime_type or "")
    chunks = chunk_text(text)
    store = VectorStore()
    for c in chunks:
        vec = [float(ord(ch) % 31) for ch in c[:64]] + [0.0] * (64 - min(len(c), 64))
        store.add(vec, {"file_id": file_id, "chunk": c[:200]})
    return {"file_id": file_id, "chunks": len(chunks)}


@router.post("/search")
def search(payload: dict, db: Session = Depends(get_db)):
    q = payload.get("query", "")
    # keyword fallback over files
    rows = db.query(File).all()
    hits = [{"id": f.id, "name": f.name, "path": f.path} for f in rows if q.lower() in (f.name or "").lower() or q.lower() in (f.path or "").lower()]
    return {"query": q, "hits": hits, "mode": "keyword"}


@router.post("/files/{file_id}/tags")
def add_tag(file_id: str, payload: dict, db: Session = Depends(get_db)):
    rec = db.get(File, file_id)
    if not rec:
        raise HTTPException(404)
    import json
    meta = json.loads(rec.meta) if rec.meta else {}
    tags = set(meta.get("tags", []))
    tags.add(payload.get("tag"))
    meta["tags"] = sorted(tags)
    rec.meta = json.dumps(meta)
    db.commit()
    return {"file_id": file_id, "tags": meta["tags"]}

@router.get("/files/{file_id}/tags")
def get_tags(file_id: str, db: Session = Depends(get_db)):
    rec = db.get(File, file_id)
    if not rec:
        raise HTTPException(404)
    import json
    meta = json.loads(rec.meta) if rec.meta else {}
    return {"file_id": file_id, "tags": meta.get("tags", [])}


@router.post("/files/{file_id}/keywords")
def add_keyword(file_id: str, payload: dict, db: Session = Depends(get_db)):
    rec = db.get(File, file_id)
    if not rec:
        raise HTTPException(404)
    import json
    meta = json.loads(rec.meta) if rec.meta else {}
    kws = set(meta.get("keywords", []))
    kws.add(payload.get("keyword"))
    meta["keywords"] = sorted(kws)
    rec.meta = json.dumps(meta)
    db.commit()
    return {"file_id": file_id, "keywords": meta["keywords"]}

@router.get("/files/{file_id}/keywords")
def get_keywords(file_id: str, db: Session = Depends(get_db)):
    rec = db.get(File, file_id)
    if not rec:
        raise HTTPException(404)
    import json
    meta = json.loads(rec.meta) if rec.meta else {}
    return {"file_id": file_id, "keywords": meta.get("keywords", [])}


@router.get("/files/{file_id}/metadata")
def get_metadata(file_id: str, db: Session = Depends(get_db)):
    rec = db.get(File, file_id)
    if not rec:
        raise HTTPException(404)
    import json
    return {"file_id": file_id, "metadata": json.loads(rec.meta) if rec.meta else {}}

@router.put("/files/{file_id}/metadata")
def set_metadata(file_id: str, payload: dict, db: Session = Depends(get_db)):
    rec = db.get(File, file_id)
    if not rec:
        raise HTTPException(404)
    import json
    rec.meta = json.dumps(payload)
    db.commit()
    return {"file_id": file_id, "metadata": payload}
