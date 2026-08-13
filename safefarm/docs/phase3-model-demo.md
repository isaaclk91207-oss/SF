---
kind: spec
title: Phase 3 - Model & Demo Mode (Step-by-Step Guide)
---

# Phase 3: Model & Demo Mode — Step-by-Step Guide

**Goal:** Add model inference with demo fallback when no checkpoint exists

**Duration:** Day 3 (3-4 hours)

---

## What This Phase Does

```
Before Phase 3:
  Upload Image → Show placeholder → "Demo mode"

After Phase 3:
  Upload Image → Model Prediction → Show result card with:
    - Damage level (Low/Medium/High/Unknown)
    - Confidence score
    - Probability breakdown
    - Color coding
    - Recommendations
```

---

## Current State (Before Phase 3)

```
safefarm/
├── app.py               ← Has image upload, shows placeholder
├── config.py            ← Has CLASSES, CLASS_COLORS
├── lang/en.py           ← Has result strings
├── lang/my.py           ← Has result strings
├── utils/image.py       ← Image pipeline works
├── model/__init__.py    ← Empty
└── model/checkpoint.pt  ← MISSING (no trained model)
```

---

## Target State (After Phase 3)

```
safefarm/
├── app.py               ← Updated with model integration
├── config.py            ← unchanged
├── lang/en.py           ← unchanged
├── lang/my.py           ← unchanged
├── utils/image.py       ← unchanged
├── model/
│   ├── __init__.py      ← unchanged
│   ├── inference.py     ← NEW: Model + demo prediction
│   └── checkpoint.pt    ← (optional, triggers real model)
```

---

## Step 1: Create model/inference.py

**What to do:** Create a new file `model/inference.py`

**Purpose:** This file handles:
- Building ResNet18 model architecture
- Loading checkpoint if it exists
- Making predictions (real or demo)
- Generating realistic demo results

**What to include in the file:**

```
1. Imports
   - os, random, torch, torch.nn, torch.nn.functional
   - torchvision.models (for ResNet18)
   - PIL.Image
   - config (CLASSES, MODEL_PATH, etc.)

2. build_model() function
   - Creates ResNet18 with pretrained weights
   - Replaces final FC layer for 4 classes
   - Returns model

3. load_checkpoint() function
   - Checks if checkpoint.pt exists
   - Loads model weights if found
   - Returns model or None

4. get_transform() function
   - Returns image transform pipeline
   - Resize to 224x224
   - Convert to tensor
   - Normalize with ImageNet values

5. FarmDamageClassifier class
   - __init__: Try to load real model, set demo mode if not found
   - predict(): Route to demo or real prediction
   - _demo_predict(): Random weighted prediction
   - _real_predict(): Actual model inference
   - get_model_info(): Return status

6. get_classifier() function
   - Returns singleton classifier instance

7. predict_image() function
   - Convenience wrapper for prediction
```

---

## Step 2: Update app.py

**What to do:** Replace the entire app.py with updated version

**Purpose:** This file now handles:
- Model status display in sidebar
- Form submission triggers prediction
- Result card shows prediction
- Color coding by damage level
- Recommendations based on severity

**What to change in app.py:**

```
1. Add new imports
   - from model.inference import get_classifier, predict_image

2. Add new session state
   - st.session_state.prediction = None

3. Add render_model_status() function
   - Shows model status in sidebar
   - Demo mode: yellow warning
   - Real model: green success

4. Update render_result_card() function
   - Now takes prediction parameter
   - Shows damage level with color
   - Shows confidence percentage
   - Shows probability breakdown (4 classes)
   - Shows recommendations

5. Update render_image_upload() function
   - Now returns image for prediction

6. Update main() function
   - Handle form submission
   - Call predict_image() on submit
   - Pass prediction to result card
```

---

## Step 3: Test the App

**What to do:** Run the app and verify

```powershell
cd D:\demo-hackathon-v2\safefarm
venv\Scripts\activate
streamlit run app.py
```

**What to check:**

```
1. App opens at http://localhost:8501
2. Sidebar shows "Demo Mode" warning
3. Upload an image
4. Fill form fields
5. Click "Assess Damage"
6. Result card appears with:
   - Damage level (Low/Medium/High/Unknown)
   - Confidence score (e.g., 78.3%)
   - Probability breakdown (4 numbers)
   - Color coding (Green/Orange/Red/Gray)
   - Recommendations
7. Switch language to မြန်မာ
8. All labels update
9. No errors in terminal
```

---

## Expected Results

### Demo Mode (No Checkpoint)

```
┌─────────────────────────────────────────────────────┐
│ Sidebar:                                            │
│   ⚠️ Demo mode — results are illustrative only      │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ 📊 Assessment Result                                │
│                                                     │
│ ⚠️ Demo mode — results are illustrative only        │
│                                                     │
│ ┌───────────────────────────────────────────────┐   │
│ │ Damage Level: Medium Damage                   │   │
│ │                                               │   │
│ │ Confidence: 78.3%                             │   │
│ └───────────────────────────────────────────────┘   │
│                                                     │
│ Low: 12.1% | Medium: 78.3% | High: 6.2% | Unknown: 3.4% │
│                                                     │
│ Recommended Actions:                                │
│ 🟠 Replanting support for next season               │
│ 🟠 Crop insurance claim processing                  │
└─────────────────────────────────────────────────────┘
```

### Real Model (With Checkpoint)

```
┌─────────────────────────────────────────────────────┐
│ Sidebar:                                            │
│   ✅ Model: ResNet18                                │
│   Device: cpu                                       │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ 📊 Assessment Result                                │
│                                                     │
│ ┌───────────────────────────────────────────────┐   │
│ │ Damage Level: High Damage                     │   │
│ │                                               │   │
│ │ Confidence: 91.2%                             │   │
│ └───────────────────────────────────────────────┘   │
│                                                     │
│ Low: 2.1% | Medium: 5.3% | High: 91.2% | Unknown: 1.4% │
│                                                     │
│ Recommended Actions:                                │
│ 🔴 Prioritize urgent assistance                     │
│ 🔴 Emergency food assistance                        │
└─────────────────────────────────────────────────────┘
```

---

## Key Concepts

### Demo Mode

```
What: Random predictions when no model exists
Why:  Allows testing UI without trained model
How:  Weighted random selection (realistic distribution)

Distribution:
  Low:    30% chance
  Medium: 35% chance
  High:   20% chance
  Unknown: 15% chance
```

### Real Model

```
What: Actual ResNet18 inference
Why:  Real predictions when checkpoint exists
How:  Load weights, run forward pass, softmax

Requirements:
  - model/checkpoint.pt must exist
  - PyTorch installed
  - ~45MB model size
```

### Color Coding

```
Low:     Green (#4CAF50)   — Continue monitoring
Medium:  Orange (#FF9800)  — Arrange recovery
High:    Red (#F44336)     — Prioritize urgent
Unknown: Gray (#9E9E9E)    — Request verification
```

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| "No module named model" | Wrong directory | Run from `safefarm/` folder |
| Model fails to load | Corrupted checkpoint | Delete checkpoint.pt, use demo mode |
| Prediction always same | Random seed | Restart app |
| Colors not showing | Missing CLASS_COLORS | Check config.py |

---

## Files Summary

| File | Action | Lines | Purpose |
|------|--------|-------|---------|
| `model/inference.py` | CREATE | ~120 | Model + demo prediction |
| `app.py` | REPLACE | ~150 | Updated with model integration |

---

## Verification Checklist

| # | Check | Expected |
|---|-------|----------|
| 1 | `model/inference.py` exists | File created |
| 2 | `app.py` updated | New imports, functions |
| 3 | App launches | No errors |
| 4 | Sidebar shows status | "Demo Mode" warning |
| 5 | Upload works | Image displays |
| 6 | Assess button works | Result appears |
| 7 | Result card shows | Damage + confidence |
| 8 | Probabilities show | 4 values |
| 9 | Colors correct | Green/Orange/Red/Gray |
| 10 | Recommendations show | Based on damage |
| 11 | Language toggle works | Labels update |
| 12 | No errors | Clean terminal |

---

## Ready to Implement?

Follow these steps:
1. Create `model/inference.py` with content from Step 1
2. Replace `app.py` with content from Step 2
3. Test with `streamlit run app.py`
4. Verify all checklist items

---

**Questions before starting?**
