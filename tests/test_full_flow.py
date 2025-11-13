"""
Manual Test: Full Flow (Upload + Search)

Run: python tests/test_full_flow.py

Expected: Complete flow from upload to job matching
"""

import requests
import time

BASE_URL = "http://localhost:8000/api"

def test_full_flow():
    print("=" * 50)
    print("Testing Full HireKarle Flow")
    print("=" * 50)
    
    # Step 1: Upload Resume
    print("\n1. Uploading Resume...")
    files = {
        'file': ('resume.txt', 
                 b'Jane Smith\nData Scientist\nSkills: Python, Machine Learning, TensorFlow, SQL, AWS\nExperience: 3 years in ML and AI', 
                 'text/plain')
    }
    
    response = requests.post(f"{BASE_URL}/upload-resume", files=files)
    assert response.status_code == 200
    session_id = response.json()['session_id']
    print(f"   ✅ Resume uploaded. Session ID: {session_id}")
    
    # Step 2: Search Jobs
    print("\n2. Searching for Data Scientist jobs...")
    time.sleep(1)  # Brief pause
    
    payload = {
        "session_id": session_id,
        "job_title": "Data Scientist"
    }
    
    response = requests.post(f"{BASE_URL}/search-jobs", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    print(f"   ✅ Found {data['total']} jobs")
    
    # Step 3: Display Results
    print("\n3. Top Matched Jobs:")
    print("-" * 50)
    
    for i, job in enumerate(data['jobs'][:5], 1):
        print(f"\n{i}. {job['title']}")
        print(f"   Company: {job['company']}")
        print(f"   Location: {job['location']}")
        print(f"   Source: {job['source']}")
        print(f"   Match Score: {job['score']}%")
        print(f"   Rationale: {job['rationale']}")
        print(f"   Apply: {job['url']}")
    
    print("\n" + "=" * 50)
    print("✅ Full Flow Test Completed Successfully!")
    print("=" * 50)

if __name__ == "__main__":
    try:
        test_full_flow()
    except Exception as e:
        print(f"\n❌ Test Failed: {e}")
        import traceback
        traceback.print_exc()
