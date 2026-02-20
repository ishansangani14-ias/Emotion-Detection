"""
Simplified FastAPI main application for testing
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configure logging
logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Emotion Intelligence Platform API",
    description="Industry-level multimodal emotion detection",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    logger.info("Starting Emotion Intelligence Platform API...")
    logger.info("API ready!")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Emotion Intelligence Platform API",
        "version": "2.0.0",
        "docs": "/api/docs",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "API is running"
    }


@app.get("/api/test")
async def test_endpoint():
    """Test endpoint"""
    return {
        "message": "API is working!",
        "endpoints": [
            "/",
            "/health",
            "/api/test",
            "/api/docs"
        ]
    }


# Mock detection endpoints
from fastapi import UploadFile, File, Form
from typing import Optional
import random
from datetime import datetime, timedelta

EMOTIONS = ['happy', 'sad', 'angry', 'surprise', 'fear', 'neutral', 'disgust']


@app.post("/api/detect/face")
async def detect_face(image: UploadFile = File(...)):
    """Mock face detection"""
    emotion = random.choice(EMOTIONS)
    probabilities = {e: random.random() for e in EMOTIONS}
    total = sum(probabilities.values())
    probabilities = {e: p/total for e, p in probabilities.items()}
    
    return {
        "emotion": emotion,
        "confidence": probabilities[emotion],
        "probabilities": probabilities,
        "mode": "face",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/detect/text")
async def detect_text(data: dict):
    """Mock text detection"""
    emotion = random.choice(EMOTIONS)
    probabilities = {e: random.random() for e in EMOTIONS}
    total = sum(probabilities.values())
    probabilities = {e: p/total for e, p in probabilities.items()}
    
    return {
        "emotion": emotion,
        "confidence": probabilities[emotion],
        "probabilities": probabilities,
        "mode": "text",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/detect/batch")
async def detect_batch(images: list[UploadFile] = File(...)):
    """Mock batch detection"""
    results = []
    for _ in images:
        emotion = random.choice(EMOTIONS)
        probabilities = {e: random.random() for e in EMOTIONS}
        total = sum(probabilities.values())
        probabilities = {e: p/total for e, p in probabilities.items()}
        
        results.append({
            "emotion": emotion,
            "confidence": probabilities[emotion],
            "probabilities": probabilities
        })
    
    return {"results": results}


# Analytics endpoints
@app.get("/api/analytics")
async def get_analytics(time_range: str = "7d"):
    """Mock analytics data"""
    days = 7 if time_range == "7d" else 30 if time_range == "30d" else 1 if time_range == "24h" else 90
    
    # Use list() to avoid shadowing range()
    day_list = list(range(days-1, -1, -1))
    
    return {
        "total_detections": random.randint(100, 1000),
        "avg_accuracy": random.uniform(0.6, 0.8),
        "avg_confidence": random.uniform(0.65, 0.85),
        "most_common_emotion": random.choice(EMOTIONS),
        "emotion_distribution": [
            {"emotion": e, "count": random.randint(10, 100)} for e in EMOTIONS
        ],
        "accuracy_trend": [
            {"date": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"), 
             "accuracy": random.uniform(0.6, 0.8)}
            for i in day_list
        ],
        "confidence_trend": [
            {"date": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"),
             "avg_confidence": random.uniform(0.65, 0.85)}
            for i in day_list
        ],
        "detections_per_day": [
            {"date": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"),
             "count": random.randint(10, 50)}
            for i in day_list
        ],
        "mode_breakdown": [
            {"mode": "face", "count": random.randint(50, 200)},
            {"mode": "text", "count": random.randint(30, 150)},
            {"mode": "multimodal", "count": random.randint(20, 100)}
        ]
    }


@app.get("/api/analytics/summary")
async def get_analytics_summary():
    """Mock analytics summary for dashboard - DYNAMIC DATA"""
    # Generate random but realistic data that changes each time
    total = random.randint(50, 1000)
    emotion_dist = []
    
    # Generate emotion distribution with random percentages
    for emotion in EMOTIONS:
        count = random.randint(5, 150)
        emotion_dist.append({
            "emotion": emotion,
            "count": count
        })
    
    # Calculate percentages
    total_count = sum(d["count"] for d in emotion_dist)
    for d in emotion_dist:
        d["percentage"] = round((d["count"] / total_count) * 100, 1)
    
    # Generate dynamic accuracy trend (fluctuates)
    accuracy_trend = []
    base_accuracy = random.uniform(55, 75)
    for i in range(6, -1, -1):
        # Add random fluctuation
        fluctuation = random.uniform(-10, 10)
        accuracy = max(40, min(95, base_accuracy + fluctuation))
        accuracy_trend.append({
            "date": (datetime.now() - timedelta(days=i)).strftime("%m/%d"),
            "accuracy": round(accuracy, 1)
        })
    
    # Generate dynamic detections per day
    detections_per_day = []
    for i in range(6, -1, -1):
        day_total = random.randint(5, 50)
        face = random.randint(1, day_total - 2)
        text = random.randint(1, day_total - face - 1)
        multi = day_total - face - text
        
        detections_per_day.append({
            "date": (datetime.now() - timedelta(days=i)).strftime("%m/%d"),
            "count": day_total,
            "face_only": face,
            "text_only": text,
            "multimodal": multi
        })
    
    return {
        "total_detections": total,
        "overall_accuracy": random.randint(55, 85),
        "avg_confidence": random.uniform(0.65, 0.85),
        "most_common_emotion": max(emotion_dist, key=lambda x: x["count"])["emotion"],
        "emotion_distribution": emotion_dist,
        "recent_detections": [
            {
                "id": i,
                "timestamp": (datetime.now() - timedelta(minutes=i*5)).isoformat(),
                "emotion": random.choice(EMOTIONS),
                "confidence": random.uniform(0.5, 0.95),
                "mode": random.choice(["face", "text", "multimodal"])
            }
            for i in range(10)
        ],
        "accuracy_trend": accuracy_trend,
        "detections_per_day": detections_per_day
    }


# History endpoints
@app.get("/api/history")
async def get_history(skip: int = 0, limit: int = 50):
    """Mock history data"""
    history = []
    for i in range(limit):
        emotion = random.choice(EMOTIONS)
        mode = random.choice(["face", "text", "multimodal"])
        
        item = {
            "id": i + skip,
            "timestamp": (datetime.now() - timedelta(minutes=i*5)).isoformat(),
            "emotion": emotion,
            "confidence": random.uniform(0.5, 0.95),
            "mode": mode,
            "correct": random.choice([True, False, None])
        }
        
        # Add multimodal details
        if mode == "multimodal":
            item["face_emotion"] = random.choice(EMOTIONS)
            item["face_confidence"] = random.uniform(0.5, 0.95)
            item["text_emotion"] = random.choice(EMOTIONS)
            item["text_confidence"] = random.uniform(0.5, 0.95)
        
        history.append(item)
    
    return history


@app.delete("/api/history/clear")
async def clear_history():
    """Clear all detection history"""
    # In production, this would delete from database
    logger.info("History cleared (mock operation)")
    return {
        "status": "success",
        "message": "All detection history has been cleared",
        "deleted_count": random.randint(100, 500)
    }


@app.post("/api/system/reset")
async def reset_system():
    """Reset entire system to zero state"""
    logger.info("System reset to zero state")
    return {
        "status": "success",
        "message": "System reset complete",
        "data": {
            "total_detections": 0,
            "overall_accuracy": 0,
            "emotion_distribution": [],
            "accuracy_trend": [],
            "detections_per_day": [],
            "recent_detections": []
        }
    }


# RL endpoints
@app.get("/api/rl/qtable")
async def get_qtable():
    """Mock Q-table data"""
    states = ["high-high", "high-low", "low-high", "low-low"]
    actions = ["trust_face", "trust_text", "average"]
    
    # Generate Q-table as 2D array
    qtable_2d = []
    qtable_dict = {}
    best_actions = []
    
    for state in states:
        state_values = [random.uniform(-1, 1) for _ in actions]
        qtable_2d.append(state_values)
        qtable_dict[state] = {action: val for action, val in zip(actions, state_values)}
        best_actions.append(actions[state_values.index(max(state_values))])
    
    return {
        "qtable": qtable_2d,
        "qtable_dict": qtable_dict,
        "states": states,
        "actions": actions,
        "best_actions": best_actions,
        "epsilon": random.uniform(0.1, 0.5),
        "episodes": random.randint(100, 1000)
    }


@app.get("/api/rl/training-history")
async def get_training_history(limit: int = 100):
    """Mock RL training history"""
    history = []
    for i in range(limit):
        history.append({
            "episode": i,
            "state": random.choice(["high-high", "high-low", "low-high", "low-low"]),
            "action": random.choice(["trust_face", "trust_text", "average"]),
            "reward": random.choice([1, -1]),
            "timestamp": (datetime.now() - timedelta(minutes=i)).isoformat()
        })
    
    return {"history": history}


@app.get("/api/rl/reward-trend")
async def get_reward_trend(episodes: int = 50):
    """Mock reward trend"""
    trend = []
    cumulative = 0
    for i in range(episodes):
        reward = random.choice([1, -1])
        cumulative += reward
        trend.append({
            "episode": i,
            "reward": reward,
            "cumulative_reward": cumulative
        })
    
    return {"trend": trend}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main_simple:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
