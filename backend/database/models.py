"""
SQLAlchemy database models
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class User(Base):
    """User model for authentication"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    detections = relationship("Detection", back_populates="user")


class Detection(Base):
    """Detection model for storing all emotion predictions"""
    __tablename__ = "detections"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Prediction results
    emotion = Column(String(20), nullable=False, index=True)
    confidence = Column(Float, nullable=False)
    mode = Column(String(20), nullable=False, index=True)  # face, text, multimodal
    
    # Modality-specific results
    face_emotion = Column(String(20), nullable=True)
    face_confidence = Column(Float, nullable=True)
    text_emotion = Column(String(20), nullable=True)
    text_confidence = Column(Float, nullable=True)
    
    # Fusion details
    fusion_method = Column(String(20), nullable=True)  # FACE, TEXT, AVERAGE
    rl_state = Column(Integer, nullable=True)
    rl_action = Column(Integer, nullable=True)
    
    # Data
    image_path = Column(String(255), nullable=True)
    text_content = Column(Text, nullable=True)
    
    # Feedback
    is_correct = Column(Boolean, nullable=True)
    correct_emotion = Column(String(20), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="detections")
    feedback = relationship("Feedback", back_populates="detection", uselist=False)


class Feedback(Base):
    """Feedback model for user corrections"""
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    detection_id = Column(Integer, ForeignKey("detections.id"), nullable=False, unique=True)
    correct_emotion = Column(String(20), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    detection = relationship("Detection", back_populates="feedback")


class RLTraining(Base):
    """RL Training model for Q-learning history"""
    __tablename__ = "rl_training"
    
    id = Column(Integer, primary_key=True, index=True)
    episode = Column(Integer, nullable=False, index=True)
    state = Column(Integer, nullable=False)
    action = Column(Integer, nullable=False)
    reward = Column(Float, nullable=False)
    q_value_before = Column(Float, nullable=True)
    q_value_after = Column(Float, nullable=True)
    epsilon = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
