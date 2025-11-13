# HireKarle Troubleshooting Guide

## 🔍 Quick Diagnostics

Run this first to check all services:
```bash
python tests/check_services.py
```

---

## ❌ Common Issues & Solutions

### 1. Redis Connection Refused

**Error:**
```
redis.exceptions.ConnectionError: Error connecting to Redis
```

**Solutions:**

**Check if Redis is running:**
```bash
redis-cli ping
# Should return: PONG
```

**Start Redis:**
```bash
# Windows
redis-server

# Mac
brew services start redis

# Linux
sudo systemctl start redis

# Docker
docker run -d -p 6379:6379 redis:alpine
```

**Check Redis port:**
```bash
redis-cli -p 6379 ping
```

**Update .env if using different host/port:**
```env
REDIS_HOST=localhost
REDIS_PORT=6379
```

---

### 2. Module Not Found Error

**Error:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solutions:**

**Backend:**
```bash
cd backend
pip install -r requirements.txt

# If still failing, upgrade pip
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install

# If failing, clear cache
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

---

### 3. Gemini API Key Error

**Error:**
```
google.api_core.exceptions.PermissionDenied: API key not valid
```

**Solutions:**

**Check .env file exists:**
```bash
cd backend
ls .env  # Should exist
```

**Verify API key format:**
```env
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# Should start with AIzaSy
```

**Get new API key:**
1. Go to https://makersuite.google.com/app/apikey
2. Create new key
3. Copy to .env file

**Test API key:**
```python
import google.generativeai as genai
genai.configure(api_key="YOUR_KEY")
model = genai.GenerativeModel('gemini-2.0-flash-exp')
response = model.generate_content("Hello")
print(response.text)
```

---

### 4. Port Already in Use

**Error:**
```
OSError: [Errno 48] Address already in use
```

**Solutions:**

**Find process using port:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -i :8000
kill -9 <PID>
```

**Use different port:**
```bash
# Backend
uvicorn app.main:app --reload --port 8001

# Frontend
PORT=3001 npm start
```

---

### 5. CORS Error

**Error:**
```
Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000' 
has been blocked by CORS policy
```

**Solutions:**

**Check backend .env:**
```env
CORS_ORIGINS=http://localhost:3000
```

**For multiple origins:**
```env
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

**Verify backend is running:**
```bash
curl http://localhost:8000/health
```

---

### 6. File Upload Fails

**Error:**
```
400 Bad Request: Unsupported file format
```

**Solutions:**

**Check file format:**
- Supported: .pdf, .doc, .docx, .txt
- Max size: 10MB (default)

**Test with sample file:**
```bash
python tests/test_resume_upload.py
```

**Check file content:**
```bash
# PDF
pdftotext resume.pdf -
# Should show text content

# DOCX
unzip -p resume.docx word/document.xml
```

---

### 7. Session Not Found

**Error:**
```
404 Not Found: Session not found or expired
```

**Solutions:**

**Check Redis has data:**
```bash
redis-cli
> KEYS resume:*
> GET resume:YOUR_SESSION_ID
```

**Check session TTL:**
```bash
redis-cli
> TTL resume:YOUR_SESSION_ID
# Should return seconds remaining (max 604800 = 7 days)
```

**Clear localStorage and re-upload:**
```javascript
// In browser console
localStorage.clear()
location.reload()
```

---

### 8. Slow Job Search

**Issue:**
Job search takes >10 seconds

**Solutions:**

**Check network:**
```bash
ping google.com
```

**Check Gemini API latency:**
```python
import time
import google.generativeai as genai

genai.configure(api_key="YOUR_KEY")
model = genai.GenerativeModel('gemini-2.0-flash-exp')

start = time.time()
response = model.generate_content("Hello")
print(f"Latency: {time.time() - start}s")
```

**Enable result caching:**
```python
# In matching_service.py
# Cache results in Redis for 1 hour
cache_key = f"search:{session_id}:{job_title}"
cached = redis_client.get_json(cache_key)
if cached:
    return cached
```

**Reduce job sources:**
```python
# In job_scraper.py
# Comment out slow sources temporarily
tasks = [
    self.fetch_linkedin_jobs(job_title),
    # self.fetch_indeed_jobs(job_title),  # Disabled
]
```

---

### 9. Docker Issues

**Error:**
```
docker-compose: command not found
```

**Solutions:**

**Install Docker:**
- Windows: Docker Desktop
- Mac: Docker Desktop
- Linux: `sudo apt install docker.io docker-compose`

**Check Docker is running:**
```bash
docker ps
```

**Rebuild containers:**
```bash
docker-compose down
docker-compose up --build
```

**View logs:**
```bash
docker-compose logs backend
docker-compose logs frontend
docker-compose logs redis
```

**Clear Docker cache:**
```bash
docker system prune -a
```

---

### 10. Frontend Build Fails

**Error:**
```
npm ERR! Failed at the react-scripts build script
```

**Solutions:**

**Clear cache:**
```bash
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

**Check Node version:**
```bash
node --version  # Should be 16+
npm --version   # Should be 8+
```

**Increase memory:**
```bash
# Windows
set NODE_OPTIONS=--max_old_space_size=4096

# Mac/Linux
export NODE_OPTIONS=--max_old_space_size=4096

npm run build
```

---

## 🔧 Advanced Debugging

### Enable Debug Logging

**Backend:**
```python
# In main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Frontend:**
```javascript
// In api.js
axios.interceptors.request.use(request => {
  console.log('Request:', request);
  return request;
});
```

### Check Redis Memory

```bash
redis-cli INFO memory
```

### Monitor API Calls

```bash
# Backend logs
tail -f backend.log

# Frontend network tab
# Open browser DevTools > Network
```

### Test Individual Components

**Test resume parser:**
```python
from app.utils.resume_parser import parse_resume

with open('resume.pdf', 'rb') as f:
    text = parse_resume(f.read(), 'resume.pdf')
    print(text)
```

**Test embeddings:**
```python
from app.utils.embeddings import embedding_service

text = "Software Engineer with Python experience"
embedding = embedding_service.generate_embedding(text)
print(len(embedding))  # Should be 384
```

**Test LLM:**
```python
from app.services.llm_service import llm_service

result = llm_service.score_job_match(
    "Python developer resume",
    "Python developer job",
    "Software Engineer"
)
print(result)
```

---

## 🐛 Reporting Bugs

When reporting issues, include:

1. **Error message** (full stack trace)
2. **Steps to reproduce**
3. **Environment:**
   - OS (Windows/Mac/Linux)
   - Python version
   - Node version
   - Redis version
4. **Logs:**
   - Backend logs
   - Frontend console
   - Redis logs
5. **Configuration:**
   - .env file (without API key)
   - docker-compose.yml (if using)

**Create issue:**
```bash
# Include this output
python tests/check_services.py
python --version
node --version
redis-cli --version
```

---

## 📞 Getting Help

1. **Check documentation first:**
   - [SETUP.md](SETUP.md)
   - [QUICKSTART.md](QUICKSTART.md)
   - [API_DOCS.md](API_DOCS.md)

2. **Search existing issues:**
   - GitHub Issues

3. **Ask in discussions:**
   - GitHub Discussions

4. **Create new issue:**
   - Provide all debugging info above

---

## ✅ Health Check Checklist

Before asking for help, verify:

- [ ] Redis is running (`redis-cli ping`)
- [ ] Backend is running (`curl http://localhost:8000/health`)
- [ ] Frontend is running (`curl http://localhost:3000`)
- [ ] .env file exists with valid API key
- [ ] All dependencies installed
- [ ] Ports 3000, 6379, 8000 are available
- [ ] No firewall blocking connections
- [ ] Correct Python/Node versions

---

## 🔄 Reset Everything

If all else fails:

```bash
# Stop all services
docker-compose down
pkill -f uvicorn
pkill -f "npm start"
redis-cli FLUSHALL

# Clean install
cd backend
rm -rf venv __pycache__
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

cd ../frontend
rm -rf node_modules package-lock.json
npm install

# Restart
redis-server &
cd backend && uvicorn app.main:app --reload &
cd frontend && npm start
```

---

## 📊 Performance Optimization

### If experiencing slowness:

**1. Enable Redis caching:**
```python
# Cache job results for 1 hour
CACHE_TTL = 3600
```

**2. Reduce embedding size:**
```python
# Use smaller model
model = SentenceTransformer('all-MiniLM-L6-v2')  # Current
# model = SentenceTransformer('paraphrase-MiniLM-L3-v2')  # Faster
```

**3. Limit job results:**
```python
# In matching_service.py
return scored_jobs[:10]  # Instead of [:20]
```

**4. Use production server:**
```bash
# Instead of uvicorn --reload
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

---

## 🎯 Still Stuck?

Create a detailed issue with:
- Output of `python tests/check_services.py`
- Full error message
- Steps you've tried
- Your environment details

We'll help you get it working! 🚀
