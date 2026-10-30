import mimetypes, uuid, os
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
    key = f"{uuid.uuid4()}/{file.filename}"
    mime = file.content_type or mimetypes.guess_type(file.filename)[0] or "application/octet-stream"
    storage.put(key, data, mime)
    rec = FileRecord(name=file.filename, path=f"/{file.filename}", mime_type=mime, size=len(data), storage_key=key)
    db.add(rec); db.commit(); db.refresh(rec)
    return {"id": rec.id, "name": rec.name, "size": rec.size, "mime_type": rec.mime_type}

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
