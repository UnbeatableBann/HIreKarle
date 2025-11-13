# ⚡ HireKarle Quick Start Guide

## 🎯 Get Running in 5 Minutes

### Step 1: Install Prerequisites (2 min)

**Windows:**
```bash
# Install Python 3.9+ from python.org
# Install Node.js 16+ from nodejs.org
# Install Redis for Windows from github.com/microsoftarchive/redis/releases
```

**Mac:**
```bash
brew install python node redis
```

**Linux:**
```bash
sudo apt install python3 python3-pip nodejs npm redis-server
```

---

### Step 2: Setup Backend (2 min)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
notepad .env  # Add your GEMINI_API_KEY
```

**Get Gemini API Key:**
1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy and paste into `.env`

---

### Step 3: Setup Frontend (1 min)

```bash
# Open new terminal
cd frontend

# Install dependencies
npm install
```

---

### Step 4: Start Services

**Terminal 1 - Redis:**
```bash
redis-server
```

**Terminal 2 - Backend:**
```bash
cd backend
venv\Scripts\activate  # Windows
uvicorn app.main:app --reload
```

**Terminal 3 - Frontend:**
```bash
cd frontend
npm start
```

---

### Step 5: Use the App! 🎉

1. Open browser: http://localhost:3000
2. Upload resume (use `tests/sample_resume.txt` for testing)
3. Search for jobs (try "Software Engineer")
4. View matched jobs with scores
5. Click "Apply Now" to visit job page

---

## 🐳 Alternative: Docker (Even Faster!)

```bash
# Set API key
export GEMINI_API_KEY=your_key_here

# Start everything
docker-compose up --build

# Access app
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

---

## 🧪 Quick Test

```bash
# Check if everything works
python tests/check_services.py

# Run full test
python tests/test_full_flow.py
```

---

## 🔧 Common Issues

### "Redis connection refused"
```bash
# Start Redis
redis-server
```

### "Module not found"
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

### "Port already in use"
```bash
# Backend - use different port
uvicorn app.main:app --reload --port 8001

# Frontend - use different port
PORT=3001 npm start
```

### "GEMINI_API_KEY not found"
```bash
# Make sure .env file exists in backend folder
# And contains: GEMINI_API_KEY=your_actual_key
```

---

## 📝 Quick Commands Reference

```bash
# Backend
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload

# Frontend
cd frontend
npm start

# Redis
redis-server

# Tests
python tests/test_full_flow.py

# Docker
docker-compose up
docker-compose down
```

---

## 🎯 What to Try

1. **Upload Different Resumes**: Test with PDF, DOCX, TXT
2. **Search Various Jobs**: "Data Scientist", "Frontend Developer", "Product Manager"
3. **Check Scores**: See how AI rates different matches
4. **Test Persistence**: Refresh page - session should remain
5. **Reset Session**: Click "Upload New Resume"

---

## 📚 Next Steps

- Read [SETUP.md](SETUP.md) for detailed setup
- Check [API_DOCS.md](API_DOCS.md) for API reference
- See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- Review [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for architecture

---

## 🆘 Need Help?

1. Check if all services are running: `python tests/check_services.py`
2. Look at terminal logs for errors
3. Verify `.env` file has correct API key
4. Make sure Redis is running
5. Check [SETUP.md](SETUP.md) troubleshooting section

---

## 🎉 You're All Set!

HireKarle is now running. Start uploading resumes and finding jobs! 🚀

**Pro Tip**: Use the sample resume in `tests/sample_resume.txt` for quick testing.
