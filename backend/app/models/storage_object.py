"""StorageObject model — physical object storage record (MinIO/local)."""
import uuid
from sqlalchemy import Column, String, BigInteger, Boolean
from sqlalchemy import Uuid

from app.models.base import Base, TimestampMixin


class StorageObject(Base, TimestampMixin):
    __tablename__ = "storage_objects"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    bucket = Column(String(255), nullable=False)
    object_key = Column(String(512), nullable=False, unique=True)
    size = Column(BigInteger, default=0)
    content_type = Column(String(255))
    sha256 = Column(String(64))
    storage_backend = Column(String(64), default="minio")  # minio, local, s3
    is_deleted = Column(Boolean, default=False)

    def __repr__(self):
        return f"<StorageObject {self.bucket}/{self.object_key}>"