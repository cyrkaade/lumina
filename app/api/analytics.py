
from fastapi import APIRouter
from app.services.supabase_client import get_call_metadata

router = APIRouter(prefix="/analytics")

@router.get("/call/{call_id}")
async def get_call_analytics(call_id: str):
    metadata = get_call_metadata(call_id)
    return metadata