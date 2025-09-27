import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost/callcenter_db"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # AI Services
    OPENAI_API_KEY: str
    
    # File storage
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_S3_BUCKET: str
    AWS_REGION: str = "us-east-1"
    
    # Application settings
    MAX_AUDIO_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB
    SUPPORTED_AUDIO_FORMATS: list = [".wav", ".mp3", ".m4a", ".flac"]
    
    class Config:
        env_file = ".env"

settings = Settings()