# HireKarle API Documentation

Base URL: `http://localhost:8000/api`

## Endpoints

### 1. Upload Resume

**POST** `/upload-resume`

Upload a resume file and create a new session.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: Form data with file field

```bash
curl -X POST http://localhost:8000/api/upload-resume \
  -F "file=@resume.pdf"
```

**Response:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Resume uploaded successfully"
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid file or format
- `500`: Server error

**Supported Formats:**
- PDF (.pdf)
- Word (.doc, .docx)
- Text (.txt)

---

### 2. Search Jobs

**POST** `/search-jobs`

Search and match jobs based on uploaded resume.

**Request:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "job_title": "Software Engineer"
}
```

```bash
curl -X POST http://localhost:8000/api/search-jobs \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "job_title": "Software Engineer"
  }'
```

**Response:**
```json
{
  "jobs": [
    {
      "title": "Senior Software Engineer",
      "company": "Tech Corp",
      "location": "San Francisco, CA",
      "source": "LinkedIn",
      "url": "https://linkedin.com/jobs/...",
      "description": "We are looking for...",
      "score": 92.5,
      "rationale": "Strong match in Python and cloud technologies"
    }
  ],
  "total": 15
}
```

**Status Codes:**
- `200`: Success
- `404`: Session not found or expired
- `500`: Server error

---

### 3. Health Check

**GET** `/health`

Check if the API is running.

**Request:**
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy"
}
```

---

## Data Models

### Job Object
```typescript
{
  title: string;        // Job title
  company: string;      // Company name
  location: string;     // Job location
  source: string;       // "LinkedIn" | "Indeed" | "Naukri" | "Internshala"
  url: string;          // Direct apply link
  description: string;  // Job description (truncated)
  score: number;        // Match score (0-100)
  rationale: string;    // AI-generated explanation
}
```

### Error Response
```typescript
{
  error: string;        // Error type
  detail?: string;      // Detailed message
}
```

---

## Scoring Algorithm

Jobs are scored using a weighted combination:

```
Final Score = 0.7 × LLM_Score + 0.2 × Embedding_Similarity + 0.1 × Heuristic_Score
```

**Components:**

1. **LLM Score (70%)**: Gemini 2.0 analyzes resume-job fit
2. **Embedding Similarity (20%)**: Semantic similarity using sentence transformers
3. **Heuristic Score (10%)**: Keyword matching

---

## Session Management

- Sessions are stored in Redis with 7-day TTL
- Session ID is a UUID v4
- No authentication required
- Sessions auto-expire after 7 days

**Session Data Structure:**
```json
{
  "resume_text": "Full resume text...",
  "embedding": [0.123, 0.456, ...],
  "filename": "resume.pdf"
}
```

---

## Rate Limiting

Currently no rate limiting implemented. For production:
- Recommended: 10 requests/minute per IP
- Use Redis for rate limit tracking
- Return 429 status when exceeded

---

## Error Handling

### Common Errors

**400 Bad Request**
```json
{
  "detail": "Unsupported file format. Please upload PDF, DOCX, or TXT"
}
```

**404 Not Found**
```json
{
  "detail": "Session not found or expired. Please upload resume again."
}
```

**500 Internal Server Error**
```json
{
  "detail": "Failed to process resume"
}
```

---

## CORS Configuration

Allowed origins configured in `.env`:
```
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

---

## Testing with cURL

### Complete Flow

```bash
# 1. Upload resume
RESPONSE=$(curl -s -X POST http://localhost:8000/api/upload-resume \
  -F "file=@resume.pdf")

SESSION_ID=$(echo $RESPONSE | jq -r '.session_id')
echo "Session ID: $SESSION_ID"

# 2. Search jobs
curl -X POST http://localhost:8000/api/search-jobs \
  -H "Content-Type: application/json" \
  -d "{
    \"session_id\": \"$SESSION_ID\",
    \"job_title\": \"Data Scientist\"
  }" | jq
```

---

## WebSocket Support

Not currently implemented. For real-time updates in future:
- WebSocket endpoint: `ws://localhost:8000/ws/{session_id}`
- Stream job results as they're fetched
- Send progress updates during matching

---

## API Versioning

Current version: `v1` (implicit in `/api` prefix)

Future versions:
- `/api/v2/upload-resume`
- Maintain backward compatibility
- Deprecation notices in headers

---

## Security Considerations

1. **File Upload**: Max size 10MB (configurable)
2. **Input Validation**: All inputs sanitized
3. **Session Isolation**: Each session is isolated
4. **No PII Storage**: Resume data auto-deleted after 7 days
5. **HTTPS**: Required for production

---

## Performance

**Typical Response Times:**
- Resume Upload: 1-3 seconds
- Job Search: 3-8 seconds (depends on sources)

**Optimization Tips:**
- Use Redis caching for repeated searches
- Implement job result caching (1 hour TTL)
- Use async/await for concurrent API calls

---

## Monitoring

Recommended metrics to track:
- Request count per endpoint
- Average response time
- Error rate
- Session creation rate
- Redis memory usage
- Gemini API usage/costs

---

## Future Enhancements

1. **Pagination**: Return jobs in pages
2. **Filters**: Location, salary, experience level
3. **Saved Searches**: Store search preferences
4. **Email Alerts**: Notify on new matches
5. **Analytics**: Track application success rate
