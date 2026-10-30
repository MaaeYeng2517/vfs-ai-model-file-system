"""Object storage service — supports MinIO and local filesystem backends."""
import os
import io
import mimetypes
from typing import Optional

from minio import Minio
from minio.error import S3Error

from app.config import settings
from app.logger import logger


class StorageService:
    """Unified object storage with MinIO as primary and local fallback."""

    def __init__(self):
        self.use_minio = False
        self.client: Optional[Minio] = None
        self.local_dir = settings.local_storage_path

        if settings.storage_backend == "minio":
            try:
                self.client = Minio(
                    settings.minio_endpoint,
                    access_key=settings.minio_access_key,
                    secret_key=settings.minio_secret_key,
                    secure=settings.minio_secure,
                )
                if not self.client.bucket_exists(settings.minio_bucket):
                    self.client.make_bucket(settings.minio_bucket)
                self.use_minio = True
                logger.info(f"Storage backend: MinIO @ {settings.minio_endpoint}")
            except Exception as e:
                logger.warning(f"MinIO unavailable, falling back to local: {e}")
                self.use_minio = False

        if not self.use_minio:
            os.makedirs(self.local_dir, exist_ok=True)
            logger.info(f"Storage backend: local @ {self.local_dir}")

    @property
    def bucket(self) -> str:
        return settings.minio_bucket

    def put(self, key: str, data: bytes, content_type: Optional[str] = None) -> str:
        """Store an object and return the storage key."""
        ct = content_type or "application/octet-stream"
        if self.use_minio and self.client:
            try:
                self.client.put_object(
                    self.bucket,
                    key,
                    io.BytesIO(data),
                    length=len(data),
                    content_type=ct,
                )
                return key
            except S3Error as e:
                logger.error(f"MinIO put failed: {e}")
                # fall through to local

        path = os.path.join(self.local_dir, key)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(data)
        return key

    def get(self, key: str) -> bytes:
        """Retrieve an object by key."""
        if self.use_minio and self.client:
            try:
                resp = self.client.get_object(self.bucket, key)
                data = resp.read()
                resp.close()
                resp.release_conn()
                return data
            except S3Error as e:
                logger.error(f"MinIO get failed: {e}")

        path = os.path.join(self.local_dir, key)
        with open(path, "rb") as f:
            return f.read()

    def delete(self, key: str) -> bool:
        """Delete an object by key."""
        if self.use_minio and self.client:
            try:
                self.client.remove_object(self.bucket, key)
                return True
            except S3Error as e:
                logger.error(f"MinIO delete failed: {e}")
                return False

        path = os.path.join(self.local_dir, key)
        if os.path.exists(path):
            os.remove(path)
            return True
        return False

    def exists(self, key: str) -> bool:
        """Check if an object exists."""
        if self.use_minio and self.client:
            try:
                self.client.stat_object(self.bucket, key)
                return True
            except S3Error:
                return False

        return os.path.exists(os.path.join(self.local_dir, key))

    def get_url(self, key: str, expires: int = 3600) -> str:
        """Get a presigned URL for an object (MinIO only)."""
        if self.use_minio and self.client:
            try:
                return self.client.presigned_get_object(self.bucket, key, expires)
            except Exception as e:
                logger.error(f"Failed to generate URL: {e}")
        return f"/api/vfs/download/{key}"