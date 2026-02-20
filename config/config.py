"""
Configuration module for Adaptive Multimodal Emotion Detection System
Centralizes all hyperparameters, paths, and constants
"""
import os


class Config:
    """Central configuration class for all system parameters"""
    
    # Emotion classes
    EMOTIONS = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
    NUM_EMOTIONS = len(EMOTIONS)
    
    # CNN parameters
    IMG_SIZE = (48, 48)
    CNN_BLOCKS = 4
    CNN_FILTERS = [32, 64, 128, 256]  # Filters for each block
    CNN_DROPOUT = 0.25  # Dropout rate for regularization
    CNN_LEARNING_RATE = 0.0001
    CNN_BATCH_SIZE = 32
    CNN_EPOCHS = 30
    CNN_PATIENCE = 8  # Early stopping patience
    
    # NLP parameters
    TFIDF_MAX_FEATURES = 10000
    TFIDF_NGRAM_RANGE = (1, 2)  # Unigrams and bigrams
    TFIDF_MIN_DF = 2
    LR_MAX_ITER = 1000
    LR_RANDOM_STATE = 42
    
    # Q-learning parameters
    Q_LEARNING_RATE = 0.1  # Alpha
    Q_DISCOUNT_FACTOR = 0.9  # Gamma
    Q_EPSILON = 0.2  # Initial exploration rate
    Q_EPSILON_MIN = 0.05  # Minimum exploration rate
    Q_EPSILON_DECAY = 0.995  # Decay rate per episode
    CONFIDENCE_THRESHOLD_HIGH = 0.7
    NUM_STATES = 4
    NUM_ACTIONS = 3
    
    # Incremental learning parameters
    RETRAIN_THRESHOLD = 50  # Images per emotion class to trigger retrain
    TRANSFER_LEARNING_RATE = 0.00001
    RETRAIN_EPOCHS = 10
    
    # Paths
    BASE_DIR = 'emotion_detection_system'
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    MODELS_DIR = os.path.join(BASE_DIR, 'models')
    LOGS_DIR = os.path.join(BASE_DIR, 'logs')
    INCREMENTAL_DIR = os.path.join(DATA_DIR, 'incremental')
    UPLOADS_DIR = os.path.join(BASE_DIR, 'uploads')
    
    # Dataset paths
    FACE_DATASET_DIR = os.path.join(DATA_DIR, 'face_dataset')
    TEXT_DATASET_PATH = os.path.join(DATA_DIR, 'text_dataset', 'text_emotions.csv')
    
    # Model file paths
    CNN_MODEL_PATH = os.path.join(MODELS_DIR, 'cnn_model.keras')
    TFIDF_VECTORIZER_PATH = os.path.join(MODELS_DIR, 'tfidf_vectorizer.pkl')
    LR_MODEL_PATH = os.path.join(MODELS_DIR, 'lr_model.pkl')
    Q_TABLE_PATH = os.path.join(MODELS_DIR, 'q_table.npy')
    
    # Logging
    LOG_FILE = os.path.join(LOGS_DIR, 'system.log')
    LOG_MAX_BYTES = 10 * 1024 * 1024  # 10 MB
    LOG_BACKUP_COUNT = 5
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Flask configuration
    FLASK_HOST = '0.0.0.0'
    FLASK_PORT = 5000
    FLASK_DEBUG = True
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}
    
    # UI Color scheme
    COLOR_PRIMARY = '#FF6B35'  # Orange
    COLOR_SECONDARY = '#2C2C2C'  # Dark grey/black
    COLOR_ACCENT = '#4A4A4A'  # Medium grey
    COLOR_BACKGROUND = '#1A1A1A'  # Very dark grey
    COLOR_TEXT = '#E0E0E0'  # Light grey text
    COLOR_SUCCESS = '#4CAF50'  # Green for success
    COLOR_ERROR = '#F44336'  # Red for errors
    
    @classmethod
    def create_directories(cls):
        """Create all necessary directories if they don't exist"""
        directories = [
            cls.BASE_DIR,
            cls.DATA_DIR,
            cls.MODELS_DIR,
            cls.LOGS_DIR,
            cls.INCREMENTAL_DIR,
            cls.UPLOADS_DIR,
            cls.FACE_DATASET_DIR,
            os.path.dirname(cls.TEXT_DATASET_PATH)
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        
        # Create emotion subdirectories in incremental folder
        for emotion in cls.EMOTIONS:
            emotion_dir = os.path.join(cls.INCREMENTAL_DIR, emotion)
            os.makedirs(emotion_dir, exist_ok=True)
    
    @classmethod
    def allowed_file(cls, filename):
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in cls.ALLOWED_EXTENSIONS
