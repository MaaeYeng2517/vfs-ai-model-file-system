from sqlalchemy import Column, Integer, String, BigInteger, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class FileRecord(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    path = Column(String, nullable=False, unique=True)
    mime_type = Column(String)
    size = Column(BigInteger, default=0)
    storage_key = Column(String)
    namespace = Column(String)
    created_at = Column(DateTime, server_default=func.now())
