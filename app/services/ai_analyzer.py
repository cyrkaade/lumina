import openai
import json
from typing import Dict, List

class AIAnalyzer:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY