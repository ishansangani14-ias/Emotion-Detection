"""
Download and prepare FER2013 dataset for better emotion detection
FER2013 is a well-known facial expression dataset with 35,887 images
"""
import os
import requests
import zipfile
import pandas as pd
import numpy as np
import cv2
from tqdm import tqdm

def download_fer2013():
    """Download FER2013 dataset from Kaggle"""
    print("=" * 60)
    print("FER2013 Dataset Download Instructions")
    print("=" * 60)
    print("\nThe FER2013 dataset is available on Kaggle.")
    print("\nOption 1: Manual Download (Recommended)")
    print("-" * 60)
    print("1. Go to: https://www.kaggle.com/datasets/msambare/fer2013")
    print("2. Click 'Download' button")
    print("3. Extract the downloaded zip file")
    print("4. Copy the 'train' and 'test' folders to:")
    print(f"   {os.path.abspath('emotion_detection_system/data/fer2013/')}")
    print("\nOption 2: Use Kaggle API")
    print("-" * 60)
    print("1. Install kaggle: pip install kaggle")
    print("2. Setup API credentials from kaggle.com/account")
    print("3. Run: kaggle datasets download -d msambare/fer2013")
    print("4. Extract to emotion_detection_system/data/fer2013/")
    print("\n" + "=" * 60)
    
    # Create directory
    os.makedirs('emotion_detection_system/data/fer2013', exist_ok=True)
    
    # Check if data already exists
    train_path = 'emotion_detection_system/data/fer2013/train'
    test_path = 'emotion_detection_system/data/fer2013/test'
    
    if os.path.exists(train_path) and os.path.exists(test_path):
        print("\n✓ FER2013 dataset found!")
        
        # Count images
        emotions = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
        total_train = sum([len(os.listdir(os.path.join(train_path, e))) 
                          for e in emotions if os.path.exists(os.path.join(train_path, e))])
        total_test = sum([len(os.listdir(os.path.join(test_path, e))) 
                         for e in emotions if os.path.exists(os.path.join(test_path, e))])
        
        print(f"  Training images: {total_train}")
        print(f"  Test images: {total_test}")
        print("\nYou can now run: python train_with_fer2013.py")
        return True
    else:
        print("\n✗ FER2013 dataset not found. Please download it manually.")
        return False

if __name__ == '__main__':
    download_fer2013()
