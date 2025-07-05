from fastapi import APIRouter
from services.db_service import get_all_pools, get_top_pools

router = APIRouter()

@router.get("/api/all-pools")
def all_pools():
    return get_all_pools()

@router.get("/api/pools")
async def get_pools():
    return get_top_pools()
