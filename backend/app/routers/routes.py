from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.schemas import (
    ResumeUploadResponse, JobSearchRequest, 
    JobSearchResponse
)
from app.core.redis_client import redis_client
from app.utils.resume_parser import parse_resume
from app.utils.embeddings import embedding_service
from app.services.matching_service import matching_service
import uuid

router = APIRouter()

@router.post("/upload-resume", response_model=ResumeUploadResponse)
async def upload_resume(file: UploadFile = File(...,)):
    """Upload and parse resume, store in Redis"""
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(400, "No file provided")
        
        if not file.filename.lower().endswith((".pdf", ".docx", ".txt")):
            raise HTTPException(status_code=400, detail="Only PDF, DOCX, or TXT files supported")
        
        # Read file content
        content = await file.read()
        
        # Parse resume
        resume_text = await parse_resume(content, file.filename)

        if not resume_text or len(resume_text) < 50:
            raise HTTPException(400, "Resume text too short or empty")
        
        # Generate embedding
        embedding = embedding_service.generate_embedding(resume_text)
        
        # Create session
        session_id = str(uuid.uuid4())
        
        # Store in Redis
        resume_data = {
            "resume_text": resume_text,
            "embedding": embedding,
            "filename": file.filename
        }
        
        success = await redis_client.set_json(f"resume:{session_id}", resume_data)
        
        if not success:
            raise HTTPException(500, "Failed to store resume")
        
        return ResumeUploadResponse(
            session_id=session_id,
            message="Resume uploaded successfully"
        )
    
    except ValueError as e:
        raise HTTPException(400, str(e))
    except HTTPException:
        # Let FastAPI handle HTTPExceptions correctly
        raise
    except Exception as e:
        print(f"Upload error: {e}")
        raise HTTPException(500, "Failed to process resume")

@router.post("/search-jobs", response_model=JobSearchResponse)
async def search_jobs(request: JobSearchRequest):
    """Search and match jobs based on resume"""
    try:
        # Retrieve resume from Redis
        resume_data = await redis_client.get_json(f"resume:{request.session_id}")
        
        if not resume_data:
            raise HTTPException(404, "Session not found or expired. Please upload resume again.")
        
        # Match jobs
        jobs = await matching_service.match_jobs(resume_data, request.job_title)
        
        return JobSearchResponse(
            jobs=jobs,
            total=len(jobs)
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Search error: {e}")
        raise HTTPException(500, "Failed to search jobs")

