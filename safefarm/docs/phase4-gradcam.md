---
kind: spec
title: Phase 4 - Grad-CAM Integration (Hands-On Guide)
---

# Phase 4: Grad-CAM Integration — Hands-On Guide

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

## Step 1: Create model/gradcam.py

**File:** `model/gradcam.py`

**Action:** Create this file with the following content:

```python
"""SafeFarm Myanmar - Grad-CAM Visual Evidence"""

import torch
import torch.nn.functional as F
import numpy as np
from PIL import Image


class GradCAM:
    """Generate Grad-CAM attention maps."""
    
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        
        # Register hooks
        target_layer.register_forward_hook(self._forward_hook)
        target_layer.register_backward_hook(self._backward_hook)
    
    def _forward_hook(self, module, input, output):
        self.activations = output.detach()
    
    def _backward_hook(self, module, grad_input, grad_output):
        self.gradients = grad_output[0].detach()
    
    def generate(self, input_tensor, target_class=None):
        """Generate CAM for input tensor."""
        # Forward pass
        output = self.model(input_tensor)
        
        if target_class is None:
            target_class = output.argmax(dim=1).item()
        
        # Backward pass
        self.model.zero_grad()
        output[0, target_class].backward()
        
        # Compute weights
        weights = self.gradients.mean(dim=(2, 3), keepdim=True)
        cam = F.relu((weights * self.activations).sum(dim=1))
        
        # Normalize
        cam = F.interpolate(cam, size=(224, 224), mode='bilinear')
        cam = cam - cam.min()
        cam = cam / (cam.max() + 1e-8)
        
        return cam.squeeze().numpy()


def overlay_gradcam(original_image, cam, alpha=0.4):
    """Overlay CAM on original image."""
    import matplotlib.cm as cm
    
    # Apply colormap
    heatmap = cm.jet(cam)[:, :, :3]  # RGB only
    heatmap = (heatmap * 255).astype(np.uint8)
    heatmap = Image.fromarray(heatmap).resize(original_image.size)
    
    # Overlay
    result = Image.blend(original_image, heatmap, alpha)
    return result


def save_gradcam(image, path):
    """Save Grad-CAM image to file."""
    image.save(path)
    return path
```

---

## Step 2: Update model/inference.py

**File:** `model/inference.py`

**Action:** Open this file and make these changes:

### Change 1: Add import at the top

Find this line:
```python
from config import CLASSES, MODEL_PATH, MODEL_INPUT_SIZE, MODEL_MEAN, MODEL_STD, NUM_CLASSES
```

Add this line after it:
```python
from model.gradcam import GradCAM, overlay_gradcam
```

### Change 2: Update __init__ method

Find this code in FarmDamageClassifier class:
```python
def __init__(self):
    self.model = None
    self.is_demo = True
    self.device = "cpu"
    
    # Try to load real model
    if os.path.exists(MODEL_PATH):
        self.model = load_checkpoint(MODEL_PATH)
        if self.model is not None:
            self.is_demo = False
            self.model.to(self.device)
    
    # Set transform
    self.transform = get_transform()
```

Replace with:
```python
def __init__(self):
    self.model = None
    self.is_demo = True
    self.device = "cpu"
    self.gradcam = None
    
    # Try to load real model
    if os.path.exists(MODEL_PATH):
        self.model = load_checkpoint(MODEL_PATH)
        if self.model is not None:
            self.is_demo = False
            self.model.to(self.device)
            # Initialize Grad-CAM
            self.gradcam = GradCAM(self.model, self.model.layer4)
    
    # Set transform
    self.transform = get_transform()
```

### Change 3: Update _demo_predict method

Find this code:
```python
def _demo_predict(self, image):
    """Return random prediction for demo mode."""
    # Weighted random selection (realistic distribution)
    weights = [0.30, 0.35, 0.20, 0.15]  # low, medium, high, unknown
    pred_class = random.choices(CLASSES, weights=weights)[0]
    pred_index = CLASSES.index(pred_class)
    
    # Generate realistic confidence
    confidence = random.uniform(0.65, 0.92)
    
    # Generate probabilities that sum to 1
    probs = self._generate_realistic_probs(pred_index)
    
    return {
        "class": pred_class,
        "class_index": pred_index,
        "confidence": confidence,
        "probabilities": {CLASSES[i]: probs[i] for i in range(len(CLASSES))},
        "is_demo": True
    }
```

Replace with:
```python
def _demo_predict(self, image):
    """Return random prediction for demo mode."""
    # Weighted random selection (realistic distribution)
    weights = [0.30, 0.35, 0.20, 0.15]  # low, medium, high, unknown
    pred_class = random.choices(CLASSES, weights=weights)[0]
    pred_index = CLASSES.index(pred_class)
    
    # Generate realistic confidence
    confidence = random.uniform(0.65, 0.92)
    
    # Generate probabilities that sum to 1
    probs = self._generate_realistic_probs(pred_index)
    
    return {
        "class": pred_class,
        "class_index": pred_index,
        "confidence": confidence,
        "probabilities": {CLASSES[i]: probs[i] for i in range(len(CLASSES))},
        "is_demo": True,
        "gradcam_image": None,
        "has_gradcam": False
    }
```

### Change 4: Update _real_predict method

Find this code:
```python
def _real_predict(self, image):
    """Run actual model inference."""
    # Preprocess image
    input_tensor = self.transform(image).unsqueeze(0).to(self.device)
    
    # Run inference
    with torch.no_grad():
        output = self.model(input_tensor)
        probs = F.softmax(output, dim=1)
    
    # Get prediction
    pred_class_idx = probs.argmax(dim=1).item()
    confidence = probs[0, pred_class_idx].item()
    
    # Build probability dict
    probs_dict = {
        CLASSES[i]: probs[0, i].item() 
        for i in range(len(CLASSES))
    }
    
    return {
        "class": CLASSES[pred_class_idx],
        "class_index": pred_class_idx,
        "confidence": confidence,
        "probabilities": probs_dict,
        "is_demo": False
    }
```

Replace with:
```python
def _real_predict(self, image):
    """Run actual model inference."""
    # Preprocess image
    input_tensor = self.transform(image).unsqueeze(0).to(self.device)
    
    # Run inference
    with torch.no_grad():
        output = self.model(input_tensor)
        probs = F.softmax(output, dim=1)
    
    # Get prediction
    pred_class_idx = probs.argmax(dim=1).item()
    confidence = probs[0, pred_class_idx].item()
    
    # Build probability dict
    probs_dict = {
        CLASSES[i]: probs[0, i].item() 
        for i in range(len(CLASSES))
    }
    
    # Generate Grad-CAM
    gradcam_image = None
    if self.gradcam is not None:
        cam = self.gradcam.generate(input_tensor, pred_class_idx)
        gradcam_image = overlay_gradcam(image, cam)
    
    return {
        "class": CLASSES[pred_class_idx],
        "class_index": pred_class_idx,
        "confidence": confidence,
        "probabilities": probs_dict,
        "is_demo": False,
        "gradcam_image": gradcam_image,
        "has_gradcam": gradcam_image is not None
    }
```

---

## Step 3: Update app.py

**File:** `app.py`

**Action:** Open this file and make these changes:

### Change 1: Add new session state

Find this code:
```python
if "prediction" not in st.session_state:
    st.session_state.prediction = None
```

Add this after it:
```python
if "gradcam_image" not in st.session_state:
    st.session_state.gradcam_image = None
```

### Change 2: Update render_result_card function

Find this entire function:
```python
def render_result_card(prediction):
    """Render result card with prediction."""
    st.subheader(f"📊 {t('result_title')}")
    
    if prediction is None:
        st.info("Upload an image and click 'Assess Damage' to see results")
        return
    
    # Get damage level and color
    damage_class = prediction["class"]
    confidence = prediction["confidence"]
    color = CLASS_COLORS.get(damage_class, "#9E9E9E")
    
    # Demo mode warning
    if prediction.get("is_demo", False):
        st.warning(f"⚠️ {t('model_demo')}")
    
    # Main result card
    st.markdown(f"""
    <div style="
        border: 2px solid {color};
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        background-color: {color}15;
    ">
        <h3 style="color: {color}; margin: 0;">
            {t('damage_level')}: {t(damage_class)}
        </h3>
        <p style="font-size: 24px; margin: 10px 0;">
            {t('confidence')}: {confidence:.1%}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Probability breakdown
    st.markdown("**Probability Breakdown:**")
    probs = prediction["probabilities"]
    
    # Create columns for each class
    cols = st.columns(4)
    for i, (cls, prob) in enumerate(probs.items()):
        with cols[i]:
            st.metric(
                label=t(cls),
                value=f"{prob:.1%}"
            )
    
    # Recommendations based on damage level
    st.markdown("---")
    st.markdown("**Recommended Actions:**")
    
    if damage_class == "high":
        st.error(f"🔴 {t('rec_urgent')}")
        st.error(f"🔴 {t('rec_emergency_food')}")
    elif damage_class == "medium":
        st.warning(f"🟠 {t('rec_replanting')}")
        st.warning(f"🟠 {t('rec_insurance')}")
    elif damage_class == "low":
        st.success(f"🟢 {t('rec_monitoring')}")
    else:
        st.info(f"⚪ {t('rec_verify')}")
```

Replace with:
```python
def render_result_card(prediction):
    """Render result card with prediction."""
    st.subheader(f"📊 {t('result_title')}")
    
    if prediction is None:
        st.info("Upload an image and click 'Assess Damage' to see results")
        return
    
    # Get damage level and color
    damage_class = prediction["class"]
    confidence = prediction["confidence"]
    color = CLASS_COLORS.get(damage_class, "#9E9E9E")
    
    # Demo mode warning
    if prediction.get("is_demo", False):
        st.warning(f"⚠️ {t('model_demo')}")
    
    # Main result card
    st.markdown(f"""
    <div style="
        border: 2px solid {color};
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        background-color: {color}15;
    ">
        <h3 style="color: {color}; margin: 0;">
            {t('damage_level')}: {t(damage_class)}
        </h3>
        <p style="font-size: 24px; margin: 10px 0;">
            {t('confidence')}: {confidence:.1%}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Probability breakdown
    st.markdown("**Probability Breakdown:**")
    probs = prediction["probabilities"]
    
    # Create columns for each class
    cols = st.columns(4)
    for i, (cls, prob) in enumerate(probs.items()):
        with cols[i]:
            st.metric(
                label=t(cls),
                value=f"{prob:.1%}"
            )
    
    # Grad-CAM Visual Evidence
    st.markdown("---")
    st.subheader("🔍 Visual Evidence (Grad-CAM)")
    
    if prediction.get("has_gradcam", False) and prediction.get("gradcam_image") is not None:
        # Show Grad-CAM overlay
        col_orig, col_cam = st.columns(2)
        
        with col_orig:
            st.markdown("**Original Image:**")
            st.image(st.session_state.uploaded_image, use_column_width=True)
        
        with col_cam:
            st.markdown("**Grad-CAM Heat Map:**")
            st.image(prediction["gradcam_image"], use_column_width=True)
        
        # Legend
        st.markdown("""
        **Legend:**
        - 🔴 **Red** = Model focused here (high attention)
        - 🟡 **Yellow** = Medium attention
        - 🟢 **Green/Blue** = Model ignored here (low attention)
        """)
    else:
        # Demo mode message
        st.info("⚠️ Grad-CAM not available in demo mode")
        st.caption("Grad-CAM requires a trained model to show which image regions influenced the prediction.")
    
    # Recommendations based on damage level
    st.markdown("---")
    st.markdown("**Recommended Actions:**")
    
    if damage_class == "high":
        st.error(f"🔴 {t('rec_urgent')}")
        st.error(f"🔴 {t('rec_emergency_food')}")
    elif damage_class == "medium":
        st.warning(f"🟠 {t('rec_replanting')}")
        st.warning(f"🟠 {t('rec_insurance')}")
    elif damage_class == "low":
        st.success(f"🟢 {t('rec_monitoring')}")
    else:
        st.info(f"⚪ {t('rec_verify')}")
```

### Change 3: Update form submission handler

Find this code in main() function:
```python
        # Handle form submission
        if form_data["submitted"] and image is not None:
            with st.spinner("Analyzing image..."):
                prediction = predict_image(image)
                st.session_state.prediction = prediction
                st.rerun()
```

Replace with:
```python
        # Handle form submission
        if form_data["submitted"] and image is not None:
            with st.spinner("Analyzing image..."):
                prediction = predict_image(image)
                st.session_state.prediction = prediction
                st.session_state.gradcam_image = prediction.get("gradcam_image")
                st.rerun()
```

---

## Step 4: Test the App

**Command:**
```powershell
cd D:\demo-hackathon-v2\safefarm
venv\Scripts\activate
streamlit run app.py
```

**Opens at:** `http://localhost:8501`

---

## Step 5: Verify Features

| # | Check | How to Test |
|---|-------|-------------|
| 1 | App launches | No errors in terminal |
| 2 | Sidebar shows status | "Demo Mode" warning |
| 3 | Upload image | Click upload, select JPG/PNG |
| 4 | Click "Assess Damage" | Form submits |
| 5 | Result card appears | Damage level + confidence shown |
| 6 | Probabilities displayed | 4 class probabilities visible |
| 7 | Grad-CAM section shows | Title "Visual Evidence (Grad-CAM)" |
| 8 | Demo mode message | "Grad-CAM not available in demo mode" |
| 9 | Language toggle | Switch to မြန်မာ, labels update |
| 10 | No errors | Clean terminal output |

---

## Expected Results

### Demo Mode (No Checkpoint)

```
┌─────────────────────────────────────────────────────┐
│ 📊 Assessment Result                                │
│                                                     │
│ ⚠️ Demo mode — results are illustrative only        │
│                                                     │
│ Damage Level: Medium Damage                         │
│ Confidence: 78.3%                                   │
│                                                     │
│ Low: 12.1% | Medium: 78.3% | High: 6.2% | Unknown: 3.4% │
│                                                     │
│ ─────────────────────────────────────────────────   │
│                                                     │
│ 🔍 Visual Evidence (Grad-CAM)                       │
│                                                     │
│ ⚠️ Grad-CAM not available in demo mode              │
│ Grad-CAM requires a trained model to show which     │
│ image regions influenced the prediction.            │
│                                                     │
│ ─────────────────────────────────────────────────   │
│                                                     │
│ Recommended Actions:                                │
│ 🟠 Replanting support for next season               │
│ 🟠 Crop insurance claim processing                  │
└─────────────────────────────────────────────────────┘
```

### Real Model (With Checkpoint)

```
┌─────────────────────────────────────────────────────┐
│ 📊 Assessment Result                                │
│                                                     │
│ Damage Level: High Damage                           │
│ Confidence: 91.2%                                   │
│                                                     │
│ Low: 2.1% | Medium: 5.3% | High: 91.2% | Unknown: 1.4% │
│                                                     │
│ ─────────────────────────────────────────────────   │
│                                                     │
│ 🔍 Visual Evidence (Grad-CAM)                       │
│                                                     │
│ ┌─────────────┐  ┌─────────────┐                   │
│ │ Original    │  │ Grad-CAM    │                   │
│ │ Image       │  │ Heat Map    │                   │
│ │             │  │             │                   │
│ │ 🌾🌾🌾🌾    │  │ 🔴🟡🟢⚪    │                   │
│ │ 🌾🌾🌾🌾    │  │ 🟡🔴🟡🟢    │                   │
│ │ 🌾🌾🌾🌾    │  │ 🟢🟡🔴🔴    │                   │
│ └─────────────┘  └─────────────┘                   │
│                                                     │
│ Legend:                                              │
│ 🔴 Red = Model focused here (high attention)        │
│ 🟢 Green/Blue = Model ignored here (low attention)  │
│                                                     │
│ ─────────────────────────────────────────────────   │
│                                                     │
│ Recommended Actions:                                │
│ 🔴 Prioritize urgent assistance                     │
│ 🔴 Emergency food assistance                        │
└─────────────────────────────────────────────────────┘
```

---

## Files Summary

| File | Action | Lines Changed |
|------|--------|---------------|
| `model/gradcam.py` | CREATE | +80 lines |
| `model/inference.py` | UPDATE | +20 lines |
| `app.py` | UPDATE | +30 lines |

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| "No module named gradcam" | Wrong directory | Run from `safefarm/` folder |
| "No attribute 'layer4'" | Wrong model | Check ResNet18 architecture |
| Grad-CAM all blue | Model untrained | Expected with random weights |
| Heat map not showing | Demo mode | Expected behavior |
| Slow generation | CPU only | Normal, takes ~1-2s |

---

**Ready to implement?** Follow Steps 1-5 above.
