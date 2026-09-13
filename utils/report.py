"""SafeFarm Myanmar - PDF Report Generator (xhtml2pdf)"""

import os
import base64
import random
import tempfile
from io import BytesIO
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from xhtml2pdf import pisa
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from config import BASE_DIR

FONT_PATH = os.path.join(BASE_DIR, "utils", "fonts", "Pyidaungsu.ttf")
FONT_NAME = "Pyidaungsu"

# Register font with reportlab (xhtml2pdf uses reportlab under the hood)
try:
    pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))
except Exception:
    pass

try:
    _pil_font = ImageFont.truetype(FONT_PATH, 14)
except Exception:
    _pil_font = ImageFont.load_default()


def _render_text_to_base64(text, font_size=14, color="#212529", bg="transparent"):
    """Render text as PNG using Pillow, return base64 data URI."""
    if not text or not text.strip():
        return ""

    try:
        font = ImageFont.truetype(FONT_PATH, font_size)
    except Exception:
        font = _pil_font

    dummy = Image.new("RGBA", (1, 1))
    draw = ImageDraw.Draw(dummy)

    words = text.split()
    lines = []
    line = ""
    max_w = 550
    for word in words:
        test = f"{line} {word}".strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_w:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    if not lines:
        lines = [text]

    line_h = font_size + 4
    img_w = max_w + 20
    img_h = len(lines) * line_h + 6

    if bg == "transparent":
        img = Image.new("RGBA", (img_w, img_h), (255, 255, 255, 0))
    else:
        img = Image.new("RGB", (img_w, img_h), bg)

    draw = ImageDraw.Draw(img)
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)

    for i, ln in enumerate(lines):
        draw.text((2, i * line_h + 2), ln, font=font, fill=(r, g, b, 255))

    buf = BytesIO()
    img.save(buf, "PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/png;base64,{b64}"


def _myanmar_img(text, font_size=14, color="#212529", extra_style=""):
    """Return an <img> tag for Myanmar text."""
    src = _render_text_to_base64(text, font_size, color)
    if not src:
        return text
    h = font_size + 6
    return f'<img src="{src}" style="height:{h}px;vertical-align:middle;{extra_style}" />'


def generate_report_id():
    date_str = datetime.now().strftime("%Y-%m-%d")
    rand = random.randint(100, 999)
    return f"SF-{date_str}-{rand}"


def image_to_base64(image_path):
    if not image_path or not os.path.exists(image_path):
        return ""
    with open(image_path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return f"data:image/png;base64,{data}"


def build_pdf(assessment_data, output_path, lang="en"):
    from lang.en import STRINGS as EN
    from lang.my import STRINGS as MY

    def t(key):
        if lang == "my":
            val = MY.get(key, EN.get(key, key))
            return _myanmar_img(val, font_size=14, color="#212529")
        return EN.get(key, key)

    def t_plain(key):
        if lang == "my":
            return MY.get(key, EN.get(key, key))
        return EN.get(key, key)

    def t_bold(key):
        if lang == "my":
            val = MY.get(key, EN.get(key, key))
            return _myanmar_img(val, font_size=14, color="#212529", extra_style="font-weight:bold;")
        return f"<b>{EN.get(key, key)}</b>"

    def t_small(key):
        if lang == "my":
            val = MY.get(key, EN.get(key, key))
            return _myanmar_img(val, font_size=11, color="#212529")
        return EN.get(key, key)

    def t_xs(key):
        if lang == "my":
            val = MY.get(key, EN.get(key, key))
            return _myanmar_img(val, font_size=9, color="#999999")
        return EN.get(key, key)

    def val(text):
        if lang == "my" and text and str(text).strip():
            return _myanmar_img(str(text), font_size=13, color="#212529")
        return str(text) if text else ""

    damage_level = assessment_data.get("damage_level", "unknown")
    confidence = assessment_data.get("confidence", 0)
    priority_score = assessment_data.get("priority_score", 0)
    recs = assessment_data.get("recommendations", [])
    image_path = assessment_data.get("image_path")

    recs_html = "".join(f'<li style="margin:2px 0;">{t(r)}</li>' for r in recs)

    img_html = ""
    if image_path and os.path.exists(image_path):
        img_b64 = image_to_base64(image_path)
        img_html = f'<img src="{img_b64}" style="max-width:100%;height:auto;border-radius:8px;margin:12px 0;" />'

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_id = generate_report_id()

    priority_label = "high" if priority_score >= 70 else ("medium" if priority_score >= 40 else "low")
    pcolor = {"high": "#F44336", "medium": "#FF9800", "low": "#4CAF50"}.get(priority_label, "#999")
    damage_border_color = {"high": "#F44336", "medium": "#FF9800", "low": "#4CAF50"}.get(damage_level, "#999")
    damage_bg_color = {"high": "#FFF5F5", "medium": "#FFF8E1", "low": "#F1F8E9"}.get(damage_level, "#FFF")

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<style>
body {{
    font-family: '{FONT_NAME}', sans-serif;
    font-size: 11px;
    line-height: 1.5;
    color: #212529;
    margin: 0;
    padding: 10px;
}}
.header {{
    text-align: center;
    border-bottom: 2px solid #212529;
    padding-bottom: 8px;
    margin-bottom: 12px;
}}
.header h1 {{
    margin: 0;
    font-size: 20px;
    font-family: '{FONT_NAME}', sans-serif;
}}
.header p {{
    margin: 2px 0 0 0;
    font-size: 12px;
    color: #555;
    font-family: '{FONT_NAME}', sans-serif;
}}
.section {{
    margin-bottom: 10px;
}}
.section-title {{
    font-size: 13px;
    font-weight: bold;
    font-family: '{FONT_NAME}', sans-serif;
    border-bottom: 1px solid #ccc;
    padding-bottom: 3px;
    margin-bottom: 6px;
}}
.field {{
    margin: 2px 0;
    font-family: '{FONT_NAME}', sans-serif;
}}
.field-label {{
    font-weight: bold;
    display: inline-block;
    width: 110px;
}}
.damage-card {{
    border: 2px solid {damage_border_color};
    border-radius: 6px;
    padding: 8px;
    margin: 6px 0;
    background: {damage_bg_color};
}}
.priority-card {{
    text-align: center;
    border: 2px solid {pcolor};
    border-radius: 6px;
    padding: 8px;
    margin: 6px 0;
}}
.score-text {{
    font-size: 32px;
    font-weight: bold;
    color: {pcolor};
    margin: 0;
}}
ul {{
    margin: 4px 0;
    padding-left: 20px;
}}
.disclaimer {{
    font-size: 8px;
    color: #999;
    border-top: 1px solid #ddd;
    padding-top: 6px;
    margin-top: 12px;
    font-family: '{FONT_NAME}', sans-serif;
}}
.footer {{
    font-size: 8px;
    color: #999;
    margin-top: 3px;
    font-family: '{FONT_NAME}', sans-serif;
}}
</style>
</head>
<body>
    <div class="header">
        <h1>SafeFarm Myanmar</h1>
        <p>{t("report_title")}</p>
    </div>

    {img_html}

    <div class="section">
        <div class="section-title">{t_bold("assessment_details")}</div>
        <div class="field"><span class="field-label">{t_bold("region")}:</span> {val(assessment_data.get("region", ""))}</div>
        <div class="field"><span class="field-label">{t_bold("township")}:</span> {val(assessment_data.get("township", ""))}</div>
        <div class="field"><span class="field-label">{t_bold("village")}:</span> {val(assessment_data.get("village", ""))}</div>
        <div class="field"><span class="field-label">{t_bold("crop_type")}:</span> {val(assessment_data.get("crop_type", ""))}</div>
        <div class="field"><span class="field-label">{t_bold("farm_area")}:</span> {val(assessment_data.get("farm_area", 0))} acres</div>
        <div class="field"><span class="field-label">{t_bold("flood_days")}:</span> {val(assessment_data.get("flood_days", 0))}</div>
        <div class="field"><span class="field-label">{t_bold("growth_stage")}:</span> {val(assessment_data.get("growth_stage", ""))}</div>
    </div>

    <div class="section">
        <div class="section-title">{t_bold("damage_assessment")}</div>
        <div class="damage-card">
            <div class="field"><span class="field-label">{t_bold("damage_level")}:</span> {t(damage_level)}</div>
            <div class="field"><span class="field-label">{t_bold("confidence")}:</span> {confidence:.1%}</div>
        </div>
    </div>

    <div class="section">
        <div class="section-title">{t_bold("priority_score")}</div>
        <div class="priority-card">
            <p class="score-text">{priority_score}</p>
            <p style="margin:2px 0;font-size:11px;">{t("priority_" + priority_label)}</p>
        </div>
    </div>

    <div class="section">
        <div class="section-title">{t_bold("recommended_support")}</div>
        <ul>{recs_html}</ul>
    </div>

    <div class="disclaimer">
        {t_xs("disclaimer")}
    </div>

    <div class="footer">
        Generated: {timestamp} | Report ID: {report_id} | SafeFarm Myanmar | Team M-Matrix
    </div>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    with open(output_path, "r", encoding="utf-8") as html_file:
        pisa_status = pisa.CreatePDF(
            html_file.read(),
            dest=open(output_path, "wb"),
            encoding="utf-8"
        )

    return output_path
