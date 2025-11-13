import google.generativeai as genai
from app.core.config import settings
import json

class LLMService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    
    def score_job_match(self, resume_text: str, job_description: str, job_title: str) -> dict:
        """Score how well a resume matches a job using Gemini"""
        prompt = f"""You are an expert recruiter. Analyze how well this resume matches the job.

Resume:
{resume_text[:2000]}

Job Title: {job_title}
Job Description:
{job_description[:1000]}

Provide a JSON response with:
- score: integer 0-100 (how well the candidate fits)
- rationale: brief explanation (max 100 chars)

Response format:
{{"score": 85, "rationale": "Strong match in Python and ML skills"}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            print(text)
            # Extract JSON from response
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            
            result = json.loads(text)
            return {
                "score": min(100, max(0, result.get("score", 50))),
                "rationale": result.get("rationale", "Match analysis completed")[:150]
            }
        except Exception as e:
            print(f"LLM scoring error: {e}")
            return {"score": 50, "rationale": "Unable to analyze match"}

llm_service = LLMService()
