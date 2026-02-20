"""
Logging module for Adaptive Multimodal Emotion Detection System
Provides rotating file and console logging with configurable verbosity
"""
import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime


class SystemLogger:
    """System logger with rotating file handler and console handler"""
    
    def __init__(self, log_file: str, max_bytes: int, backup_count: int):
        """
        Initialize logger with rotating file handler and console handler
        
        Args:
            log_file: Path to log file
            max_bytes: Maximum size of log file before rotation
            backup_count: Number of backup files to keep
        """
        # Create logger
        self.logger = logging.getLogger('EmotionDetectionSystem')
        self.logger.setLevel(logging.DEBUG)
        
        # Prevent duplicate handlers
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        # Create logs directory if it doesn't exist
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        # Create rotating file handler
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setLevel(logging.DEBUG)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Add formatter to handlers
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def log_prediction(self, modality: str, input_data: dict, 
                      prediction: str, confidence: float):
        """
        Log prediction with timestamp and details
        
        Args:
            modality: Type of prediction ('face', 'text', 'fusion')
            input_data: Dictionary with input metadata
            prediction: Predicted emotion label
            confidence: Confidence score
        """
        log_message = (
            f"PREDICTION | Modality: {modality} | "
            f"Prediction: {prediction} | Confidence: {confidence:.4f} | "
            f"Input: {input_data}"
        )
        self.logger.info(log_message)
    
    def log_q_update(self, state: int, action: int, reward: float, 
                     old_q: float, new_q: float):
        """
        Log Q-table update
        
        Args:
            state: State index (0-3)
            action: Action index (0-2)
            reward: Reward received
            old_q: Q-value before update
            new_q: Q-value after update
        """
        log_message = (
            f"Q-UPDATE | State: {state} | Action: {action} | "
            f"Reward: {reward:.2f} | Old Q: {old_q:.4f} | New Q: {new_q:.4f}"
        )
        self.logger.info(log_message)
    
    def log_retrain(self, trigger_reason: str, samples_count: dict, 
                   metrics: dict):
        """
        Log retraining event with performance metrics
        
        Args:
            trigger_reason: Reason for retraining
            samples_count: Dictionary with sample counts per emotion
            metrics: Dictionary with performance metrics
        """
        log_message = (
            f"RETRAIN | Reason: {trigger_reason} | "
            f"Samples: {samples_count} | Metrics: {metrics}"
        )
        self.logger.info(log_message)
    
    def info(self, message: str):
        """Log info level message"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log warning level message"""
        self.logger.warning(message)
    
    def error(self, message: str, exc_info: bool = False):
        """
        Log error level message with optional exception info
        
        Args:
            message: Error message
            exc_info: Whether to include exception traceback
        """
        self.logger.error(message, exc_info=exc_info)
    
    def debug(self, message: str):
        """Log debug level message"""
        self.logger.debug(message)
