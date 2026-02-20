"""
Analytics API routes
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.schemas import (
    EmotionDistribution, AccuracyTrend, ConfidenceTrend,
    DetectionsPerDay, ModeUsage, AnalyticsSummary
)
from backend.services import analytics_service

router = APIRouter()


@router.get("/analytics/emotions", response_model=List[EmotionDistribution])
async def get_emotion_distribution(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """
    Get emotion distribution for last N days
    
    - **days**: Number of days to analyze (default: 30)
    - Returns list of emotions with counts and percentages
    """
    return analytics_service.get_emotion_distribution(db, days)


@router.get("/analytics/accuracy", response_model=List[AccuracyTrend])
async def get_accuracy_trend(
    days: int = Query(7, ge=1, le=90),
    db: Session = Depends(get_db)
):
    """
    Get accuracy trend for last N days
    
    - **days**: Number of days to analyze (default: 7)
    - Returns daily accuracy percentages
    """
    return analytics_service.get_accuracy_trend(db, days)


@router.get("/analytics/confidence", response_model=List[ConfidenceTrend])
async def get_confidence_trend(
    days: int = Query(7, ge=1, le=90),
    db: Session = Depends(get_db)
):
    """
    Get confidence trend for last N days
    
    - **days**: Number of days to analyze (default: 7)
    - Returns daily average confidence scores
    """
    return analytics_service.get_confidence_trend(db, days)


@router.get("/analytics/detections-per-day", response_model=List[DetectionsPerDay])
async def get_detections_per_day(
    days: int = Query(7, ge=1, le=90),
    db: Session = Depends(get_db)
):
    """
    Get detections per day for last N days
    
    - **days**: Number of days to analyze (default: 7)
    - Returns daily detection counts by mode
    """
    return analytics_service.get_detections_per_day(db, days)


@router.get("/analytics/mode-usage", response_model=List[ModeUsage])
async def get_mode_usage(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """
    Get mode usage statistics for last N days
    
    - **days**: Number of days to analyze (default: 30)
    - Returns usage counts by mode (face, text, multimodal)
    """
    return analytics_service.get_mode_usage(db, days)


@router.get("/analytics/summary", response_model=AnalyticsSummary)
async def get_analytics_summary(
    db: Session = Depends(get_db)
):
    """
    Get complete analytics summary
    
    - Returns comprehensive analytics including all metrics
    """
    return analytics_service.get_summary(db)
