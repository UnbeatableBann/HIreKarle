# 🗺️ HireKarle Project Map

## 📍 Navigation Guide

This document helps you navigate the HireKarle project and find what you need quickly.

---

## 🎯 I Want To...

### Get Started Immediately
→ **[START_HERE.md](START_HERE.md)** - 3-step quick start

### Understand the Project
→ **[README.md](README.md)** - Project overview with features

### Set Up Development Environment
→ **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup guide
→ **[SETUP.md](SETUP.md)** - Detailed installation instructions

### Learn the Architecture
→ **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Complete architecture
→ **[FINAL_SUMMARY.md](FINAL_SUMMARY.md)** - Project statistics

### Use the API
→ **[API_DOCS.md](API_DOCS.md)** - Complete API reference

### Deploy to Production
→ **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deployment guide for AWS/GCP/VPS

### Fix Issues
→ **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common problems & solutions

### See What's Included
→ **[FEATURES.md](FEATURES.md)** - Feature list & roadmap
→ **[PROJECT_COMPLETE.md](PROJECT_COMPLETE.md)** - Completion checklist

### Run Tests
→ **[tests/README.md](tests/README.md)** - Testing guide

---

## 📁 File Structure Map

```
HireKarle/
│
├── 📖 DOCUMENTATION (Start Here!)
│   ├── START_HERE.md ⭐          # Begin here!
│   ├── README.md                 # Project overview
│   ├── QUICKSTART.md             # 5-min setup
│   ├── SETUP.md                  # Detailed setup
│   ├── API_DOCS.md               # API reference
│   ├── DEPLOYMENT.md             # Production guide
│   ├── TROUBLESHOOTING.md        # Problem solving
│   ├── FEATURES.md               # Feature list
│   ├── PROJECT_SUMMARY.md        # Architecture
│   ├── PROJECT_COMPLETE.md       # Checklist
│   ├── FINAL_SUMMARY.md          # Statistics
│   └── PROJECT_MAP.md            # This file
│
├── 🔧 BACKEND (FastAPI + Python)
│   ├── app/
│   │   ├── main.py               # FastAPI app entry
│   │   ├── api/
│   │   │   └── routes.py         # API endpoints
│   │   ├── core/
│   │   │   ├── config.py         # Configuration
│   │   │   └── redis_client.py   # Redis wrapper
│   │   ├── services/
│   │   │   ├── job_scraper.py    # Job fetching
│   │   │   ├── llm_service.py    # Gemini AI
│   │   │   ├── matching_service.py # Scoring
│   │   │   └── job_scraper_real.py # API guide
│   │   ├── utils/
│   │   │   ├── resume_parser.py  # PDF/DOCX parser
│   │   │   └── embeddings.py     # Semantic similarity
│   │   └── models/
│   │       └── schemas.py        # Data models
│   ├── requirements.txt          # Python dependencies
│   ├── .env.example              # Environment template
│   └── Dockerfile                # Docker config
│
├── 📱 FRONTEND (React)
│   ├── src/
│   │   ├── App.js                # Main component
│   │   ├── App.css               # Styles
│   │   ├── index.js              # Entry point
│   │   ├── components/
│   │   │   ├── ResumeUpload.js   # Upload UI
│   │   │   └── JobSearch.js      # Search UI
│   │   └── services/
│   │       └── api.js            # API client
│   ├── public/
│   │   └── index.html            # HTML template
│   ├── package.json              # Node dependencies
│   └── Dockerfile                # Docker config
│
├── 🧪 TESTS
│   ├── test_resume_upload.py     # Upload test
│   ├── test_job_search.py        # Search test
│   ├── test_full_flow.py         # Integration test
│   ├── check_services.py         # Health check
│   ├── sample_resume.txt         # Test data
│   └── README.md                 # Test guide
│
├── 🐳 DEPLOYMENT
│   ├── docker-compose.yml        # Multi-container setup
│   ├── start.bat                 # Windows startup
│   └── .gitignore                # Git exclusions
│
└── 📝 CONFIGURATION
    ├── backend/.env.example      # Backend config
    └── backend/requirements.txt  # Python packages
```

---

## 🎯 Common Tasks

### Task: First Time Setup
```
1. Read: START_HERE.md
2. Get: Gemini API key
3. Configure: backend/.env
4. Run: docker-compose up
5. Test: http://localhost:3000
```

### Task: Understand Code
```
1. Read: PROJECT_SUMMARY.md (architecture)
2. Explore: backend/app/main.py (entry point)
3. Check: backend/app/api/routes.py (endpoints)
4. Review: frontend/src/App.js (UI)
```

### Task: Add New Feature
```
1. Read: FEATURES.md (roadmap)
2. Modify: Relevant service file
3. Test: Run test scripts
4. Document: Update README.md
```

### Task: Deploy to Production
```
1. Read: DEPLOYMENT.md
2. Choose: Platform (AWS/GCP/VPS)
3. Configure: Environment variables
4. Deploy: Follow platform guide
5. Monitor: Set up logging
```

### Task: Fix Bug
```
1. Check: TROUBLESHOOTING.md
2. Run: tests/check_services.py
3. Review: Error logs
4. Debug: Relevant component
5. Test: Verify fix
```

---

## 🔍 Find Specific Information

### Configuration
- **Environment Variables**: `backend/.env.example`
- **Python Dependencies**: `backend/requirements.txt`
- **Node Dependencies**: `frontend/package.json`
- **Docker Setup**: `docker-compose.yml`

### API Information
- **Endpoints**: `API_DOCS.md` or `backend/app/api/routes.py`
- **Request/Response Models**: `backend/app/models/schemas.py`
- **Error Handling**: `backend/app/api/routes.py`

### Business Logic
- **Job Fetching**: `backend/app/services/job_scraper.py`
- **AI Scoring**: `backend/app/services/llm_service.py`
- **Matching Algorithm**: `backend/app/services/matching_service.py`
- **Resume Parsing**: `backend/app/utils/resume_parser.py`

### UI Components
- **Main App**: `frontend/src/App.js`
- **Upload Form**: `frontend/src/components/ResumeUpload.js`
- **Search Interface**: `frontend/src/components/JobSearch.js`
- **Styling**: `frontend/src/App.css`

### Testing
- **Test Scripts**: `tests/` directory
- **Test Guide**: `tests/README.md`
- **Sample Data**: `tests/sample_resume.txt`

---

## 📚 Reading Order

### For Beginners
1. **START_HERE.md** - Get started
2. **README.md** - Understand project
3. **QUICKSTART.md** - Set up environment
4. **FEATURES.md** - See what's possible

### For Developers
1. **PROJECT_SUMMARY.md** - Architecture
2. **API_DOCS.md** - API reference
3. **Code files** - Implementation
4. **FEATURES.md** - Roadmap

### For DevOps
1. **DEPLOYMENT.md** - Production setup
2. **docker-compose.yml** - Container config
3. **TROUBLESHOOTING.md** - Common issues
4. **.env.example** - Configuration

---

## 🎨 Component Relationships

```
User Browser
    ↓
ResumeUpload.js → api.js → /api/upload-resume → routes.py
                                                      ↓
                                                resume_parser.py
                                                      ↓
                                                embeddings.py
                                                      ↓
                                                redis_client.py

User Browser
    ↓
JobSearch.js → api.js → /api/search-jobs → routes.py
                                                ↓
                                          redis_client.py
                                                ↓
                                          job_scraper.py
                                                ↓
                                          matching_service.py
                                                ↓
                                    ┌───────────┴───────────┐
                                    ↓                       ↓
                              llm_service.py          embeddings.py
                                    ↓                       ↓
                              Gemini API            Sentence Transformers
```

---

## 🔧 Modification Guide

### Change Scoring Algorithm
**File**: `backend/app/services/matching_service.py`
**Function**: `match_jobs()`
**Line**: ~50-55

### Add New Job Source
**File**: `backend/app/services/job_scraper.py`
**Add**: New async function
**Update**: `fetch_all_jobs()` method

### Modify UI Colors
**File**: `frontend/src/App.css`
**Section**: `.App` background gradient

### Change Session TTL
**File**: `backend/.env`
**Variable**: `SESSION_TTL`

### Add New API Endpoint
**File**: `backend/app/api/routes.py`
**Add**: New route function with decorator

---

## 🎯 Quick Reference

### Start Services
```bash
# Redis
redis-server

# Backend
cd backend && uvicorn app.main:app --reload

# Frontend
cd frontend && npm start

# All (Docker)
docker-compose up
```

### Run Tests
```bash
python tests/check_services.py
python tests/test_full_flow.py
```

### Access Points
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

---

## 📞 Need Help?

### Quick Answers
→ **TROUBLESHOOTING.md** - Common issues

### Detailed Help
→ **SETUP.md** - Installation problems
→ **API_DOCS.md** - API questions
→ **DEPLOYMENT.md** - Deployment issues

### Still Stuck?
1. Run: `python tests/check_services.py`
2. Check: Error logs
3. Search: TROUBLESHOOTING.md
4. Create: GitHub issue

---

## ✅ Checklist for Success

### Setup Complete When:
- [ ] All services start without errors
- [ ] `check_services.py` passes
- [ ] Resume upload works
- [ ] Job search returns results
- [ ] Session persists on refresh

### Ready to Deploy When:
- [ ] All tests pass
- [ ] Real APIs integrated
- [ ] Environment configured
- [ ] Documentation updated
- [ ] Monitoring set up

---

## 🎊 You're All Set!

Use this map to navigate the project efficiently. Everything is organized and documented for your success!

**Happy coding! 🚀**

---

<div align="center">

[🏠 Home](README.md) • [🚀 Quick Start](START_HERE.md) • [📚 Docs](SETUP.md) • [🐳 Deploy](DEPLOYMENT.md)

</div>
