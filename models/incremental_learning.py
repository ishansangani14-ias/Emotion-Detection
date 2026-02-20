"""
Incremental learning module for runtime knowledge growth
Manages feedback storage and automatic retraining
"""
import os
import shutil
import numpy as np
from typing import Dict
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import Config
from models.face_model import FaceEmotionModel
from utils.logger import SystemLogger


class IncrementalLearner:
    """Manages incremental learning and auto-retraining"""
    
    def __init__(self, config: Config, face_model: FaceEmotionModel,
                 logger: SystemLogger):
        """
        Initialize incremental learner
        
        Args:
            config: Configuration object
            face_model: Face emotion model instance
            logger: System logger instance
        """
        self.config = config
        self.face_model = face_model
        self.logger = logger
        self.storage_stats = {emotion: 0 for emotion in config.EMOTIONS}
        
        # Initialize storage directories
        for emotion in config.EMOTIONS:
            emotion_dir = os.path.join(config.INCREMENTAL_DIR, emotion)
            os.makedirs(emotion_dir, exist_ok=True)
        
        # Count existing images
        self._update_storage_stats()
    
    def _update_storage_stats(self):
        """Update storage statistics by counting files"""
        for emotion in self.config.EMOTIONS:
            emotion_dir = os.path.join(self.config.INCREMENTAL_DIR, emotion)
            if os.path.exists(emotion_dir):
                count = len([f for f in os.listdir(emotion_dir) 
                           if f.endswith(('.png', '.jpg', '.jpeg', '.bmp'))])
                self.storage_stats[emotion] = count
    
    def store_feedback(self, image_path: str, emotion: str):
        """
        Store image in emotion-specific folder for incremental learning
        
        Args:
            image_path: Path to image file
            emotion: Correct emotion label
        
        Raises:
            ValueError: If emotion label is invalid or image path doesn't exist
        """
        # Validate emotion
        if emotion not in self.config.EMOTIONS:
            raise ValueError(f"Invalid emotion: {emotion}")
        
        # Validate image path
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        # Create destination path
        emotion_dir = os.path.join(self.config.INCREMENTAL_DIR, emotion)
        os.makedirs(emotion_dir, exist_ok=True)
        
        # Generate unique filename
        count = self.storage_stats[emotion]
        filename = f"{emotion}_{count:05d}.png"
        dest_path = os.path.join(emotion_dir, filename)
        
        # Copy image
        shutil.copy2(image_path, dest_path)
        
        # Update statistics
        self.storage_stats[emotion] += 1
        
        self.logger.info(f"Stored feedback image: {emotion} (total: {self.storage_stats[emotion]})")
        
        return dest_path, self.storage_stats[emotion]
    
    def check_retrain_trigger(self) -> bool:
        """
        Check if any emotion class has reached retrain threshold
        
        Returns:
            True if retraining should be triggered
        """
        for emotion, count in self.storage_stats.items():
            if count >= self.config.RETRAIN_THRESHOLD and count % self.config.RETRAIN_THRESHOLD == 0:
                self.logger.info(f"Retrain trigger reached for {emotion}: {count} images")
                return True
        return False
    
    def auto_retrain(self):
        """
        Automatically retrain CNN with accumulated samples
        
        Process:
        1. Load all stored images
        2. Create new model with same architecture
        3. Transfer weights from old model
        4. Train with lower learning rate
        5. Update face_model with new weights
        """
        try:
            self.logger.info("Starting auto-retrain...")
            
            # Load all incremental images
            images = []
            labels = []
            
            for emotion in self.config.EMOTIONS:
                emotion_dir = os.path.join(self.config.INCREMENTAL_DIR, emotion)
                if os.path.exists(emotion_dir):
                    for filename in os.listdir(emotion_dir):
                        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                            img_path = os.path.join(emotion_dir, filename)
                            try:
                                img = self.face_model.preprocess_image(img_path)
                                images.append(img)
                                labels.append(emotion)
                            except Exception as e:
                                self.logger.warning(f"Failed to load {img_path}: {e}")
            
            if len(images) < 10:
                self.logger.warning("Not enough images for retraining")
                return
            
            # Convert to numpy arrays
            X = np.array(images)
            y = np.zeros((len(labels), self.config.NUM_EMOTIONS))
            for i, label in enumerate(labels):
                idx = self.config.EMOTIONS.index(label)
                y[i, idx] = 1
            
            # Create new model
            new_model = self.face_model.build_model()
            
            # Transfer weights from old model
            if self.face_model.model is not None:
                self.face_model.transfer_weights(new_model)
                self.logger.info("Transferred weights from old model")
            
            # Split for validation
            split_idx = int(0.8 * len(X))
            X_val, y_val = X[split_idx:], y[split_idx:]
            X_train, y_train = X[:split_idx], y[:split_idx]
            
            # Train with lower learning rate
            import tensorflow as tf
            new_model.compile(
                optimizer=tf.keras.optimizers.Adam(learning_rate=self.config.TRANSFER_LEARNING_RATE),
                loss='categorical_crossentropy',
                metrics=['accuracy']
            )
            
            history = new_model.fit(
                X_train, y_train,
                validation_data=(X_val, y_val),
                batch_size=self.config.CNN_BATCH_SIZE,
                epochs=self.config.RETRAIN_EPOCHS,
                verbose=1
            )
            
            # Update face model
            self.face_model.model = new_model
            self.face_model.save_model()
            
            # Log metrics
            metrics = {
                'final_loss': float(history.history['loss'][-1]),
                'final_accuracy': float(history.history['accuracy'][-1]),
                'val_loss': float(history.history['val_loss'][-1]),
                'val_accuracy': float(history.history['val_accuracy'][-1])
            }
            
            self.logger.log_retrain(
                'auto_trigger',
                self.storage_stats.copy(),
                metrics
            )
            
            self.logger.info(f"Auto-retrain completed. Metrics: {metrics}")
            
        except Exception as e:
            self.logger.error(f"Auto-retrain failed: {e}", exc_info=True)
    
    def get_statistics(self) -> Dict[str, int]:
        """
        Get current storage statistics
        
        Returns:
            Dictionary with samples per emotion class
        """
        self._update_storage_stats()
        return self.storage_stats.copy()
    
    def reset_statistics(self):
        """Reset storage statistics after retraining"""
        self.storage_stats = {emotion: 0 for emotion in self.config.EMOTIONS}
        self.logger.info("Storage statistics reset")
