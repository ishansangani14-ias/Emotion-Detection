# Technical Requirement Document (TRD)
## Adaptive Multimodal Emotion Detection System

---

### 1. Project Overview
The **Adaptive Multimodal Emotion Detection System** is an advanced AI application designed to detect human emotions using two primary modalities: facial expressions (Vision) and textual utterances (Language). The system uses a Reinforcement Learning (RL) agent to fuse these inputs based on real-time confidence scores, ensuring the most reliable prediction is prioritized.

### 2. Core Features
- **Multimodal Fusion**: Combines CNN-based face detection and NLP-based text analysis.
- **RL-Based Policy**: A Q-Learning agent learns to trust the most accurate modality dynamically.
- **Incremental Learning**: Automatically retrains models as new feedback data is collected without losing old knowledge.
- **Voice Assistant**: Integrated background voice processing (Hindi, Gujarati, English) with real-time translation and emotion fusion.
- **Premium Dashboard**: A state-of-the-art Streamlit interface with high-FPS monitoring and glass-morphism aesthetics.

---

### 3. System Architecture
The system follows a modular architecture:
1.  **Vision Pipeline**: `face_model.py` - VGG-inspired CNN (48x48 greyscale).
2.  **Language Pipeline**: `text_model.py` - TF-IDF Vectorization + Logistic Regression.
3.  **Fusion Pipeline**: `rl_fusion.py` - Q-Learning agent (Bellman equation) for decision making.
4.  **Service Layer**: `voice_service.py`, `logger_service.py` - Handles external interactions and data logging.
5.  **UI Layer**: `app.py` - High-performance Streamlit dashboard.

---

### 4. Technical Specifications
#### 4.1 Vision Model (CNN)
- **Input**: 48x48x1 (Greyscale)
- **Architecture**: 4 blocks (Conv2D -> BatchNormalization -> MaxPool -> Dropout)
- **Framework**: TensorFlow / Keras

#### 4.2 Language Model (NLP)
- **Algorithm**: Logistic Regression (Multinomial)
- **Vectorization**: TF-IDF (Unigrams + Bigrams)
- **Features**: 10,000 max features

#### 4.3 Fusion Model (RL)
- **Algorithm**: Q-Learning
- **State Space**: 4 states (Comparative confidence levels)
- **Action Space**: 3 actions (Trust Face, Trust Text, Average Both)
- **Learning Rate ($\alpha$)**: 0.1
- **Discount Factor ($\gamma$)**: 0.9

---

### 5. Data & Storage
- **Training Data**: Stored in `data/` and `sample_data/`.
- **Feedback Loop**: New user-corrected data is saved in `feedback_data/` for incremental retraining.
- **Logs**: Detailed activity logs stored in `logs/` as CSV and standard log files.

---

### 6. Scalability Roadmap
- **Microservices**: Migrating models to dedicated API endpoints (TensorFlow Serving).
- **Shared State**: Moving the local Q-Table to a Redis-backed cloud store for multi-user sync.
- **Asynchronous Processing**: Implementing Kafka/RabbitMQ for non-blocking retraining cycles.

---

### 7. Installation & Setup
1.  Install dependencies: `pip install -r requirements.txt`
2.  Run the application: `streamlit run app.py`
3.  Configure all paths and thresholds in `config.py`.

---
*Created by Emotion AI Technical Team*
