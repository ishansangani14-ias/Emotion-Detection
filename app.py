"""
Flask web application for Adaptive Multimodal Emotion Detection System
Provides REST API endpoints and web UI
"""
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import sys
import numpy as np
from datetime import datetime
import uuid

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.config import Config
from utils.logger import SystemLogger
from utils.data_generator import SyntheticDataGenerator
from models.face_model import FaceEmotionModel
from models.text_model import TextEmotionModel
from models.rl_fusion import RLFusionAgent

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
config = Config()
config.create_directories()

app.config['UPLOAD_FOLDER'] = config.UPLOADS_DIR
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH

# Initialize system components
logger = SystemLogger(config.LOG_FILE, config.LOG_MAX_BYTES, config.LOG_BACKUP_COUNT)
face_model = FaceEmotionModel(config)
text_model = TextEmotionModel(config)
fusion_agent = RLFusionAgent(config)

# Session statistics
session_stats = {
    'predictions': 0,
    'face_only': 0,
    'text_only': 0,
    'fusion': 0,
    'correct': 0,
    'start_time': datetime.now()
}


def initialize_system():
    """Load or train all models"""
    logger.info("Initializing Emotion Detection System...")
    
    # Try to load existing models
    models_exist = all([
        os.path.exists(config.CNN_MODEL_PATH),
        os.path.exists(config.TFIDF_VECTORIZER_PATH),
        os.path.exists(config.LR_MODEL_PATH)
    ])
    
    if models_exist:
        try:
            logger.info("Loading existing models...")
            face_model.load_model()
            text_model.load_model()
            logger.info("Models loaded successfully")
        except Exception as e:
            logger.error(f"Error loading models: {e}", exc_info=True)
            models_exist = False
    
    if not models_exist:
        logger.info("Training new models from scratch...")
        
        # Generate synthetic data
        data_gen = SyntheticDataGenerator(config.EMOTIONS, config.IMG_SIZE)
        
        # Generate face dataset
        logger.info("Generating synthetic face images...")
        face_paths = data_gen.generate_face_images(80, config.FACE_DATASET_DIR)
        
        # Generate text dataset
        logger.info("Generating synthetic text samples...")
        text_samples = data_gen.generate_text_samples(150)
        data_gen.save_text_dataset_csv(text_samples, config.TEXT_DATASET_PATH)
        
        # Train face model
        logger.info("Training CNN model...")
        X_train, y_train = load_face_dataset()
        face_model.build_model()
        
        # Split for validation
        split_idx = int(0.8 * len(X_train))
        X_val, y_val = X_train[split_idx:], y_train[split_idx:]
        X_train, y_train = X_train[:split_idx], y_train[:split_idx]
        
        face_model.train(X_train, y_train, X_val, y_val)
        face_model.save_model()
        logger.info("CNN model trained and saved")
        
        # Train text model
        logger.info("Training text model...")
        texts, labels = load_text_dataset()
        metrics = text_model.train(texts, labels)
        text_model.save_model()
        logger.info(f"Text model trained and saved. Metrics: {metrics}")
    
    # Load Q-table if exists
    if os.path.exists(config.Q_TABLE_PATH):
        try:
            fusion_agent.load_q_table()
            logger.info("Q-table loaded successfully")
        except:
            logger.info("Starting with new Q-table")
    
    logger.info("System initialization complete!")


def load_face_dataset():
    """Load face dataset for training"""
    images = []
    labels = []
    
    for emotion in config.EMOTIONS:
        emotion_dir = os.path.join(config.FACE_DATASET_DIR, emotion)
        if os.path.exists(emotion_dir):
            for filename in os.listdir(emotion_dir):
                if filename.endswith('.png'):
                    img_path = os.path.join(emotion_dir, filename)
                    img = face_model.preprocess_image(img_path)
                    images.append(img)
                    labels.append(emotion)
    
    X = np.array(images)
    
    # One-hot encode labels
    y = np.zeros((len(labels), config.NUM_EMOTIONS))
    for i, label in enumerate(labels):
        idx = config.EMOTIONS.index(label)
        y[i, idx] = 1
    
    return X, y


def load_text_dataset():
    """Load text dataset for training"""
    import pandas as pd
    
    df = pd.read_csv(config.TEXT_DATASET_PATH)
    texts = df['text'].tolist()
    labels = df['label'].tolist()
    
    return texts, labels


@app.route('/')
def index():
    """Render main web interface"""
    return render_template('index.html', config=config)


@app.route('/api/predict/multimodal', methods=['POST'])
def predict_multimodal():
    """Predict emotion using both face and text"""
    try:
        # Get uploaded file
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not config.allowed_file(file.filename):
            return jsonify({'error': 'Invalid file format'}), 400
        
        # Get text input
        text = request.form.get('text', '')
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Save uploaded file
        filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Predict from face
        face_emotion, face_probs, face_conf = face_model.predict(filepath)
        
        # Predict from text
        text_emotion, text_probs, text_conf = text_model.predict(text)
        
        # Fusion
        state = fusion_agent.determine_state(face_conf, text_conf)
        action = fusion_agent.select_action(state)
        final_emotion, final_probs, fusion_method = fusion_agent.fuse_predictions(
            face_probs, text_probs, action
        )
        final_conf = float(np.max(final_probs))
        
        # Log prediction
        logger.log_prediction(
            'fusion',
            {'image': filename, 'text': text[:50]},
            final_emotion,
            final_conf
        )
        
        # Update stats
        session_stats['predictions'] += 1
        session_stats['fusion'] += 1
        
        # Prepare response
        response = {
            'emotion': final_emotion,
            'confidence': final_conf,
            'probabilities': {emotion: float(final_probs[i]) 
                            for i, emotion in enumerate(config.EMOTIONS)},
            'modality': 'fusion',
            'fusion_method': fusion_method,
            'face_emotion': face_emotion,
            'face_confidence': face_conf,
            'text_emotion': text_emotion,
            'text_confidence': text_conf,
            'state': int(state),
            'action': int(action),
            'image_path': filepath
        }
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Error in multimodal prediction: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/predict/face', methods=['POST'])
def predict_face():
    """Predict emotion from facial image only"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not config.allowed_file(file.filename):
            return jsonify({'error': 'Invalid file format'}), 400
        
        # Save uploaded file
        filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Predict
        emotion, probs, confidence = face_model.predict(filepath)
        
        # Log prediction
        logger.log_prediction('face', {'image': filename}, emotion, confidence)
        
        # Update stats
        session_stats['predictions'] += 1
        session_stats['face_only'] += 1
        
        response = {
            'emotion': emotion,
            'confidence': confidence,
            'probabilities': {emotion: float(probs[i]) 
                            for i, emotion in enumerate(config.EMOTIONS)},
            'modality': 'face',
            'image_path': filepath
        }
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Error in face prediction: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/predict/text', methods=['POST'])
def predict_text():
    """Predict emotion from text only"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Predict
        emotion, probs, confidence = text_model.predict(text)
        
        # Log prediction
        logger.log_prediction('text', {'text': text[:50]}, emotion, confidence)
        
        # Update stats
        session_stats['predictions'] += 1
        session_stats['text_only'] += 1
        
        response = {
            'emotion': emotion,
            'confidence': confidence,
            'probabilities': {emotion: float(probs[i]) 
                            for i, emotion in enumerate(config.EMOTIONS)},
            'modality': 'text'
        }
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Error in text prediction: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Submit user feedback for incremental learning"""
    try:
        data = request.get_json()
        correct_emotion = data.get('correct_emotion')
        predicted_emotion = data.get('predicted_emotion')
        state = data.get('state')
        action = data.get('action')
        
        if not all([correct_emotion, predicted_emotion, state is not None, action is not None]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Compute reward
        reward = fusion_agent.compute_reward(predicted_emotion, correct_emotion)
        
        # Update Q-table
        next_state = state  # Simplified: use same state
        old_q, new_q = fusion_agent.update_q_table(state, action, reward, next_state)
        
        # Log Q-update
        logger.log_q_update(state, action, reward, old_q, new_q)
        
        # Save Q-table
        fusion_agent.save_q_table()
        
        # Update stats
        if reward > 0:
            session_stats['correct'] += 1
        
        response = {
            'success': True,
            'message': 'Feedback received and Q-table updated',
            'reward': reward,
            'old_q': old_q,
            'new_q': new_q
        }
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Error in feedback submission: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/qtable', methods=['GET'])
def get_qtable():
    """Get current Q-table state"""
    try:
        state_names = [
            "Both High (≥0.7)",
            "Face High, Text Low",
            "Face Low, Text High",
            "Both Low (<0.7)"
        ]
        action_names = ["FACE", "TEXT", "AVERAGE"]
        
        response = {
            'qtable': fusion_agent.q_table.tolist(),
            'states': state_names,
            'actions': action_names,
            'epsilon': fusion_agent.epsilon,
            'episodes': fusion_agent.episode_count
        }
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Error getting Q-table: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get dataset and session statistics"""
    try:
        # Calculate accuracy
        accuracy = (session_stats['correct'] / session_stats['predictions'] * 100) \
                   if session_stats['predictions'] > 0 else 0
        
        # Runtime
        runtime = (datetime.now() - session_stats['start_time']).total_seconds()
        
        response = {
            'session': {
                'predictions': session_stats['predictions'],
                'face_only': session_stats['face_only'],
                'text_only': session_stats['text_only'],
                'fusion': session_stats['fusion'],
                'correct': session_stats['correct'],
                'accuracy': round(accuracy, 2),
                'runtime_seconds': round(runtime, 2)
            }
        }
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Error getting statistics: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'models_loaded': face_model.model is not None and text_model.classifier is not None,
        'version': '1.0.0'
    })


if __name__ == '__main__':
    initialize_system()
    app.run(
        host=config.FLASK_HOST,
        port=config.FLASK_PORT,
        debug=config.FLASK_DEBUG
    )
