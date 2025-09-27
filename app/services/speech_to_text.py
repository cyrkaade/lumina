import openai
from pydub import AudioSegment
import io
import tempfile
import os

class SpeechToTextService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY

    def transcribe_audio(self, audio_file_path: str) -> dict:
        """
        whisper api
        returns: {
            'transcript': str,
            'language': str,
            'duration': float
        }
        """
        try:

            audio_path = self._prepare_audio_file(audio_file_path)
            
            with open(audio_path, 'rb') as audio_file:
                transcript = openai.Audio.transcribe(
                    model="whisper-1",
                    file=audio_file,
                    language="ru",  
                    response_format="verbose_json",
                    temperature=0
                )
            
            return {
                'transcript': transcript['text'],
                'language': transcript.get('language', 'ru'),
                'duration': transcript.get('duration', 0),
                'segments': transcript.get('segments', [])
            }
            
        except Exception as e:
            raise Exception(f"Speech-to-text conversion failed: {str(e)}")
    
    def _prepare_audio_file(self, file_path: str) -> str:

        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension in ['.wav', '.mp3', '.m4a', '.flac']:
            return file_path
        

        audio = AudioSegment.from_file(file_path)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        audio.export(temp_file.name, format="wav")
        return temp_file.name