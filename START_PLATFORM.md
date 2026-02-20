# 🚀 How to Start the Platform

## ✅ Setup Complete!

Everything is installed and ready to run!

---

## 🎯 Quick Start (3 Steps)

### Step 1: Database is Already Running ✅
PostgreSQL is running in Docker

### Step 2: Start Backend
Open a **new terminal** and run:
```bash
start_backend.bat
```
Or manually:
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Wait for: `Application startup complete`

### Step 3: Start Frontend
Open **another new terminal** and run:
```bash
start_frontend.bat
```
Or manually:
```bash
cd frontend
npm run dev
```

---

## 🌐 Access the Platform

Once both are running:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs

---

## 📊 What You'll See

1. **Dashboard** - Overview with stats
2. **Real-Time Detection** - Live camera with emoji overlay
3. **Upload Analysis** - Batch image processing
4. **Text Analysis** - Text emotion detection
5. **History** - All past detections
6. **Analytics** - Charts and visualizations
7. **RL Visualization** - Q-learning insights
8. **Model Insights** - Explainable AI
9. **Theory** - Documentation
10. **Settings** - Configuration

---

## 🛑 To Stop

Press `Ctrl+C` in each terminal window

---

## 🔧 Troubleshooting

### Backend won't start?
```bash
# Check if port 8000 is free
netstat -ano | findstr :8000

# If occupied, kill the process or change port
```

### Frontend won't start?
```bash
# Check if port 3000 is free
netstat -ano | findstr :3000

# If occupied, it will ask to use port 3001
```

### Database connection error?
```bash
# Check if PostgreSQL is running
docker ps

# If not, start it:
docker-compose up -d postgres
```

---

## ✨ You're All Set!

Just run the two batch files in separate terminals and access http://localhost:3000

**Enjoy your Emotion Intelligence Platform!** 🎭✨
