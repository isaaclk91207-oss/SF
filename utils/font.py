"""SafeFarm Myanmar - Font Loading Utility"""

import base64
import os
from config import FONT_PATH


def get_font_base64():
    """Read font file and return base64 encoded string."""
    if os.path.exists(FONT_PATH):
        with open(FONT_PATH, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


def get_myanmar_font_css():
    """Return CSS string with embedded Myanmar font."""
    font_b64 = get_font_base64()
    if not font_b64:
        return ""

    return f"""
    <style>
    @font-face {{
        font-family: 'NotoSansMyanmar';
        src: url(data:font/truetype;base64,{font_b64}) format('truetype');
        font-weight: normal;
        font-style: normal;
    }}
    * {{
        font-family: 'NotoSansMyanmar', 'Noto Sans Myanmar', sans-serif !important;
    }}
    </style>
    """
