---
kind: spec
title: Phase 1 - Project Scaffolding
---

# Phase 1: Project Scaffolding

**Goal:** Create project structure, app launches on localhost:8501

**Duration:** Day 1 (2-3 hours)

## Current State

```
safefarm/
├── data/
│   ├── train/          (empty)
│   └── test_myanmar/   (empty)
├── docs/               (8 plan files)
├── images/             (8 sample images)
└── model/              (empty)
```

## Target State

```
safefarm/
├── app.py              ← Streamlit entry point
├── requirements.txt    ← Dependencies
├── config.py           ← Constants and paths
├── __init__.py         ← Package init
├── lang/
│   ├── __init__.py
│   ├── en.py           ← English strings
│   └── my.py           ← Myanmar strings
├── model/
│   ├── __init__.py
│   └── checkpoint.pt   ← (later)
├── utils/
│   ├── __init__.py
│   └── fonts/          ← (later)
├── data/
│   ├── train/
│   └── test_myanmar/
├── images/
└── docs/
```

## Tasks

### Task 1: Create Directory Structure

```bash
# Run in D:\demo-hackathon-v2\safefarm
mkdir lang
mkdir utils
mkdir utils\fonts
```

### Task 2: Create Package Init Files

| File | Content |
|------|---------|
| `__init__.py` | `"""SafeFarm Myanmar - Flood Damage Assessment"""` |
| `lang/__init__.py` | `"""Bilingual language support"""` |
| `model/__init__.py` | `"""ML model and inference"""` |
| `utils/__init__.py` | `"""Utility functions"""` |

### Task 3: Create config.py

```python
"""SafeFarm Myanmar - Configuration Constants"""

import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Paths
MODEL_PATH = os.path.join(BASE_DIR, "model", "checkpoint.pt")
FONT_PATH = os.path.join(BASE_DIR, "utils", "fonts", "NotoSansMyanmar.ttf")
SAMPLES_DIR = os.path.join(BASE_DIR, "data", "test_myanmar")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Classes
CLASSES = ["low", "medium", "high", "unknown"]
CLASS_COLORS = {
    "low": "#4CAF50",       # Green
    "medium": "#FF9800",    # Orange
    "high": "#F44336",      # Red
    "unknown": "#9E9E9E",   # Gray
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

# Regions
REGIONS = [
    "Ayeyarwady", "Bago", "Chin", "Kachin", "Kayah",
    "Kayin", "Magway", "Mandalay", "Mon", "Naypyidaw",
    "Rakhine", "Sagaing", "Shan", "Tanintharyi", "Yangon"
]

# Crops
CROPS = {
    "en": ["Rice", "Corn", "Sesame", "Pulses", "Other"],
    "my": ["စပါး", "ပြောင်း", "နှမ်း", "ပဲ", "အခြား"]
}

# Growth stages
GROWTH_STAGES = {
    "en": ["Seedling", "Vegetative", "Flowering", "Harvest", "Post-harvest"],
    "my": ["အပင်ဖြူ", "အရွက်ဖြူ", "ပွင့်ဖူး", "ရိတ်သိမ်း", "ရိတ်ပြီး"]
}

# Language strings lookup
def get_string(key, lang="en"):
    """Get localized string by key."""
    from lang.en import STRINGS as EN_STRINGS
    from lang.my import STRINGS as MY_STRINGS
    
    if lang == "my":
        return MY_STRINGS.get(key, EN_STRINGS.get(key, key))
    return EN_STRINGS.get(key, key)
```

### Task 4: Create lang/en.py

```python
"""English language strings for SafeFarm Myanmar"""

STRINGS = {
    # App
    "app_title": "SafeFarm Myanmar",
    "team_name": "M-Matrix Team",
    "tagline": "Flood Damage Assessment for Myanmar Agriculture",
    
    # Language
    "language": "Language",
    "lang_en": "English",
    "lang_my": "မြန်မာ",
    
    # Form
    "form_title": "Farm Assessment Form",
    "region": "Region",
    "township": "Township",
    "village": "Village",
    "farm_location": "Farm Location",
    "crop_type": "Crop Type",
    "farm_area": "Farm Area (acres)",
    "flood_days": "Number of Flood Days",
    "growth_stage": "Crop Growth Stage",
    "urgent_support": "Urgent Support Needed",
    "upload_photo": "Upload Farm Photo",
    "assess_button": "Assess Damage",
    
    # Result
    "result_title": "Assessment Result",
    "damage_level": "Damage Level",
    "confidence": "Confidence",
    "priority_score": "Support Priority Score",
    "download_pdf": "Download PDF Report",
    
    # Damage levels
    "low": "Low Damage",
    "medium": "Medium Damage",
    "high": "High Damage",
    "unknown": "Unknown",
    
    # Recommendations
    "rec_emergency_food": "Emergency food assistance",
    "rec_insurance": "Crop insurance claim processing",
    "rec_replanting": "Replanting support for next season",
    "rec_monitoring": "Continue monitoring",
    "rec_verify": "Request further verification",
    "rec_urgent": "Prioritize urgent assistance",
    
    # Warnings
    "image_too_dark": "Image is very dark",
    "image_blurry": "Image appears blurry",
    "image_overexposed": "Image is overexposed",
    "image_too_small": "Image is too small",
    "image_too_large": "Image is too large",
    "invalid_format": "Supported formats: JPG, PNG",
    
    # Model
    "model_demo": "Demo mode — results are illustrative only",
    "model_loading": "Loading model...",
    "model_error": "Model could not be loaded",
    
    # Disclaimer
    "disclaimer": "This result is a preliminary assessment based on the uploaded image and user-provided information. It is not an official damage assessment, compensation decision, or substitute for field verification.",
    
    # Priority labels
    "priority_high": "High Priority",
    "priority_medium": "Medium Priority",
    "priority_low": "Low Priority",
    
    # Footer
    "footer_text": "SafeFarm Myanmar © 2026 | Team M-Matrix",
}
```

### Task 5: Create lang/my.py

```python
"""Myanmar language strings for SafeFarm Myanmar"""

STRINGS = {
    # App
    "app_title": "SafeFarm Myanmar",
    "team_name": "M-Matrix အဖွဲ့",
    "tagline": "မြန်မာ့စိုက်ပျိုးရေးအတွက် ရေကြီးထိခိုက်မှု အကဲဖြတ်ချက်",
    
    # Language
    "language": "ဘာသာစကား",
    "lang_en": "English",
    "lang_my": "မြန်မာ",
    
    # Form
    "form_title": "စိုက်ခင်း အကဲဖြတ်ချက် ဖောင်",
    "region": "ဒေသ",
    "township": "မြို့နယ်",
    "village": "ကျေးရွာ",
    "farm_location": "စိုက်ခင်း တည်နေရာ",
    "crop_type": "သီးနှံ အမျိုးအစား",
    "farm_area": "စိုက်ခင်း ဧရိယာ (ဧက)",
    "flood_days": "ရေကြီးနေသည့် ရက်အရေအတွက်",
    "growth_stage": "သီးနှံ ကြီးထွားမှု အဆင့်",
    "urgent_support": "အရေးပေါ် အကူအညီ လိုအပ်",
    "upload_photo": "စိုက်ခင်း ဓာတ်ပုံ တင်ပါ",
    "assess_button": "ထိခိုက်မှု အကဲဖြတ်ပါ",
    
    # Result
    "result_title": "အကဲဖြတ်ချက် ရလဒ်",
    "damage_level": "ထိခိုက်မှု အဆင့်",
    "confidence": "ယုံကြည်မှု",
    "priority_score": "အကူအညီ ဦးစားပေး အဆင့်",
    "download_pdf": "PDF အစီရင်ခံစာ ဒေါင်းလုဒ်",
    
    # Damage levels
    "low": "ထိခိုက်မှု နည်း",
    "medium": "ထိခိုက်မှု အလယ်အလတ်",
    "high": "ထိခိုက်မှု ပြင်းထန်",
    "unknown": "မသိရ",
    
    # Recommendations
    "rec_emergency_food": "အရေးပေါ် အစားအစာ အကူအညီ",
    "rec_insurance": "စိုက်ပျိုးရေး အာမခံ တောင်းဆိုမှု",
    "rec_replanting": "နောက်ရာသီ ပြန်လည်စိုက်ပျိုးရေး အကူအညီ",
    "rec_monitoring": "ဆက်လက်စောင့်ကြည့်ပါ",
    "rec_verify": "နောက်ထပ် အတည်ပြုရန် တောင်းဆိုပါ",
    "rec_urgent": "အရေးပေါ် အကူအညီကို ဦးစားပေးပါ",
    
    # Warnings
    "image_too_dark": "ဓာတ်ပုံသည် အလွန်မှောင်နေသည်",
    "image_blurry": "ဓာတ်ပုံသည် မှုန်နေသည်",
    "image_overexposed": "ဓာတ်ပုံသည် အလင်းပိုနေသည်",
    "image_too_small": "ဓာတ်ပုံသည် အရမ်းသေးနေသည်",
    "image_too_large": "ဓာတ်ပုံသည် အရမ်းကြီးနေသည်",
    "invalid_format": "ပံ့ပိုးထားသည့် ပုံစံများ - JPG, PNG",
    
    # Model
    "model_demo": "Demo mode — ရလဒ်များသည် ရှင်းလင်းပြသရန်သာဖြစ်သည်",
    "model_loading": "မော်ဒယ် ဖွင့်နေသည်...",
    "model_error": "မော်ဒယ်ကို ဖွင့်မတတ်နိုင်ပါ",
    
    # Disclaimer
    "disclaimer": "ဤရလဒ်သည် တင်သွင်းထားသည့် ဓာတ်ပုံနှင့် အသုံးပြုသူ ပေးထားသည့် အချက်အလက်များအပေါ် အခြေခံထားသည့် ကြိုတင်အကဲဖြတ်ချက်တစ်ခုဖြစ်ပါသည်။ ၎င်းသည် တရားဝင် ထိခိုက်မှု အကဲဖြတ်ချက်၊ လျော်ကြေး ဆုံးဖြတ်ချက် သို့မဟုတ် ကွင်းဆင်း စစ်ဆေးမှုနေရာတွင် အစားထိုးနိုင်သည့် အရာ မဟုတ်ပါ။",
    
    # Priority labels
    "priority_high": "ဦးစားပေးမြင့်",
    "priority_medium": "ဦးစားပေးအလယ်အလတ်",
    "priority_low": "ဦးစားပေးနည်း",
    
    # Footer
    "footer_text": "SafeFarm Myanmar © 2026 | M-Matrix အဖွဲ့",
}
```

### Task 6: Create requirements.txt

```
streamlit>=1.28.0
torch>=2.0.0
torchvision>=0.15.0
Pillow>=10.0.0
reportlab>=4.0.0
numpy>=1.24.0
opencv-python>=4.8.0
```

### Task 7: Create app.py

```python
"""SafeFarm Myanmar - Flood Damage Assessment"""

import streamlit as st
from config import get_string, REGIONS, CROPS, GROWTH_STAGES, CLASS_COLORS

# Page config
st.set_page_config(
    page_title="SafeFarm Myanmar",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if "lang" not in st.session_state:
    st.session_state.lang = "en"

def t(key):
    """Helper to get translated string."""
    return get_string(key, st.session_state.lang)

def render_header():
    """Render app header with language toggle."""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.title(f"🌾 {t('app_title')}")
        st.caption(f"{t('team_name')} | {t('tagline')}")
    
    with col2:
        lang = st.radio(
            t("language"),
            [t("lang_en"), t("lang_my")],
            horizontal=True,
            label_visibility="collapsed",
            index=1 if st.session_state.lang == "my" else 0
        )
        st.session_state.lang = "my" if lang == t("lang_my") else "en"

def render_form():
    """Render assessment form."""
    st.subheader(f"📋 {t('form_title')}")
    
    with st.form("assessment_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            region = st.selectbox(t("region"), REGIONS)
            township = st.text_input(t("township"))
            village = st.text_input(t("village"))
            farm_location = st.text_input(t("farm_location"))
        
        with col2:
            crop_type = st.selectbox(t("crop_type"), CROPS[st.session_state.lang])
            farm_area = st.number_input(t("farm_area"), min_value=0.1, max_value=1000.0, value=1.0, step=0.1)
            flood_days = st.number_input(t("flood_days"), min_value=1, max_value=90, value=7, step=1)
            growth_stage = st.selectbox(t("growth_stage"), GROWTH_STAGES[st.session_state.lang])
        
        urgent_support = st.checkbox(t("urgent_support"))
        uploaded_image = st.file_uploader(t("upload_photo"), type=["jpg", "jpeg", "png"])
        
        submitted = st.form_submit_button(t("assess_button"), use_container_width=True)
    
    return {
        "region": region,
        "township": township,
        "village": village,
        "farm_location": farm_location,
        "crop_type": crop_type,
        "farm_area": farm_area,
        "flood_days": flood_days,
        "growth_stage": growth_stage,
        "urgent_support": urgent_support,
        "uploaded_image": uploaded_image,
        "submitted": submitted
    }

def render_result_placeholder():
    """Render result area placeholder."""
    st.subheader(f"📊 {t('result_title')}")
    st.info(t("model_demo"))

def render_disclaimer():
    """Render disclaimer footer."""
    st.divider()
    st.caption(f"⚠️ {t('disclaimer')}")
    st.caption(t("footer_text"))

def main():
    """Main app entry point."""
    render_header()
    
    col_form, col_result = st.columns([1, 1])
    
    with col_form:
        form_data = render_form()
    
    with col_result:
        render_result_placeholder()
    
    render_disclaimer()

if __name__ == "__main__":
    main()
```

### Task 8: Create assets Directory

```bash
mkdir assets
```

### Task 9: Test App Launch

```bash
# Activate environment
venv\Scripts\activate

# Run app
streamlit run app.py
```

Expected: Opens at http://localhost:8501

## Verification Checklist

| # | Check | Expected |
|---|-------|----------|
| 1 | Directory structure created | All folders exist |
| 2 | `config.py` imports work | No errors |
| 3 | `lang/en.py` imports work | No errors |
| 4 | `lang/my.py` imports work | No errors |
| 5 | `app.py` runs | Streamlit launches |
| 6 | Language toggle works | Labels switch |
| 7 | Form renders | All fields visible |
| 8 | No errors in console | Clean output |

## Files to Create

| # | File | Lines | Purpose |
|---|------|-------|---------|
| 1 | `__init__.py` | 1 | Package init |
| 2 | `lang/__init__.py` | 1 | Package init |
| 3 | `lang/en.py` | 65 | English strings |
| 4 | `lang/my.py` | 65 | Myanmar strings |
| 5 | `model/__init__.py` | 1 | Package init |
| 6 | `utils/__init__.py` | 1 | Package init |
| 7 | `config.py` | 60 | Constants |
| 8 | `requirements.txt` | 7 | Dependencies |
| 9 | `app.py` | 95 | Main app |

**Total: 9 files, ~300 lines of code**
