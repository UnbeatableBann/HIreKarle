# 💼 HireKarle — AI-Powered Job Matcher

> **"Where your resume meets reality — AI-style."**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2.0-blue.svg)](https://reactjs.org/)
[![Redis](https://img.shields.io/badge/Redis-5.0.1-red.svg)](https://redis.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**HireKarle** is an intelligent, AI-powered job matching platform that automatically fetches jobs from multiple sources, analyzes them against your resume, and ranks them using advanced machine learning. No login required, no hassle — just upload and discover your perfect job match.

---

## ✨ Key Features

🎯 **AI-Powered Matching** - Uses Gemini 2.0 Flash for intelligent job-resume analysis
🔍 **Multi-Source Aggregation** - Fetches from LinkedIn, Indeed, Naukri, Internshala
📊 **Smart Scoring** - Combines LLM reasoning, semantic similarity, and heuristics
🚀 **No Login Required** - Session-based architecture for instant access
⏰ **Auto-Cleanup** - 7-day TTL with Redis for privacy
💡 **Explainable AI** - Get clear rationale for each job match
🎨 **Beautiful UI** - Modern, responsive design with gradient theme
🐳 **Docker Ready** - One-command deployment

---

## 🚀 Quick Start (5 Minutes)

### Option 1: Docker (Recommended)
```bash
export GEMINI_API_KEY=your_api_key_here
docker-compose up --build
# Open http://localhost:3000
```

### Option 2: Manual Setup

**1. Prerequisites**
- Python 3.9+
- Node.js 16+
- Redis Server
- [Gemini API Key](https://makersuite.google.com/app/apikey)

**2. Backend**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
cp .env.example .env
# Add GEMINI_API_KEY to .env
uvicorn app.main:app --reload
```

**3. Frontend**
```bash
cd frontend
npm install
npm start
```

**4. Redis**
```bash
redis-server
```

**5. Open Browser**
```
http://localhost:3000
```

📖 **Detailed Setup**: See [QUICKSTART.md](QUICKSTART.md) or [SETUP.md](SETUP.md)

---

## 🏗️ Architecture

```
┌─────────────────┐
│  React Frontend │  (Port 3000)
│  + Tailwind CSS │
└────────┬────────┘
         │ REST API
         ↓
┌─────────────────┐
│  FastAPI Backend│  (Port 8000)
│  + Uvicorn      │
└────────┬────────┘
         │
    ┌────┴────┬──────────┬─────────────┐
    ↓         ↓          ↓             ↓
┌──────┐  ┌──────┐  ┌────────┐  ┌──────────┐
│Redis │  │Gemini│  │Sentence│  │Job APIs  │
│Cache │  │ API  │  │Transform│  │(Multi)   │
└──────┘  └──────┘  └────────┘  └──────────┘
```

**Scoring Algorithm:**
```
Final Score = 0.7 × LLM + 0.2 × Semantic + 0.1 × Heuristic
```

---

## 📁 Project Structure
```
HireKarle/
├── backend/
│   ├── app/
│   │   ├── api/routes.py           # REST endpoints
│   │   ├── core/
│   │   │   ├── config.py           # Settings
│   │   │   └── redis_client.py     # Redis wrapper
│   │   ├── services/
│   │   │   ├── job_scraper.py      # Job fetching
│   │   │   ├── llm_service.py      # Gemini integration
│   │   │   └── matching_service.py # Scoring engine
│   │   ├── utils/
│   │   │   ├── resume_parser.py    # PDF/DOCX parser
│   │   │   └── embeddings.py       # Semantic similarity
│   │   └── main.py                 # FastAPI app
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ResumeUpload.js
│   │   │   └── JobSearch.js
│   │   ├── services/api.js
│   │   ├── App.js
│   │   └── App.css
│   ├── package.json
│   └── Dockerfile
├── tests/
│   ├── test_full_flow.py           # Integration test
│   ├── check_services.py           # Health check
│   └── sample_resume.txt           # Test data
├── docker-compose.yml
├── README.md                       # This file
├── QUICKSTART.md                   # 5-min setup
├── SETUP.md                        # Detailed setup
├── API_DOCS.md                     # API reference
├── DEPLOYMENT.md                   # Production guide
└── PROJECT_SUMMARY.md              # Architecture deep-dive
```

---

## 🎯 How It Works

### 1️⃣ Upload Resume
```
User uploads PDF/DOCX/TXT → Parse text → Generate embedding
→ Create session → Store in Redis (7 days) → Return session_id
```

### 2️⃣ Search Jobs
```
User enters job title → Fetch from multiple sources
→ Generate job embeddings → Calculate scores
→ Rank by AI analysis → Return top matches
```

### 3️⃣ View Results
```
Display jobs with:
- Compatibility score (0-100)
- AI-generated rationale
- Direct apply links
- Color-coded badges
```

---

## 🧪 Testing

```bash
# Check all services
python tests/check_services.py

# Test full workflow
python tests/test_full_flow.py

# Test individual components
python tests/test_resume_upload.py
python tests/test_job_search.py
```

**Manual UI Testing:**
1. Upload `tests/sample_resume.txt`
2. Search for "Software Engineer"
3. Verify scores and results
4. Test apply links
5. Refresh page (session persists)

---

## 🔒 Environment Variables

Create `backend/.env`:
```env
GEMINI_API_KEY=your_api_key_here
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
SESSION_TTL=604800
CORS_ORIGINS=http://localhost:3000
```

**Get Gemini API Key**: https://makersuite.google.com/app/apikey

---

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/upload-resume` | Upload resume, get session_id |
| POST | `/api/search-jobs` | Search jobs with session_id |
| GET | `/health` | Health check |

📖 **Full API Docs**: [API_DOCS.md](API_DOCS.md)

---

## 🚀 Deployment

### Quick Deploy Options
- **AWS**: EC2 + ElastiCache + S3 (~$50/month)
- **GCP**: Cloud Run + Memorystore (~$50/month)
- **VPS**: DigitalOcean + Docker (~$12/month)
- **Hybrid**: Vercel (Frontend) + Railway (Backend)

📖 **Deployment Guide**: [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 🛠️ Tech Stack

**Backend:**
- FastAPI 0.109.0
- Python 3.9+
- Redis 5.0.1
- Google Gemini 2.0 Flash
- Sentence Transformers
- PyPDF2, python-docx

**Frontend:**
- React 18.2.0
- Axios 1.6.5
- Custom CSS

**Infrastructure:**
- Docker + Docker Compose
- Uvicorn (ASGI)
- Nginx (production)

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [QUICKSTART.md](QUICKSTART.md) | Get running in 5 minutes |
| [SETUP.md](SETUP.md) | Detailed installation guide |
| [API_DOCS.md](API_DOCS.md) | Complete API reference |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Production deployment |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Architecture & design |
| [FEATURES.md](FEATURES.md) | Feature list & roadmap |
| [tests/README.md](tests/README.md) | Testing guide |

---

## 🎨 Screenshots

**Upload Resume:**
```
┌─────────────────────────────────┐
│     💼 HireKarle                │
│  AI-Powered Job Matcher         │
│                                 │
│  Upload Your Resume             │
│  Supported: PDF, DOCX, TXT      │
│                                 │
│  [Choose File] [Upload Resume]  │
└─────────────────────────────────┘
```

**Job Results:**
```
┌─────────────────────────────────┐
│  Senior Software Engineer  [95%]│
│  Tech Corp                      │
│  San Francisco, CA              │
│  Source: LinkedIn               │
│  "Strong match in Python..."    │
│  [Apply Now →]                  │
└─────────────────────────────────┘
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

---

## 📄 License

MIT License - Free to use and modify

---

## 🎯 Roadmap

- [x] MVP with AI matching
- [x] Multi-source job aggregation
- [x] Docker deployment
- [ ] Real job API integrations
- [ ] Advanced filters
- [ ] User accounts (optional)
- [ ] Email alerts
- [ ] Mobile app

📖 **Full Roadmap**: [FEATURES.md](FEATURES.md)

---

## 🏆 Why HireKarle?

✅ **No Login Friction** - Start immediately
✅ **AI-Powered** - Smart, explainable matching
✅ **Privacy-First** - Auto-delete after 7 days
✅ **Production-Ready** - Error handling, Docker, docs
✅ **Open Source** - Free to use and modify
✅ **Well-Documented** - Comprehensive guides
✅ **Scalable** - Redis-based, stateless design

---

## 📞 Support

- 📖 **Documentation**: Check guides above
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/hirekarle/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/hirekarle/discussions)

---

## 🙏 Acknowledgments

- Google Gemini for AI capabilities
- Sentence Transformers for embeddings
- FastAPI for the amazing framework
- React community for frontend tools

---

<div align="center">

**Made with ❤️ for job seekers everywhere**

⭐ Star this repo if you find it helpful!

[Get Started](QUICKSTART.md) • [Documentation](SETUP.md) • [Deploy](DEPLOYMENT.md)

</div>
