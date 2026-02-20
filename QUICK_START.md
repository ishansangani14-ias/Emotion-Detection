# 🚀 Quick Start Guide

## Adaptive Multimodal Emotion Detection System

### 1️⃣ Installation (One-Time Setup)

```bash
# Install Python dependencies
pip install -r requirements.txt
```

**Required**: Python 3.9, 3.10, or 3.11

---

### 2️⃣ Run the Application

```bash
# Simple method
python run.py

# Or directly
python app.py
```

**First run will take 5-10 minutes** to generate data and train models.

---

### 3️⃣ Access the Web Interface

Open your browser and go to:
```
http://localhost:5000
```

---

### 4️⃣ Using the System

#### **Multimodal Mode** (Recommended)
1. Click "Multimodal" button
2. Upload a facial image (click or drag)
3. Enter text in the text box
4. Click "Predict Emotion"
5. View fusion results with Q-learning decision

#### **Face Only Mode**
1. Click "Face Only" button
2. Upload a facial image
3. Click "Predict Emotion"
4. View CNN prediction results

#### **Text Only Mode**
1. Click "Text Only" button
2. Enter text in the text box
3. Click "Predict Emotion"
4. View NLP prediction results

---

### 5️⃣ Providing Feedback

After each prediction:
1. Click "Yes" if prediction is correct
2. Click "No" if incorrect, then select correct emotion
3. System updates Q-table automatically
4. Watch Q-table values change in real-time!

---

### 6️⃣ Understanding the Interface

#### **Top Stats**
- **Predictions**: Total number of predictions made
- **Accuracy**: Percentage of correct predictions

#### **Q-Learning Agent Panel**
- Shows the Q-table (4 states × 3 actions)
- **Epsilon**: Exploration rate (decreases over time)
- **Episodes**: Number of feedback updates
- **Best Action**: Optimal action for each state

#### **Session Statistics**
- **Face Only**: Count of face-only predictions
- **Text Only**: Count of text-only predictions
- **Fusion**: Count of multimodal predictions
- **Correct**: Count of correct predictions

---

### 7️⃣ Supported Emotions

The system recognizes 7 emotions:
- 😠 Angry
- 🤢 Disgust
- 😨 Fear
- 😊 Happy
- 😐 Neutral
- 😢 Sad
- 😲 Surprise

---

### 8️⃣ File Formats

**Images**: PNG, JPG, JPEG, BMP (max 16MB)

**Text**: Any text input (English recommended)

---

### 9️⃣ Troubleshooting

#### **Port 5000 already in use**
```bash
# Change port in config/config.py
FLASK_PORT = 5001  # Or any available port
```

#### **Missing dependencies**
```bash
pip install -r requirements.txt --upgrade
```

#### **Models not loading**
Delete the `emotion_detection_system/` folder and restart. The system will retrain automatically.

#### **Slow predictions**
First predictions are slower due to model initialization. Subsequent predictions are faster.

---

### 🔟 Tips for Best Results

1. **Images**: Use clear, well-lit facial images
2. **Text**: Write complete sentences expressing emotions
3. **Feedback**: Provide feedback to improve Q-learning
4. **Multimodal**: Use both image and text for best accuracy
5. **Patience**: First run takes time to train models

---

### 📊 What Happens Behind the Scenes

#### **First Run**
1. Creates directory structure
2. Generates 560 synthetic face images (80 per emotion)
3. Generates 1,050 synthetic text samples (150 per emotion)
4. Trains CNN model (30 epochs with early stopping)
5. Trains text model (TF-IDF + Logistic Regression)
6. Initializes Q-table (all zeros)
7. Starts Flask server

#### **Subsequent Runs**
1. Loads saved models from disk
2. Loads Q-table with learned values
3. Starts Flask server immediately

#### **During Prediction**
1. Preprocesses input (image resize, text cleaning)
2. Runs through respective models
3. Fusion agent determines state from confidences
4. Selects action using epsilon-greedy policy
5. Returns final prediction with probabilities

#### **After Feedback**
1. Computes reward (+1 correct, -1 incorrect)
2. Updates Q-table using Bellman equation
3. Saves Q-table to disk
4. Decays epsilon (less exploration over time)

---

### 🎨 Color Scheme

The interface uses a professional color palette:
- **Orange** (#FF6B35): Primary actions, highlights
- **Dark Grey** (#2C2C2C): Cards, surfaces
- **Black** (#1A1A1A): Background
- **Light Grey** (#E0E0E0): Text
- **Medium Grey** (#4A4A4A): Borders

---

### 📝 Logs

System logs are saved to:
```
emotion_detection_system/logs/system.log
```

View logs for:
- Prediction details
- Q-table updates
- Training events
- Errors and warnings

---

### 🛑 Stopping the Server

Press `Ctrl+C` in the terminal to stop the Flask server gracefully.

---

### ✅ System Requirements

- **OS**: Windows, macOS, Linux
- **Python**: 3.9, 3.10, or 3.11
- **RAM**: 4GB minimum (8GB recommended)
- **Disk**: 2GB free space
- **CPU**: Any modern CPU (GPU optional, speeds up training)

---

### 🎯 Ready to Start!

```bash
python run.py
```

Then open: **http://localhost:5000**

Enjoy exploring multimodal emotion detection with reinforcement learning! 🎭
