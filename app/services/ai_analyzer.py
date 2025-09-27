
import requests
from app.config import config
from app.models.schemas import CallAnalysis

def analyze_transcript(transcript: str) -> CallAnalysis:
    url = "https://api.x.ai/v1/chat/completions"  
    headers = {
        "Authorization": f"Bearer {config.GROK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "grok-4",
        "messages": [
            {"role": "system", "content": "You are an AI analyzer for call center performance. Analyze the Russian transcript for: 1) Customer emotions (dict with scores 0-1 for positive, neutral, angry, frustrated). 2) Key phrases indicating issue resolution (list). 3) Whether the issue was solved (bool). Output as JSON."},
            {"role": "user", "content": transcript}
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    analysis_json = response.json()["choices"][0]["message"]["content"]

    import json
    parsed = json.loads(analysis_json)
    return CallAnalysis(
        transcript=transcript,
        emotions=parsed["emotions"],
        key_phrases=parsed["key_phrases"],
        issue_resolved=parsed["issue_resolved"],
        score=0  
    )