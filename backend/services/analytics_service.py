"""
Analytics service for generating statistics and insights
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from typing import List, Dict
from collections import defaultdict

from backend.database.models import Detection, Feedback
from backend.config import settings


class AnalyticsService:
    """Service for analytics and statistics"""
    
    def get_emotion_distribution(self, db: Session, days: int = 30) -> List[Dict]:
        """Get emotion distribution for last N days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        results = db.query(
            Detection.emotion,
            func.count(Detection.id).label('count')
        ).filter(
            Detection.timestamp >= cutoff_date
        ).group_by(
            Detection.emotion
        ).all()
        
        total = sum(r.count for r in results)
        
        distribution = []
        for result in results:
            distribution.append({
                "emotion": result.emotion,
                "count": result.count,
                "percentage": round((result.count / total * 100) if total > 0 else 0, 2)
            })
        
        return distribution
    
    def get_accuracy_trend(self, db: Session, days: int = 7) -> List[Dict]:
        """Get accuracy trend for last N days"""
        trends = []
        
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = start_of_day + timedelta(days=1)
            
            total = db.query(func.count(Detection.id)).filter(
                and_(
                    Detection.timestamp >= start_of_day,
                    Detection.timestamp < end_of_day
                )
            ).scalar()
            
            correct = db.query(func.count(Detection.id)).filter(
                and_(
                    Detection.timestamp >= start_of_day,
                    Detection.timestamp < end_of_day,
                    Detection.is_correct == True
                )
            ).scalar()
            
            accuracy = (correct / total * 100) if total > 0 else 0
            
            trends.append({
                "date": start_of_day.strftime("%Y-%m-%d"),
                "accuracy": round(accuracy, 2),
                "total_predictions": total,
                "correct_predictions": correct
            })
        
        return list(reversed(trends))
    
    def get_confidence_trend(self, db: Session, days: int = 7) -> List[Dict]:
        """Get confidence trend for last N days"""
        trends = []
        
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = start_of_day + timedelta(days=1)
            
            # Overall confidence
            avg_conf = db.query(func.avg(Detection.confidence)).filter(
                and_(
                    Detection.timestamp >= start_of_day,
                    Detection.timestamp < end_of_day
                )
            ).scalar() or 0
            
            # Face confidence
            face_conf = db.query(func.avg(Detection.face_confidence)).filter(
                and_(
                    Detection.timestamp >= start_of_day,
                    Detection.timestamp < end_of_day,
                    Detection.face_confidence.isnot(None)
                )
            ).scalar() or 0
            
            # Text confidence
            text_conf = db.query(func.avg(Detection.text_confidence)).filter(
                and_(
                    Detection.timestamp >= start_of_day,
                    Detection.timestamp < end_of_day,
                    Detection.text_confidence.isnot(None)
                )
            ).scalar() or 0
            
            trends.append({
                "date": start_of_day.strftime("%Y-%m-%d"),
                "avg_confidence": round(float(avg_conf), 4),
                "face_confidence": round(float(face_conf), 4),
                "text_confidence": round(float(text_conf), 4)
            })
        
        return list(reversed(trends))
    
    def get_detections_per_day(self, db: Session, days: int = 7) -> List[Dict]:
        """Get detections per day for last N days"""
        results = []
        
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = start_of_day + timedelta(days=1)
            
            total = db.query(func.count(Detection.id)).filter(
                and_(
                    Detection.timestamp >= start_of_day,
                    Detection.timestamp < end_of_day
                )
            ).scalar()
            
            face_only = db.query(func.count(Detection.id)).filter(
                and_(
                    Detection.timestamp >= start_of_day,
                    Detection.timestamp < end_of_day,
                    Detection.mode == "face"
                )
            ).scalar()
            
            text_only = db.query(func.count(Detection.id)).filter(
                and_(
                    Detection.timestamp >= start_of_day,
                    Detection.timestamp < end_of_day,
                    Detection.mode == "text"
                )
            ).scalar()
            
            multimodal = db.query(func.count(Detection.id)).filter(
                and_(
                    Detection.timestamp >= start_of_day,
                    Detection.timestamp < end_of_day,
                    Detection.mode == "multimodal"
                )
            ).scalar()
            
            results.append({
                "date": start_of_day.strftime("%Y-%m-%d"),
                "count": total,
                "face_only": face_only,
                "text_only": text_only,
                "multimodal": multimodal
            })
        
        return list(reversed(results))
    
    def get_mode_usage(self, db: Session, days: int = 30) -> List[Dict]:
        """Get mode usage statistics"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        results = db.query(
            Detection.mode,
            func.count(Detection.id).label('count')
        ).filter(
            Detection.timestamp >= cutoff_date
        ).group_by(
            Detection.mode
        ).all()
        
        total = sum(r.count for r in results)
        
        usage = []
        for result in results:
            usage.append({
                "mode": result.mode,
                "count": result.count,
                "percentage": round((result.count / total * 100) if total > 0 else 0, 2)
            })
        
        return usage
    
    def get_summary(self, db: Session) -> Dict:
        """Get complete analytics summary"""
        total_detections = db.query(func.count(Detection.id)).scalar()
        
        correct_count = db.query(func.count(Detection.id)).filter(
            Detection.is_correct == True
        ).scalar()
        
        overall_accuracy = (correct_count / total_detections * 100) if total_detections > 0 else 0
        
        return {
            "total_detections": total_detections,
            "overall_accuracy": round(overall_accuracy, 2),
            "emotion_distribution": self.get_emotion_distribution(db),
            "accuracy_trend": self.get_accuracy_trend(db),
            "confidence_trend": self.get_confidence_trend(db),
            "detections_per_day": self.get_detections_per_day(db),
            "mode_usage": self.get_mode_usage(db)
        }


# Global service instance
analytics_service = AnalyticsService()
