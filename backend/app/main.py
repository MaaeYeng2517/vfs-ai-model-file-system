from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.vfs import router
from app.api.assets import router as assets_router
from app.api.knowledge import router as knowledge_router
from app.api.retrieval import router as retrieval_router
from app.api.context import router as context_router
from app.api.answers import router as answers_router
from app.api.memory import router as memory_router

app = FastAPI(title="VFS AI Engine")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(router)
app.include_router(assets_router)
app.include_router(knowledge_router)
app.include_router(retrieval_router)
app.include_router(context_router)
app.include_router(answers_router)
app.include_router(memory_router)

@app.get("/health")
def health():
    return {"status": "ok"}
