# HireKarle Setup Guide

## 🚀 Quick Start (Recommended)

### Using Docker Compose
```bash
# 1. Set your Gemini API key
export GEMINI_API_KEY=your_api_key_here

# 2. Start all services
docker-compose up --build

# 3. Access the app
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

## 📦 Manual Setup

### Prerequisites
- Python 3.9+
- Node.js 16+
- Redis Server
- Gemini API Key

### Backend Setup

```bash
# 1. Navigate to backend
cd backend

# 2. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
cp .env.example .env

# 5. Edit .env and add your Gemini API key
# GEMINI_API_KEY=your_api_key_here

# 6. Start Redis (separate terminal)
redis-server

# 7. Run backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Start development server
npm start

# 4. Open browser
# http://localhost:3000
```

## 🔑 Getting Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key and add to `.env` file

## 🧪 Testing

```bash
# Install test dependencies
pip install requests

# Run tests
python tests/test_full_flow.py
```

## 🐛 Troubleshooting

### Redis Connection Error
```bash
# Check if Redis is running
redis-cli ping
# Should return: PONG

# If not running, start Redis
redis-server
```

### Port Already in Use
```bash
# Backend (8000)
uvicorn app.main:app --reload --port 8001

# Frontend (3000)
PORT=3001 npm start
```

### Module Not Found
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

### CORS Error
Check that `CORS_ORIGINS` in `.env` matches your frontend URL.

## 📊 Project Structure

```
HireKarle/
├── backend/
│   ├── app/
│   │   ├── api/routes.py          # API endpoints
│   │   ├── core/
│   │   │   ├── config.py          # Configuration
│   │   │   └── redis_client.py    # Redis wrapper
│   │   ├── services/
│   │   │   ├── job_scraper.py     # Job fetching
│   │   │   ├── llm_service.py     # Gemini integration
│   │   │   └── matching_service.py # Scoring logic
│   │   ├── utils/
│   │   │   ├── resume_parser.py   # Resume extraction
│   │   │   └── embeddings.py      # Semantic similarity
│   │   └── main.py                # FastAPI app
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ResumeUpload.js
│   │   │   └── JobSearch.js
│   │   ├── services/api.js
│   │   ├── App.js
│   │   └── App.css
│   └── package.json
└── tests/
    ├── test_resume_upload.py
    ├── test_job_search.py
    └── test_full_flow.py
```

## 🎯 Usage Flow

1. **Upload Resume**: User uploads PDF/DOCX/TXT resume
2. **Get Session**: System generates unique session_id (stored in localStorage)
3. **Search Jobs**: User enters job title
4. **AI Matching**: System fetches jobs and scores them using:
   - LLM reasoning (70%)
   - Semantic similarity (20%)
   - Keyword matching (10%)
5. **View Results**: Jobs displayed with scores and rationale
6. **Apply**: Click to open job on original platform

## 🔒 Security Notes

- Resume data auto-expires after 7 days
- No user credentials stored
- Session-based (no login required)
- CORS configured for security
- Redis password recommended for production

## 🚀 Production Deployment

### Environment Variables
```env
GEMINI_API_KEY=your_production_key
REDIS_HOST=your_redis_host
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password
CORS_ORIGINS=https://yourdomain.com
SESSION_TTL=604800
```

### Recommended Stack
- Backend: AWS EC2 / Google Cloud Run
- Redis: AWS ElastiCache / Redis Cloud
- Frontend: Vercel / Netlify
- Domain: Cloudflare

## 📝 Notes

- Job scraping uses placeholder data. Integrate real APIs for production.
- Gemini 2.0 Flash is used for fast, cost-effective scoring.
- Redis TTL automatically cleans up old sessions.
- Frontend uses localStorage for session persistence.
