---
kind: spec
title: SafeFarm Myanmar - Technical Plan
---

# SafeFarm Myanmar - Technical Plan

## Project Overview

| Field | Value |
|-------|-------|
| Product Name | SafeFarm Myanmar |
| Team Name | M-Matrix |
| Purpose | Flood-related agricultural damage assessment |
| Target Users | Myanmar farmers, local aid workers, field verifiers |
| MVP Scope | Flood damage only (earthquake, cyclone = future) |
| Tech Stack | Python 3.10, Streamlit, PyTorch, ReportLab |

## Technical Architecture

### System Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Streamlit App                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   Language    │    │    Form      │    │   Result     │      │
│  │   Toggle      │    │   Handler    │    │   Display    │      │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘      │
│         │                   │                   │                │
│         └───────────────────┼───────────────────┘                │
│                             │                                    │
│                    ┌────────▼────────┐                           │
│                    │  Session State  │                           │
│                    └────────┬────────┘                           │
│                             │                                    │
│         ┌───────────────────┼───────────────────┐                │
│         │                   │                   │                │
│  ┌──────▼───────┐    ┌──────▼───────┐    ┌──────▼───────┐      │
│  │    Image     │    │    Model     │    │   Priority   │      │
│  │  Pipeline    │    │  Inference   │    │   Calculator │      │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘      │
│         │                   │                   │                │
│         └───────────────────┼───────────────────┘                │
│                             │                                    │
│                    ┌────────▼────────┐                           │
│                    │   Report Gen    │                           │
│                    │   (PDF/CSV)     │                           │
│                    └─────────────────┘                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Module Dependency Graph

```
app.py
  ├── config.py
  ├── lang/en.py, lang/my.py
  ├── utils/image.py
  ├── model/inference.py
  │   └── model/gradcam.py
  ├── utils/priority.py
  └── utils/report.py
```

## Implementation Phases

### Phase 1: Project Scaffolding (Day 1)

**Goal:** Basic project structure, app launches

| Task | File | Status |
|------|------|--------|
| Create directory structure | All folders | |
| Create `config.py` | Constants, paths | |
| Create `lang/en.py` | English strings | |
| Create `lang/my.py` | Myanmar strings | |
| Create `app.py` | Basic Streamlit page | |
| Create `requirements.txt` | Dependencies | |
| Create `utils/__init__.py` | Package init | |
| Create `model/__init__.py` | Package init | |
| Create `lang/__init__.py` | Package init | |

**Files to Create:**

```
safefarm/
├── __init__.py
├── config.py
├── lang/
│   ├── __init__.py
│   ├── en.py
│   └── my.py
├── model/
│   └── __init__.py
├── utils/
│   └── __init__.py
└── app.py
```

### Phase 2: Image Pipeline (Day 2)

**Goal:** Image upload, validation, preprocessing

| Task | File | Status |
|------|------|--------|
| Image validation | `utils/image.py` | |
| Format checking | `utils/image.py` | |
| Size checking | `utils/image.py` | |
| Quality checks (dark, blurry) | `utils/image.py` | |
| Preprocessing pipeline | `utils/image.py` | |
| Upload widget | `app.py` | |
| Image preview | `app.py` | |

**Key Functions:**

```python
# utils/image.py
def validate_image(uploaded_file) -> dict
def preprocess_image(image) -> torch.Tensor
def check_image_quality(image) -> list[str]
def get_image_info(image) -> dict
```

### Phase 3: Model & Demo Mode (Day 3)

**Goal:** Model inference or demo predictions

| Task | File | Status |
|------|------|--------|
| ResNet18 architecture | `model/inference.py` | |
| Demo mode (random predictions) | `model/inference.py` | |
| Model loading | `model/inference.py` | |
| Prediction pipeline | `model/inference.py` | |
| Probability output | `model/inference.py` | |
| Checkpoint loading | `model/inference.py` | |

**Key Functions:**

```python
# model/inference.py
def build_model(num_classes=4) -> nn.Module
def load_checkpoint(path) -> dict
def predict(image, model) -> dict
def demo_predict(image) -> dict
```

### Phase 4: Grad-CAM Integration (Day 4)

**Goal:** Visual attention overlay

| Task | File | Status |
|------|------|--------|
| Grad-CAM class | `model/gradcam.py` | |
| Hook registration | `model/gradcam.py` | |
| CAM generation | `model/gradcam.py` | |
| Overlay visualization | `model/gradcam.py` | |
| Display in UI | `app.py` | |

**Key Functions:**

```python
# model/gradcam.py
class GradCAM:
    def __init__(self, model, target_layer)
    def generate(self, input_tensor, target_class) -> np.ndarray

def overlay_gradcam(original, cam, alpha=0.4) -> Image
def save_gradcam(image, path) -> str
```

### Phase 5: Bilingual System (Day 5)

**Goal:** Language toggle, string lookup

| Task | File | Status |
|------|------|--------|
| English strings | `lang/en.py` | |
| Myanmar strings | `lang/my.py` | |
| String lookup function | `config.py` | |
| Language toggle widget | `app.py` | |
| Session state update | `app.py` | |

**Key Functions:**

```python
# config.py
def get_string(key, lang="en") -> str
def get_all_strings(lang="en") -> dict
```

### Phase 6: Priority Score (Day 6)

**Goal:** Support priority calculation

| Task | File | Status |
|------|------|--------|
| Score calculator | `utils/priority.py` | |
| Component scores | `utils/priority.py` | |
| Weight configuration | `utils/priority.py` | |
| Recommendations | `utils/priority.py` | |
| Display in UI | `app.py` | |

**Key Functions:**

```python
# utils/priority.py
def calculate_priority(damage, area, flood_days, growth, urgent) -> float
def get_priority_label(score) -> str
def get_recommendations(damage, score, urgent) -> list[str]
```

### Phase 7: PDF Report (Day 7)

**Goal:** Bilingual PDF generation

| Task | File | Status |
|------|------|--------|
| Font registration | `utils/report.py` | |
| Report builder | `utils/report.py` | |
| PDF layout | `utils/report.py` | |
| Download button | `app.py` | |
| Error handling | `utils/report.py` | |

**Key Functions:**

```python
# utils/report.py
def register_fonts() -> bool
class ReportBuilder:
    def build_report(data, output_path) -> str
    def _get_string(key) -> str
    def _get_recommendations(damage, data) -> list[str]
```

### Phase 8: Form & Result Card (Day 8)

**Goal:** Complete UI with validation

| Task | File | Status |
|------|------|--------|
| Assessment form | `app.py` | |
| Form validation | `app.py` | |
| Result card | `app.py` | |
| Error states | `app.py` | |
| Success states | `app.py` | |
| Disclaimer | `app.py` | |

### Phase 9: Testing & Polish (Day 9)

**Goal:** Bug fixes, edge cases

| Task | File | Status |
|------|------|--------|
| Test all features | All | |
| Fix image upload edge cases | `utils/image.py` | |
| Fix PDF generation edge cases | `utils/report.py` | |
| Fix Myanmar text rendering | `utils/report.py` | |
| Mobile responsiveness | `app.py` | |
| Performance optimization | All | |

### Phase 10: Deployment (Day 10)

**Goal:** GitHub, HF Spaces, demo video

| Task | File | Status |
|------|------|--------|
| GitHub repo setup | `.gitignore`, `README.md` | |
| HF Spaces config | `Dockerfile`, `README.md` | |
| Landing page | `docs/landing-page.html` | |
| Demo video recording | `docs/demo-video.mp4` | |
| Screenshots | `docs/screenshots/` | |

## Technology Stack

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | >=1.28.0 | Web interface |
| torch | >=2.0.0 | ML framework |
| torchvision | >=0.15.0 | Image models |
| Pillow | >=10.0.0 | Image processing |
| reportlab | >=4.0.0 | PDF generation |
| numpy | >=1.24.0 | Numerical ops |
| opencv-python | >=4.8.0 | Image quality checks |

### System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Python | 3.10 | 3.10+ |
| RAM | 4GB | 8GB |
| Disk | 500MB | 2GB |
| CPU | Any | Multi-core |

## Data Flow

### Upload → Result Flow

```
1. User uploads image
   └→ utils/image.py: validate_image()

2. User fills form
   └→ app.py: collect form data

3. User clicks "Assess"
   └→ utils/image.py: preprocess_image()
   └→ model/inference.py: predict()
   └→ model/gradcam.py: generate()
   └→ utils/priority.py: calculate_priority()

4. Result displayed
   └→ app.py: render_result_card()

5. User downloads PDF
   └→ utils/report.py: build_report()
```

### Session State Keys

| Key | Type | Description |
|-----|------|-------------|
| `lang` | str | "en" or "my" |
| `uploaded_image` | PIL.Image | Current image |
| `prediction` | dict | Model output |
| `form_data` | dict | Assessment form |
| `priority_score` | float | Calculated score |
| `report_path` | str | Generated PDF path |

## Configuration

### config.py

```python
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Paths
MODEL_PATH = os.path.join(BASE_DIR, "model", "checkpoint.pt")
FONT_PATH = os.path.join(BASE_DIR, "utils", "fonts", "NotoSansMyanmar.ttf")
SAMPLES_DIR = os.path.join(BASE_DIR, "data", "test_myanmar")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
TEMP_DIR = os.path.join(BASE_DIR, "temp")

# Classes
CLASSES = ["low", "medium", "high", "unknown"]
CLASS_COLORS = {
    "low": "#4CAF50",
    "medium": "#FF9800",
    "high": "#F44336",
    "unknown": "#9E9E9E",
}

# Model
MODEL_INPUT_SIZE = (224, 224)
MODEL_MEAN = [0.485, 0.456, 0.406]
MODEL_STD = [0.229, 0.224, 0.225]
NUM_CLASSES = 4

# Upload
MAX_UPLOAD_SIZE_MB = 10
SUPPORTED_FORMATS = ["jpg", "jpeg", "png"]

# Priority weights
PRIORITY_WEIGHTS = {
    "damage": 0.35,
    "area": 0.20,
    "flood_days": 0.20,
    "growth_stage": 0.15,
    "urgent": 0.10
}
```

## Error Handling

| Error | Location | Handler |
|-------|----------|---------|
| No model checkpoint | `model/inference.py` | Demo mode fallback |
| Invalid image format | `utils/image.py` | Reject upload |
| Image too large | `utils/image.py` | Reject upload |
| Corrupted image | `utils/image.py` | Reject upload |
| Dark image | `utils/image.py` | Warning tag |
| Blurry image | `utils/image.py` | Warning tag |
| Myanmar font missing | `utils/report.py` | Fall back to Helvetica |
| PDF generation fails | `utils/report.py` | Show error |

## Testing Strategy

### Unit Tests

| Test | File | Coverage |
|------|------|----------|
| Image validation | `tests/test_image.py` | Format, size, quality |
| Preprocessing | `tests/test_image.py` | Resize, normalize |
| Priority calculator | `tests/test_priority.py` | Score calculation |
| Language strings | `tests/test_lang.py` | All keys present |

### Integration Tests

| Test | File | Coverage |
|------|------|----------|
| Full pipeline | `tests/test_pipeline.py` | Upload → Result |
| PDF generation | `tests/test_report.py` | Report creation |
| Demo mode | `tests/test_demo.py` | Fallback behavior |

### Manual Tests

| Test | Steps | Expected |
|------|-------|----------|
| Offline mode | Wi-Fi off, run app | Works without internet |
| Language toggle | Switch EN/MY | All labels update |
| Image upload | Upload JPG/PNG | Preview shows |
| Result card | Click Assess | Damage level displays |
| Grad-CAM | Upload image | Overlay shows |
| PDF download | Click download | File saves |
| Myanmar PDF | Open PDF | Text renders correctly |

## Performance Targets

| Metric | Target | Notes |
|--------|--------|-------|
| App launch | < 3s | First load |
| Image upload | < 1s | Preview display |
| Inference | < 500ms | CPU only |
| Grad-CAM | < 1s | Overlay generation |
| PDF generation | < 2s | Single page |
| Memory usage | < 500MB | Runtime |

## Security Considerations

| Concern | Mitigation |
|---------|------------|
| File upload | Validate format, size, content |
| Temp files | Clean up after use |
| Model loading | Check file integrity |
| User data | No server storage |
| Network | No external API calls |

## Deployment Checklist

### Local Offline

- [ ] Python 3.10 installed
- [ ] All packages installed
- [ ] Model checkpoint present
- [ ] Myanmar font bundled
- [ ] Sample images available
- [ ] App launches on localhost:8501
- [ ] All features work offline

### Hugging Face Spaces

- [ ] Dockerfile created
- [ ] requirements.txt complete
- [ ] Space configuration set
- [ ] App launches on Space
- [ ] Online label displayed
- [ ] No sensitive data exposed

### GitHub Repository

- [ ] .gitignore configured
- [ ] README.md complete
- [ ] License file added
- [ ] No secrets committed
- [ ] Documentation updated

## Future Enhancements

| Feature | Priority | Effort |
|---------|----------|--------|
| Multi-language (Chinese, Thai) | Medium | 2 days |
| Batch upload | Low | 1 day |
| CSV export | Medium | 1 day |
| User authentication | Low | 3 days |
| Database storage | Medium | 2 days |
| Mobile app | Low | 5 days |
| Satellite image support | High | 3 days |
| Earthquake damage | Medium | 2 days |
| Cyclone damage | Medium | 2 days |
| Real-time monitoring | Low | 5 days |
