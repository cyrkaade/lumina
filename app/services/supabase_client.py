
from supabase import create_client, Client
from app.config import config

supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

def upload_audio(file_name: str, file_content: bytes) -> str:

    response = supabase.storage.from_("call_audios").upload(file_name, file_content)
    return f"{config.SUPABASE_URL}/storage/v1/object/public/call_audios/{file_name}"

def insert_call_metadata(metadata: dict):
    supabase.table("calls").insert(metadata).execute()

def update_call_metadata(call_id: str, updates: dict):
    supabase.table("calls").update(updates).eq("id", call_id).execute()

def get_call_metadata(call_id: str) -> dict:
    return supabase.table("calls").select("*").eq("id", call_id).execute().data[0]