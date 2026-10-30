import os, io, mimetypes
from minio import Minio

BUCKET = os.getenv("MINIO_BUCKET", "vfs")
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET = os.getenv("MINIO_SECRET_KEY", "minioadmin")
LOCAL_DIR = os.getenv("LOCAL_STORAGE", "./storage")

class StorageService:
    def __init__(self):
        try:
            self.client = Minio(MINIO_ENDPOINT, access_key=MINIO_ACCESS, secret_key=MINIO_SECRET, secure=False)
            self.use_minio = True
            if not self.client.bucket_exists(BUCKET):
                self.client.make_bucket(BUCKET)
        except Exception:
            self.client = None
            self.use_minio = False
            os.makedirs(LOCAL_DIR, exist_ok=True)

    def put(self, key, data, content_type=None):
        if self.use_minio:
            self.client.put_object(BUCKET, key, io.BytesIO(data), len(data), content_type=content_type or "application/octet-stream")
        else:
            path = os.path.join(LOCAL_DIR, key)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "wb") as f:
                f.write(data)

    def get(self, key):
        if self.use_minio:
            resp = self.client.get_object(BUCKET, key)
            data = resp.read()
            resp.close()
            resp.release_conn()
            return data
        with open(os.path.join(LOCAL_DIR, key), "rb") as f:
            return f.read()

    def delete(self, key):
        if self.use_minio:
            self.client.remove_object(BUCKET, key)
        else:
            p = os.path.join(LOCAL_DIR, key)
            if os.path.exists(p):
                os.remove(p)
