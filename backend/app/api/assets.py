import json, uuid, mimetypes, hashlib
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.services.db import get_db
from app.services.storage import StorageService
from app.models.asset import Asset
from app.models.namespace import Namespace

router = APIRouter(prefix="/api/assets", tags=["assets"])
storage = StorageService()


def _get_namespace(db: Session, slug: str) -> Namespace:
    ns = db.query(Namespace).filter((Namespace.slug == slug) | (Namespace.name == slug)).first()
    if not ns:
        raise HTTPException(404, "namespace not found")
    return ns


@router.post("/register")
async def register_asset(
    namespace: str = Query(...),
    asset_type: str = Query("file"),
    name: str = Query(...),
    path: str = Query(...),
    metadata: str = Query(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    ns = _get_namespace(db, namespace)
    data = await file.read()
    key = f"{ns.slug}/{asset_type}/{uuid.uuid4()}/{name}"
    mime = file.content_type or mimetypes.guess_type(name)[0] or "application/octet-stream"
    storage.put(key, data, mime)
    digest = hashlib.sha256(data).hexdigest()
    meta = None
    if metadata:
        try:
            meta = json.loads(metadata)
        except json.JSONDecodeError:
            raise HTTPException(400, "invalid metadata json")
    rec = Asset(
        namespace_id=ns.id,
        asset_type=asset_type,
        name=name,
        path=path,
        mime_type=mime,
        size=len(data),
        storage_key=key,
        hash=digest,
        meta=json.dumps(meta) if meta is not None else None,
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return {
        "id": str(rec.id),
        "namespace": ns.slug,
        "asset_type": rec.asset_type,
        "name": rec.name,
        "path": rec.path,
        "mime_type": rec.mime_type,
        "size": rec.size,
        "hash": rec.hash,
    }


@router.get("")
def list_assets(
    namespace: str = Query(None),
    asset_type: str = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(Asset).filter(Asset.is_deleted == False)
    if namespace:
        ns = _get_namespace(db, namespace)
        q = q.filter(Asset.namespace_id == ns.id)
    if asset_type:
        q = q.filter(Asset.asset_type == asset_type)
    rows = q.all()
    return [
        {
            "id": str(a.id),
            "namespace_id": str(a.namespace_id),
            "asset_type": a.asset_type,
            "name": a.name,
            "path": a.path,
            "mime_type": a.mime_type,
            "size": a.size,
            "hash": a.hash,
            "metadata": json.loads(a.meta) if a.meta else None,
            "created_at": a.created_at.isoformat(),
        }
        for a in rows
    ]


@router.get("/{asset_id}")
def get_asset(asset_id: str, db: Session = Depends(get_db)):
    try:
        aid = uuid.UUID(asset_id)
    except ValueError:
        raise HTTPException(400, "invalid id")
    a = db.get(Asset, aid)
    if not a or a.is_deleted:
        raise HTTPException(404)
    return {
        "id": str(a.id),
        "namespace_id": str(a.namespace_id),
        "asset_type": a.asset_type,
        "name": a.name,
        "path": a.path,
        "mime_type": a.mime_type,
        "size": a.size,
        "storage_key": a.storage_key,
        "hash": a.hash,
        "metadata": json.loads(a.meta) if a.meta else None,
        "created_at": a.created_at.isoformat(),
        "updated_at": a.updated_at.isoformat(),
    }


@router.get("/{asset_id}/download")
def download_asset(asset_id: str, db: Session = Depends(get_db)):
    try:
        aid = uuid.UUID(asset_id)
    except ValueError:
        raise HTTPException(400, "invalid id")
    a = db.get(Asset, aid)
    if not a or a.is_deleted or not a.storage_key:
        raise HTTPException(404)
    data = storage.get(a.storage_key)
    return Response(content=data, media_type=a.mime_type or "application/octet-stream")


@router.delete("/{asset_id}")
def delete_asset(asset_id: str, db: Session = Depends(get_db)):
    try:
        aid = uuid.UUID(asset_id)
    except ValueError:
        raise HTTPException(400, "invalid id")
    a = db.get(Asset, aid)
    if not a:
        raise HTTPException(404)
    if a.storage_key:
        storage.delete(a.storage_key)
    a.is_deleted = True
    db.commit()
    return {"deleted": str(a.id)}