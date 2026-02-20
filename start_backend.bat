@echo off
echo Starting Emotion Intelligence Platform Backend...
echo.
set PYTHONPATH=%CD%
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
