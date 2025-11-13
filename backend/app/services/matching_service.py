from typing import List, Dict
from app.utils.embeddings import embedding_service
from app.services.llm_service import llm_service  # noqa: F401
from app.services.job_scraper import job_scraper

class MatchingService:
    def calculate_heuristic_score(self, resume_text: str, job_description: str) -> float:
        """Simple keyword-based heuristic scoring"""
        resume_lower = resume_text.lower()
        job_lower = job_description.lower()
        
        # Common tech keywords
        keywords = ['python', 'java', 'javascript', 'react', 'node', 'sql', 'aws', 
                   'docker', 'kubernetes', 'machine learning', 'data', 'api']
        
        matches = sum(1 for kw in keywords if kw in resume_lower and kw in job_lower)
        return min(1.0, matches / 10.0)
    
    async def match_jobs(self, resume_data: dict, job_title: str) -> List[Dict]:
        """Main matching pipeline"""
        # Fetch jobs
        jobs = await job_scraper.fetch_all_jobs(job_title)
        
        if not jobs:
            return []
        
        resume_text = resume_data.get("resume_text", "")
        resume_embedding = resume_data.get("embedding", [])
        
        scored_jobs = []
        
        for job in jobs:
            try:
                # Generate job embedding
                job_embedding = embedding_service.generate_embedding(job["description"])
                
                # Calculate similarity
                similarity_score = embedding_service.calculate_similarity(
                    resume_embedding, job_embedding
                )
                
                # Get LLM score
                # llm_result = llm_service.score_job_match(
                #     resume_text, job["description"], job["title"]
                # )
                
                # Calculate heuristic score
                heuristic_score = self.calculate_heuristic_score(
                    resume_text, job["description"]
                )
                
                # Final weighted score
                final_score = (
                    #0.7 * (llm_result["score"] / 100.0) +
                    0.9 * similarity_score +
                    0.1 * heuristic_score
                ) * 100
                
                scored_jobs.append({
                    "title": job["title"],
                    "company": job["company"],
                    "location": job["location"],
                    "source": job["source"],
                    "url": job["url"],
                    "description": job["description"][:200],
                    "score": round(final_score, 1),
                    "rationale": "Unable to find."
                })
            except Exception as e:
                print(f"Error scoring job {job.get('title')}: {e}")
                continue
        
        # Sort by score descending
        scored_jobs.sort(key=lambda x: x["score"], reverse=True)
        
        return scored_jobs  

matching_service = MatchingService()
