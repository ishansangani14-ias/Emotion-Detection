"""
FastAPI main application
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import logging

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.config import settings
from backend.database import init_db
from backend.api import (
    routes_detection,
    routes_analytics,
    routes_rl,
    routes_history
)

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Emotion Intelligence Platform API",
    description="Industry-level multimodal emotion detection with RL fusion",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(routes_detection.router, prefix="/api", tags=["Detection"])
app.include_router(routes_analytics.router, prefix="/api", tags=["Analytics"])
app.include_router(routes_rl.router, prefix="/api", tags=["Reinforcement Learning"])
app.include_router(routes_history.router, prefix="/api", tags=["History"])


@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    logger.info("Starting Emotion Intelligence Platform API...")
    
    # Initialize database
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
    
    logger.info("API ready!")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down Emotion Intelligence Platform API...")


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
        "timestamp": "2026-02-21T00:00:00Z"
    }


# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)


manager = ConnectionManager()


@app.websocket("/ws/realtime-detection")
async def websocket_detection(websocket: WebSocket):
    """
    WebSocket endpoint for real-time emotion detection
    Client sends image frames, server responds with predictions
    """
    await manager.connect(websocket)
    logger.info("WebSocket client connected")
    
    try:
        while True:
            # Receive data from client
            data = await websocket.receive_bytes()
            
            # TODO: Process frame and detect emotion
            # For now, send mock response
            response = {
                "emotion": "happy",
                "confidence": 0.85,
                "timestamp": "2026-02-21T00:00:00Z"
            }
            
            await manager.send_personal_message(response, websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True,
        log_level=settings.LOG_LEVEL.lower()
    )
