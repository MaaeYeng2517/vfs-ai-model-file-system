"""AuditLog model — immutable record of user/system actions."""
import uuid
from sqlalchemy import Column, String, Text, DateTime, func, ForeignKey
from sqlalchemy import Uuid

from app.models.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    namespace_id = Column(Uuid, ForeignKey("namespaces.id"))
    actor_id = Column(String(255))  # user / system id
    actor_type = Column(String(64))  # user, system, service
    action = Column(String(128), nullable=False)  # create, read, update, delete
    resource_type = Column(String(64))  # file, directory, namespace, model
    resource_id = Column(String(512))
    resource_path = Column(String(4096))
    ip_address = Column(String(64))
    user_agent = Column(Text)
    meta = Column("metadata", Text)  # JSON-encoded
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<AuditLog {self.action} {self.resource_type}>"