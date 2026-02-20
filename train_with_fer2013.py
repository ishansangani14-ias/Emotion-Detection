"""
Train the emotion detection model with FER2013 dataset
This will significantly improve real-world emotion detection accuracy
"""
import os
import sys
import numpy as np
import cv2
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from tqdm import tqdm

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.config import Config
from models.face_model import FaceEmotionModel
from utils.logger import EmotionLogger

def load_fer2013_data(data_dir='emotion_detection_system/data/fer2013'):
    """
    Load FER2013 dataset from directory structure
    
    Expected structure:
    fer2013/
        train/
            angry/
            disgust/
            fear/
            happy/
            neutral/
            sad/
            surprise/
        test/
            angry/
            ...
    """
    config = Config()
    emotions = config.EMOTIONS
    
    print("Loading FER2013 dataset...")
    
    X_train, y_train = [], []
    X_test, y_test = [], []
    
    # Load training data
    train_dir = os.path.join(data_dir, 'train')
    if os.path.exists(train_dir):
        print("\nLoading training data...")
        for emotion_idx, emotion in enumerate(emotions):
            emotion_dir = os.path.join(train_dir, emotion)
            if not os.path.exists(emotion_dir):
                print(f"Warning: {emotion_dir} not found")
                continue
            
            image_files = [f for f in os.listdir(emotion_dir) 
                          if f.endswith(('.jpg', '.png', '.jpeg'))]
            
            print(f"  {emotion}: {len(image_files)} images")
            
            for img_file in tqdm(image_files, desc=f"  Loading {emotion}"):
                img_path = os.path.join(emotion_dir, img_file)
                try:
                    # Load and preprocess
                    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                    if img is None:
                        continue
                    
                    img = cv2.resize(img, config.IMG_SIZE)
                    img = img.astype(np.float32) / 255.0
                    img = np.expand_dims(img, axis=-1)
                    
                    X_train.append(img)
                    y_train.append(emotion_idx)
                except Exception as e:
                    print(f"Error loading {img_path}: {e}")
                    continue
    
    # Load test data
    test_dir = os.path.join(data_dir, 'test')
    if os.path.exists(test_dir):
        print("\nLoading test data...")
        for emotion_idx, emotion in enumerate(emotions):
            emotion_dir = os.path.join(test_dir, emotion)
            if not os.path.exists(emotion_dir):
                continue
            
            image_files = [f for f in os.listdir(emotion_dir) 
                          if f.endswith(('.jpg', '.png', '.jpeg'))]
            
            print(f"  {emotion}: {len(image_files)} images")
            
            for img_file in tqdm(image_files, desc=f"  Loading {emotion}"):
                img_path = os.path.join(emotion_dir, img_file)
                try:
                    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                    if img is None:
                        continue
                    
                    img = cv2.resize(img, config.IMG_SIZE)
                    img = img.astype(np.float32) / 255.0
                    img = np.expand_dims(img, axis=-1)
                    
                    X_test.append(img)
                    y_test.append(emotion_idx)
                except Exception as e:
                    continue
    
    # Convert to numpy arrays
    X_train = np.array(X_train)
    y_train = np.array(y_train)
    X_test = np.array(X_test)
    y_test = np.array(y_test)
    
    # One-hot encode labels
    y_train = to_categorical(y_train, config.NUM_EMOTIONS)
    y_test = to_categorical(y_test, config.NUM_EMOTIONS)
    
    print(f"\nDataset loaded:")
    print(f"  Training: {X_train.shape[0]} images")
    print(f"  Test: {X_test.shape[0]} images")
    
    return X_train, y_train, X_test, y_test

def train_model():
    """Train the face emotion model with FER2013 data"""
    config = Config()
    logger = EmotionLogger(config)
    
    print("=" * 60)
    print("Training Emotion Detection Model with FER2013")
    print("=" * 60)
    
    # Load data
    try:
        X_train, y_train, X_test, y_test = load_fer2013_data()
    except Exception as e:
        print(f"\nError loading data: {e}")
        print("\nPlease run: python download_fer2013.py")
        print("And follow the instructions to download the dataset.")
        return
    
    if len(X_train) == 0:
        print("\nNo training data found!")
        print("Please download FER2013 dataset first.")
        return
    
    # Split training data for validation
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, 
        test_size=0.15, 
        random_state=42,
        stratify=np.argmax(y_train, axis=1)
    )
    
    print(f"\nData split:")
    print(f"  Training: {X_train.shape[0]} images")
    print(f"  Validation: {X_val.shape[0]} images")
    print(f"  Test: {X_test.shape[0]} images")
    
    # Initialize model
    print("\nBuilding model...")
    face_model = FaceEmotionModel(config)
    face_model.build_model()
    
    print(f"\nModel architecture:")
    face_model.model.summary()
    
    # Train model
    print("\n" + "=" * 60)
    print("Starting training...")
    print("=" * 60)
    
    history = face_model.train(X_train, y_train, X_val, y_val)
    
    # Evaluate on test set
    print("\n" + "=" * 60)
    print("Evaluating on test set...")
    print("=" * 60)
    
    test_loss, test_acc = face_model.model.evaluate(X_test, y_test, verbose=1)
    print(f"\nTest accuracy: {test_acc * 100:.2f}%")
    print(f"Test loss: {test_loss:.4f}")
    
    # Save model
    print("\nSaving model...")
    face_model.save_model()
    print(f"Model saved to: {config.CNN_MODEL_PATH}")
    
    # Log training
    logger.info(f"Model trained with FER2013 - Test accuracy: {test_acc * 100:.2f}%")
    
    print("\n" + "=" * 60)
    print("Training complete!")
    print("=" * 60)
    print("\nYou can now restart the Flask app to use the new model:")
    print("  python app.py")
    print("\nThe model should now detect emotions much more accurately!")

if __name__ == '__main__':
    train_model()
