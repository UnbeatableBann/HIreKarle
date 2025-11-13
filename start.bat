@echo off
echo ========================================
echo Starting HireKarle Application
echo ========================================
echo.

echo Checking if Redis is running...
redis-cli ping >nul 2>&1
if %errorlevel% neq 0 (
    echo Redis is not running. Please start Redis first:
    echo   redis-server
    echo.
    pause
    exit /b 1
)
echo Redis: OK
echo.

echo Starting Backend...
start "HireKarle Backend" cmd /k "cd backend && venv\Scripts\activate && uvicorn app.main:app --reload"
timeout /t 3 >nul

echo Starting Frontend...
start "HireKarle Frontend" cmd /k "cd frontend && npm start"

echo.
echo ========================================
echo HireKarle is starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo ========================================
echo.
echo Press any key to stop all services...
pause >nul

taskkill /FI "WINDOWTITLE eq HireKarle Backend" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq HireKarle Frontend" /F >nul 2>&1
echo Services stopped.
