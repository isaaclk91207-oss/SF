# SafeFarm Myanmar 🌾

**Flood Damage Assessment for Myanmar Agriculture**

Team: M-Matrix

[![Streamlit App](https://img.shields.io/badge/Streamlit-Deploy-red?logo=streamlit)](https://huggingface.co/spaces)

## Overview

SafeFarm Myanmar is a preliminary flood damage assessment tool for Myanmar farmers. It uses image classification to estimate crop damage severity and prioritizes support allocation.

## Features

- 📸 **Image-Based Assessment** - Upload a farm photo to get preliminary damage classification
- 🔍 **Grad-CAM Visual Evidence** - See which parts of the image influenced the decision
- 🌐 **Bilingual Support** - Available in English and မြန်မာ (Myanmar)
- 📊 **Priority Scoring** - Helps prioritize field verification and aid distribution
- 📄 **PDF Reports** - Generate bilingual assessment reports
- 💻 **Offline Capable** - Works without internet connection

## Quick Start

### Option 1: Streamlit Cloud (Online)

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://huggingface.co/spaces)

### Option 2: Local Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/safefarm-myanmar.git
cd safefarm-myanmar

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Open: http://localhost:8501

### Option 3: PWA (Progressive Web App)

```bash
# Windows
start.bat

# Linux/Mac
./start.sh
```

## Project Structure

```
safefarm-myanmar/
├── app.py                 # Streamlit entry point
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── config.toml        # Streamlit configuration
├── safefarm/
│   ├── config.py          # App configuration
│   ├── lang/              # Bilingual strings
│   │   ├── en.py          # English
│   │   └── my.py          # Myanmar
│   ├── model/             # ML inference
│   │   ├── inference.py   # ResNet18 classifier
│   │   └── gradcam.py     # Grad-CAM visualization
│   ├── utils/             # Utilities
│   │   ├── image.py       # Image processing
│   │   ├── priority.py    # Priority scoring
│   │   ├── report.py      # PDF generation
│   │   └── font.py        # Myanmar font handling
│   └── pwa/               # PWA files
│       ├── index.html     # PWA wrapper
│       ├── manifest.json  # PWA manifest
│       └── sw.js          # Service worker
└── README.md
```

## How It Works

1. **Upload Image** - Take or upload a photo of the damaged farm
2. **Fill Assessment Form** - Enter farm details (region, crop, area, etc.)
3. **Get Results** - View damage level, confidence score, and recommendations
4. **Visual Evidence** - See Grad-CAM heatmap showing model attention
5. **Download Report** - Generate bilingual PDF report

## Limitations

- ⚠️ Prototype model - not for official damage assessment
- ⚠️ Limited training data
- ⚠️ Results are preliminary estimates only
- ⚠️ Requires field verification for actual aid decisions

## Technology Stack

- **Frontend**: Streamlit
- **ML Framework**: PyTorch
- **Model**: ResNet18 (pretrained)
- **PDF Generation**: xhtml2pdf
- **Image Processing**: OpenCV, Pillow

## License

MIT License

## Team

**M-Matrix**
- Flood Damage Assessment for Myanmar Agriculture
