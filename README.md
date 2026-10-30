# VFS-AI-Engine

Unified system for managing AI files, models, datasets, vectors and knowledge in one place.

## Architecture

VFS-AI-Engine consists of 5 core engines:

| Engine | Purpose |
| --- | --- |
| **VFS Engine** | Virtual File System - manages files, directories, namespaces |
| **AI Model Engine** | Manages model artifacts (GGUF, Safetensors, PyTorch, ONNX) |
| **Dataset Engine** | Manages datasets with versioning (JSONL, CSV, Parquet) |
| **Vector Engine** | Manages embeddings and vector indexes for similarity search |
| **Knowledge Engine** | Manages documents, chunking, and knowledge graph for RAG |

## Quick Start

```bash
# Install dependencies
pnpm install

# Initialize
pnpm --filter @vfs-ai/cli dev init

# Create namespace
pnpm --filter @vfs-ai/cli dev ns:create myproject

# Write a file
pnpm --filter @vfs-ai/cli dev fs:write default hello.txt "Hello World"

# List files
pnpm --filter @vfs-ai/cli dev fs:ls default
```

## Project Structure

```
vfs-ai-engine/
├── apps/
│   ├── api/    # REST API (Hono)
│   ├── cli/    # CLI tool
│   └── web/    # Web UI (coming soon)
├── packages/
│   ├── types/           # Shared types
│   ├── utils/           # Utilities
│   ├── vfs-core/        # VFS Engine
│   ├── model-engine/    # Model Engine
│   ├── dataset-engine/  # Dataset Engine
│   ├── vector-engine/   # Vector Engine
│   └── knowledge-engine/# Knowledge Engine
└── data/                # Local storage
```

## CLI Commands

```bash
vfs init                    # Initialize engine
vfs ns:create <name>        # Create namespace
vfs ns:list                 # List namespaces
vfs fs:write <ns> <path> <content>
vfs fs:read <ns> <path>
vfs fs:ls [ns] [dir]
vfs model:register <ns> <path>
vfs model:list
vfs dataset:register <ns> <path>
vfs dataset:list
vfs vector:create <ns> <name>
vfs vector:list
vfs knowledge:ingest <ns> <path>
vfs knowledge:list
```

## API

Start API server:
```bash
pnpm --filter @vfs-ai/api dev
```

Endpoints available at `http://localhost:3000`
# vfs-ai-model-file-system

## System Summary

VFS AI Knowledge System integrates:
- VFS Core: namespaces, inodes, files, versions, storage
- Storage Engine: local/MinIO, blocks, manifests, dedup, integrity
- AI Knowledge: parsing, chunking, embedding, vector search, RAG
- Enterprise: RBAC, audit, retention, legal hold
- Frontend: Next.js dashboard, file explorer, admin pages
- Chatbot: connected to VFS search

## Workflow

Upload -> VFS -> Storage -> Blocks/Manifest -> Metadata/Version -> AI Ingestion -> RAG Answer
