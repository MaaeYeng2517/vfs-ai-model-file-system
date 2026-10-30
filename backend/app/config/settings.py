"""Application configuration — loads from environment variables with sensible defaults."""
import os
from typing import Optional, List
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment / .env file."""

    # General
    app_name: str = "VFS AI Engine"
    app_version: str = "0.1.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000

    # Database
    database_url: str = "sqlite:///./vfs.db"

    # Storage
    storage_backend: str = "minio"  # minio, local, s3
    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_bucket: str = "vfs"
    minio_secure: bool = False
    local_storage_path: str = "./storage"

    # AI / LLM (Phase 7)
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o"
    openai_base_url: Optional[str] = None

    anthropic_api_key: Optional[str] = None
    anthropic_model: str = "claude-3-5-sonnet-20241022"

    # Embedding
    embedding_model: str = "text-embedding-3-small"
    embedding_provider: str = "openai"

    # Vector DB (Phase 5)
    vector_db_provider: str = "pgvector"  # pgvector, qdrant, chroma
    qdrant_url: Optional[str] = None
    qdrant_api_key: Optional[str] = None

    # Security (Phase 10)
    secret_key: str = "dev-secret-change-me"
    jwt_algorithm: str = "HS256"
    jwt_expires_minutes: int = 60
    allowed_origins: List[str] = ["*"]

    # Rate limiting
    rate_limit_enabled: bool = True
    rate_limit_per_minute: int = 100

    # Monitoring
    sentry_dsn: Optional[str] = None
    log_level: str = "INFO"

    # Backup
    backup_enabled: bool = False
    backup_interval_hours: int = 24

    model_config = {
        "env_prefix": "",
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore",
    }


settings = Settings()