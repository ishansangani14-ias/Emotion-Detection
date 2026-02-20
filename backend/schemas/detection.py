"""
Pydantic schemas for detection endpoints
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime


class DetectionBase(BaseModel):
    """Base detection schema"""
    emotion: str
    confidence: float
    mode: str


class FaceDetectionRequest(BaseModel):
    """Request schema for face detection"""
    pass  # Image comes as file upload


class TextDetectionRequest(BaseModel):
    """Request schema for text detection"""
    text: str = Field(..., min_length=1, max_length=5000)


class MultimodalDetectionRequest(BaseModel):
    """Request schema for multimodal detection"""
    text: str = Field(..., min_length=1, max_length=5000)


class DetectionResponse(BaseModel):
    """Response schema for detection"""
    emotion: str
    confidence: float
    probabilities: Dict[str, float]
    mode: str
    timestamp: datetime
    
    # Optional multimodal fields
    face_emotion: Optional[str] = None
    face_confidence: Optional[float] = None
    text_emotion: Optional[str] = None
    text_confidence: Optional[float] = None
    fusion_method: Optional[str] = None
    rl_state: Optional[int] = None
    rl_action: Optional[int] = None
    
    class Config:
        from_attributes = True


class FeedbackRequest(BaseModel):
    """Request schema for feedback"""
    detection_id: int
    correct_emotion: str
    predicted_emotion: str
    state: Optional[int] = None
    action: Optional[int] = None


class FeedbackResponse(BaseModel):
    """Response schema for feedback"""
    message: str
    q_table_updated: bool
    reward: float


class BatchDetectionResponse(BaseModel):
    """Response schema for batch detection"""
    total: int
    processed: int
    results: List[DetectionResponse]
    errors: List[str]
