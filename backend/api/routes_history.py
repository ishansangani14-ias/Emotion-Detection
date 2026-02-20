"""
History API routes
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from backend.database import get_db, Detection
from backend.schemas import DetectionResponse

router = APIRouter()


@router.get("/history", response_model=List[DetectionResponse])
async def get_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    emotion: Optional[str] = None,
    mode: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get detection history with filters
    
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    - **emotion**: Filter by emotion (optional)
    - **mode**: Filter by mode (face, text, multimodal) (optional)
    - **start_date**: Filter by start date (YYYY-MM-DD) (optional)
    - **end_date**: Filter by end date (YYYY-MM-DD) (optional)
    - Returns list of detection records
    """
    query = db.query(Detection)
    
    # Apply filters
    if emotion:
        query = query.filter(Detection.emotion == emotion)
    
    if mode:
        query = query.filter(Detection.mode == mode)
    
    if start_date:
        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            query = query.filter(Detection.timestamp >= start_dt)
        except ValueError:
            pass
    
    if end_date:
        try:
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            query = query.filter(Detection.timestamp <= end_dt)
        except ValueError:
            pass
    
    # Order by timestamp descending (newest first)
    query = query.order_by(Detection.timestamp.desc())
    
    # Apply pagination
    detections = query.offset(skip).limit(limit).all()
    
    # Convert to response format
    results = []
    for d in detections:
        # Create probabilities dict (mock for now)
        probabilities = {emotion: 0.0 for emotion in ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']}
        probabilities[d.emotion] = d.confidence
        
        result = {
            "emotion": d.emotion,
            "confidence": d.confidence,
            "probabilities": probabilities,
            "mode": d.mode,
            "timestamp": d.timestamp,
            "face_emotion": d.face_emotion,
            "face_confidence": d.face_confidence,
            "text_emotion": d.text_emotion,
            "text_confidence": d.text_confidence,
            "fusion_method": d.fusion_method,
            "rl_state": d.rl_state,
            "rl_action": d.rl_action
        }
        results.append(DetectionResponse(**result))
    
    return results


@router.get("/history/count")
async def get_history_count(
    emotion: Optional[str] = None,
    mode: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get total count of detections with filters
    
    - **emotion**: Filter by emotion (optional)
    - **mode**: Filter by mode (optional)
    - Returns total count
    """
    query = db.query(Detection)
    
    if emotion:
        query = query.filter(Detection.emotion == emotion)
    
    if mode:
        query = query.filter(Detection.mode == mode)
    
    count = query.count()
    
    return {"total": count}


@router.delete("/history/clear")
async def clear_history(
    db: Session = Depends(get_db)
):
    """
    Clear all detection history
    
    - Deletes all detection records
    - Returns count of deleted records
    """
    count = db.query(Detection).delete()
    db.commit()
    
    return {
        "message": "History cleared successfully",
        "deleted_count": count
    }
