---
kind: spec
title: Phase 5 - Bilingual System (Completed)
---

# Phase 5: Bilingual System

**Status:** ✅ Already Complete (implemented in Phase 1)

**Duration:** Day 5 (completed early)

---

## What This Phase Does

```
User clicks "English" → All labels show in English
User clicks "မြန်မာ"  → All labels show in Myanmar
```

---

## How It Works

### Language Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Radio      │     │  Session     │     │  String      │
│   Button     │────▶│  State       │────▶│  Lookup      │
│              │     │  .lang       │     │              │
└──────────────┘     └──────────────┘     └──────────────┘
     "English"           "en"              get_string(key, "en")
     "မြန်မာ"           "my"              get_string(key, "my")
```

### Components

| # | File | Purpose | Lines |
|---|------|---------|-------|
| 1 | `lang/en.py` | English string dictionary | 47 strings |
| 2 | `lang/my.py` | Myanmar string dictionary | 47 strings |
| 3 | `config.py` | `get_string()` lookup function | 15 lines |
| 4 | `app.py` | Language toggle widget + `t()` helper | 20 lines |

---

## Files Detail

### 1. `lang/en.py` — English Strings

```python
STRINGS = {
    "app_title": "SafeFarm Myanmar",
    "team_name": "M-Matrix Team",
    "tagline": "Flood Damage Assessment for Myanmar Agriculture",
    "form_title": "Farm Assessment Form",
    "region": "Region",
    "township": "Township",
    "village": "Village",
    "crop_type": "Crop Type",
    "farm_area": "Farm Area (acres)",
    "flood_days": "Number of Flood Days",
    "upload_photo": "Upload Farm Photo",
    "assess_button": "Assess Damage",
    "result_title": "Assessment Result",
    "damage_level": "Damage Level",
    "confidence": "Confidence",
    "low": "Low Damage",
    "medium": "Medium Damage",
    "high": "High Damage",
    "unknown": "Unknown",
    "disclaimer": "This result is a preliminary assessment...",
    # ... 47 total strings
}
```

### 2. `lang/my.py` — Myanmar Strings

```python
STRINGS = {
    "app_title": "SafeFarm Myanmar",
    "team_name": "M-Matrix အဖွဲ့",
    "tagline": "မြန်မာ့စိုက်ပျိုးရေးအတွက် ရေကြီးထိခိုက်မှု အကဲဖြတ်ချက်",
    "form_title": "စိုက်ခင်း အကဲဖြတ်ချက် ဖောင်",
    "region": "ဒေသ",
    "township": "မြို့နယ်",
    "village": "ကျေးရွာ",
    "crop_type": "သီးနှံ အမျိုးအစား",
    "farm_area": "စိုက်ခင်း ဧရိယာ (ဧက)",
    "flood_days": "ရေကြီးနေသည့် ရက်အရေအတွက်",
    "upload_photo": "စိုက်ခင်း ဓာတ်ပုံ တင်ပါ",
    "assess_button": "ထိခိုက်မှု အကဲဖြတ်ပါ",
    "result_title": "အကဲဖြတ်ချက် ရလဒ်",
    "damage_level": "ထိခိုက်မှု အဆင့်",
    "confidence": "ယုံကြည်မှု",
    "low": "ထိခိုက်မှု နည်း",
    "medium": "ထိခိုက်မှု အလယ်အလတ်",
    "high": "ထိခိုက်မှု ပြင်းထန်",
    "unknown": "မသိရ",
    "disclaimer": "ဤရလဒ်သည် တင်သွင်းထားသည့် ဓာတ်ပုံနှင့်...",
    # ... 47 total strings
}
```

### 3. `config.py` — String Lookup

```python
def get_string(key, lang="en"):
    """Get localized string by key."""
    from lang.en import STRINGS as EN_STRINGS
    from lang.my import STRINGS as MY_STRINGS
    
    if lang == "my":
        return MY_STRINGS.get(key, EN_STRINGS.get(key, key))
    return EN_STRINGS.get(key, key)
```

### 4. `app.py` — Language Toggle + Helper

```python
# Session state
if "lang" not in st.session_state:
    st.session_state.lang = "en"

# Helper function
def t(key):
    """Helper to get translated string."""
    return get_string(key, st.session_state.lang)

# Language toggle widget
lang = st.radio(
    t("language"),
    [t("lang_en"), t("lang_my")],
    horizontal=True,
    index=1 if st.session_state.lang == "my" else 0
)
st.session_state.lang = "my" if lang == t("lang_my") else "en"
```

---

## String Key Reference

### App Labels

| Key | English | Myanmar |
|-----|---------|---------|
| `app_title` | SafeFarm Myanmar | SafeFarm Myanmar |
| `team_name` | M-Matrix Team | M-Matrix အဖွဲ့ |
| `tagline` | Flood Damage Assessment... | မြန်မာ့စိုက်ပျိုးရေးအတွက်... |

### Form Fields

| Key | English | Myanmar |
|-----|---------|---------|
| `form_title` | Farm Assessment Form | စိုက်ခင်း အကဲဖြတ်ချက် ဖောင် |
| `region` | Region | ဒေသ |
| `township` | Township | မြို့နယ် |
| `village` | Village | ကျေးရွာ |
| `crop_type` | Crop Type | သီးနှံ အမျိုးအစား |
| `farm_area` | Farm Area (acres) | စိုက်ခင်း ဧရိယာ (ဧက) |
| `flood_days` | Number of Flood Days | ရေကြီးနေသည့် ရက်အရေအတွက် |
| `upload_photo` | Upload Farm Photo | စိုက်ခင်း ဓာတ်ပုံ တင်ပါ |
| `assess_button` | Assess Damage | ထိခိုက်မှု အကဲဖြတ်ပါ |

### Results

| Key | English | Myanmar |
|-----|---------|---------|
| `result_title` | Assessment Result | အကဲဖြတ်ချက် ရလဒ် |
| `damage_level` | Damage Level | ထိခိုက်မှု အဆင့် |
| `confidence` | Confidence | ယုံကြည်မှု |
| `low` | Low Damage | ထိခိုက်မှု နည်း |
| `medium` | Medium Damage | ထိခိုက်မှု အလယ်အလတ် |
| `high` | High Damage | ထိခိုက်မှု ပြင်းထန် |
| `unknown` | Unknown | မသိရ |

### Recommendations

| Key | English | Myanmar |
|-----|---------|---------|
| `rec_urgent` | Prioritize urgent assistance | အရေးပေါ် အကူအညီကို ဦးစားပေးပါ |
| `rec_emergency_food` | Emergency food assistance | အရေးပေါ် အစားအစာ အကူအညီ |
| `rec_replanting` | Replanting support... | နောက်ရာသီ ပြန်လည်စိုက်ပျိုးရေး အကူအညီ |
| `rec_monitoring` | Continue monitoring | ဆက်လက်စောင့်ကြည့်ပါ |
| `rec_verify` | Request further verification | နောက်ထပ် အတည်ပြုရန် တောင်းဆိုပါ |

---

## Adding New Strings

### Step 1: Add to `lang/en.py`

```python
STRINGS = {
    # ... existing strings
    "new_key": "English Text",
}
```

### Step 2: Add to `lang/my.py`

```python
STRINGS = {
    # ... existing strings
    "new_key": "Myanmar စာသား",
}
```

### Step 3: Use in `app.py`

```python
st.write(t("new_key"))
```

---

## Verification

| # | Check | How |
|---|-------|-----|
| 1 | Language toggle works | Click မြန်မာ, labels change |
| 2 | All form labels translate | Region, Township, Village... |
| 3 | Result labels translate | Damage Level, Confidence... |
| 4 | Recommendations translate | Urgent, Replanting... |
| 5 | Disclaimer translates | Bottom text changes |
| 6 | Toggle back to English | All labels revert |
| 7 | No errors | Clean terminal output |

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Strings show keys | Missing translation | Add key to both lang files |
| Toggle doesn't work | Session state issue | Check `st.session_state.lang` |
| Myanmar text garbled | Font issue | Check Noto Sans Myanmar font |

---

**Status:** ✅ Complete — No action needed. Move to Phase 6 (Priority Score).
