"""
Data generation utilities for Adaptive Multimodal Emotion Detection System
Generates synthetic training data for bootstrapping the system
"""
import os
import numpy as np
import cv2
import pandas as pd
from typing import Dict, Tuple, List


class SyntheticDataGenerator:
    """Generator for synthetic facial images and text samples"""
    
    def __init__(self, emotions: List[str], img_size: Tuple[int, int]):
        """
        Initialize generator with emotion classes and image dimensions
        
        Args:
            emotions: List of emotion labels
            img_size: Tuple of (width, height) for images
        """
        self.emotions = emotions
        self.img_size = img_size
        
        # Emotion-specific text templates
        self.text_templates = {
            'angry': [
                "I am so frustrated with this situation",
                "This makes me really mad",
                "I can't believe how annoying this is",
                "I'm furious about what happened",
                "This is absolutely infuriating"
            ],
            'disgust': [
                "This is absolutely revolting",
                "I find this really gross",
                "That's disgusting and unacceptable",
                "I'm repulsed by this behavior",
                "This makes me feel sick"
            ],
            'fear': [
                "I'm really scared about this",
                "This situation terrifies me",
                "I'm worried something bad will happen",
                "I feel anxious and afraid",
                "This is frightening and overwhelming"
            ],
            'happy': [
                "I'm so excited and joyful",
                "This makes me really happy",
                "I feel wonderful and blessed",
                "I'm thrilled about this news",
                "This brings me so much joy"
            ],
            'neutral': [
                "I went to the store today",
                "The meeting is scheduled for tomorrow",
                "I need to finish this report",
                "The weather is typical for this season",
                "I'm working on the project"
            ],
            'sad': [
                "I feel really down and depressed",
                "This makes me so sad",
                "I'm heartbroken about what happened",
                "I feel lonely and miserable",
                "This situation brings me to tears"
            ],
            'surprise': [
                "I can't believe this happened",
                "This is so unexpected and shocking",
                "I'm amazed by this revelation",
                "Wow, I never saw that coming",
                "This is absolutely astonishing"
            ]
        }
    
    def generate_face_images(self, samples_per_emotion: int, 
                            output_dir: str) -> Dict[str, List[str]]:
        """
        Generate synthetic facial images with emotion-specific patterns
        
        Args:
            samples_per_emotion: Number of images to generate per emotion
            output_dir: Directory to save generated images
        
        Returns:
            Dictionary mapping emotion to list of image paths
        """
        image_paths = {emotion: [] for emotion in self.emotions}
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        for emotion in self.emotions:
            # Create emotion subdirectory
            emotion_dir = os.path.join(output_dir, emotion)
            os.makedirs(emotion_dir, exist_ok=True)
            
            for i in range(samples_per_emotion):
                # Generate synthetic face image
                img = self._generate_emotion_face(emotion)
                
                # Save image
                filename = f"{emotion}_{i:04d}.png"
                filepath = os.path.join(emotion_dir, filename)
                cv2.imwrite(filepath, img)
                
                image_paths[emotion].append(filepath)
        
        return image_paths
    
    def _generate_emotion_face(self, emotion: str) -> np.ndarray:
        """
        Generate a synthetic face image with emotion-specific patterns
        
        Args:
            emotion: Emotion label
        
        Returns:
            Greyscale image as numpy array
        """
        # Create base image with random noise
        img = np.random.randint(50, 200, self.img_size, dtype=np.uint8)
        
        # Add emotion-specific patterns
        center_x, center_y = self.img_size[0] // 2, self.img_size[1] // 2
        
        if emotion == 'happy':
            # Brighter image with smile-like curve
            img = np.clip(img + 30, 0, 255).astype(np.uint8)
            cv2.ellipse(img, (center_x, center_y + 5), (15, 10), 0, 0, 180, 200, 2)
        
        elif emotion == 'sad':
            # Darker image with frown-like curve
            img = np.clip(img - 30, 0, 255).astype(np.uint8)
            cv2.ellipse(img, (center_x, center_y + 10), (15, 10), 0, 180, 360, 100, 2)
        
        elif emotion == 'angry':
            # High contrast with angular features
            img = np.clip(img + np.random.randint(-50, 50, self.img_size), 0, 255).astype(np.uint8)
            cv2.line(img, (center_x - 15, center_y - 10), (center_x - 5, center_y - 5), 50, 2)
            cv2.line(img, (center_x + 15, center_y - 10), (center_x + 5, center_y - 5), 50, 2)
        
        elif emotion == 'surprise':
            # Bright with circular features
            img = np.clip(img + 20, 0, 255).astype(np.uint8)
            cv2.circle(img, (center_x, center_y), 8, 220, 2)
        
        elif emotion == 'fear':
            # Darker with scattered patterns
            img = np.clip(img - 20, 0, 255).astype(np.uint8)
            for _ in range(10):
                x, y = np.random.randint(0, self.img_size[0]), np.random.randint(0, self.img_size[1])
                cv2.circle(img, (x, y), 2, 80, -1)
        
        elif emotion == 'disgust':
            # Medium contrast with asymmetric features
            cv2.line(img, (center_x - 10, center_y + 5), (center_x, center_y), 100, 2)
            cv2.line(img, (center_x, center_y), (center_x + 10, center_y + 5), 100, 2)
        
        # Add face-like ellipse
        cv2.ellipse(img, (center_x, center_y), (18, 24), 0, 0, 360, 150, 1)
        
        return img
    
    def generate_text_samples(self, samples_per_emotion: int) -> Dict[str, List[str]]:
        """
        Generate synthetic text samples with emotion-specific keywords
        
        Args:
            samples_per_emotion: Number of text samples per emotion
        
        Returns:
            Dictionary mapping emotion to list of text strings
        """
        text_samples = {emotion: [] for emotion in self.emotions}
        
        for emotion in self.emotions:
            templates = self.text_templates.get(emotion, ["I feel {emotion}"])
            
            for i in range(samples_per_emotion):
                # Select template and add variation
                template = templates[i % len(templates)]
                
                # Add slight variations
                variations = [
                    template,
                    template + " right now",
                    template + " today",
                    "Honestly, " + template.lower(),
                    template + " and I can't help it"
                ]
                
                text = variations[i % len(variations)]
                text_samples[emotion].append(text)
        
        return text_samples
    
    def load_real_dataset(self, dataset_name: str, 
                         dataset_path: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        Load real datasets (FER-2013, ISEAR, GoEmotions)
        
        Args:
            dataset_name: Name of dataset ('fer2013', 'isear', 'goemotions')
            dataset_path: Path to dataset files
        
        Returns:
            Tuple of (data, labels)
        """
        if dataset_name.lower() == 'fer2013':
            return self._load_fer2013(dataset_path)
        elif dataset_name.lower() in ['isear', 'goemotions']:
            return self._load_text_dataset(dataset_path)
        else:
            raise ValueError(f"Unknown dataset: {dataset_name}")
    
    def _load_fer2013(self, dataset_path: str) -> Tuple[np.ndarray, np.ndarray]:
        """Load FER-2013 facial expression dataset"""
        # Check if dataset exists
        if not os.path.exists(dataset_path):
            raise FileNotFoundError(f"FER-2013 dataset not found at {dataset_path}")
        
        # Load images from subdirectories
        images = []
        labels = []
        
        for emotion in self.emotions:
            emotion_dir = os.path.join(dataset_path, emotion)
            if os.path.exists(emotion_dir):
                for filename in os.listdir(emotion_dir):
                    if filename.endswith(('.png', '.jpg', '.jpeg')):
                        img_path = os.path.join(emotion_dir, filename)
                        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                        if img is not None:
                            img = cv2.resize(img, self.img_size)
                            images.append(img)
                            labels.append(emotion)
        
        return np.array(images), np.array(labels)
    
    def _load_text_dataset(self, dataset_path: str) -> Tuple[List[str], List[str]]:
        """Load text emotion dataset from CSV"""
        if not os.path.exists(dataset_path):
            raise FileNotFoundError(f"Text dataset not found at {dataset_path}")
        
        # Load CSV
        df = pd.read_csv(dataset_path)
        
        # Auto-detect column names
        text_col = None
        label_col = None
        
        for col in df.columns:
            col_lower = col.lower()
            if col_lower in ['text', 'sentence', 'content', 'message']:
                text_col = col
            elif col_lower in ['label', 'emotion', 'category', 'class']:
                label_col = col
        
        if text_col is None or label_col is None:
            raise ValueError(f"Could not auto-detect text and label columns in {dataset_path}")
        
        texts = df[text_col].tolist()
        labels = df[label_col].tolist()
        
        return texts, labels
    
    def save_text_dataset_csv(self, text_samples: Dict[str, List[str]], 
                             output_path: str):
        """
        Save text samples to CSV file
        
        Args:
            text_samples: Dictionary mapping emotion to list of texts
            output_path: Path to save CSV file
        """
        # Create DataFrame
        data = []
        for emotion, texts in text_samples.items():
            for text in texts:
                data.append({'text': text, 'label': emotion})
        
        df = pd.DataFrame(data)
        
        # Create directory if needed
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save to CSV
        df.to_csv(output_path, index=False)
