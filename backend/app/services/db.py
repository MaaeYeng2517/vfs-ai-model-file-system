"""Database session management and initialization."""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.models import Base

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./vfs.db",
)

# Use NullPool for SQLite to avoid threading issues; for Postgres, use default pool
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, future=True, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL, future=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db():
    """Create all tables from models."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """FastAPI dependency that yields a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def dispose_engine():
    """Dispose the engine (used on shutdown)."""
    engine.dispose()