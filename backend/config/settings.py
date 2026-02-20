"""
Application settings and configuration
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database
    DATABASE_URL: str = "postgresql://admin:password@localhost:5432/emotion_db"
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_WORKERS: int = 4
    SECRET_KEY: str = "your-secret-key-change-this"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    
    # Model Paths
    MODEL_BASE_PATH: str = "../emotion_detection_system/models"
    CNN_MODEL_FILE: str = "cnn_model.keras"
    TEXT_MODEL_FILE: str = "text_emotion_model.joblib"
    TFIDF_VECTORIZER_FILE: str = "tfidf_vectorizer.joblib"
    HAAR_CASCADE_FILE: str = "haarcascade_frontalface_default.xml"
    
    # Storage
    UPLOAD_DIR: str = "../emotion_detection_system/uploads"
    MAX_FILE_SIZE: int = 16777216  # 16MB
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "../emotion_detection_system/logs/api.log"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_ENABLED: bool = False
    
    # Emotion Configuration
    EMOTIONS: List[str] = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
    IMG_SIZE: tuple = (48, 48)
    CONFIDENCE_THRESHOLD: float = 0.7
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    @property
    def cnn_model_path(self) -> str:
        """Full path to CNN model"""
        return os.path.join(self.MODEL_BASE_PATH, self.CNN_MODEL_FILE)
    
    @property
    def text_model_path(self) -> str:
        """Full path to text model"""
        return os.path.join(self.MODEL_BASE_PATH, self.TEXT_MODEL_FILE)
    
    @property
    def tfidf_path(self) -> str:
        """Full path to TF-IDF vectorizer"""
        return os.path.join(self.MODEL_BASE_PATH, self.TFIDF_VECTORIZER_FILE)
    
    @property
    def haar_cascade_path(self) -> str:
        """Full path to Haar Cascade"""
        return os.path.join(self.MODEL_BASE_PATH, self.HAAR_CASCADE_FILE)
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
