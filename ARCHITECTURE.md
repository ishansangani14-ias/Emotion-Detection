# System Architecture

## Adaptive Multimodal Emotion Detection System

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                    (Web Browser - Port 5000)                    │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │  Multimodal  │  │  Face Only   │  │  Text Only   │        │
│  │     Mode     │  │     Mode     │  │     Mode     │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  Image Upload  │  Text Input  │  Predict Button        │  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FLASK WEB SERVER                           │
│                         (app.py)                                │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                    REST API Endpoints                     │ │
│  │  /api/predict/multimodal  │  /api/predict/face           │ │
│  │  /api/predict/text        │  /api/feedback               │ │
│  │  /api/qtable              │  /api/statistics             │ │
│  └──────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      PROCESSING LAYER                           │
│                                                                 │
│  ┌──────────────────┐         ┌──────────────────┐            │
│  │  Vision Pipeline │         │ Language Pipeline │            │
│  │                  │         │                   │            │
│  │  ┌────────────┐ │         │  ┌────────────┐  │            │
│  │  │ Preprocess │ │         │  │ Preprocess │  │            │
│  │  │ 48x48 Grey │ │         │  │   TF-IDF   │  │            │
│  │  └────────────┘ │         │  └────────────┘  │            │
│  │        ▼         │         │        ▼         │            │
│  │  ┌────────────┐ │         │  ┌────────────┐  │            │
│  │  │    CNN     │ │         │  │  Logistic  │  │            │
│  │  │  4-block   │ │         │  │ Regression │  │            │
│  │  │    VGG     │ │         │  │            │  │            │
│  │  └────────────┘ │         │  └────────────┘  │            │
│  │        ▼         │         │        ▼         │            │
│  │  ┌────────────┐ │         │  ┌────────────┐  │            │
│  │  │ Emotion +  │ │         │  │ Emotion +  │  │            │
│  │  │Confidence  │ │         │  │Confidence  │  │            │
│  │  └────────────┘ │         │  └────────────┘  │            │
│  └──────────────────┘         └──────────────────┘            │
│           │                            │                       │
│           └────────────┬───────────────┘                       │
│                        ▼                                       │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │              Q-LEARNING FUSION AGENT                    │  │
│  │                                                         │  │
│  │  ┌──────────────────────────────────────────────────┐ │  │
│  │  │  State Determination (4 states)                  │ │  │
│  │  │  - Both High (≥0.7)                              │ │  │
│  │  │  - Face High, Text Low                           │ │  │
│  │  │  - Face Low, Text High                           │ │  │
│  │  │  - Both Low (<0.7)                               │ │  │
│  │  └──────────────────────────────────────────────────┘ │  │
│  │                        ▼                               │  │
│  │  ┌──────────────────────────────────────────────────┐ │  │
│  │  │  Action Selection (ε-greedy)                     │ │  │
│  │  │  - FACE: Use face prediction                     │ │  │
│  │  │  - TEXT: Use text prediction                     │ │  │
│  │  │  - AVERAGE: Average both predictions             │ │  │
│  │  └──────────────────────────────────────────────────┘ │  │
│  │                        ▼                               │  │
│  │  ┌──────────────────────────────────────────────────┐ │  │
│  │  │  Q-Table (4×3 matrix)                            │ │  │
│  │  │  Updated via Bellman equation                    │ │  │
│  │  │  Q(s,a) ← Q(s,a) + α[r + γmax Q(s',a') - Q(s,a)]│ │  │
│  │  └──────────────────────────────────────────────────┘ │  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   INCREMENTAL LEARNING LAYER                    │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  User Feedback → Image Storage → Statistics Update       │ │
│  └──────────────────────────────────────────────────────────┘ │
│                              │                                  │
│                              ▼                                  │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  Check Retrain Trigger (50 images per emotion)           │ │
│  └──────────────────────────────────────────────────────────┘ │
│                              │                                  │
│                              ▼                                  │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  Auto-Retrain with Weight Transfer                       │ │
│  │  1. Load accumulated images                              │ │
│  │  2. Create new model                                     │ │
│  │  3. Transfer old weights                                 │ │
│  │  4. Train with lower learning rate                       │ │
│  │  5. Update active model                                  │ │
│  └──────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      PERSISTENCE LAYER                          │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │  CNN Model   │  │  NLP Model   │  │   Q-Table    │        │
│  │   (.h5)      │  │   (.pkl)     │  │   (.npy)     │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │  Face Data   │  │  Text Data   │  │  Logs        │        │
│  │  (images)    │  │   (.csv)     │  │  (.log)      │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### 1. Multimodal Prediction Flow

```
User Input (Image + Text)
    │
    ├─► Image → Preprocess → CNN → Face Emotion + Confidence
    │                                      │
    └─► Text → Preprocess → TF-IDF → LR → Text Emotion + Confidence
                                           │
                                           ▼
                        ┌──────────────────────────────────┐
                        │  Determine State                 │
                        │  (based on both confidences)     │
                        └──────────────────────────────────┘
                                           │
                                           ▼
                        ┌──────────────────────────────────┐
                        │  Select Action (ε-greedy)        │
                        │  - Explore: Random               │
                        │  - Exploit: Best Q-value         │
                        └──────────────────────────────────┘
                                           │
                                           ▼
                        ┌──────────────────────────────────┐
                        │  Fuse Predictions                │
                        │  - FACE: Use face prediction     │
                        │  - TEXT: Use text prediction     │
                        │  - AVERAGE: (face + text) / 2    │
                        └──────────────────────────────────┘
                                           │
                                           ▼
                                  Final Prediction
                                           │
                                           ▼
                                    Display Results
```

### 2. Feedback Loop

```
User Provides Feedback
    │
    ├─► Correct? → Reward = +1.0
    │
    └─► Incorrect? → Reward = -1.0
                │
                ▼
    ┌──────────────────────────────────┐
    │  Update Q-Table                  │
    │  Q(s,a) ← Q(s,a) + α[TD_error]  │
    │  TD_error = r + γmax Q(s',a') - Q(s,a) │
    └──────────────────────────────────┘
                │
                ▼
    ┌──────────────────────────────────┐
    │  Decay Epsilon                   │
    │  ε ← max(ε_min, ε × decay)      │
    └──────────────────────────────────┘
                │
                ▼
    ┌──────────────────────────────────┐
    │  Save Q-Table to Disk            │
    └──────────────────────────────────┘
                │
                ▼
    ┌──────────────────────────────────┐
    │  Store Image (if provided)       │
    └──────────────────────────────────┘
                │
                ▼
    ┌──────────────────────────────────┐
    │  Check Retrain Trigger           │
    │  (50 images per emotion)         │
    └──────────────────────────────────┘
                │
                ▼
         Auto-Retrain (if triggered)
```

---

## Component Interactions

```
┌─────────────┐
│   Config    │◄──────────────────────────────────┐
└─────────────┘                                    │
       │                                           │
       │ provides parameters                       │
       ▼                                           │
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Face Model  │     │ Text Model  │     │ RL Fusion   │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                     │
       │                   │                     │
       └───────────────────┴─────────────────────┘
                           │
                           │ uses
                           ▼
                  ┌─────────────────┐
                  │ Incremental     │
                  │ Learner         │
                  └─────────────────┘
                           │
                           │ triggers
                           ▼
                  ┌─────────────────┐
                  │ Auto-Retrain    │
                  └─────────────────┘
                           │
                           │ logs to
                           ▼
                  ┌─────────────────┐
                  │ System Logger   │
                  └─────────────────┘
```

---

## File System Structure

```
emotion_detection_system/
├── data/
│   ├── face_dataset/
│   │   ├── angry/
│   │   ├── disgust/
│   │   ├── fear/
│   │   ├── happy/
│   │   ├── neutral/
│   │   ├── sad/
│   │   └── surprise/
│   ├── text_dataset/
│   │   └── text_emotions.csv
│   └── incremental/
│       ├── angry/
│       ├── disgust/
│       ├── fear/
│       ├── happy/
│       ├── neutral/
│       ├── sad/
│       └── surprise/
├── models/
│   ├── cnn_model.h5
│   ├── tfidf_vectorizer.pkl
│   ├── lr_model.pkl
│   └── q_table.npy
├── logs/
│   └── system.log
└── uploads/
    └── [temporary uploaded files]
```

---

## Technology Stack

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND                             │
│  HTML5 │ CSS3 │ JavaScript │ Fetch API                 │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                    BACKEND                              │
│  Flask │ Flask-CORS │ Werkzeug                         │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                 MACHINE LEARNING                        │
│  TensorFlow/Keras │ scikit-learn │ OpenCV             │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                  DATA PROCESSING                        │
│  NumPy │ Pandas │ Joblib                               │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                   PERSISTENCE                           │
│  File System │ HDF5 │ Pickle │ NumPy Binary           │
└─────────────────────────────────────────────────────────┘
```

---

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    CLIENT BROWSER                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │   HTML   │  │   CSS    │  │    JS    │            │
│  └──────────┘  └──────────┘  └──────────┘            │
└─────────────────────────────────────────────────────────┘
                        │
                        │ HTTP/HTTPS
                        ▼
┌─────────────────────────────────────────────────────────┐
│                  FLASK SERVER                           │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Werkzeug WSGI Server (Development)              │  │
│  │  or                                               │  │
│  │  Gunicorn/uWSGI (Production)                     │  │
│  └──────────────────────────────────────────────────┘  │
│                        │                                │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Application Logic (app.py)                      │  │
│  └──────────────────────────────────────────────────┘  │
│                        │                                │
│  ┌──────────────────────────────────────────────────┐  │
│  │  ML Models (in-memory)                           │  │
│  │  - CNN Model                                     │  │
│  │  - Text Model                                    │  │
│  │  - Q-Learning Agent                              │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                        │
                        │ File I/O
                        ▼
┌─────────────────────────────────────────────────────────┐
│                  FILE SYSTEM                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │  Models  │  │   Data   │  │   Logs   │            │
│  └──────────┘  └──────────┘  └──────────┘            │
└─────────────────────────────────────────────────────────┘
```

---

This architecture provides a complete, modular, and scalable system for multimodal emotion detection with reinforcement learning-based fusion and incremental learning capabilities.
