from fastapi import APIRouter
router = APIRouter(prefix="/api/billing", tags=["billing"])
@router.get("/")
def billing_status():
    return {"status": "ok"}
