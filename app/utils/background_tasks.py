
from celery import Celery
from app.config import config
from app.services.speech_to_text import transcribe_audio
from app.services.ai_analyzer import analyze_transcript
from app.services.score_calculator import calculate_score
from app.services.supabase_client import update_call_metadata

app = Celery("tasks", broker=config.CELERY_BROKER_URL, backend=config.CELERY_RESULT_BACKEND)

@app.task
def process_call(call_id: str, audio_content: bytes):
    transcript = transcribe_audio(audio_content)
    analysis = analyze_transcript(transcript)
    score = calculate_score(analysis)
    updates = {
        "transcript": transcript,
        "analysis": analysis.dict(),
        "score": score
    }
    update_call_metadata(call_id, updates)