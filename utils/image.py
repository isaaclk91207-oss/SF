"""SafeFarm Myanmar - Image Processing Pipeline"""

import os
import numpy as np
from PIL import Image
import cv2

# Constants
VALID_FORMATS = {"jpg", "jpeg", "png"}
MAX_SIZE_MB = 10
MIN_DIMENSION = 64
MAX_DIMENSION = 4096
MODEL_INPUT_SIZE = (224, 224)


def validate_image(uploaded_file) -> dict:
    """
    Validate uploaded image file.
    
    Returns:
        dict: {valid: bool, error: str|None, warning: str|None}
    """
    result = {"valid": False, "error": None, "warning": None}
    
    if uploaded_file is None:
        result["error"] = "No file uploaded"
        return result
    
    # Check format
    file_ext = uploaded_file.name.split(".")[-1].lower()
    if file_ext not in VALID_FORMATS:
        result["error"] = f"Invalid format. Supported: {', '.join(VALID_FORMATS)}"
        return result
    
    # Check file size
    file_size_mb = uploaded_file.size / (1024 * 1024)
    if file_size_mb > MAX_SIZE_MB:
        result["error"] = f"File too large ({file_size_mb:.1f}MB). Max: {MAX_SIZE_MB}MB"
        return result
    
    # Try to open image
    try:
        image = Image.open(uploaded_file)
        image.verify()  # Verify it's a valid image
        uploaded_file.seek(0)  # Reset file pointer
        image = Image.open(uploaded_file)  # Re-open after verify
    except Exception as e:
        result["error"] = f"Corrupted image file"
        return result
    
    # Check dimensions
    width, height = image.size
    if width < MIN_DIMENSION or height < MIN_DIMENSION:
        result["error"] = f"Image too small ({width}x{height}). Min: {MIN_DIMENSION}px"
        return result
    
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        result["error"] = f"Image too large ({width}x{height}). Max: {MAX_DIMENSION}px"
        return result
    
    # Check quality
    warnings = check_image_quality(image)
    if warnings:
        result["warning"] = "; ".join(warnings)
    
    result["valid"] = True
    return result


def check_image_quality(image: Image.Image) -> list:
    """
    Check image quality issues.
    
    Returns:
        list: List of warning messages
    """
    warnings = []
    
    # Convert to numpy array
    img_array = np.array(image.convert("L"))  # Convert to grayscale
    
    # Check brightness
    mean_brightness = img_array.mean()
    if mean_brightness < 30:
        warnings.append("Image is very dark")
    elif mean_brightness > 220:
        warnings.append("Image is overexposed")
    
    # Check blur (Laplacian variance)
    try:
        gray = cv2.cvtColor(np.array(image.convert("RGB")), cv2.COLOR_RGB2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        if laplacian_var < 100:
            warnings.append("Image appears blurry")
    except Exception:
        pass  # Skip blur check if cv2 fails
    
    return warnings


def preprocess_image(image: Image.Image) -> Image.Image:
    """
    Preprocess image for model input.
    
    Steps:
        1. Convert to RGB
        2. Resize to 224x224
        3. Return processed image
    """
    # Convert to RGB (handle RGBA, grayscale, palette)
    if image.mode != "RGB":
        image = image.convert("RGB")
    
    # Resize
    image = image.resize(MODEL_INPUT_SIZE, Image.BICUBIC)
    
    return image


def get_image_info(image: Image.Image) -> dict:
    """
    Get image information.
    
    Returns:
        dict: {width, height, mode, format}
    """
    return {
        "width": image.size[0],
        "height": image.size[1],
        "mode": image.mode,
        "format": image.format or "Unknown"
    }


def save_temp_image(image: Image.Image, prefix: str = "temp") -> str:
    """
    Save image to temporary location.
    
    Returns:
        str: Path to saved image
    """
    import tempfile
    
    temp_dir = tempfile.gettempdir()
    filename = f"{prefix}_{id(image)}.png"
    filepath = os.path.join(temp_dir, filename)
    
    image.save(filepath, "PNG")
    return filepath


def cleanup_temp_images(prefix: str = "temp"):
    """Clean up temporary images."""
    import tempfile
    import glob
    
    temp_dir = tempfile.gettempdir()
    pattern = os.path.join(temp_dir, f"{prefix}_*.png")
    
    for filepath in glob.glob(pattern):
        try:
            os.remove(filepath)
        except Exception:
            pass
