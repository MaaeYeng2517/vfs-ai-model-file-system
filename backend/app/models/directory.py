"""Directory model — logical grouping of files within a namespace."""
import uuid
from sqlalchemy import Column, String, Text, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy import Uuid

from app.models.base import Base, TimestampMixin


class Directory(Base, TimestampMixin):
    __tablename__ = "directories"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    namespace_id = Column(Uuid, ForeignKey("namespaces.id"), nullable=False)
    parent_id = Column(Uuid, ForeignKey("directories.id"))
    name = Column(String(255), nullable=False)
    path = Column(String(4096), nullable=False)
    is_deleted = Column(Boolean, default=False)

    __table_args__ = (
        UniqueConstraint("namespace_id", "path", name="uq_dir_ns_path"),
    )

    def __repr__(self):
        return f"<Directory {self.path}>"