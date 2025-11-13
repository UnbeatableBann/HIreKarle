# Manual Testing Guide

## Prerequisites
1. Backend running: `cd backend && uvicorn app.main:app --reload`
2. Redis running: `redis-server`
3. Python requests installed: `pip install requests`

## Test Files

### 1. test_resume_upload.py
Tests resume upload functionality.
```bash
python tests/test_resume_upload.py
```
Expected: Returns session_id

### 2. test_job_search.py
Tests job search with existing session.
```bash
# First, get session_id from test_resume_upload.py
# Update SESSION_ID in the file
python tests/test_job_search.py
```
Expected: Returns matched jobs

### 3. test_full_flow.py
Tests complete flow from upload to search.
```bash
python tests/test_full_flow.py
```
Expected: Complete workflow with results

## Manual UI Testing

1. Start backend: `cd backend && uvicorn app.main:app --reload`
2. Start frontend: `cd frontend && npm start`
3. Open browser: `http://localhost:3000`
4. Upload a resume (PDF/DOCX/TXT)
5. Search for jobs (e.g., "Software Engineer")
6. Verify results display with scores
7. Click "Apply Now" to test links
8. Refresh page - session should persist
9. Click "Upload New Resume" to reset

## Error Testing

### Test Session Expiry
```python
import requests
response = requests.post("http://localhost:8000/api/search-jobs", 
    json={"session_id": "invalid-id", "job_title": "Engineer"})
print(response.json())  # Should return 404 error
```

### Test Invalid File
Upload a non-resume file (e.g., image) and verify error handling.

### Test Empty Resume
Upload an empty text file and verify validation.
