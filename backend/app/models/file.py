"""File model — metadata record for a VFS file asset."""
import uuid
from sqlalchemy import Column, String, Text, BigInteger, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy import Uuid

from app.models.base import Base, TimestampMixin


class File(Base, TimestampMixin):
    __tablename__ = "files"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    namespace_id = Column(Uuid, ForeignKey("namespaces.id"), nullable=False)
    directory_id = Column(Uuid, ForeignKey("directories.id"))
    name = Column(String(255), nullable=False)
    path = Column(String(4096), nullable=False)
    mime_type = Column(String(255))
    size = Column(BigInteger, default=0)
    storage_key = Column(String(512), nullable=False)
    hash = Column(String(64))  # SHA-256 content hash
    is_deleted = Column(Boolean, default=False)
    meta = Column("metadata", Text)  # JSON-encoded metadata

    __table_args__ = (
        UniqueConstraint("namespace_id", "path", name="uq_file_ns_path"),
    )

    def __repr__(self):
        return f"<File {self.path}>"