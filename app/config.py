import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_KEY: str 
    SUPABASE_ANON_KEY: str 

    OPENAI_API_KEY: str
    

    MAX_AUDIO_FILE_SIZE: int = 100 * 1024 * 1024
    SUPPORTED_AUDIO_FORMATS: list = [".wav", ".mp3", ".m4a", ".flac", ".ogg"]

    STORAGE_BUCKET_NAME: str = "call-recordings"
    
    class Config:
        env_file = ".env"

settings = Settings()