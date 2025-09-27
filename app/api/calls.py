from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from app.services.supabase_client import supabase_service
from app.services.score_calculator import ScoreCalculator
from app.utils.background_tasks import process_call_recording
from app.config import settings
import uuid
import os
import asyncio

router = APIRouter()

@router.post("/upload-call")
async def upload_call_recording(
    background_tasks: BackgroundTasks,
    worker_id: str,
    customer_phone: str = None,
    audio_file: UploadFile = File(...)
):
    """
    Upload call recording for analysis
    """
    try:

        if audio_file.size > settings.MAX_AUDIO_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large")
        
        file_extension = os.path.splitext(audio_file.filename)[1].lower()
        if file_extension not in settings.SUPPORTED_AUDIO_FORMATS:
            raise HTTPException(status_code=400, detail="Unsupported audio format")

        call_id = str(uuid.uuid4())
        file_path = f"calls/{call_id}/{audio_file.filename}"

        file_content = await audio_file.read()

        file_url = await supabase_service.upload_audio_file(file_content, file_path)

        call_data = {
            "call_id": call_id,
            "worker_id": worker_id,
            "customer_phone": customer_phone,
            "audio_file_path": file_path,
            "audio_file_url": file_url,
            "processing_status": "pending"
        }
        
        call_record = await supabase_service.create_call_record(call_data)

        background_tasks.add_task(process_call_recording, call_id)
        
        return {
            "call_id": call_id,
            "status": "uploaded",
            "processing_status": "pending",
            "message": "Call uploaded successfully and queued for processing"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/call-score/{call_id}")
async def get_call_score(call_id: str):
    """
    Get performance score for a specific call
    """
    try:

        call = await supabase_service.get_call_by_id(call_id)
        if not call:
            raise HTTPException(status_code=404, detail="Call not found")

        if call['processing_status'] == 'pending':
            return {
                "status": "pending", 
                "message": "Call is queued for processing"
            }
        elif call['processing_status'] == 'processing':
            return {
                "status": "processing", 
                "message": "Call is currently being processed"
            }
        elif call['processing_status'] == 'failed':
            return {
                "status": "failed", 
                "message": "Call processing failed"
            }

        performance = await supabase_service.get_performance_score(call_id)
        if not performance:
            raise HTTPException(status_code=404, detail="Performance data not found")
        
        return {
            "call_id": call_id,
            "status": "completed",
            "overall_score": performance['overall_score'],
            "performance_level": ScoreCalculator.get_performance_level(performance['overall_score']),
            "detailed_scores": {
                "customer_satisfaction": performance['customer_satisfaction_score'],
                "problem_resolution": performance['problem_resolution_score'],
                "communication": performance['communication_score'],
                "professionalism": performance['professionalism_score']
            },
            "analysis": {
                "customer_emotional_state": performance['customer_emotional_state'],
                "issue_resolved": performance['issue_resolved'],
                "key_issues": performance['key_issues'],
                "positive_aspects": performance['positive_aspects'],
                "improvement_areas": performance['improvement_areas'],
                "detailed_analysis": performance['detailed_analysis']
            },
            "call_info": {
                "worker_id": call['worker_id'],
                "call_date": call['call_date'],
                "call_duration": call['call_duration'],
                "customer_phone": call['customer_phone']
            },
            "transcript": performance['transcript_full']
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/worker-analytics/{worker_id}")
async def get_worker_analytics(worker_id: str, limit: int = 50):
    """
    Get analytics for a specific worker
    """
    try:
        scores = await supabase_service.get_worker_analytics(worker_id, limit)
        
        if not scores:
            raise HTTPException(status_code=404, detail="No data found for this worker")

        total_calls = len(scores)
        overall_scores = [s['overall_score'] for s in scores]
        average_score = sum(overall_scores) / total_calls

        recent_scores = overall_scores[:10]

        score_distribution = {
            "excellent": len([s for s in overall_scores if s >= 90]),
            "good": len([s for s in overall_scores if 75 <= s < 90]),
            "satisfactory": len([s for s in overall_scores if 60 <= s < 75]),
            "needs_improvement": len([s for s in overall_scores if s < 60])
        }

        criteria_averages = {
            "customer_satisfaction": round(sum(s['customer_satisfaction_score'] for s in scores) / total_calls, 2),
            "problem_resolution": round(sum(s['problem_resolution_score'] for s in scores) / total_calls, 2),
            "communication": round(sum(s['communication_score'] for s in scores) / total_calls, 2),
            "professionalism": round(sum(s['professionalism_score'] for s in scores) / total_calls, 2)
        }

        all_improvement_areas = []
        for score in scores:
            all_improvement_areas.extend(score.get('improvement_areas', []))
        
        from collections import Counter
        common_improvements = dict(Counter(all_improvement_areas).most_common(5))
        
        return {
            "worker_id": worker_id,
            "total_calls_analyzed": total_calls,
            "average_score": round(average_score, 2),
            "performance_level": ScoreCalculator.get_performance_level(int(average_score)),
            "recent_performance_trend": recent_scores,
            "score_distribution": score_distribution,
            "criteria_averages": criteria_averages,
            "common_improvement_areas": common_improvements,
            "latest_analysis_date": scores[0]['analysis_timestamp'] if scores else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/call-status/{call_id}")
async def get_call_status(call_id: str):
    """
    Get current processing status of a call
    """
    try:
        call = await supabase_service.get_call_by_id(call_id)
        if not call: