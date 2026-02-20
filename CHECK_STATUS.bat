@echo off
echo.
echo ========================================
echo   Checking Server Status
echo ========================================
echo.

echo Checking Backend (port 8000)...
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Backend is running at http://localhost:8000
    echo [OK] API Docs: http://localhost:8000/api/docs
) else (
    echo [WAIT] Backend is starting or not running yet...
    echo       Check the PowerShell window for backend logs
)

echo.
echo Checking Frontend (port 3000)...
curl -s http://localhost:3000 >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Frontend is running at http://localhost:3000
    echo.
    echo ========================================
    echo   READY! Open: http://localhost:3000
    echo ========================================
) else (
    echo [WAIT] Frontend is starting or not running yet...
    echo       Check the PowerShell window for frontend logs
)

echo.
pause
