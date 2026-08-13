"""SafeFarm Myanmar - Model Inference & Demo Mode"""

import os
import random
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
from PIL import Image

# Import config
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CLASSES, MODEL_PATH, MODEL_INPUT_SIZE, MODEL_MEAN, MODEL_STD, NUM_CLASSES


def build_model(num_classes=4, use_pretrained=True):
    """Build ResNet18 model for classification."""
    model = models.resnet18(pretrained=use_pretrained)
    
    # Replace final fully connected layer
    in_features = model.fc.in_features  # 512
    model.fc = nn.Sequential(
        nn.Dropout(0.3),
        nn.Linear(in_features, num_classes)
    )
    
    return model


def load_checkpoint(path):
    """Load model checkpoint if it exists."""
    if not os.path.exists(path):
        return None
    
    try:
        checkpoint = torch.load(path, map_location="cpu")
        model = build_model(num_classes=NUM_CLASSES)
        model.load_state_dict(checkpoint["model_state_dict"])
        model.eval()
        return model
    except Exception as e:
        print(f"Warning: Could not load checkpoint: {e}")
        return None


def get_transform():
    """Get image transform for model input."""
    from torchvision import transforms
    return transforms.Compose([
        transforms.Resize(MODEL_INPUT_SIZE),
        transforms.ToTensor(),
        transforms.Normalize(MODEL_MEAN, MODEL_STD)
    ])


class FarmDamageClassifier:
    """Main classifier that handles real model or demo mode."""
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

    def predict(self, image):
        """
        Predict damage level for an image.

        Args:
            image: PIL Image

        Returns:
            dict with keys: class, class_index, confidence, probabilities, is_demo
        """
        if self.is_demo:
            return self._demo_predict(image)
        else:
            return self._real_predict(image)
        
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
    
    def _generate_realistic_probs(self, target_idx):
        """Generate realistic probability distribution."""
        probs = [random.random() for _ in range(len(CLASSES))]
        
        # Make target class highest
        probs[target_idx] = max(probs) + 0.3
        
        # Normalize to sum to 1
        total = sum(probs)
        probs = [p / total for p in probs]
        
        return probs
    
    def get_model_info(self):
        """Get information about current model state."""
        if self.is_demo:
            return {
                "status": "demo",
                "name": "Demo Mode (No Model)",
                "device": "N/A"
            }
        else:
            return {
                "status": "active",
                "name": "ResNet18",
                "device": self.device
            }


# Global classifier instance
_classifier = None


def get_classifier():
    """Get or create the global classifier instance."""
    global _classifier
    if _classifier is None:
        _classifier = FarmDamageClassifier()
    return _classifier


def predict_image(image):
    """Convenience function to predict from image."""
    classifier = get_classifier()
    return classifier.predict(image)
