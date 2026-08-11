---
kind: spec
title: SafeFarm Myanmar - UI Plan
---

# SafeFarm Myanmar - UI Plan

## Application Layout

```
┌─────────────────────────────────────────────────────────┐
│  [Logo] SafeFarm Myanmar          [🌐 EN | မြန်မာ]     │
│  M-Matrix Team                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────┐  ┌─────────────────────────────┐  │
│  │   ASSESSMENT    │  │        RESULT CARD           │  │
│  │     FORM        │  │                             │  │
│  │                 │  │  [Image]  [Grad-CAM]        │  │
│  │  Region: [   ]  │  │                             │  │
│  │  Township: [ ]  │  │  Damage: ████████ HIGH      │  │
│  │  Village: [  ]  │  │  Confidence: 87%            │  │
│  │  Crop: [    ]   │  │  Priority Score: 78/100     │  │
│  │  Area: [   ]    │  │                             │  │
│  │  Flood Days: [ ]│  │  [📥 Download PDF Report]   │  │
│  │  Urgent: [ ]    │  │                             │  │
│  │                 │  │  ⚠️ Disclaimer text...       │  │
│  │  [📤 Upload]    │  │                             │  │
│  │  [🔍 Assess]    │  └─────────────────────────────┘  │
│  └─────────────────┘                                    │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │  ℹ️ This is a preliminary assessment...          │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## Streamlit Pages

### Single-Page App (MVP)

All content in `app.py` using `st.columns` for layout:

```python
# app.py structure
def main():
    init_session_state()
    render_header()          # Logo, title, language toggle
    
    col_form, col_result = st.columns([1, 1])
    
    with col_form:
        render_assessment_form()
    
    with col_result:
        render_result_card()
    
    render_disclaimer()
```

## Header Component

```python
def render_header():
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.image("assets/logo.png", width=40)
        st.title("SafeFarm Myanmar")
        st.caption("M-Matrix Team")
    
    with col2:
        lang = st.radio(
            "Language",
            ["English", "မြန်မာ"],
            horizontal=True,
            label_visibility="collapsed"
        )
        st.session_state.lang = "en" if lang == "English" else "my"
```

## Assessment Form

### Form Fields

| Field | Widget | Options | Required |
|-------|--------|---------|----------|
| Region | `st.selectbox` | 7 regions of Myanmar | Yes |
| Township | `st.text_input` | Free text | Yes |
| Village | `st.text_input` | Free text | No |
| Farm Location | `st.text_input` | GPS or description | No |
| Crop Type | `st.selectbox` | Rice, Corn, Sesame, Pulses, Other | Yes |
| Farm Area | `st.number_input` | 0.1 - 1000 (acres) | Yes |
| Flood Days | `st.number_input` | 1 - 90 | Yes |
| Growth Stage | `st.selectbox` | Seedling, Vegetative, Flowering, Harvest, Post-harvest | Yes |
| Urgent Support | `st.checkbox` | Yes/No | No |
| Photo Upload | `st.file_uploader` | jpg, png | Yes |

### Region Options (Myanmar)

```python
REGIONS = [
    "Ayeyarwady",
    "Bago",
    "Chin",
    "Kachin",
    "Kayah",
    "Kayin",
    "Magway",
    "Mandalay",
    "Mon",
    "Naypyidaw",
    "Rakhine",
    "Sagaing",
    "Shan",
    "Tanintharyi",
    "Yangon"
]
```

### Crop Type Options

```python
CROPS = {
    "en": ["Rice", "Corn", "Sesame", "Pulses", "Other"],
    "my": ["စပါး", "ပြောင်း", "နှမ်း", "ပဲ", "အခြား"]
}
```

## Result Card

### Damage Level Display

```python
def render_damage_level(damage_class, confidence):
    colors = {
        "low": ("#4CAF50", "🟢"),
        "medium": ("#FF9800", "🟠"),
        "high": ("#F44336", "🔴"),
        "unknown": ("#9E9E9E", "⚪")
    }
    
    color, icon = colors[damage_class]
    
    st.markdown(f"""
    <div style="background-color: {color}20; border-left: 4px solid {color}; padding: 16px; border-radius: 4px;">
        <h3 style="color: {color}; margin: 0;">
            {icon} Damage Level: {damage_class.upper()}
        </h3>
        <p style="margin: 4px 0 0 0;">Confidence: {confidence:.1%}</p>
    </div>
    """, unsafe_allow_html=True)
```

### Grad-CAM Display

```python
def render_gradcam(gradcam_path, original_image):
    if gradcam_path:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Original")
            st.image(original_image, use_column_width=True)
        with col2:
            st.subheader("Model Attention (Grad-CAM)")
            st.image(gradcam_path, use_column_width=True)
    else:
        st.info("Grad-CAM not available for demo mode")
```

### Priority Score Display

```python
def render_priority_score(score):
    # Score: 0-100
    if score >= 70:
        color = "#F44336"
        label = "High Priority"
    elif score >= 40:
        color = "#FF9800"
        label = "Medium Priority"
    else:
        color = "#4CAF50"
        label = "Low Priority"
    
    st.progress(score / 100)
    st.markdown(f"**{label}** — Score: {score}/100")
```

## Form Validation

```python
def validate_form(form_data, uploaded_image):
    errors = []
    
    if not uploaded_image:
        errors.append("Please upload a farm photo")
    
    if not form_data.get("region"):
        errors.append("Please select a region")
    
    if not form_data.get("township"):
        errors.append("Please enter a township")
    
    if not form_data.get("crop_type"):
        errors.append("Please select a crop type")
    
    if form_data.get("farm_area", 0) <= 0:
        errors.append("Farm area must be greater than 0")
    
    if form_data.get("flood_days", 0) <= 0:
        errors.append("Flood days must be at least 1")
    
    return errors
```

## Image Quality Warnings

```python
def check_image_quality(image):
    warnings = []
    
    # Check brightness
    import numpy as np
    img_array = np.array(image.convert("L"))
    mean_brightness = img_array.mean()
    
    if mean_brightness < 30:
        warnings.append("Image is very dark — results may be less accurate")
    
    if mean_brightness > 220:
        warnings.append("Image is overexposed — results may be less accurate")
    
    # Check blur (Laplacian variance)
    import cv2
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    if laplacian_var < 100:
        warnings.append("Image appears blurry — results may be less accurate")
    
    return warnings
```

## Language Toggle

### English Strings

```python
# lang/en.py
STRINGS = {
    "app_title": "SafeFarm Myanmar",
    "team_name": "M-Matrix Team",
    "language": "Language",
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
    "result_title": "Assessment Result",
    "damage_level": "Damage Level",
    "confidence": "Confidence",
    "priority_score": "Support Priority Score",
    "download_pdf": "Download PDF Report",
    "disclaimer": "This result is a preliminary assessment based on the uploaded image and user-provided information. It is not an official damage assessment, compensation decision, or substitute for field verification.",
    "image_too_dark": "Image is very dark",
    "image_blurry": "Image appears blurry",
    "model_demo": "Demo mode — results are illustrative only",
}
```

### Myanmar Strings

```python
# lang/my.py
STRINGS = {
    "app_title": "SafeFarm Myanmar",
    "team_name": "M-Matrix အဖွဲ့",
    "language": "ဘာသာစကား",
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
    "result_title": "အကဲဖြတ်ချက် ရလဒ်",
    "damage_level": "ထိခိုက်မှု အဆင့်",
    "confidence": "ယုံကြည်မှု",
    "priority_score": "အကူအညီ ဦးစားပေး အဆင့်",
    "download_pdf": "PDF အစီရင်ခံစာ ဒေါင်းလုဒ်",
    "disclaimer": "ဤရလဒ်သည် တင်သွင်းထားသည့် ဓာတ်ပုံနှင့် အသုံးပြုသူ ပေးထားသည့် အချက်အလက်များအပေါ် အခြေခံထားသည့် ကြိုတင်အကဲဖြတ်ချက်တစ်ခုဖြစ်ပါသည်။ ၎င်းသည် တရားဝင် ထိခိုက်မှု အကဲဖြတ်ချက်၊ လျော်ကြေး ဆုံးဖြတ်ချက် သို့မဟုတ် ကွင်းဆင်း စစ်ဆေးမှုနေရာတွင် အစားထိုးနိုင်သည့် အရာ မဟုတ်ပါ။",
    "image_too_dark": "ဓာတ်ပုံသည် အလွန်မှောင်နေသည်",
    "image_blurry": "ဓာတ်ပုံသည် မှုန်နေသည်",
    "model_demo": "Demo mode — ရလဒ်များသည် ရှင်းလင်းပြသရန်သာဖြစ်သည်",
}
```

## Responsive Layout

```python
# Mobile-friendly layout
st.set_page_config(
    page_title="SafeFarm Myanmar",
    page_icon="🌾",
    layout="wide",  # or "centered" for mobile
    initial_sidebar_state="collapsed"
)

# Custom CSS for better mobile display
st.markdown("""
<style>
    .stButton > button {
        width: 100%;
    }
    .stSelectbox > div {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)
```

## Error States

| State | Display |
|-------|---------|
| No image uploaded | Red border on upload area, message: "Please upload a photo" |
| Invalid format | Error: "Supported formats: JPG, PNG" |
| Image too large | Error: "Maximum file size: 10MB" |
| Model not loaded | Warning banner: "Demo mode — results are illustrative" |
| All fields empty | Validation errors listed below form |
| Network error (online) | "Connection lost. Working in offline mode." |

## Success States

| State | Display |
|-------|---------|
| Assessment complete | Green result card with damage level |
| PDF generated | Download button appears |
| Language switched | All labels update instantly |
