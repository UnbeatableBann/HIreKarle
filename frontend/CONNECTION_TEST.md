# Frontend-Backend Connection Test

## Quick Test

1. **Start Backend**
```bash
cd backend
uvicorn app.main:app --reload
```

2. **Start Frontend**
```bash
cd frontend
npm start
```

3. **Test Connection**
- Open browser: http://localhost:3000
- Upload a resume (PDF/DOCX/TXT)
- Search for jobs (e.g., "Software Engineer")
- Verify results display

## Expected Flow

### Upload Resume
```
Frontend → POST http://localhost:8000/api/upload-resume
Backend → Returns { session_id, message }
Frontend → Stores session_id in localStorage
```

### Search Jobs
```
Frontend → POST http://localhost:8000/api/search-jobs
         → Body: { session_id, job_title }
Backend → Returns { jobs[], total }
Frontend → Displays jobs with scores
```

## Troubleshooting

### CORS Error
- Check backend CORS_ORIGINS includes http://localhost:3000
- Verify backend is running on port 8000

### Session Not Found
- Backend Redis must be running
- Session expires after 7 days
- Clear localStorage and re-upload resume

### File Upload Fails
- Only PDF, DOCX, TXT supported
- Check file is not empty
- Verify backend can parse the file
