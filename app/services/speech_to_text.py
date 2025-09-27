
import openai
from app.config import config
import tempfile
import os

openai.api_key = config.OPENAI_API_KEY

def transcribe_audio(audio_content: bytes) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        temp_file.write(audio_content)
        temp_file_path = temp_file.name

    try:    
        with open(temp_file_path, "rb") as audio_file:
            response = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file,
                language="ru"  
            )
        return response["text"]
    finally:
        os.unlink(temp_file_path)