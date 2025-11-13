"""
Manual Test: Job Search

1. First run test_resume_upload.py to get a session_id
2. Update SESSION_ID below with the returned value
3. Run this test: python tests/test_job_search.py

Expected: Should return list of matched jobs
"""

import requests

SESSION_ID = "YOUR_SESSION_ID_HERE"  # Replace with actual session_id

def test_search_jobs():
    url = "http://localhost:8000/api/search-jobs"
    
    payload = {
        "session_id": SESSION_ID,
        "job_title": "Software Engineer"
    }
    
    response = requests.post(url, json=payload)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 200
    data = response.json()
    assert 'jobs' in data
    assert 'total' in data
    
    print(f"\nFound {data['total']} jobs")
    for job in data['jobs'][:3]:
        print(f"\n- {job['title']} at {job['company']}")
        print(f"  Score: {job['score']}%")
        print(f"  Rationale: {job['rationale']}")

if __name__ == "__main__":
    try:
        test_search_jobs()
        print("\n✅ Test Passed!")
    except Exception as e:
        print(f"\n❌ Test Failed: {e}")
