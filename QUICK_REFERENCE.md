# 🚀 Quick Reference - Emotion Intelligence Platform

## ⚡ Start Commands

### Docker (Recommended)
```bash
docker-compose up -d
```
Access: http://localhost

### Manual Development
```bash
# Terminal 1 - Backend
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload

# Terminal 2 - Frontend  
cd frontend
npm install
npm run dev

# Terminal 3 - Database
docker-compose up -d postgres
```

## 📁 Key Files

### Backend
- `backend/main.py` - FastAPI app
- `backend/requirements.txt` - Dependencies
- `backend/.env.example` - Configuration template

### Frontend
- `frontend/src/App.jsx` - Main React app
- `frontend/package.json` - Dependencies
- `frontend/src/pages/` - 10 pages

### Docker
- `docker-compose.yml` - Orchestration
- `docker/Dockerfile.backend` - Backend image
- `docker/Dockerfile.frontend` - Frontend image

## 🌐 URLs

- Frontend: http://localhost:3000 (dev) or http://localhost (prod)
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs
- Database: localhost:5432

## 📊 Pages

1. `/` - Dashboard
2. `/realtime` - Real-Time Detection
3. `/upload` - Upload Analysis
4. `/text` - Text Analysis
5. `/history` - History
6. `/analytics` - Analytics
7. `/rl-viz` - RL Visualization
8. `/insights` - Model Insights
9. `/theory` - Theory
10. `/settings` - Settings

## 🔧 Common Commands

```bash
# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild
docker-compose up -d --build

# Database shell
docker-compose exec postgres psql -U admin -d emotion_db

# Backend shell
docker-compose exec backend bash

# Check status
docker-compose ps
```

## 📚 Documentation

- `README_V2.md` - Complete documentation
- `DEPLOYMENT_COMPLETE.md` - Deployment guide
- `IMPLEMENTATION_SUMMARY.md` - What was built
- `START_HERE.md` - Quick start guide

## ✅ Checklist

- [ ] Install Docker (or Python 3.9+ & Node 18+)
- [ ] Copy `backend/.env.example` to `backend/.env`
- [ ] Run `docker-compose up -d`
- [ ] Access http://localhost
- [ ] Test real-time detection
- [ ] Check API docs at /api/docs

## 🎯 Features

- ✅ Real-time emoji overlay
- ✅ 10-page dashboard
- ✅ PostgreSQL database
- ✅ Advanced analytics
- ✅ RL visualization
- ✅ Batch processing
- ✅ WebSocket support
- ✅ Docker deployment

## 🆘 Troubleshooting

**Port already in use:**
```bash
# Change ports in docker-compose.yml
ports:
  - "3001:80"  # Frontend
  - "8001:8000"  # Backend
```

**Database connection error:**
```bash
# Wait for database to start
docker-compose logs postgres
# Look for "database system is ready to accept connections"
```

**Frontend can't reach backend:**
```bash
# Check CORS settings in backend/.env
CORS_ORIGINS=http://localhost:3000
```

## 📞 Support

Check logs: `docker-compose logs -f`
Test API: `curl http://localhost:8000/health`
Restart: `docker-compose restart`

---

**Ready to go! 🎭✨**
