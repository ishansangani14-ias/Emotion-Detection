"""
Detection service for emotion prediction
"""
import os
import cv2
import numpy as np
from typing import Tuple, Dict
from datetime import datetime
from sqlalchemy.orm import Session

from backend.config import settings
from backend.database.models import Detection
from backend.models.face_model import FaceEmotionModel
from backend.models.text_model import TextEmotionModel
from backend.models.rl_fusion import RLFusionAgent


class DetectionService:
    """Service for handling emotion detection"""
    
    def __init__(self):
        """Initialize models"""
        self.face_model = None
        self.text_model = None
        self.rl_agent = None
        self._load_models()
    
    def _load_models(self):
        """Load all ML models"""
        try:
            # Import config from parent directory
            import sys
            import os
            parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            sys.path.insert(0, parent_dir)
            
            from config.config import Config
            config = Config()
            
            self.face_model = FaceEmotionModel(config)
            self.face_model.load_model(settings.cnn_model_path)
            
            # Load text model
            self.text_model = TextEmotionModel(config)
            self.text_model.load_model(
                settings.tfidf_path,
                settings.text_model_path
            )
            
            # Load RL agent
            self.rl_agent = RLFusionAgent(config)
            try:
                self.rl_agent.load_q_table()
            except FileNotFoundError:
                # Q-table doesn't exist yet, will be created
                pass
                
        except Exception as e:
            print(f"Error loading models: {e}")
            raise
    
    async def detect_face(
        self, 
        image_path: str,
        db: Session,
        user_id: int = None
    ) -> Tuple[Dict, Detection]:
        """
        Detect emotion from face image
        
        Args:
            image_path: Path to image file
            db: Database session
            user_id: Optional user ID
        
        Returns:
            Tuple of (result_dict, detection_record)
        """
        # Predict emotion
        emotion, probabilities, confidence = self.face_model.predict(image_path)
        
        # Create probability dictionary
        prob_dict = {
            emotion_name: float(prob)
            for emotion_name, prob in zip(settings.EMOTIONS, probabilities)
        }
        
        # Save to database
        detection = Detection(
            user_id=user_id,
            emotion=emotion,
            confidence=confidence,
            mode="face",
            face_emotion=emotion,
            face_confidence=confidence,
            image_path=image_path
        )
        db.add(detection)
        db.commit()
        db.refresh(detection)
        
        result = {
            "emotion": emotion,
            "confidence": confidence,
            "probabilities": prob_dict,
            "mode": "face",
            "timestamp": detection.timestamp
        }
        
        return result, detection
    
    async def detect_text(
        self,
        text: str,
        db: Session,
        user_id: int = None
    ) -> Tuple[Dict, Detection]:
        """
        Detect emotion from text
        
        Args:
            text: Input text
            db: Database session
            user_id: Optional user ID
        
        Returns:
            Tuple of (result_dict, detection_record)
        """
        # Predict emotion
        emotion, probabilities, confidence = self.text_model.predict(text)
        
        # Create probability dictionary
        prob_dict = {
            emotion_name: float(prob)
            for emotion_name, prob in zip(settings.EMOTIONS, probabilities)
        }
        
        # Save to database
        detection = Detection(
            user_id=user_id,
            emotion=emotion,
            confidence=confidence,
            mode="text",
            text_emotion=emotion,
            text_confidence=confidence,
            text_content=text
        )
        db.add(detection)
        db.commit()
        db.refresh(detection)
        
        result = {
            "emotion": emotion,
            "confidence": confidence,
            "probabilities": prob_dict,
            "mode": "text",
            "timestamp": detection.timestamp
        }
        
        return result, detection
    
    async def detect_multimodal(
        self,
        image_path: str,
        text: str,
        db: Session,
        user_id: int = None
    ) -> Tuple[Dict, Detection]:
        """
        Detect emotion using multimodal fusion
        
        Args:
            image_path: Path to image file
            text: Input text
            db: Database session
            user_id: Optional user ID
        
        Returns:
            Tuple of (result_dict, detection_record)
        """
        # Get face prediction
        face_emotion, face_probs, face_conf = self.face_model.predict(image_path)
        
        # Get text prediction
        text_emotion, text_probs, text_conf = self.text_model.predict(text)
        
        # Determine RL state
        state = self.rl_agent.determine_state(face_conf, text_conf)
        
        # Select action
        action = self.rl_agent.select_action(state)
        
        # Fuse predictions
        final_emotion, final_probs, fusion_method = self.rl_agent.fuse_predictions(
            face_probs, text_probs, action
        )
        
        final_confidence = float(np.max(final_probs))
        
        # Create probability dictionary
        prob_dict = {
            emotion_name: float(prob)
            for emotion_name, prob in zip(settings.EMOTIONS, final_probs)
        }
        
        # Save to database
        detection = Detection(
            user_id=user_id,
            emotion=final_emotion,
            confidence=final_confidence,
            mode="multimodal",
            face_emotion=face_emotion,
            face_confidence=face_conf,
            text_emotion=text_emotion,
            text_confidence=text_conf,
            fusion_method=fusion_method,
            rl_state=state,
            rl_action=action,
            image_path=image_path,
            text_content=text
        )
        db.add(detection)
        db.commit()
        db.refresh(detection)
        
        result = {
            "emotion": final_emotion,
            "confidence": final_confidence,
            "probabilities": prob_dict,
            "mode": "multimodal",
            "face_emotion": face_emotion,
            "face_confidence": face_conf,
            "text_emotion": text_emotion,
            "text_confidence": text_conf,
            "fusion_method": fusion_method,
            "rl_state": state,
            "rl_action": action,
            "timestamp": detection.timestamp
        }
        
        return result, detection


# Global service instance
detection_service = DetectionService()
