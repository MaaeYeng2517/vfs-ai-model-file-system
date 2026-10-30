# VFS AI Knowledge System

Unified platform for managing files, storage, metadata, versions, and AI knowledge.

## Architecture

- VFS Core: namespaces, inodes, files, directories
- Storage Engine: local/MinIO, blocks, manifests, dedup, integrity
- Metadata & Versioning: metadata, lifecycle, RBAC, audit, retention
- AI Knowledge: parsing, chunking, embedding, vector search, RAG
- Frontend: Next.js + Tailwind
- Backend: FastAPI + PostgreSQL

## 
## 


## Architecture Diagram

```mermaid
flowchart LR
  U[User] --> FE[Next.js Frontend]
  FE --> API[FastAPI Backend]
  API --> VFS[VFS Core]
  VFS --> DB[(PostgreSQL)]
  VFS --> ST[Storage: Local/MinIO]
  ST --> BL[Blocks/Manifests]
  API --> AI[AI Knowledge Engine]
  AI --> VS[(Vector Store)]
  AI --> LLM[LLM/Embedding]
```




## Workflow Diagram

```mermaid
flowchart TD
  A[Upload File] --> B[VFS Core]
  B --> C[Storage Engine]
  C --> D[Blocks & Manifest]
  B --> E[Metadata & Version]
  E --> F[Audit Log]
  B --> G[AI Ingestion]
  G --> H[Chunking]
  H --> I[Embedding]
  I --> J[Vector Store]
  J --> K[RAG Answer]
```


## Components & Features

```mermaid
graph TB
  subgraph VFS["VFS Core"]
    NS[Namespace]
    IN[Inode]
    FL[File]
    VR[Version]
  end
  subgraph Storage
    OB[Object]
    BK[Block]
    MN[Manifest]
  end
  subgraph AI["AI Knowledge"]
    PR[Parser]
    CK[Chunker]
    EM[Embedding]
    VS[Vector Search]
    RAG[RAG]
  end
  subgraph Ent["Enterprise"]
    RBAC[RBAC]
    AUD[Audit]
    RET[Retention]
  end
  VFS --> Storage
  VFS --> AI
  VFS --> Ent
```


## Class Diagram

```mermaid
classDiagram
  class Tenant
  class Namespace
  class Inode
  class File
  class FileVersion
  class StorageObject
  class Block
  class Manifest
  Tenant --> Namespace
  Namespace --> Inode
  Inode --> File
  File --> FileVersion
  FileVersion --> Manifest
  Manifest --> Block
  File --> StorageObject
```


## Database Diagram

```mermaid
erDiagram
  TENANT ||--o{ NAMESPACE : has
  NAMESPACE ||--o{ INODE : contains
  INODE ||--|| FILE : maps
  FILE ||--o{ FILE_VERSION : versions
  FILE_VERSION ||--|| MANIFEST : has
  MANIFEST ||--o{ MANIFEST_BLOCK : contains
  MANIFEST_BLOCK }o--|| BLOCK : references
  FILE ||--o{ STORAGE_OBJECT : stores
```

## AI Agent

- Provider Manager with quota/rate limit/budget
- Providers: OpenAI, Anthropic, Gemini
- DB usage tracking
