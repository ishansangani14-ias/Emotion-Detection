# 🎭 Adaptive Multimodal Emotion Detection System

An advanced real-time emotion detection system using deep learning, combining facial recognition (CNN), text analysis (NLP), and reinforcement learning (Q-learning) for multimodal emotion classification.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange.svg)
![Flask](https://img.shields.io/badge/Flask-2.x-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 🎥 Real-Time Live Camera Detection
- **Automatic emotion detection** from webcam every 500ms
- **Face detection** using Haar Cascade
- **No manual capture** - continuous real-time analysis
- **7 emotions**: Angry, Disgust, Fear, Happy, Neutral, Sad, Surprise

### 🤖 Multimodal AI System
- **CNN Model**: 4-block VGG-inspired architecture for facial emotion recognition
- **NLP Model**: TF-IDF + Logistic Regression for text emotion analysis
- **Q-Learning Fusion**: Reinforcement learning agent that combines face and text predictions
- **Incremental Learning**: Auto-retrains when new data reaches threshold

### 🎨 Modern UI
- **Dark multicolor gradient theme** (Red → Orange → Yellow → Green)
- **Animated gradients** on buttons, borders, and text
- **Real-time statistics** and confidence scores
- **Responsive design** with smooth transitions

### 📊 Three Detection Modes
1. **Multimodal**: Combines face image + text for fusion prediction
2. **Face Only**: Camera or upload image for facial emotion detection
3. **Text Only**: Analyze text for emotion classification

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Webcam (for live detection)
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/ishansangani14-ias/Emotion-Detection.git
cd Emotion-Detection
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python app.py
```

4. **Open your browser**
```
http://localhost:5000
```

## 📖 Usage

### Live Camera Detection
1. Click **"Face Only"** mode
2. Click **"Live Camera"** button
3. Click **"Start Live Detection"**
4. Make different facial expressions
5. Watch real-time emotion detection!

### Upload Image
1. Select any mode (Multimodal or Face Only)
2. Click **"Upload Image"**
3. Drag & drop or click to select image
4. Add text (if Multimodal mode)
5. Click **"Predict Emotion"**

### Text Analysis
1. Click **"Text Only"** mode
2. Enter your text
3. Click **"Predict Emotion"**

## 🏗️ Architecture

### CNN Model (Face Recognition)
```
Input (48x48x1) 
→ Block 1: Conv(64) → Conv(64) → BatchNorm → MaxPool → Dropout
→ Block 2: Conv(128) → Conv(128) → BatchNorm → MaxPool → Dropout
→ Block 3: Conv(256) → Conv(256) → BatchNorm → MaxPool → Dropout
→ Block 4: Conv(512) → Conv(512) → BatchNorm → MaxPool → Dropout
→ GlobalAveragePooling → Dense(256) → Dropout → Dense(7) → Softmax
```

### NLP Model (Text Analysis)
```
Text Input 
→ TF-IDF Vectorization (10,000 features, unigrams + bigrams)
→ Logistic Regression
→ Emotion Classification (7 classes)
```

### Q-Learning Fusion Agent
```
State: Confidence levels of face and text predictions
Actions: Trust Face, Trust Text, Average Both
Reward: Based on prediction accuracy
Updates: Q-table with α=0.1, γ=0.9, ε-greedy exploration
```

## 📁 Project Structure

```
Emotion-Detection/
├── app.py                          # Flask application
├── requirements.txt                # Python dependencies
├── config/
│   └── config.py                   # Configuration settings
├── models/
│   ├── face_model.py              # CNN model
│   ├── text_model.py              # NLP model
│   ├── rl_fusion.py               # Q-learning agent
│   └── incremental_learning.py    # Auto-retrain system
├── utils/
│   ├── logger.py                  # Logging system
│   └── data_generator.py          # Synthetic data generation
├── emotion_detection_system/
│   ├── models/                    # Trained model files
│   ├── data/                      # Training datasets
│   ├── logs/                      # System logs
│   └── uploads/                   # Uploaded images
├── templates/
│   └── index.html                 # Web interface
└── static/
    ├── css/
    │   └── style.css              # Styles with gradient theme
    └── js/
        └── app.js                 # Frontend JavaScript
```

## 🎨 Color Scheme

The interface uses a dark multicolor gradient theme:
- 🔴 **Dark Red** (#CC2F2F) - Intensity, determination
- 🟠 **Dark Orange** (#D97326) - Energy, confidence
- 🟡 **Dark Yellow** (#CCA82E) - Optimism, wisdom
- 🟢 **Dark Green** (#4A9B5C) - Stability, growth

## 🔧 Configuration

Edit `config/config.py` to customize:
- Model hyperparameters
- Learning rates
- Batch sizes
- Image dimensions
- Q-learning parameters
- File paths

## 📊 Model Performance

- **Face Model**: Trained on 48x48 grayscale images
- **Text Model**: TF-IDF with 10,000 features
- **Fusion Agent**: Adaptive Q-learning with ε-greedy exploration
- **Real-time**: ~150ms per prediction (face detection + inference)

## 🛠️ Technologies Used

- **Backend**: Python, Flask
- **Deep Learning**: TensorFlow, Keras
- **Computer Vision**: OpenCV, Haar Cascade
- **NLP**: scikit-learn, TF-IDF
- **Reinforcement Learning**: Q-learning (NumPy)
- **Frontend**: HTML5, CSS3, JavaScript
- **UI**: Animated gradients, WebRTC for camera

## 📝 API Endpoints

- `GET /` - Main web interface
- `POST /api/predict/multimodal` - Multimodal prediction (face + text)
- `POST /api/predict/face` - Face-only prediction
- `POST /api/predict/text` - Text-only prediction
- `POST /api/feedback` - Submit feedback for Q-learning
- `GET /api/qtable` - Get current Q-table state
- `GET /api/statistics` - Get session statistics

## 🎯 Future Enhancements

- [ ] Train on FER2013 dataset for better accuracy
- [ ] Add voice emotion detection
- [ ] Multi-language text support
- [ ] Export predictions to CSV
- [ ] User authentication
- [ ] Cloud deployment
- [ ] Mobile app version

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Ishan Sangani**
- GitHub: [@ishansangani14-ias](https://github.com/ishansangani14-ias)

## 🙏 Acknowledgments

- FER2013 dataset for emotion recognition research
- OpenCV for computer vision tools
- TensorFlow team for deep learning framework
- Flask for web framework

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Made with ❤️ and AI** | Real-time emotion detection for everyone!
