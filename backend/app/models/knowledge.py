import uuid, json
from sqlalchemy import Column, String, Text, Integer, ForeignKey, Float
from sqlalchemy import Uuid
from app.models.base import Base, TimestampMixin

class KnowledgeDocument(Base, TimestampMixin):
    __tablename__ = "knowledge_documents"
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    namespace_id = Column(Uuid, ForeignKey("namespaces.id"), nullable=False)
    title = Column(String(512), nullable=False)
    source_path = Column(String(4096))
    content = Column(Text)
    status = Column(String(64), default="ingested")
    meta = Column("metadata", Text)

class KnowledgeChunk(Base, TimestampMixin):
    __tablename__ = "knowledge_chunks"
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    document_id = Column(Uuid, ForeignKey("knowledge_documents.id"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    token_count = Column(Integer, default=0)
    embedding = Column("embedding", Text)
