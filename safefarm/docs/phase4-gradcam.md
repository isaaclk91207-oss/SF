---
kind: spec
title: Phase 4 - Grad-CAM Integration (Step-by-Step Guide)
---

# Phase 4: Grad-CAM Integration — Step-by-Step Guide

**Goal:** Add visual attention overlay showing which image regions influenced the model's decision

**Duration:** Day 4 (3-4 hours)

---

## What This Phase Does

```
Before Phase 4:
  Upload Image → Model Prediction → Result Card

After Phase 4:
  Upload Image → Model Prediction → Result Card + Grad-CAM Overlay
                                         ↓
                              Shows "heat map" of model attention
```

---

## Current State (Before Phase 4)

```
safefarm/
├── app.py               ← Shows result card, no visual evidence
├── config.py            ← unchanged
├── lang/en.py           ← unchanged
├── lang/my.py           ← unchanged
├── utils/image.py       ← Image pipeline works
├── model/
│   ├── __init__.py      ← unchanged
│   ├── inference.py     ← Phase 3 complete, no Grad-CAM
│   └── checkpoint.pt    ← (optional)
```

---

## Target State (After Phase 4)

```
safefarm/
├── app.py               ← Updated to show Grad-CAM
├── config.py            ← unchanged
├── lang/en.py           ← unchanged
├── lang/my.py           ← unchanged
├── utils/image.py       ← unchanged
├── model/
│   ├── __init__.py      ← unchanged
│   ├── inference.py     ← Updated with Grad-CAM integration
│   ├── gradcam.py       ← NEW: Grad-CAM class
│   └── checkpoint.pt    ← (optional)
```

---

## What is Grad-CAM?

```
Grad-CAM = Gradient-weighted Class Activation Mapping

Purpose: Shows which parts of the image the model "looked at"
         when making its decision.

Example:
  ┌─────────────┐      ┌─────────────┐
  │ Original    │  →   │ Grad-CAM    │
  │ Farm Image  │      │ Heat Map    │
  │             │      │             │
  │ 🌾🌾🌾🌾    │      │ 🔴🟡🟢⚪    │
  │ 🌾🌾🌾🌾    │      │ 🟡🔴🟡🟢    │
  │ 🌾🌾🌾🌾    │      │ 🟢🟡🔴🔴    │
  └─────────────┘      └─────────────┘
                              ↓
                    Red = High attention
                    Green = Low attention
```

---

## Step 1: Create model/gradcam.py

**What to do:** Create a new file `model/gradcam.py`

**Purpose:** This file handles:
- Grad-CAM class for generating attention maps
- Hook registration for capturing gradients
- CAM computation and normalization
- Overlay visualization on original image

**What to include in the file:**

```
1. Imports
   - torch
   - torch.nn.functional as F
   - numpy as np
   - PIL.Image
   - matplotlib.cm (for colormap)

2. GradCAM class
   - __init__(self, model, target_layer)
     • Store model reference
     • Register forward hook
     • Register backward hook
   
   - _forward_hook(self, module, input, output)
     • Capture activations from target layer
   
   - _backward_hook(self, module, grad_input, grad_output)
     • Capture gradients from target layer
   
   - generate(self, input_tensor, target_class=None)
     • Forward pass through model
     • Backward pass for target class
     • Compute CAM weights
     • Normalize CAM
     • Return numpy array (224x224)

3. overlay_gradcam() function
   - Takes: original_image, cam, alpha=0.4
   - Applies jet colormap to CAM
   - Blends with original image
   - Returns PIL Image

4. save_gradcam() function
   - Takes: image, path
   - Saves Grad-CAM image to file
```

---

## Step 2: Update model/inference.py

**What to do:** Update the existing `model/inference.py`

**Purpose:** Add Grad-CAM generation to prediction pipeline

**What to change:**

```
1. Add new import
   - from model.gradcam import GradCAM, overlay_gradcam

2. Update FarmDamageClassifier class
   - __init__: 
     • Create GradCAM instance after model loads
     • Target layer: model.layer4 (for ResNet18)
   
   - _real_predict:
     • Generate CAM after prediction
     • Create overlay image
     • Store in result dict
   
   - _demo_predict:
     • Set gradcam_image to None (no real model)

3. Update predict() return dict
   - Add: "gradcam_image" (PIL Image or None)
   - Add: "has_gradcam" (bool)
```

---

## Step 3: Update app.py

**What to do:** Update `app.py` to display Grad-CAM

**Purpose:** Show visual evidence in the result area

**What to change:**

```
1. Add new session state
   - st.session_state.gradcam_image = None

2. Update render_result_card() function
   - Check if prediction has gradcam_image
   - If yes, show Grad-CAM overlay
   - If demo mode, show placeholder message

3. Add Grad-CAM display section
   - Show original image vs Grad-CAM side by side
   - Add opacity slider (optional)
   - Add explanation text

4. Add Grad-CAM legend
   - Red = High attention (model focused here)
   - Green/Blue = Low attention (model ignored here)
```

---

## Step 4: Test the App

**What to do:** Run the app and verify

```powershell
cd D:\demo-hackathon-v2\safefarm
venv\Scripts\activate
streamlit run app.py
```

**What to check:**

```
1. App opens at http://localhost:8501
2. Upload an image
3. Click "Assess Damage"
4. Result card shows with:
   - Damage level
   - Confidence
   - Probability breakdown
5. Grad-CAM section shows:
   - If real model: Heat map overlay
   - If demo mode: "Grad-CAM not available in demo mode"
6. Heat map shows colored regions
7. Original vs Grad-CAM comparison visible
8. No errors in terminal
```

---

## Expected Results

### Real Model (With Checkpoint)

```
┌─────────────────────────────────────────────────────┐
│ 📊 Assessment Result                                │
│                                                     │
│ Damage Level: High Damage                           │
│ Confidence: 91.2%                                   │
│                                                     │
│ ┌───────────────────────────────────────────────┐   │
│ │ 🔍 Visual Evidence (Grad-CAM)                 │   │
│ │                                               │   │
│ │ ┌─────────────┐  ┌─────────────┐             │   │
│ │ │ Original    │  │ Grad-CAM    │             │   │
│ │ │ Image       │  │ Heat Map    │             │   │
│ │ │             │  │             │             │   │
│ │ │ 🌾🌾🌾🌾    │  │ 🔴🟡🟢⚪    │             │   │
│ │ │ 🌾🌾🌾🌾    │  │ 🟡🔴🟡🟢    │             │   │
│ │ │ 🌾🌾🌾🌾    │  │ 🟢🟡🔴🔴    │             │   │
│ │ └─────────────┘  └─────────────┘             │   │
│ │                                               │   │
│ │ 🔴 Red = Model focused here                   │   │
│ │ 🟢 Green = Model ignored here                 │   │
│ └───────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

### Demo Mode (No Checkpoint)

```
┌─────────────────────────────────────────────────────┐
│ 📊 Assessment Result                                │
│                                                     │
│ Damage Level: Medium Damage                         │
│ Confidence: 78.3%                                   │
│                                                     │
│ ┌───────────────────────────────────────────────┐   │
│ │ 🔍 Visual Evidence (Grad-CAM)                 │   │
│ │                                               │   │
│ │ ⚠️ Grad-CAM not available in demo mode        │   │
│ │                                               │   │
│ │ Grad-CAM requires a trained model to show     │   │
│ │ which image regions influenced the prediction.│   │
│ └───────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## Key Concepts

### How Grad-CAM Works

```
1. Forward Pass
   - Image goes through model
   - Activations captured at layer4

2. Backward Pass
   - Gradient flows back from prediction
   - Gradients captured at layer4

3. Weight Computation
   - weights = gradients.mean(dim=(2,3))
   - weights show importance of each channel

4. CAM Generation
   - cam = weights × activations
   - cam = ReLU(cam) (only positive)
   - cam = normalize to 0-1

5. Overlay
   - Apply jet colormap
   - Blend with original image
   - Red = high attention
   - Blue = low attention
```

### Target Layer Selection

| Model | Target Layer | Why |
|-------|--------------|-----|
| ResNet18 | `model.layer4` | Last conv layer, rich features |
| MobileNetV3 | `model.features[-1]` | Last feature block |

### Color Map (Jet)

```
🔴 Red       = High attention (model focused here)
🟡 Yellow    = Medium attention
🟢 Green     = Low attention
🔵 Blue      = Very low attention (model ignored here)
```

---

## Files Summary

| File | Action | Lines | Purpose |
|------|--------|-------|---------|
| `model/gradcam.py` | CREATE | ~80 | Grad-CAM class + overlay |
| `model/inference.py` | UPDATE | +20 | Add Grad-CAM to prediction |
| `app.py` | UPDATE | +30 | Display Grad-CAM overlay |

---

## Verification Checklist

| # | Check | Expected |
|---|-------|----------|
| 1 | `model/gradcam.py` exists | File created |
| 2 | `model/inference.py` updated | Grad-CAM import added |
| 3 | `app.py` updated | Grad-CAM display added |
| 4 | App launches | No errors |
| 5 | Upload image | Image displays |
| 6 | Click "Assess Damage" | Result appears |
| 7 | Grad-CAM section shows | Title visible |
| 8 | Real model: Heat map shows | Colored overlay |
| 9 | Demo mode: Message shows | "Not available" |
| 10 | Original vs Grad-CAM | Side by side |
| 11 | Legend shows | Red/Green explanation |
| 12 | No errors | Clean terminal |

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| "No module named gradcam" | Wrong directory | Run from `safefarm/` folder |
| Grad-CAM not showing | Demo mode | Expected behavior |
| Heat map all blue | Model not trained | Need real checkpoint |
| Heat map all red | Bad normalization | Check GradCAM class |
| Slow generation | CPU only | Normal, takes ~1-2s |

---

## Prerequisites

| Requirement | Status |
|-------------|--------|
| Phase 3 complete | Must have `model/inference.py` |
| PyTorch installed | For tensor operations |
| matplotlib installed | For colormap |

---

## Ready to Implement?

Follow these steps:
1. Create `model/gradcam.py` with content from Step 1
2. Update `model/inference.py` with content from Step 2
3. Update `app.py` with content from Step 3
4. Test with `streamlit run app.py`
5. Verify all checklist items

---

**Questions before starting?**
