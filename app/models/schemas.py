
from pydantic import BaseModel
from typing import Optional

class CallUpload(BaseModel):
    worker_id: str
    audio_file: bytes 

class CallAnalysis(BaseModel):
    transcript: str
    emotions: dict 
    key_phrases: list[str]
    issue_resolved: bool
    score: int 

class CallMetadata(BaseModel):
    id: str
    worker_id: str
    audio_url: str
    transcript: Optional[str]
    analysis: Optional[CallAnalysis]
    score: Optional[int]