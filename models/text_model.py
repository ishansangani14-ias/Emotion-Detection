"""
Text emotion recognition model using TF-IDF and Logistic Regression
"""
import os
import numpy as np
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from typing import Tuple, Dict, List
import re
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import Config


class TextEmotionModel:
    """TF-IDF + Logistic Regression model for text emotion recognition"""
    
    def __init__(self, config: Config):
        """
        Initialize with configuration
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.vectorizer = None
        self.classifier = None
        
        # Stopwords list
        self.stopwords = set([
            'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your',
            'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she',
            'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their',
            'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
            'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an',
            'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',
            'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
            'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
            'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then',
            'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'both',
            'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
            'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will',
            'just', 'don', 'should', 'now'
        ])
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocess text: lowercase, remove URLs, punctuation, stopwords
        
        Args:
            text: Raw text string
        
        Returns:
            Preprocessed text string
        
        Raises:
            ValueError: If text is empty after preprocessing
        """
        if not text or not isinstance(text, str):
            raise ValueError("Input text is empty or invalid")
        
        # Lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+', '', text)
        
        # Remove punctuation and digits
        text = re.sub(r'[^a-z\s]', '', text)
        
        # Tokenize and remove stopwords
        tokens = text.split()
        tokens = [word for word in tokens if word not in self.stopwords and len(word) > 2]
        
        # Rejoin
        text = ' '.join(tokens)
        
        if not text.strip():
            raise ValueError("Input text is empty after preprocessing")
        
        return text
    
    def build_vectorizer(self) -> TfidfVectorizer:
        """
        Build TF-IDF vectorizer with max 10k features and bigrams
        
        Returns:
            TfidfVectorizer instance
        """
        self.vectorizer = TfidfVectorizer(
            max_features=self.config.TFIDF_MAX_FEATURES,
            ngram_range=self.config.TFIDF_NGRAM_RANGE,
            min_df=self.config.TFIDF_MIN_DF,
            sublinear_tf=True,
            analyzer='word'
        )
        return self.vectorizer
    
    def build_classifier(self) -> LogisticRegression:
        """
        Build Logistic Regression classifier with warm_start
        
        Returns:
            LogisticRegression instance
        """
        self.classifier = LogisticRegression(
            max_iter=self.config.LR_MAX_ITER,
            random_state=self.config.LR_RANDOM_STATE,
            warm_start=True,
            multi_class='multinomial',
            solver='lbfgs',
            verbose=0
        )
        return self.classifier
    
    def train(self, texts: List[str], labels: List[str]) -> Dict:
        """
        Train TF-IDF + LR model
        
        Args:
            texts: List of text strings
            labels: List of emotion labels
        
        Returns:
            Training metrics (accuracy, precision, recall, f1)
        """
        # Preprocess texts
        processed_texts = []
        valid_labels = []
        
        for text, label in zip(texts, labels):
            try:
                processed_text = self.preprocess_text(text)
                processed_texts.append(processed_text)
                valid_labels.append(label)
            except ValueError:
                # Skip empty texts
                continue
        
        # Build vectorizer if not exists
        if self.vectorizer is None:
            self.build_vectorizer()
        
        # Vectorize texts
        X = self.vectorizer.fit_transform(processed_texts)
        
        # Build classifier if not exists
        if self.classifier is None:
            self.build_classifier()
        
        # Train classifier
        self.classifier.fit(X, valid_labels)
        
        # Compute metrics
        y_pred = self.classifier.predict(X)
        accuracy = accuracy_score(valid_labels, y_pred)
        precision, recall, f1, _ = precision_recall_fscore_support(
            valid_labels, y_pred, average='weighted', zero_division=0
        )
        
        metrics = {
            'accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'f1_score': float(f1)
        }
        
        return metrics
    
    def predict(self, text: str) -> Tuple[str, np.ndarray, float]:
        """
        Predict emotion from text
        
        Args:
            text: Raw text string
        
        Returns:
            Tuple of (emotion_label, probabilities, confidence_score)
        """
        # Preprocess text
        processed_text = self.preprocess_text(text)
        
        # Vectorize
        X = self.vectorizer.transform([processed_text])
        
        # Predict probabilities
        probabilities = self.classifier.predict_proba(X)[0]
        
        # Get emotion label and confidence
        emotion_idx = np.argmax(probabilities)
        emotion_label = self.classifier.classes_[emotion_idx]
        confidence = float(probabilities[emotion_idx])
        
        # Create full probability array for all emotions
        full_probs = np.zeros(self.config.NUM_EMOTIONS)
        for i, emotion in enumerate(self.classifier.classes_):
            if emotion in self.config.EMOTIONS:
                idx = self.config.EMOTIONS.index(emotion)
                full_probs[idx] = probabilities[i]
        
        return emotion_label, full_probs, confidence
    
    def save_model(self, vectorizer_path: str = None, classifier_path: str = None):
        """
        Save vectorizer and classifier using joblib
        
        Args:
            vectorizer_path: Path to save vectorizer
            classifier_path: Path to save classifier
        """
        if vectorizer_path is None:
            vectorizer_path = self.config.TFIDF_VECTORIZER_PATH
        if classifier_path is None:
            classifier_path = self.config.LR_MODEL_PATH
        
        # Create directory if needed
        os.makedirs(os.path.dirname(vectorizer_path), exist_ok=True)
        
        # Save models
        joblib.dump(self.vectorizer, vectorizer_path)
        joblib.dump(self.classifier, classifier_path)
    
    def load_model(self, vectorizer_path: str = None, classifier_path: str = None):
        """
        Load vectorizer and classifier using joblib
        
        Args:
            vectorizer_path: Path to load vectorizer from
            classifier_path: Path to load classifier from
        """
        if vectorizer_path is None:
            vectorizer_path = self.config.TFIDF_VECTORIZER_PATH
        if classifier_path is None:
            classifier_path = self.config.LR_MODEL_PATH
        
        if os.path.exists(vectorizer_path) and os.path.exists(classifier_path):
            self.vectorizer = joblib.load(vectorizer_path)
            self.classifier = joblib.load(classifier_path)
        else:
            raise FileNotFoundError("Model files not found")
    
    def incremental_train(self, texts: List[str], labels: List[str]):
        """
        Incrementally train classifier using warm_start
        
        Args:
            texts: List of new text strings
            labels: List of new emotion labels
        """
        # Preprocess texts
        processed_texts = []
        valid_labels = []
        
        for text, label in zip(texts, labels):
            try:
                processed_text = self.preprocess_text(text)
                processed_texts.append(processed_text)
                valid_labels.append(label)
            except ValueError:
                continue
        
        # Vectorize texts
        X = self.vectorizer.transform(processed_texts)
        
        # Incrementally train
        self.classifier.fit(X, valid_labels)
