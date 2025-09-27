import openai
from pydub import AudioSegment
import io
import tempfile
import os
from app.config import settings

class SpeechToTextService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
    
    async def transcribe_audio(self, audio_content: bytes, file_extension: str) -> dict:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
                temp_file.write(audio_content)
                temp_file_path = temp_file.name

            prepared_audio_path = await self._prepare_audio_file(temp_file_path)

            with open(prepared_audio_path, 'rb') as audio_file:
                transcript = openai.Audio.transcribe(
                    model="whisper-1",
                    file=audio_file,
                    language="ru",
                    response_format="verbose_json",
                    temperature=0
                )

            os.unlink(temp_file_path)
            if prepared_audio_path != temp_file_path:
                os.unlink(prepared_audio_path)
            
            return {
                'transcript': transcript['text'],
                'language': transcript.get('language', 'ru'),
                'duration': transcript.get('duration', 0),
                'segments': transcript.get('segments', [])
            }
            
        except Exception as e:
            raise Exception(f"Speech-to-text conversion failed: {str(e)}")
    
    async def _prepare_audio_file(self, file_path: str) -> str:
        """Convert audio file to format supported by Whisper API"""
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension in ['.wav', '.mp3', '.m4a', '.flac']:
            return file_path
        

        audio = AudioSegment.from_file(file_path)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        audio.export(temp_file.name, format="wav")
        return temp_file.name