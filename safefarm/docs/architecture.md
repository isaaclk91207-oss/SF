---
kind: spec
title: SafeFarm Myanmar - Architecture Overview
---

# SafeFarm Myanmar - Architecture

## Project Identity

| Field | Value |
|-------|-------|
| Product Name | SafeFarm Myanmar |
| Team Name | M-Matrix |
| Purpose | Flood-related agricultural damage assessment |
| Target Users | Myanmar farmers, local aid workers, field verifiers |
| MVP Scope | Flood damage only (earthquake, cyclone = future) |

## Directory Structure

```
safefarm/
├── app.py                    # Streamlit entry point
├── requirements.txt          # Python dependencies
├── config.py                 # App configuration, paths, constants
├── lang/
│   ├── en.py                 # English strings
│   └── my.py                 # Myanmar strings
├── model/
│   ├── checkpoint.pt         # ResNet18 trained weights
│   ├── inference.py          # Load model, predict, Grad-CAM
│   └── gradcam.py            # Grad-CAM implementation
├── utils/
│   ├── image.py              # Pillow preprocessing, validation
│   ├── report.py             # ReportLab PDF generation
│   ├── priority.py           # Support priority score calculator
│   └── fonts/
│       └── NotoSansMyanmar.ttf  # Bundled Myanmar font
├── data/
│   ├── train/
│   │   ├── low/
│   │   ├── medium/
│   │   ├── high/
│   │   └── unknown/
│   └── test_myanmar/         # 6-9 demo test images
├── samples/                  # Sample images for demo
└── assets/
    └── logo.png              # App logo
```

## Module Responsibilities

| Module | File | Responsibility |
|--------|------|----------------|
| Entry | `app.py` | Page routing, session state, language toggle |
| Config | `config.py` | Paths, class labels, color map, default weights |
| Language | `lang/*.py` | Bilingual string dictionaries |
| Model | `model/inference.py` | Load checkpoint, preprocess, predict |
| Grad-CAM | `model/gradcam.py` | Generate attention overlay |
| Image | `utils/image.py` | Open, resize, RGB convert, validate |
| Report | `utils/report.py` | Build bilingual PDF with ReportLab |
| Priority | `utils/priority.py` | Calculate support priority score |

## Data Flow

```
User Upload → image.py (validate/resize) → inference.py (predict)
                                                ↓
                                          gradcam.py (overlay)
                                                ↓
                                    ┌───────────┴───────────┐
                                    ↓                       ↓
                              Result Card              priority.py
                              (Streamlit)              (score calc)
                                    ↓                       ↓
                              language.py              report.py
                              (translate)              (PDF gen)
                                    └───────────┬───────────┘
                                                ↓
                                          Download PDF
```

## Configuration Constants

```python
# config.py
CLASSES = ["low", "medium", "high", "unknown"]
CLASS_COLORS = {
    "low": "#4CAF50",       # Green
    "medium": "#FF9800",    # Orange
    "high": "#F44336",      # Red
    "unknown": "#9E9E9E",   # Gray
}
MODEL_INPUT_SIZE = (224, 224)
MODEL_MEAN = [0.485, 0.456, 0.406]
MODEL_STD = [0.229, 0.224, 0.225]
MAX_UPLOAD_SIZE_MB = 10
SUPPORTED_FORMATS = ["jpg", "jpeg", "png"]
```

## Session State Keys

| Key | Type | Purpose |
|-----|------|---------|
| `lang` | str | "en" or "my" |
| `uploaded_image` | Image | Current uploaded farm photo |
| `prediction` | dict | Class, confidence, gradcam_path |
| `form_data` | dict | Region, crop, area, flood days, etc. |
| `priority_score` | float | Calculated support priority |

## Error Handling Strategy

| Error | Handler |
|-------|---------|
| No model checkpoint | Show warning: "Demo mode — results are illustrative" |
| Invalid image format | Block upload, show supported formats |
| Image too large | Block upload, show max size |
| Blurry/dark image | Show quality warning, still allow classification |
| Myanmar font missing | Fall back to system font, warn in console |
| PDF generation fails | Show error, offer raw data download |
