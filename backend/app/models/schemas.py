from pydantic import BaseModel
from typing import List, Optional

class ResumeUploadResponse(BaseModel):
    session_id: str
    message: str

class JobSearchRequest(BaseModel):
    session_id: str
    job_title: str

class Job(BaseModel):
    title: str
    company: str
    location: str
    source: str
    url: str
    description: str
    score: float
    rationale: Optional[str]

class JobSearchResponse(BaseModel):
    jobs: List[Job]
    total: int

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
