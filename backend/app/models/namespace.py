"""Namespace model — top-level isolation boundary for VFS assets."""
import uuid
from sqlalchemy import Column, String, Text, Boolean
from sqlalchemy import Uuid

from app.models.base import Base, TimestampMixin


class Namespace(Base, TimestampMixin):
    __tablename__ = "namespaces"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, unique=True)
    slug = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    owner_id = Column(String(255))
    is_active = Column(Boolean, default=True)
    settings = Column(Text)  # JSON-encoded settings

    def __repr__(self):
        return f"<Namespace {self.name}>"