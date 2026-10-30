"""Asset model — unified asset record for files, directories, models, datasets, etc."""
import uuid
from sqlalchemy import Column, String, Text, ForeignKey, Boolean, BigInteger
from sqlalchemy import Uuid

from app.models.base import Base, TimestampMixin


class Asset(Base, TimestampMixin):
    __tablename__ = "assets"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    namespace_id = Column(Uuid, ForeignKey("namespaces.id"), nullable=False)
    parent_id = Column(Uuid, ForeignKey("assets.id"))  # parent directory
    asset_type = Column(String(64), nullable=False)  # file, directory, model, dataset, document
    name = Column(String(255), nullable=False)
    path = Column(String(4096), nullable=False)
    mime_type = Column(String(255))
    size = Column(BigInteger, default=0)
    storage_key = Column(String(512))
    hash = Column(String(64))
    is_deleted = Column(Boolean, default=False)
    meta = Column("metadata", Text)  # JSON-encoded metadata

    def __repr__(self):
        return f"<Asset {self.asset_type} {self.path}>"