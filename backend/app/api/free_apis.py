from fastapi import APIRouter
router = APIRouter(prefix="/api/free", tags=["free"])

@router.get("/")
def list_free():
    return {"apis": ["chat", "search", "files"]}
