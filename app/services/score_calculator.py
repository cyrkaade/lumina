
from app.models.schemas import CallAnalysis

def calculate_score(analysis: CallAnalysis) -> int:
 
    emotion_score = (analysis.emotions.get("positive", 0) - analysis.emotions.get("angry", 0) - analysis.emotions.get("frustrated", 0)) * 40
    phrases_score = min(len(analysis.key_phrases) / 5, 1) * 30 
    resolution_score = 30 if analysis.issue_resolved else 0
    total = int(emotion_score + phrases_score + resolution_score)
    return max(0, min(100, total)) 