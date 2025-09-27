
import openai
from app.config import config
from app.models.schemas import CallAnalysis

openai.api_key = config.OPENAI_API_KEY

def analyze_transcript(transcript: str) -> CallAnalysis:
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini", 
        messages=[
            {"role": "system", "content": "You are an AI analyzer for call center performance. Analyze the Russian transcript for: 1) Customer emotions (dict with scores 0-1 for positive, neutral, angry, frustrated). 2) Key phrases indicating issue resolution (list). 3) Whether the issue was solved (bool). Output as JSON."},
            {"role": "user", "content": transcript}
        ],
        response_format={"type": "json_object"} 
    )
    
    # Parse JSON
    import json
    parsed = json.loads(response.choices[0].message.content)
    return CallAnalysis(
        transcript=transcript,
        emotions=parsed["emotions"],
        key_phrases=parsed["key_phrases"],
        issue_resolved=parsed["issue_resolved"],
        score=0  
    )