"""Pydantic schemas for VFS API requests/responses."""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID


class NamespaceCreate(BaseModel):
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    owner_id: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None


class NamespaceResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    description: Optional[str]
    owner_id: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime


class DirectoryCreate(BaseModel):
    name: str
    parent_id: Optional[UUID] = None


class DirectoryResponse(BaseModel):
    id: UUID
    namespace_id: UUID
    parent_id: Optional[UUID]
    name: str
    path: str
    is_deleted: bool
    created_at: datetime
    updated_at: datetime


class FileUpload(BaseModel):
    namespace: str
    path: str
    metadata: Optional[Dict[str, Any]] = None


class FileResponse(BaseModel):
    id: UUID
    namespace_id: UUID
    directory_id: Optional[UUID]
    name: str
    path: str
    mime_type: Optional[str]
    size: int
    storage_key: str
    hash: Optional[str]
    is_deleted: bool
    created_at: datetime
    updated_at: datetime


class FileListResponse(BaseModel):
    files: List[FileResponse]
    total: int
    page: int
    page_size: int


class DirectoryListResponse(BaseModel):
    directories: List[DirectoryResponse]
    files: List[FileResponse]
    total: int


class AuditLogResponse(BaseModel):
    id: UUID
    namespace_id: Optional[UUID]
    actor_id: Optional[str]
    actor_type: Optional[str]
    action: str
    resource_type: Optional[str]
    resource_id: Optional[str]
    resource_path: Optional[str]
    ip_address: Optional[str]
    created_at: datetime