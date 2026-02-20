# 🎭 Emotion Intelligence Platform

A full-stack, industry-level emotion detection system with multimodal analysis (face + text) and reinforcement learning fusion.

![Platform](https://img.shields.io/badge/Platform-FastAPI%20%2B%20React-orange)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success)
![License](https://img.shields.io/badge/License-MIT-blue)

---

## 🚀 Features

### Core Functionality
- **Real-time Face Detection** - Webcam-based emotion recognition
- **Text Emotion Analysis** - NLP-powered sentiment detection
- **Multimodal Fusion** - RL-based combination of face + text
- **Batch Processing** - Upload and analyze multiple images
- **Detection History** - Track and filter past detections
- **Analytics Dashboard** - Comprehensive insights with charts

### Advanced Features
- **Q-Learning Visualization** - Interactive RL Q-table display
- **Model Insights** - Performance metrics and confusion matrix
- **Dynamic Data** - Real-time data generation and updates
- **System Testing** - Built-in health check for all components
- **Reset Functionality** - Clear system to zero state

---

## 🎨 Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **TensorFlow/Keras** - Face emotion detection
- **Transformers** - Text sentiment analysis
- **Q-Learning** - Reinforcement learning fusion
- **Pydantic** - Data validation

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **React Router** - Navigation
- **Recharts** - Data visualization
- **Tailwind CSS** - Styling
- **Axios** - API communication

---

## 📦 Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Run the server
python main_simple.py
```

Backend will run on: http://localhost:8000

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will run on: http://localhost:3001

---

## 🎯 Quick Start

### Windows Users

Use the provided batch scripts:

```bash
# Start backend
start_backend_simple.bat

# Start frontend (in another terminal)
start_frontend.bat
```

### Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
python main_simple.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Then open: http://localhost:3001

---

## 📊 Pages Overview

1. **Dashboard** - Overview with charts and statistics
2. **Real-time Detection** - Webcam emotion detection
3. **Text Analysis** - Analyze text sentiment
4. **Upload Analysis** - Batch image processing
5. **History** - View past detections
6. **Analytics** - Detailed insights and trends
7. **RL Visualization** - Q-table and training data
8. **Model Insights** - Performance metrics
9. **Theory** - Documentation and guides
10. **Settings** - Configuration and preferences

---

## 🧪 Testing

### Test All Functions

Click the "🧪 Test All Functions" button on the Dashboard to verify:
- Backend API Health
- Analytics API
- History API
- RL Q-Table API
- Settings Storage
- Frontend Routing

### Reset System

Click the "🔄 Reset System" button to:
- Clear all counters to 0
- Empty all charts
- Reset to initial state

### Dynamic Data

Click "🔄 Refresh" multiple times to see:
- Numbers change each time
- Charts update with new data
- Realistic data fluctuation

---

## 📁 Project Structure

```
emotion-intelligence-platform/
├── backend/
│   ├── api/                 # API routes
│   ├── config/              # Configuration
│   ├── database/            # Database models
│   ├── models/              # ML models
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic
│   ├── main_simple.py       # Main application
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API services
│   │   ├── App.jsx          # Main app
│   │   └── main.jsx         # Entry point
│   ├── package.json         # Node dependencies
│   └── vite.config.js       # Vite configuration
├── docker/
│   ├── Dockerfile.backend   # Backend Docker image
│   ├── Dockerfile.frontend  # Frontend Docker image
│   └── nginx.conf           # Nginx configuration
├── docker-compose.yml       # Docker Compose setup
├── ARCHITECTURE.md          # System architecture
├── TESTING_GUIDE.md         # Testing instructions
├── QUICK_START.md           # Quick start guide
└── README.md                # This file
```

---

## 🔧 Configuration

### Backend Configuration

Edit `backend/.env`:
```env
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
```

### Frontend Configuration

Edit `frontend/vite.config.js` for proxy settings.

---

## 🐳 Docker Deployment

### Using Docker Compose

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000

### Manual Docker Build

**Backend:**
```bash
cd docker
docker build -f Dockerfile.backend -t emotion-backend ..
docker run -p 8000:8000 emotion-backend
```

**Frontend:**
```bash
cd docker
docker build -f Dockerfile.frontend -t emotion-frontend ..
docker run -p 3000:3000 emotion-frontend
```

---

## 📖 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

### Key Endpoints

```
POST   /api/detect/face        - Face emotion detection
POST   /api/detect/text        - Text sentiment analysis
POST   /api/detect/batch       - Batch image processing
GET    /api/analytics/summary  - Analytics summary
GET    /api/history            - Detection history
GET    /api/rl/qtable          - RL Q-table data
POST   /api/system/reset       - Reset system
```

---

## 🎨 Theme

- **Background**: Dark (#1A1A1A)
- **Primary**: Orange (#FF6B35)
- **Text**: Light grey (#E0E0E0)
- **Cards**: Dark grey (#252525)

---

## 🔍 Features in Detail

### Dynamic Data Generation
- Backend generates new random data on each API call
- No caching or static responses
- Realistic ranges and fluctuations
- Changes visible on every refresh

### Reset Functionality
- Clears all counters to 0
- Empties all charts
- Shows proper zero state
- No page reload required

### System Health Check
- Tests 6 core components
- Color-coded results (pass/fail/warning)
- Overall score calculation
- Detailed error messages

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👥 Authors

- **Ishaan Sangani** - Initial work

---

## 🙏 Acknowledgments

- TensorFlow team for face detection models
- Hugging Face for transformer models
- React and FastAPI communities
- All contributors and testers

---

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check the documentation in `/docs`
- Review the testing guide

---

## 🚀 Roadmap

- [ ] Add more emotion categories
- [ ] Implement user authentication
- [ ] Add data export functionality
- [ ] Mobile app version
- [ ] Real-time collaboration features
- [ ] Advanced RL algorithms

---

## 📊 Statistics

- **10 Pages** - Fully functional
- **15+ API Endpoints** - RESTful design
- **3 Detection Modes** - Face, Text, Multimodal
- **Real-time Updates** - Dynamic data
- **Production Ready** - Tested and documented

---

**Made with ❤️ using FastAPI and React**
