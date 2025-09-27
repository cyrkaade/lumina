import openai
from pydub import AudioSegment
import io
import tempfile
import os

class SpeechToTextService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY