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
   