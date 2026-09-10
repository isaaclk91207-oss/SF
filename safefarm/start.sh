#!/bin/bash

# SafeFarm Myanmar - Start Script
# For Linux and macOS

echo ""
echo "========================================"
echo "   SafeFarm Myanmar - Flood Damage"
echo "        Assessment Tool"
echo "========================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Python is installed
echo -e "${YELLOW}[1/5]${NC} Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python3 is not installed!${NC}"
    echo ""
    echo "Please install Python 3.10 or higher:"
    echo "  - Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
    echo "  - macOS: brew install python3"
    echo "  - Or download from: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "        Python ${PYTHON_VERSION} found!"

# Check if virtual environment exists
echo ""
echo -e "${YELLOW}[2/5]${NC} Checking virtual environment..."
if [ ! -d "venv" ]; then
    echo "        Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}ERROR: Failed to create virtual environment!${NC}"
        exit 1
    fi
    echo "        Virtual environment created!"
else
    echo "        Virtual environment found!"
fi

# Activate virtual environment
echo ""
echo -e "${YELLOW}[3/5]${NC} Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: Failed to activate virtual environment!${NC}"
    exit 1
fi
echo "        Virtual environment activated!"

# Install/update dependencies
echo ""
echo -e "${YELLOW}[4/5]${NC} Installing dependencies..."
pip install -r requirements.txt --quiet --upgrade
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}WARNING: Some dependencies may not have installed correctly.${NC}"
fi

# Generate PNG icons if needed
echo ""
echo -e "${YELLOW}[5/5]${NC} Preparing PWA icons..."
if [ ! -f "pwa/icons/icon-192.png" ]; then
    python3 -c "from PIL import Image; img = Image.new('RGB', (192, 192), '#4CAF50'); img.save('pwa/icons/icon-192.png')" 2>/dev/null
    if [ -f "pwa/icons/icon-192.png" ]; then
        echo "        Generated icon-192.png"
    else
        echo "        Using SVG icons instead"
    fi
fi
if [ ! -f "pwa/icons/icon-512.png" ]; then
    python3 -c "from PIL import Image; img = Image.new('RGB', (512, 512), '#4CAF50'); img.save('pwa/icons/icon-512.png')" 2>/dev/null
    if [ -f "pwa/icons/icon-512.png" ]; then
        echo "        Generated icon-512.png"
    else
        echo "        Using SVG icons instead"
    fi
fi

echo ""
echo "========================================"
echo "   Starting SafeFarm Myanmar..."
echo "========================================"
echo ""
echo "   Server will start at:"
echo "   http://localhost:8501"
echo ""
echo "   PWA Interface:"
echo "   file://$(pwd)/pwa/index.html"
echo ""
echo "   Press Ctrl+C to stop the server."
echo "========================================"
echo ""

# Start Streamlit server in background
streamlit run app.py \
    --server.port=8501 \
    --server.address=localhost \
    --server.headless=true \
    --browser.gatherUsageStats=false &
STREAMLIT_PID=$!

# Wait for server to start
echo "Waiting for server to start..."
sleep 5

# Open browser (cross-platform)
echo "Opening browser..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open http://localhost:8501
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v xdg-open &> /dev/null; then
        xdg-open http://localhost:8501
    elif command -v gnome-open &> /dev/null; then
        gnome-open http://localhost:8501
    else
        echo "Please open http://localhost:8501 in your browser"
    fi
fi

echo ""
echo "Server is running! (PID: $STREAMLIT_PID)"
echo "Press Ctrl+C to stop the server."
echo ""

# Wait for user to press Ctrl+C
trap "echo ''; echo 'Stopping SafeFarm Myanmar...'; kill $STREAMLIT_PID 2>/dev/null; echo 'Server stopped.'; exit 0" INT TERM
wait $STREAMLIT_PID
