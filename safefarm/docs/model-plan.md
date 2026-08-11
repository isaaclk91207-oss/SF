---
kind: spec
title: SafeFarm Myanmar - Model Plan
---

# SafeFarm Myanmar - Model Plan

## Model Selection

| Option | Model | Params | CPU Speed | Accuracy | Recommendation |
|--------|-------|--------|-----------|----------|----------------|
| A | ResNet18 | 11.7M | ~50ms | Higher | **Default** |
| B | MobileNetV3-Small | 2.5M | ~20ms | Lower | Lightweight toggle |

**Decision: ResNet18 as primary, MobileNetV3 as optional lightweight mode.**

## Model Architecture

### ResNet18 for Farm Damage Classification

```python
import torchvision.models as models
import torch.nn as nn

def build_model(num_classes=4, use_pretrained=True):
    model = models.resnet18(pretrained=use_pretrained)
    
    # Replace final fully connected layer
    in_features = model.fc.in_features  # 512
    model.fc = nn.Sequential(
        nn.Dropout(0.3),
        nn.Linear(in_features, num_classes)
    )
    
    return model
```

### MobileNetV3 Alternative

```python
def build_mobilenet(num_classes=4, use_pretrained=True):
    model = models.mobilenet_v3_small(pretrained=use_pretrained)
    
    in_features = model.classifier[3].in_features
    model.classifier[3] = nn.Linear(in_features, num_classes)
    
    return model
```

## Training Strategy

### Fine-Tuning Approach

```
Phase 1: Feature extraction (5 epochs)
  - Freeze all layers except final FC
  - LR: 1e-3
  - Optimizer: Adam
  - Loss: CrossEntropyLoss

Phase 2: Full fine-tune (15-20 epochs)
  - Unfreeze all layers
  - LR: 1e-4 (backbone), 1e-3 (FC head)
  - Optimizer: AdamW
  - Scheduler: CosineAnnealingLR
  - Loss: CrossEntropyLoss with class weights
```

### Class Weights

Since classes may be imbalanced:

```python
# Calculate from training set
class_counts = {"low": 50, "medium": 40, "high": 35, "unknown": 25}
total = sum(class_counts.values())
weights = {k: total / (len(class_counts) * v) for k, v in class_counts.items()}
# → {"low": 0.8, "medium": 1.0, "high": 1.14, "unknown": 1.6}
```

### Training Configuration

```python
# train.py config
BATCH_SIZE = 16
EPOCHS = 25
LEARNING_RATE = 1e-4
WEIGHT_DECAY = 1e-4
IMAGE_SIZE = 224
TRAIN_SPLIT = 0.8
VAL_SPLIT = 0.1
TEST_SPLIT = 0.1
RANDOM_SEED = 42
```

## Grad-CAM Implementation

### How It Works

Grad-CAM (Gradient-weighted Class Activation Mapping) highlights which image regions influenced the model's decision.

### Implementation

```python
# model/gradcam.py

import torch
import torch.nn.functional as F
import numpy as np
from PIL import Image

class GradCAM:
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
```

### Target Layer Selection

| Model | Target Layer | Output Size |
|-------|--------------|-------------|
| ResNet18 | `model.layer4` | (512, 7, 7) |
| MobileNetV3 | `model.features[-1]` | (576, 7, 7) |

### Overlay Visualization

```python
def overlay_gradcam(original_image, cam, alpha=0.4):
    """
    original_image: PIL Image (224x224)
    cam: numpy array (224x224), values 0-1
    alpha: overlay opacity
    """
    import matplotlib.cm as cm
    
    # Apply colormap
    heatmap = cm.jet(cam)[:, :, :3]  # RGB only
    heatmap = (heatmap * 255).astype(np.uint8)
    heatmap = Image.fromarray(heatmap).resize(original_image.size)
    
    # Overlay
    result = Image.blend(original_image, heatmap, alpha)
    return result
```

## Inference API

```python
# model/inference.py

class FarmDamageClassifier:
    def __init__(self, checkpoint_path, device="cpu"):
        self.device = device
        self.model = build_model(num_classes=4)
        self.model.load_state_dict(torch.load(checkpoint_path, map_location=device))
        self.model.eval()
        self.gradcam = GradCAM(self.model, self.model.layer4)
        self.transform = self._build_transform()
    
    def _build_transform(self):
        return transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406],
                                 [0.229, 0.224, 0.225])
        ])
    
    def predict(self, image: Image.Image) -> dict:
        """
        Returns: {
            "class": "medium",
            "class_index": 1,
            "confidence": 0.87,
            "probabilities": {"low": 0.05, "medium": 0.87, "high": 0.06, "unknown": 0.02},
            "gradcam_path": "temp/gradcam_123.png"
        }
        """
        input_tensor = self.transform(image).unsqueeze(0).to(self.device)
        
        # Get prediction
        with torch.no_grad():
            output = self.model(input_tensor)
            probs = F.softmax(output, dim=1)
        
        pred_class = probs.argmax(dim=1).item()
        confidence = probs[0, pred_class].item()
        
        # Generate Grad-CAM
        cam = self.gradcam.generate(input_tensor, pred_class)
        gradcam_image = overlay_gradcam(image, cam)
        gradcam_path = self._save_gradcam(gradcam_image)
        
        return {
            "class": CLASSES[pred_class],
            "class_index": pred_class,
            "confidence": confidence,
            "probabilities": {CLASSES[i]: probs[0, i].item() for i in range(4)},
            "gradcam_path": gradcam_path
        }
    
    def _save_gradcam(self, image):
        import tempfile, os
        path = os.path.join(tempfile.gettempdir(), f"gradcam_{id(image)}.png")
        image.save(path)
        return path
```

## Model Fallback (Demo Mode)

If no checkpoint exists, provide illustrative results:

```python
def demo_predict(image: Image.Image) -> dict:
    """Return random prediction for demo when model is not trained."""
    import random
    pred_class = random.choices(
        CLASSES, 
        weights=[0.3, 0.3, 0.2, 0.2]
    )[0]
    
    return {
        "class": pred_class,
        "class_index": CLASSES.index(pred_class),
        "confidence": random.uniform(0.6, 0.95),
        "probabilities": {c: random.random() for c in CLASSES},
        "gradcam_path": None,
        "is_demo": True
    }
```

## Model Checkpoint Format

```python
checkpoint = {
    "model_state_dict": model.state_dict(),
    "optimizer_state_dict": optimizer.state_dict(),
    "epoch": 25,
    "class_to_idx": {"low": 0, "medium": 1, "high": 2, "unknown": 3},
    "idx_to_class": {0: "low", 1: "medium", 2: "high", 3: "unknown"},
    "train_acc": 0.92,
    "val_acc": 0.85,
    "config": {
        "model": "resnet18",
        "num_classes": 4,
        "image_size": 224
    }
}
```

## Performance Benchmarks

| Metric | ResNet18 | MobileNetV3 |
|--------|----------|-------------|
| Inference time (CPU) | ~50ms | ~20ms |
| Model size | ~45MB | ~10MB |
| RAM usage | ~200MB | ~80MB |
| Accuracy (target) | >80% | >75% |

## Limitations to Document

1. **Prototype status**: Model trained on limited data
2. **Not for official use**: Results are preliminary assessments only
3. **Class imbalance**: Unknown class may be underrepresented
4. **Image quality**: Poor images reduce accuracy significantly
5. **Regional bias**: Training data may not represent all Myanmar regions
6. **Seasonal variation**: Flood damage differs by season and crop stage
