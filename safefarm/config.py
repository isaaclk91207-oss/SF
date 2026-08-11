"""SafeFarm Myanmar - Configuration Constants"""

import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Paths
MODEL_PATH = os.path.join(BASE_DIR, "model", "checkpoint.pt")
FONT_PATH = os.path.join(BASE_DIR, "utils", "fonts", "NotoSansMyanmar.ttf")
SAMPLES_DIR = os.path.join(BASE_DIR, "data", "test_myanmar")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Classes
CLASSES = ["low", "medium", "high", "unknown"]
CLASS_COLORS = {
    "low": "#4CAF50",
    "medium": "#FF9800",
    "high": "#F44336",
    "unknown": "#9E9E9E",
}

# Model
MODEL_INPUT_SIZE = (224, 224)
MODEL_MEAN = [0.485, 0.456, 0.406]
MODEL_STD = [0.229, 0.224, 0.225]
NUM_CLASSES = 4

# Upload
MAX_UPLOAD_SIZE_MB = 10
SUPPORTED_FORMATS = ["jpg", "jpeg", "png"]

# Priority weights
PRIORITY_WEIGHTS = {
    "damage": 0.35,
    "area": 0.20,
    "flood_days": 0.20,
    "growth_stage": 0.15,
    "urgent": 0.10
}

# Regions
REGIONS = [
    "Ayeyarwady", "Bago", "Chin", "Kachin", "Kayah",
    "Kayin", "Magway", "Mandalay", "Mon", "Naypyidaw",
    "Rakhine", "Sagaing", "Shan", "Tanintharyi", "Yangon"
]

# Crops
CROPS = {
    "en": ["Rice", "Corn", "Sesame", "Pulses", "Other"],
    "my": ["စပါး", "ပြောင်း", "နှမ်း", "ပဲ", "အခြား"]
}

# Growth stages
GROWTH_STAGES = {
    "en": ["Seedling", "Vegetative", "Flowering", "Harvest", "Post-harvest"],
    "my": ["အပင်ဖြူ", "အရွက်ဖြူ", "ပွင့်ဖူး", "ရိတ်သိမ်း", "ရိတ်ပြီး"]
}

# Language strings lookup
def get_string(key, lang="en"):
    """Get localized string by key."""
    from lang.en import STRINGS as EN_STRINGS
    from lang.my import STRINGS as MY_STRINGS
    
    if lang == "my":
        return MY_STRINGS.get(key, EN_STRINGS.get(key, key))
    return EN_STRINGS.get(key, key)
