"""Block storage models for VFS Block Engine."""
import uuid
from sqlalchemy import Column, String, BigInteger, ForeignKey, Integer, UniqueConstraint
from sqlalchemy import Uuid
from app.models.base import Base, TimestampMixin


class Block(Base, TimestampMixin):
    __tablename__ = "blocks"
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    checksum_sha256 = Column(String(64), nullable=False, unique=True)
    size_bytes = Column(BigInteger, nullable=False)
    storage_key = Column(String(512), nullable=False)


class Manifest(Base, TimestampMixin):
    __tablename__ = "manifests"
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    file_version_id = Column(Uuid, ForeignKey("file_versions.id"), nullable=False)
    format_version = Column(String(20), nullable=False)
    block_size = Column(BigInteger)
    total_blocks = Column(Integer, default=0, nullable=False)


class FileBlock(Base):
    __tablename__ = "file_blocks"
    manifest_id = Column(Uuid, ForeignKey("manifests.id"), nullable=False, primary_key=True)
    block_id = Column(Uuid, ForeignKey("blocks.id"), nullable=False)
    sequence_number = Column(Integer, nullable=False, primary_key=True)
