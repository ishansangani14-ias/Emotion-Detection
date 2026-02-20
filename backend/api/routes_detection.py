"""
Detection API routes
"""
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os
import uuid
from datetime import datetime

from backend.database import get_db
from backend.schemas import (
    DetectionResponse, TextDetectionRequest,
    FeedbackRequest, FeedbackResponse, BatchDetectionResponse
)
from backend.services import detection_service
from backend.config import settings

router = APIRouter()


@router.post("/detect/face", response_model=DetectionResponse)
async def detect_face(
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Detect emotion from face image
    
    - **image**: Image file (PNG, JPG, JPEG, BMP)
    - Returns emotion, confidence, and probabilities
    """
    # Validate file type
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Save uploaded file
    file_ext = os.path.splitext(image.filename)[1]
    filename = f"{uuid.uuid4()}{file_ext}"
    filepath = os.path.join(settings.UPLOAD_DIR, filename)
    
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    with open(filepath, "wb") as f:
        content = await image.read()
        f.write(content)
    
    try:
        # Detect emotion
        result, detection = await detection_service.detect_face(filepath, db)
        return DetectionResponse(**result)
    except Exception as e:
        # Clean up file on error
        if os.path.exists(filepath):
            os.remove(filepath)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/detect/text", response_model=DetectionResponse)
async def detect_text(
    request: TextDetectionRequest,
    db: Session = Depends(get_db)
):
    """
    Detect emotion from text
    
    - **text**: Input text string
    - Returns emotion, confidence, and probabilities
    """
    try:
        result, detection = await detection_service.detect_text(request.text, db)
        return DetectionResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/detect/multimodal", response_model=DetectionResponse)
async def detect_multimodal(
    image: UploadFile = File(...),
    text: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Detect emotion using multimodal fusion (face + text)
    
    - **image**: Image file
    - **text**: Input text
    - Returns fused emotion with RL details
    """
    # Validate file type
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Save uploaded file
    file_ext = os.path.splitext(image.filename)[1]
    filename = f"{uuid.uuid4()}{file_ext}"
    filepath = os.path.join(settings.UPLOAD_DIR, filename)
    
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    with open(filepath, "wb") as f:
        content = await image.read()
        f.write(content)
    
    try:
        # Detect emotion
        result, detection = await detection_service.detect_multimodal(
            filepath, text, db
        )
        return DetectionResponse(**result)
    except Exception as e:
        # Clean up file on error
        if os.path.exists(filepath):
            os.remove(filepath)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/detect/batch", response_model=BatchDetectionResponse)
async def detect_batch(
    images: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """
    Batch detect emotions from multiple images
    
    - **images**: List of image files
    - Returns list of detection results
    """
    results = []
    errors = []
    processed = 0
    
    for image in images:
        try:
            # Validate file type
            if not image.content_type.startswith("image/"):
                errors.append(f"{image.filename}: Not an image file")
                continue
            
            # Save uploaded file
            file_ext = os.path.splitext(image.filename)[1]
            filename = f"{uuid.uuid4()}{file_ext}"
            filepath = os.path.join(settings.UPLOAD_DIR, filename)
            
            os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
            
            with open(filepath, "wb") as f:
                content = await image.read()
                f.write(content)
            
            # Detect emotion
            result, detection = await detection_service.detect_face(filepath, db)
            results.append(DetectionResponse(**result))
            processed += 1
            
        except Exception as e:
            errors.append(f"{image.filename}: {str(e)}")
    
    return BatchDetectionResponse(
        total=len(images),
        processed=processed,
        results=results,
        errors=errors
    )
