"""
Service Health Check Script
Run: python tests/check_services.py
"""

import requests
import redis
import sys

def check_redis():
    """Check if Redis is running"""
    try:
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        r.ping()
        print("✅ Redis: Running")
        return True
    except Exception as e:
        print(f"❌ Redis: Not running - {e}")
        return False

def check_backend():
    """Check if backend is running"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend: Running")
            return True
        else:
            print(f"❌ Backend: Unhealthy (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Backend: Not running - {e}")
        return False

def check_frontend():
    """Check if frontend is running"""
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend: Running")
            return True
        else:
            print(f"⚠️  Frontend: Unexpected status ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Frontend: Not running - {e}")
        return False

def main():
    print("=" * 50)
    print("HireKarle Service Health Check")
    print("=" * 50 + "\n")
    
    redis_ok = check_redis()
    backend_ok = check_backend()
    frontend_ok = check_frontend()
    
    print("\n" + "=" * 50)
    
    if redis_ok and backend_ok and frontend_ok:
        print("✅ All services are running!")
        print("=" * 50)
        sys.exit(0)
    else:
        print("⚠️  Some services are not running.")
        print("\nTo start services:")
        if not redis_ok:
            print("  Redis: redis-server")
        if not backend_ok:
            print("  Backend: cd backend && uvicorn app.main:app --reload")
        if not frontend_ok:
            print("  Frontend: cd frontend && npm start")
        print("=" * 50)
        sys.exit(1)

if __name__ == "__main__":
    main()
