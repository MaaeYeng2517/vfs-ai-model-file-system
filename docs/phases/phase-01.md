# Phase 1 — Repository Inspection and Architecture

## 1. Existing Project Analysis

Stack found:
- Monorepo (pnpm + turbo) of TypeScript packages: `packages/{types,utils,vfs-core,model-engine,dataset-engine,vector-engine,knowledge-engine}` and apps `apps/{api (Hono), cli}`.
- Python backend (FastAPI) under `backend/` with SQLAlchemy models for namespace/directory/file/storage_object/asset/knowledge/qa/audit_log, Alembic migration `001_phase1_infrastructure`, storage service (MinIO/local), settings via pydantic-settings.
- Frontend: Vite + React (`frontend/src/App.jsx`) SPA, not Next.js.
- Infra: docker-compose (postgres, minio, backend, frontend), Dockerfiles.
- Docs: phase plans 01-10, database/frontend/workflows design.

Gaps vs master prompt: no Next.js, no auth/RBAC/tenant, no Qdrant/Redis, no workers, no tests, frontend is single file, backend uses SQLite default and lacks most modules (questions, retrieval, context, answers, verification, memory, workflow, monitoring, governance). Frontend is Vite, not Next.js.

## 2. Architecture Proposal

Adopt master prompt architecture with incremental migration:
- Frontend: migrate Vite SPA to Next.js App Router + TS + Tailwind + shadcn-style components (phased).
- Backend: extend FastAPI into domain modules (auth, users, orgs, tenants, vfs, files, storage, metadata, models, datasets, knowledge, ingestion, questions, retrieval, context, runtime, answers, verification, memory, workflows, lineage, monitoring, governance).
- DB: PostgreSQL primary, Alembic migrations, UUID PKs, tenant isolation.
- Storage: MinIO/S3 via storage service; Qdrant for vectors; Redis for cache/queue.
- Workers: ARQ/Celery for ingestion/workflows.
- Observability: OpenTelemetry + structured logging.

## 3. Technology Stack

Frontend: Next.js 14+, React 18, TypeScript, Tailwind, Lucide, Recharts, TanStack Query, Zod.
Backend: Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2, Alembic, httpx.
DB: PostgreSQL 16, Redis 7, Qdrant, MinIO.
Infra: Docker Compose, GitHub Actions (later), OpenTelemetry.

## 4. Repository Structure

Target (master prompt):
```
/frontend (Next.js)
/backend (FastAPI domains, alembic, tests)
/infrastructure (docker, scripts, monitoring)
/docs
```
Keep existing `packages/*` and `apps/cli` as shared TS utilities/CLI during transition; deprecate Hono API in favor of FastAPI.

## 5. Database Domain Design

Domains: Identity (users, organizations, tenants, memberships, roles, permissions, role_permissions); VFS (files, directories, file_versions, file_metadata, storage_objects, storage_mounts, file_permissions); AI Models (models, model_versions, model_artifacts, model_runtime_configs); Datasets (datasets, dataset_versions, dataset_files, dataset_metadata); Knowledge (data_sources, documents, document_versions, document_chunks, knowledge_collections, knowledge_entities, knowledge_relations); Questions (conversations, questions, question_versions, question_relations); Retrieval/Context (retrieval_runs, retrieval_candidates, retrieval_selections, context_snapshots, context_items, embedding_registry, index_snapshots); Answers (ai_answers, answer_claims, answer_citations, answer_verifications, feedback); Memory (memories, memory_relations, memory_versions, memory_approvals); Workflow (workflows, workflow_versions, workflow_nodes, workflow_edges, workflow_executions, workflow_execution_logs); Governance (audit_logs, access_policies, retention_policies).

Principles: UUID PKs, FKs, unique constraints, indexes, check constraints, timestamps, soft delete where appropriate, tenant isolation, migrations, transactions.

## 6. Development Plan

Phases 2-14 per master prompt. Phase 2 next: Database Foundation (PostgreSQL schema + Alembic + base models). Do not start Phase 2 until this summary approved.

## 7. Risks and Dependencies

- Migration from Vite to Next.js and Hono to FastAPI may break existing CLI/API consumers; mitigate with compatibility layer.
- SQLite default in backend must be switched to PostgreSQL before production.
- Missing auth/tenant isolation is a security gap; prioritize in Phase 3.
- No tests currently; introduce pytest + frontend tests in each phase.
- Qdrant/Redis not yet wired; add in Phase 6/8.
- Existing TS packages may duplicate backend logic; decide single source of truth.
