# HireKarle Frontend

React frontend for HireKarle AI-Powered Job Matcher.

## Backend Connection

The frontend connects to the backend at `http://localhost:8000/api`

### API Endpoints Used

1. **POST /api/upload-resume**
   - Uploads resume file (PDF, DOCX, TXT)
   - Returns: `{ session_id, message }`

2. **POST /api/search-jobs**
   - Searches jobs with session_id and job_title
   - Returns: `{ jobs[], total }`

3. **GET /**
   - Health check endpoint

## Setup

```bash
# Copy environment file
cp .env.example .env

# Install dependencies
npm install

# Start development server
npm start
```

## Environment Variables

Create a `.env` file in the frontend directory:

```env
REACT_APP_API_BASE_URL=http://localhost:8000
```

- **REACT_APP_API_BASE_URL**: Backend API URL (default: http://localhost:8000)
- Frontend Port: `3000`

## Features

- Resume upload with validation
- Job search with AI scoring
- Session persistence (localStorage)
- Responsive design
- Error handling
