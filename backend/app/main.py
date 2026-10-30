from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.vfs import router
from app.api.chat import router as chat_router
from app.api.auth import router as auth_router
from app.api.assets import router as assets_router
from app.api.knowledge import router as knowledge_router
from app.api.retrieval import router as retrieval_router
from app.api.context import router as context_router
from app.api.answers import router as answers_router
from app.api.memory import router as memory_router
from app.api.monitoring import router as monitoring_router
from app.api.workflows import router as workflows_router
from app.api.questions import router as questions_router

app = FastAPI(title="VFS AI Engine")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(router)
app.include_router(chat_router)
app.include_router(auth_router)
app.include_router(assets_router)
app.include_router(knowledge_router)
app.include_router(retrieval_router)
app.include_router(context_router)
app.include_router(answers_router)
app.include_router(memory_router)
app.include_router(monitoring_router)
app.include_router(workflows_router)
app.include_router(questions_router)

@app.get("/health")
def health():
    return {"status": "ok"}
