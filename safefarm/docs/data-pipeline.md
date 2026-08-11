---
kind: spec
title: SafeFarm Myanmar - Data Pipeline
---

# SafeFarm Myanmar - Data Pipeline

## Overview

The data pipeline handles image ingestion, validation, preprocessing, and augmentation for both training and inference. Farm/flood images go through quality checks before classification.

## Image Validation Rules

```python
# utils/image.py

VALID_FORMATS = {"jpg", "jpeg", "png"}
MAX_SIZE_MB = 10
MIN_DIMENSION = 64   # Reject very small images
MAX_DIMENSION = 4096 # Reject extremely large images

def validate_image(uploaded_file) -> dict:
    """
    Returns: {valid: bool, error: str|None, warning: str|None}
    """
    # 1. Check format extension
    # 2. Check file size
    # 3. Open with Pillow, verify not corrupted
    # 4. Check dimensions
    # 5. Check if image is too dark (histogram mean < 30)
    # 6. Check if image is too blurry (Laplacian variance < 100)
```

## Preprocessing Pipeline

For inference (user uploads):

```
Raw Upload
  → Validate format + size
  → Open with PIL.Image
  → Convert to RGB (handle RGBA, grayscale, palette)
  → Resize to 224x224 (bicubic interpolation)
  → ToTensor (HWC → CHW, 0-255 → 0.0-1.0)
  → Normalize(mean=[0.485, 0.456, 0.406],
              std=[0.229, 0.224, 0.225])
  → Add batch dimension (1, 3, 224, 224)
  → Model inference
```

For training:

```
Image from disk
  → RandomResizedCrop(224)
  → RandomHorizontalFlip()
  → ColorJitter(brightness=0.2, contrast=0.2)
  → ToTensor
  → Normalize(same as inference)
```

## Class Mapping

| Internal Label | Index | English | Myanmar |
|----------------|-------|---------|---------|
| low | 0 | Low Damage | ထိခိုက်မှု နည်း |
| medium | 1 | Medium Damage | ထိခိုက်မှု အလယ်အလတ် |
| high | 2 | High Damage | ထိခိုက်မှု ပြင်းထန် |
| unknown | 3 | Unknown | မသိရ |

## Training Data Requirements

### Directory Layout

```
data/train/
├── low/          # Minimal visible flood damage
│   ├── img001.jpg
│   └── ...
├── medium/       # Partial crop/field damage
│   ├── img001.jpg
│   └── ...
├── high/         # Severe damage, major crop loss
│   ├── img001.jpg
│   └── ...
└── unknown/      # Unclear, blurry, obstructed
    ├── img001.jpg
    └── ...
```

### Minimum Data per Class

| Scenario | Images | Use Case |
|----------|--------|----------|
| Hackathon demo | 30-50 per class | Quick train, illustrative results |
| MVP baseline | 100-200 per class | Reasonable accuracy |
| Production | 500+ per class | Reliable classification |

### Image Sources

| Source | License | Notes |
|--------|---------|-------|
| Flood Map (Myanmar) | Check terms | Government/open data |
| Sentinel-2 satellite | Open | 10m resolution, needs processing |
| Unsplash flood | Free license | Street-level, general |
| Collected field photos | Own | Best if available |
| Synthetic augmentation | N/A | Expand small datasets |

### Data Documentation

Every image must have metadata:

```json
{
  "filename": "img001.jpg",
  "source": "Unsplash",
  "license": "Free commercial use",
  "location": "Hpa-An, Kayin State",
  "crop": "Rice",
  "label": "high",
  "notes": "Visible standing water, flattened rice plants"
}
```

## Quality Checks

| Check | Threshold | Action |
|-------|-----------|--------|
| Too dark | Mean brightness < 30 | Add warning tag |
| Too blurry | Laplacian variance < 100 | Add warning tag |
| Too small | Any dimension < 64px | Reject upload |
| Corrupted | PIL cannot open | Reject upload |
| Wrong format | Not jpg/png | Reject upload |
| Too large | > 10MB | Reject upload |

## Test Images

Prepare 6-9 representative test images:

| # | Description | Expected Class |
|---|-------------|----------------|
| 1 | Green rice paddy, no water | low |
| 2 | Slight water at field edge | low |
| 3 | Partially submerged crops | medium |
| 4 | Muddy field, damaged rows | medium |
| 5 | Fully flooded paddy | high |
| 6 | Collapsed crop, standing water | high |
| 7 | Very dark night photo | unknown |
| 8 | Blurry motion shot | unknown |
| 9 | Clear farm with some debris | medium |

## Augmentation Strategy

For training data expansion:

| Transform | Probability | Parameters |
|-----------|-------------|------------|
| RandomHorizontalFlip | 0.5 | — |
| RandomVerticalFlip | 0.3 | — |
| RandomRotation | 0.5 | ±15° |
| ColorJitter | 0.4 | brightness=0.3, contrast=0.3 |
| RandomResizedCrop | 1.0 | scale=(0.8, 1.0) |
| GaussianBlur | 0.2 | kernel=3 |

## Data Limitations to Document

1. No Myanmar-specific farm dataset exists publicly
2. Model trained on limited data = prototype results
3. Real flood damage varies by crop type, soil, season
4. Satellite vs street-level images have different characteristics
5. Unknown class is inherently hard to classify
