# VFS AI Knowledge System

Unified platform for managing files, storage, metadata, versions, and AI knowledge.

## Architecture

- VFS Core: namespaces, inodes, files, directories
- Storage Engine: local/MinIO, blocks, manifests, dedup, integrity
- Metadata & Versioning: metadata, lifecycle, RBAC, audit, retention
- AI Knowledge: parsing, chunking, embedding, vector search, RAG
- Frontend: Next.js + Tailwind
- Backend: FastAPI + PostgreSQL

## Workflow

Upload -> VFS -> Storage -> Blocks/Manifest -> Metadata/Version -> AI Ingestion -> RAG Answer

## Features

- File CRUD, upload/download, versioning
- Tag, keyword, metadata management
- Block storage with SHA-256 integrity
- Chatbot connected to VFS search
- Enterprise governance: RBAC, audit, retention



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

## Quick Start

```bash
docker compose up -d
cd backend && DEBUG=false python -m uvicorn app.main:app --reload
cd frontend && npm run dev
```

## API

- /api/vfs/* : file operations
- /api/chat : chatbot
- /health : status

## Testing

Frontend: npm run build
Backend: python -m uvicorn app.main:app


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
