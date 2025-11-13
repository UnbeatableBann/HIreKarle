"""
Manual Test: Resume Upload

1. Start backend: cd backend && uvicorn app.main:app --reload
2. Run this test: python tests/test_resume_upload.py

Expected: Should return session_id
"""

import requests

def test_upload_resume():
    url = "http://localhost:8000/api/upload-resume"
    
    # Create a sample resume file
    files = {
        'file': ('resume.txt', b'John Doe\nSoftware Engineer\nSkills: Python, JavaScript, React, Node.js\nExperience: 5 years', 'text/plain')
    }
    
    response = requests.post(url, files=files)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 200
    assert 'session_id' in response.json()
    
    return response.json()['session_id']

if __name__ == "__main__":
    try:
        session_id = test_upload_resume()
        print(f"\n✅ Test Passed! Session ID: {session_id}")
    except Exception as e:
        print(f"\n❌ Test Failed: {e}")
