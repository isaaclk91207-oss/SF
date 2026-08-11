---
kind: spec
title: SafeFarm Myanmar - Deployment Plan
---

# SafeFarm Myanmar - Deployment Plan

## Deployment Modes

| Mode | Description | Internet Required |
|------|-------------|-------------------|
| Local Offline | Primary mode for demo | No |
| Online Preview | Hugging Face Spaces | Yes |
| GitHub Pages | Static landing page | Yes (to access) |

## Local Offline Mode

### Requirements Checklist

| Requirement | Status |
|-------------|--------|
| Python 3.10 installed | Must have |
| All pip packages installed | Must have |
| Model checkpoint present | Must have |
| Myanmar font bundled | Must have |
| Translation dictionary bundled | Must have |
| Sample images available | Must have |

### Setup Script

```bash
# setup.sh (Windows: setup.bat)
echo "Setting up SafeFarm Myanmar..."

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Download Myanmar font
mkdir -p safefarm\utils\fonts
curl -L -o safefarm\utils\fonts\NotoSansMyanmar.ttf ^
  "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansMyanmar/NotoSansMyanmar-Regular.ttf"

# Download model checkpoint (if available)
# curl -L -o safefarm\model\checkpoint.pt <model-url>

echo "Setup complete! Run: streamlit run app.py"
```

### requirements.txt

```
streamlit>=1.28.0
torch>=2.0.0
torchvision>=0.15.0
Pillow>=10.0.0
reportlab>=4.0.0
numpy>=1.24.0
opencv-python>=4.8.0
grad-cam>=1.4.0
```

### Launch Command

```bash
# Activate environment
venv\Scripts\activate

# Run application
streamlit run app.py

# Opens at: http://localhost:8501
```

### Offline Verification Steps

```
1. Turn off Wi-Fi
2. Run: streamlit run app.py
3. Open: http://localhost:8501
4. Select language (English / မြန်မာ)
5. Upload a test image
6. Fill in assessment form
7. Click "Assess Damage"
8. Verify result card displays
9. Verify Grad-CAM overlay shows
10. Click "Download PDF Report"
11. Open PDF, verify Myanmar text renders
12. Restart application
13. Confirm no cloud API calls
```

## Online Mode (Hugging Face Spaces)

### Space Configuration

```yaml
# Hugging Face Space settings
title: SafeFarm Myanmar
emoji: 🌾
colorFrom: green
colorTo: blue
sdk: docker
sdk_version: "latest"
app_file: app.py
pinned: false
license: mit
```

### Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY safefarm/ ./safefarm/
COPY app.py .

# Expose port
EXPOSE 7860

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]
```

### Space Environment Variables

```
STREAMLIT_SERVER_PORT=7860
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

### Online Label

Display prominently in the app:

```
⚠️ Online Preview — Internet connection required
This hosted version runs on Hugging Face Spaces.
For offline use, run the local version.
```

## GitHub Repository

### Repository Structure

```
safefarm-myanmar/
├── README.md
├── requirements.txt
├── app.py
├── Dockerfile
├── .gitignore
├── LICENSE
├── safefarm/
│   ├── __init__.py
│   ├── config.py
│   ├── lang/
│   │   ├── __init__.py
│   │   ├── en.py
│   │   └── my.py
│   ├── model/
│   │   ├── __init__.py
│   │   ├── checkpoint.pt
│   │   ├── inference.py
│   │   └── gradcam.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── image.py
│   │   ├── report.py
│   │   ├── priority.py
│   │   └── fonts/
│   │       └── NotoSansMyanmar.ttf
│   ├── data/
│   │   └── test_myanmar/
│   │       └── (6-9 test images)
│   └── samples/
│       └── (demo images)
├── docs/
│   ├── screenshots/
│   └── demo-video.mp4
└── assets/
    └── logo.png
```

### README.md Template

```markdown
# SafeFarm Myanmar 🌾

**Flood Damage Assessment for Myanmar Agriculture**

Team: M-Matrix

## Overview

SafeFarm Myanmar is a preliminary flood damage assessment tool 
for Myanmar farmers. It uses image classification to estimate 
crop damage severity and prioritizes support allocation.

## Features

- Image-based damage classification (Low/Medium/High)
- Grad-CAM visual evidence
- Bilingual support (English / မြန်မာ)
- PDF report generation
- Offline-capable
- Support priority scoring

## Quick Start

### Local Installation

```bash
git clone https://github.com/yourusername/safefarm-myanmar.git
cd safefarm-myanmar
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
streamlit run app.py
```

Open: http://localhost:8501

### Online Demo

Visit: [Hugging Face Spaces](https://huggingface.co/spaces/yourusername/safefarm-myanmar)

⚠️ Online version requires internet connection.

## Project Structure

[Directory tree here]

## Limitations

- Prototype model — not for official damage assessment
- Limited training data
- Results are preliminary estimates only
- Requires field verification for actual aid decisions

## License

MIT License

## Team

M-Matrix
```

### .gitignore

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/

# Model checkpoints (large files)
*.pt
*.pth
*.onnx

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Temp
*.tmp
temp/
```

## Landing Page (Netlify/GitHub Pages)

### Simple HTML Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SafeFarm Myanmar</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .hero {
            text-align: center;
            padding: 40px 20px;
            background: linear-gradient(135deg, #4CAF50, #2196F3);
            color: white;
            border-radius: 12px;
            margin-bottom: 30px;
        }
        .feature {
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin: 10px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .btn {
            display: inline-block;
            padding: 12px 24px;
            background: #4CAF50;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            margin: 10px;
        }
    </style>
</head>
<body>
    <div class="hero">
        <h1>🌾 SafeFarm Myanmar</h1>
        <p>Flood Damage Assessment for Myanmar Agriculture</p>
        <p><strong>Team: M-Matrix</strong></p>
    </div>
    
    <div class="feature">
        <h3>📸 Image-Based Assessment</h3>
        <p>Upload a farm photo to get preliminary damage classification</p>
    </div>
    
    <div class="feature">
        <h3>🌐 Bilingual Support</h3>
        <p>Available in English and မြန်မာ (Myanmar)</p>
    </div>
    
    <div class="feature">
        <h3>📊 Priority Scoring</h3>
        <p>Helps prioritize field verification and aid distribution</p>
    </div>
    
    <div style="text-align: center; margin-top: 30px;">
        <a href="https://huggingface.co/spaces/..." class="btn">
            Try Online Demo
        </a>
        <a href="https://github.com/..." class="btn" style="background: #333;">
            View on GitHub
        </a>
    </div>
    
    <p style="text-align: center; margin-top: 30px; color: #666;">
        ⚠️ This is a prototype tool. Results are preliminary assessments only.
    </p>
</body>
</html>
```

## Demo Video Script

### 2-3 Minute Demo Structure

| Time | Content |
|------|---------|
| 0:00-0:15 | Title screen: SafeFarm Myanmar, Team M-Matrix |
| 0:15-0:30 | Problem statement: Myanmar flood damage to agriculture |
| 0:30-0:45 | Solution overview: AI-powered damage assessment |
| 0:45-1:15 | Live demo: Upload image, fill form, get results |
| 1:15-1:30 | Show Grad-CAM attention overlay |
| 1:30-1:45 | Show bilingual toggle (English/Myanmar) |
| 1:45-2:00 | Generate and show PDF report |
| 2:00-2:15 | Show offline mode (Wi-Fi off) |
| 2:15-2:30 | Limitations and future work |
| 2:30-2:45 | Thank you, team credits |

### Recording Checklist

- [ ] Clean desktop, no notifications
- [ ] Pre-load sample images
- [ ] Clear browser history
- [ ] Test all features beforehand
- [ ] Record at 1080p
- [ ] Include audio narration
- [ ] Export as MP4
- [ ] Upload to Google Drive / YouTube (unlisted)

## Screenshot Checklist

| # | Screenshot | Description |
|---|------------|-------------|
| 1 | Main interface | Full app with form empty |
| 2 | Form filled | All fields populated |
| 3 | Result card | Damage level and confidence |
| 4 | Grad-CAM overlay | Model attention visualization |
| 5 | Myanmar language | Interface in မြန်မာ |
| 6 | PDF report | Generated bilingual report |
| 7 | Error state | Model not loaded warning |
| 8 | Mobile view | Responsive layout |

## Deployment Timeline

| Day | Task |
|-----|------|
| Day 1 | Project scaffolding, basic UI |
| Day 2 | Image upload and preprocessing |
| Day 3 | Model training (or demo mode) |
| Day 4 | Grad-CAM integration |
| Day 5 | Bilingual system |
| Day 6 | PDF report generation |
| Day 7 | Testing and bug fixes |
| Day 8 | GitHub repo setup |
| Day 9 | Hugging Face Spaces deploy |
| Day 10 | Demo video and screenshots |
