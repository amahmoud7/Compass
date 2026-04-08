from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("/api/v1/health")
async def health():
    return {"status": "ok"}

@router.get("/api/v1/ready")
async def ready():
    return {"status": "ready"}
