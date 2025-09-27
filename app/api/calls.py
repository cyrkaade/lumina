
from fastapi import APIRouter, UploadFile, File
from uuid import uuid4
from app.models.schemas import CallMetadata
from app.services.supabase_client import upload_audio, insert_call_metadata
from app.utils.background_tasks import process_call

router = APIRouter(prefix="/calls")

@router.post("/upload")
async def upload_call(worker_id: str, audio: UploadFile = File(...)):
    file_content = await audio.read()
    file_name = f"{uuid4()}_{audio.filename}"
    audio_url = upload_audio(file_name, file_content)
    call_id = str(uuid4())
    metadata = {"id": call_id, "worker_id": worker_id, "audio_url": audio_url}
    insert_call_metadata(metadata)
    process_call.delay(call_id, file_content)  
    return {"call_id": call_id, "status": "processing"}