from supabase import create_client, Client
from app.config import settings
import logging

class SupabaseService:
    def __init__(self):
        self.supabase: Client = create_client(
            settings.SUPABASE_URL, 
            settings.SUPABASE_KEY
        )
    
    async def upload_audio_file(self, file_content: bytes, file_path: str) -> str:
        """Upload audio file to Supabase Storage"""
        try:
            result = self.supabase.storage.from_(settings.STORAGE_BUCKET_NAME).upload(
                file_path, file_content
            )
            
            if result.status_code == 200:

                url_response = self.supabase.storage.from_(settings.STORAGE_BUCKET_NAME).get_public_url(file_path)
                return url_response
            else:
                raise Exception(f"Upload failed: {result}")
                
        except Exception as e:
            logging.error(f"File upload error: {str(e)}")
            raise
    
    async def download_audio_file(self, file_path: str) -> bytes:
        """Download audio file from Supabase Storage"""
        try:
            result = self.supabase.storage.from_(settings.STORAGE_BUCKET_NAME).download(file_path)
            return result
        except Exception as e:
            logging.error(f"File download error: {str(e)}")
            raise
    
    async def create_call_record(self, call_data: dict) -> dict:
        """Create a new call record"""
        try:
            result = self.supabase.table("calls").insert(call_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logging.error(f"Database insert error: {str(e)}")
            raise
    
    async def update_call_status(self, call_id: str, status: str, processed: bool = None) -> bool:
        """Update call processing status"""
        try:
            update_data = {"processing_status": status}
            if processed is not None:
                update_data["processed"] = processed
            
            result = self.supabase.table("calls").update(update_data).eq("call_id", call_id).execute()
            return len(result.data) > 0
        except Exception as e:
            logging.error(f"Status update error: {str(e)}")
            return False
    
    async def save_performance_score(self, score_data: dict) -> dict:
        """Save performance analysis results"""
        try:
            result = self.supabase.table("performance_scores").insert(score_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logging.error(f"Score save error: {str(e)}")
            raise
    
    async def get_call_by_id(self, call_id: str) -> dict:
        """Get call record by ID"""
        try:
            result = self.supabase.table("calls").select("*").eq("call_id", call_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logging.error(f"Call fetch error: {str(e)}")
            return None
    
    async def get_performance_score(self, call_id: str) -> dict:
        """Get performance score by call ID"""
        try:
            result = self.supabase.table("performance_scores").select("*").eq("call_id", call_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logging.error(f"Score fetch error: {str(e)}")
            return None
    
    async def get_worker_analytics(self, worker_id: str, limit: int = 100) -> list:
        """Get worker performance analytics"""
        try:
            result = self.supabase.table("performance_scores").select("*").eq("worker_id", worker_id).order("analysis_timestamp", desc=True).limit(limit).execute()
            return result.data
        except Exception as e:
            logging.error(f"Analytics fetch error: {str(e)}")
            return []
    
    async def update_worker_average(self, worker_id: str) -> bool:
        """Update worker's average score"""
        try:

            scores_result = self.supabase.table("performance_scores").select("overall_score").eq("worker_id", worker_id).execute()
            
            if scores_result.data:
                scores = [score['overall_score'] for score in scores_result.data]
                average_score = sum(scores) / len(scores)

                update_result = self.supabase.table("workers").update({
                    "average_score": round(average_score, 2),
                    "total_calls_processed": len(scores)
                }).eq("worker_id", worker_id).execute()
                
                return len(update_result.data) > 0
            return False
        except Exception as e:
            logging.error(f"Worker update error: {str(e)}")
            return False

supabase_service = SupabaseService()