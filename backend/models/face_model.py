"""
Face emotion recognition model using CNN
Implements 4-block VGG-inspired architecture with Global Average Pooling
"""
import os
import numpy as np
import cv2
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from typing import Tuple, Dict
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import Config


class FaceEmotionModel:
    """CNN model for facial emotion recognition"""
    
    def __init__(self, config: Config):
        """
        Initialize with configuration
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.model = None
    
    def build_model(self) -> keras.Model:
        """
        Build 4-block VGG-inspired CNN with Global Average Pooling
        
        Architecture:
        - Input: 48x48x1 greyscale image
        - Block 1: Conv(32) -> Conv(32) -> BatchNorm -> MaxPool -> Dropout
        - Block 2: Conv(64) -> Conv(64) -> BatchNorm -> MaxPool -> Dropout
        - Block 3: Conv(128) -> Conv(128) -> BatchNorm -> MaxPool -> Dropout
        - Block 4: Conv(256) -> Conv(256) -> BatchNorm -> GlobalAvgPool -> Dropout
        - Dense(256) -> BatchNorm -> Dropout -> Dense(NUM_EMOTIONS) -> Softmax
        
        Returns:
            Compiled Keras model
        """
        input_shape = (*self.config.IMG_SIZE, 1)
        
        model = models.Sequential([
            # Input layer
            layers.Input(shape=input_shape),
            
            # Block 1
            layers.Conv2D(32, (3, 3), padding='same', activation='relu'),
            layers.Conv2D(32, (3, 3), padding='same', activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Block 2
            layers.Conv2D(64, (3, 3), padding='same', activation='relu'),
            layers.Conv2D(64, (3, 3), padding='same', activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Block 3
            layers.Conv2D(128, (3, 3), padding='same', activation='relu'),
            layers.Conv2D(128, (3, 3), padding='same', activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.40),
            
            # Block 4
            layers.Conv2D(256, (3, 3), padding='same', activation='relu'),
            layers.Conv2D(256, (3, 3), padding='same', activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.40),
            
            # Global Average Pooling
            layers.GlobalAveragePooling2D(),
            
            # Dense layers
            layers.Dense(256, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            
            # Output layer
            layers.Dense(self.config.NUM_EMOTIONS, activation='softmax')
        ])
        
        # Compile model
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=self.config.CNN_LEARNING_RATE),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        return model
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """
        Load and preprocess image to 48x48 greyscale
        
        Args:
            image_path: Path to image file
        
        Returns:
            Preprocessed image as numpy array with shape (48, 48, 1)
        
        Raises:
            FileNotFoundError: If image path doesn't exist
            ValueError: If image cannot be decoded
        """
        # Check if file exists
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        # Load image in greyscale
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        
        if img is None:
            raise ValueError(
                f"OpenCV could not decode: {image_path}. "
                f"Supported formats: {self.config.ALLOWED_EXTENSIONS}"
            )
        
        # Resize to target size
        img = cv2.resize(img, self.config.IMG_SIZE)
        
        # Normalize to [0, 1]
        img = img.astype(np.float32) / 255.0
        
        # Add channel dimension
        img = np.expand_dims(img, axis=-1)
        
        return img
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray,
             X_val: np.ndarray, y_val: np.ndarray) -> Dict:
        """
        Train CNN model
        
        Args:
            X_train: Training images
            y_train: Training labels (one-hot encoded)
            X_val: Validation images
            y_val: Validation labels (one-hot encoded)
        
        Returns:
            Training history with loss and accuracy metrics
        """
        # Build model if not already built
        if self.model is None:
            self.build_model()
        
        # Callbacks
        early_stopping = EarlyStopping(
            monitor='val_loss',
            patience=self.config.CNN_PATIENCE,
            restore_best_weights=True,
            verbose=1
        )
        
        reduce_lr = ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=4,
            min_lr=1e-7,
            verbose=1
        )
        
        # Train model
        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            batch_size=self.config.CNN_BATCH_SIZE,
            epochs=self.config.CNN_EPOCHS,
            callbacks=[early_stopping, reduce_lr],
            verbose=1
        )
        
        return history.history
    
    def predict(self, image_path: str) -> Tuple[str, np.ndarray, float]:
        """
        Predict emotion from image with face detection
        
        Args:
            image_path: Path to image file
        
        Returns:
            Tuple of (emotion_label, probabilities, confidence_score)
        """
        # Load image
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        # Try to detect face using Haar Cascade (optional, fallback to whole image)
        try:
            # Use local Haar Cascade file
            cascade_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                'emotion_detection_system', 'models', 'haarcascade_frontalface_default.xml'
            )
            
            if not os.path.exists(cascade_path):
                # Fallback: try to find it in OpenCV installation
                if hasattr(cv2, 'data'):
                    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            
            face_cascade = cv2.CascadeClassifier(cascade_path)
            faces = face_cascade.detectMultiScale(img, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30))
            
            if len(faces) > 0:
                # Use the largest detected face
                (x, y, w, h) = sorted(faces, key=lambda f: f[2]*f[3], reverse=True)[0]
                face_img = img[y:y+h, x:x+w]
            else:
                # No face detected, use whole image
                face_img = img
        except Exception as e:
            # If face detection fails, use whole image
            face_img = img
        
        # Preprocess
        face_img = cv2.resize(face_img, self.config.IMG_SIZE)
        face_img = face_img.astype(np.float32) / 255.0
        face_img = np.expand_dims(face_img, axis=-1)
        
        # Add batch dimension
        img_batch = np.expand_dims(face_img, axis=0)
        
        # Predict
        probabilities = self.model.predict(img_batch, verbose=0)[0]
        
        # Get emotion label and confidence
        emotion_idx = np.argmax(probabilities)
        emotion_label = self.config.EMOTIONS[emotion_idx]
        confidence = float(probabilities[emotion_idx])
        
        return emotion_label, probabilities, confidence
    
    def save_model(self, path: str = None):
        """
        Save model weights to disk
        
        Args:
            path: Path to save model (defaults to config path)
        """
        if path is None:
            path = self.config.CNN_MODEL_PATH
        
        # Create directory if needed
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Save model
        self.model.save(path)
    
    def load_model(self, path: str = None):
        """
        Load model weights from disk
        
        Args:
            path: Path to load model from (defaults to config path)
        """
        if path is None:
            path = self.config.CNN_MODEL_PATH
        
        if os.path.exists(path):
            self.model = keras.models.load_model(path)
        else:
            raise FileNotFoundError(f"Model file not found: {path}")
    
    def transfer_weights(self, new_model: keras.Model):
        """
        Transfer weights to new model for incremental learning
        
        Args:
            new_model: New model to transfer weights to
        """
        if self.model is None:
            raise ValueError("No model loaded to transfer weights from")
        
        # Transfer weights from matching layers
        for old_layer, new_layer in zip(self.model.layers, new_model.layers):
            if old_layer.name == new_layer.name:
                try:
                    new_layer.set_weights(old_layer.get_weights())
                except:
                    # Skip if shapes don't match (e.g., output layer with different classes)
                    pass
