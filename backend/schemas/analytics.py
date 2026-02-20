"""
Pydantic schemas for analytics endpoints
"""
from pydantic import BaseModel
from typing import Dict, List
from datetime import datetime


class EmotionDistribution(BaseModel):
    """Emotion distribution data"""
    emotion: str
    count: int
    percentage: float


class AccuracyTrend(BaseModel):
    """Accuracy trend data point"""
    date: str
    accuracy: float
    total_predictions: int
    correct_predictions: int


class ConfidenceTrend(BaseModel):
    """Confidence trend data point"""
    date: str
    avg_confidence: float
    face_confidence: float
    text_confidence: float


class DetectionsPerDay(BaseModel):
    """Detections per day data"""
    date: str
    count: int
    face_only: int
    text_only: int
    multimodal: int


class ModeUsage(BaseModel):
    """Mode usage statistics"""
    mode: str
    count: int
    percentage: float


class AnalyticsSummary(BaseModel):
    """Complete analytics summary"""
    total_detections: int
    overall_accuracy: float
    emotion_distribution: List[EmotionDistribution]
    accuracy_trend: List[AccuracyTrend]
    confidence_trend: List[ConfidenceTrend]
    detections_per_day: List[DetectionsPerDay]
    mode_usage: List[ModeUsage]
