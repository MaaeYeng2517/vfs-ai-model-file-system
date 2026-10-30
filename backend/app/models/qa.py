import uuid
from sqlalchemy import Column, String, Text, Integer, Float, ForeignKey, Boolean
from sqlalchemy import Uuid
from app.models.base import Base, TimestampMixin

class Conversation(Base, TimestampMixin):
    __tablename__="conversations"
    id=Column(Uuid,primary_key=True,default=uuid.uuid4)
    user_id=Column(String(255))

class Question(Base, TimestampMixin):
    __tablename__="questions"
    id=Column(Uuid,primary_key=True,default=uuid.uuid4)
    conversation_id=Column(Uuid,ForeignKey("conversations.id"))
    original_text=Column(Text,nullable=False)
    language=Column(String(10),default="th")

class QuestionVersion(Base, TimestampMixin):
    __tablename__="question_versions"
    id=Column(Uuid,primary_key=True,default=uuid.uuid4)
    question_id=Column(Uuid,ForeignKey("questions.id"),nullable=False)
    normalized_text=Column(Text)
    intent=Column(String(128))
    status=Column(String(32),default="processed")

class Document(Base, TimestampMixin):
    __tablename__="documents"
    id=Column(Uuid,primary_key=True,default=uuid.uuid4)
    title=Column(Text,nullable=False)
    source_type=Column(String(50))

class DocumentVersion(Base, TimestampMixin):
    __tablename__="document_versions"
    id=Column(Uuid,primary_key=True,default=uuid.uuid4)
    document_id=Column(Uuid,ForeignKey("documents.id"),nullable=False)
    version=Column(String(50))
    storage_key=Column(Text,nullable=False)
    checksum_sha256=Column(String(64))

class DocumentChunk(Base, TimestampMixin):
    __tablename__="document_chunks"
    id=Column(Uuid,primary_key=True,default=uuid.uuid4)
    document_version_id=Column(Uuid,ForeignKey("document_versions.id"),nullable=False)
    content=Column(Text,nullable=False)
    page_number=Column(Integer)
    section_name=Column(Text)
    start_offset=Column(Integer)
    end_offset=Column(Integer)

class RetrievalRun(Base, TimestampMixin):
    __tablename__="retrieval_runs"
    id=Column(Uuid,primary_key=True,default=uuid.uuid4)
    question_id=Column(Uuid,ForeignKey("questions.id"),nullable=False)
    search_method=Column(String(50))
    query=Column(Text)
    top_k=Column(Integer)
    status=Column(String(32),default="completed")

class RetrievalCandidate(Base):
    __tablename__="retrieval_candidates"
    retrieval_id=Column(Uuid,ForeignKey("retrieval_runs.id"),primary_key=True)
    chunk_id=Column(Uuid,ForeignKey("document_chunks.id"),primary_key=True)
    rank=Column(Integer)
    score=Column(Float)
    selected=Column(Boolean,default=False)

class AIAnswer(Base, TimestampMixin):
    __tablename__="ai_answers"
    id=Column(Uuid,primary_key=True,default=uuid.uuid4)
    question_id=Column(Uuid,ForeignKey("questions.id"),nullable=False)
    retrieval_id=Column(Uuid,ForeignKey("retrieval_runs.id"))
    answer_text=Column(Text,nullable=False)
    model_name=Column(String(150))
    model_version=Column(String(100))
    verification_status=Column(String(30))

class AnswerCitation(Base, TimestampMixin):
    __tablename__="answer_citations"
    id=Column(Uuid,primary_key=True,default=uuid.uuid4)
    answer_id=Column(Uuid,ForeignKey("ai_answers.id"),nullable=False)
    chunk_id=Column(Uuid,ForeignKey("document_chunks.id"),nullable=False)
    claim_text=Column(Text)

class ContextSnapshot(Base, TimestampMixin):
    __tablename__="context_snapshots"
    id=Column(Uuid,primary_key=True,default=uuid.uuid4)
    question_id=Column(Uuid,ForeignKey("questions.id"),nullable=False)
    retrieval_id=Column(Uuid,ForeignKey("retrieval_runs.id"))
    token_budget=Column(Integer)
    actual_token_count=Column(Integer)
    context_hash=Column(String(64))

class Memory(Base, TimestampMixin):
    __tablename__="memories"
    id=Column(Uuid,primary_key=True,default=uuid.uuid4)
    memory_type=Column(String(64),nullable=False)
    content=Column(Text,nullable=False)
    tenant_id=Column(String(255))
    confidence=Column(Float,default=1.0)
