@echo off
chcp 65001 >nul 2>&1
title SafeFarm Myanmar - Starting...

echo.
echo ========================================
echo    SafeFarm Myanmar - Flood Damage
echo         Assessment Tool
echo ========================================
echo.

REM Check if Python is installed
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.10 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo        Python %PYTHON_VERSION% found!

REM Check if virtual environment exists
echo.
echo [2/5] Checking virtual environment...
if not exist "venv" (
    echo        Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to create virtual environment!
        echo.
        pause
        exit /b 1
    )
    echo        Virtual environment created!
) else (
    echo        Virtual environment found!
)

REM Activate virtual environment
echo.
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo.
    echo ERROR: Failed to activate virtual environment!
    echo.
    pause
    exit /b 1
)
echo        Virtual environment activated!

REM Install/update dependencies
echo.
echo [4/5] Installing dependencies...
pip install -r requirements.txt --quiet --upgrade
if errorlevel 1 (
    echo.
    echo WARNING: Some dependencies may not have installed correctly.
    echo          The app may still work, but some features might be unavailable.
)

REM Generate PNG icons if needed
echo.
echo [5/5] Preparing PWA icons...
if not exist "pwa\icons\icon-192.png" (
    python -c "from PIL import Image, ImageDraw, ImageFont; img = Image.new('RGB', (192, 192), '#4CAF50'); img.save('pwa/icons/icon-192.png')" 2>nul
    if exist "pwa\icons\icon-192.png" (
        echo        Generated icon-192.png
    ) else (
        echo        Using SVG icons instead
    )
)
if not exist "pwa\icons\icon-512.png" (
    python -c "from PIL import Image, ImageDraw, ImageFont; img = Image.new('RGB', (512, 512), '#4CAF50'); img.save('pwa/icons/icon-512.png')" 2>nul
    if exist "pwa\icons\icon-512.png" (
        echo        Generated icon-512.png
    ) else (
        echo        Using SVG icons instead
    )
)

echo.
echo ========================================
echo    Starting SafeFarm Myanmar...
echo ========================================
echo.
echo    Server will start at:
echo    http://localhost:8501
echo.
echo    PWA Interface:
echo    file:///%CD%/pwa/index.html
echo.
echo    Press Ctrl+C to stop the server.
echo ========================================
echo.

REM Start Streamlit server
start /b streamlit run app.py --server.port=8501 --server.address=localhost --server.headless=true --browser.gatherUsageStats=false

REM Wait for server to start
echo Waiting for server to start...
timeout /t 5 /nobreak >nul

REM Open browser
echo Opening browser...
start http://localhost:8501

echo.
echo Server is running! 
echo Press any key to stop the server and exit.
echo.
pause >nul

REM Kill Streamlit process
taskkill /f /im streamlit.exe >nul 2>&1
echo.
echo SafeFarm Myanmar has been stopped.
timeout /t 2 /nobreak >nul
