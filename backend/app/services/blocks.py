"""Block engine: chunking, dedup, manifest."""
import hashlib, uuid
from sqlalchemy.orm import Session
from sqlalchemy import text

CHUNK_SIZE = 1024 * 1024  # 1MB


def store_blocks(db: Session, file_id: str, version: int, data: bytes, storage) -> dict:
    chunks = [data[i:i + CHUNK_SIZE] for i in range(0, len(data), CHUNK_SIZE)] or [b""]
    manifest_id = str(uuid.uuid4())
    db.execute(text("INSERT INTO manifests (id,file_version_id,format_version,block_size,total_blocks) VALUES (:id,:fv,'1.0',:bs,:tb)"),
               {"id": manifest_id, "fv": None, "bs": CHUNK_SIZE, "tb": len(chunks)})
    # link manifest to version
    db.execute(text("UPDATE file_versions SET manifest_id=:m WHERE file_id=:fid AND version_number=:v"),
               {"m": manifest_id, "fid": file_id, "v": version})
    for i, c in enumerate(chunks):
        h = hashlib.sha256(c).hexdigest()
        row = db.execute(text("SELECT id,storage_key FROM blocks WHERE checksum_sha256=:h"), {"h": h}).fetchone()
        if row:
            block_id = row.id
        else:
            block_id = str(uuid.uuid4())
            key = f"blocks/{h}"
            storage.put(key, c, "application/octet-stream")
            db.execute(text("INSERT INTO blocks (id,checksum_sha256,size_bytes,storage_key) VALUES (:id,:h,:sz,:sk)"),
                       {"id": block_id, "h": h, "sz": len(c), "sk": key})
        db.execute(text("INSERT INTO file_blocks (manifest_id,block_id,sequence_number) VALUES (:m,:b,:seq)"),
                   {"m": manifest_id, "b": block_id, "seq": i})
    db.commit()
    return {"manifest_id": manifest_id, "total_blocks": len(chunks), "unique": len(set(hashlib.sha256(c).hexdigest() for c in chunks))}
