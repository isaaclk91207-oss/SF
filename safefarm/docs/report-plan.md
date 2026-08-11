---
kind: spec
title: SafeFarm Myanmar - Report Plan
---

# SafeFarm Myanmar - Report Plan

## PDF Report Structure

### Page Layout

```
┌─────────────────────────────────────────────────┐
│  [Logo]  SafeFarm Myanmar                       │
│          Farm Damage Assessment Report          │
│          စိုက်ခင်း ထိခိုက်မှု အကဲဖြတ်ချက် အစီရင်ခံစာ  │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │  [Uploaded Farm Photo]                  │   │
│  │  224x224 or fitted to page width        │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  ASSESSMENT DETAILS                             │
│  ─────────────────                              │
│  Region:     Ayeyarwady                        │
│  Township:   Labutta                           │
│  Village:    Kyunbone                          │
│  Crop Type:  Rice (စပါး)                       │
│  Farm Area:  5.2 acres                         │
│  Flood Days: 12                                │
│  Growth Stage: Flowering                       │
│                                                 │
│  DAMAGE ASSESSMENT                              │
│  ─────────────────                              │
│  Damage Level:  HIGH (ပြင်းထန်)                │
│  Confidence:    87.3%                           │
│  Priority Score: 78/100                         │
│                                                 │
│  RECOMMENDED SUPPORT                            │
│  ─────────────────                              │
│  • Emergency food assistance                    │
│  • Crop insurance claim processing              │
│  • Replanting support for next season           │
│                                                 │
│  ─────────────────────────────────────────────  │
│  DISCLAIMER                                     │
│  This result is a preliminary assessment...     │
│  ဤရလဒ်သည် ကြိုတင်အကဲဖြတ်ချက်တစ်ခုဖြစ်ပါသည်...  │
│                                                 │
│  Generated: 2026-08-06 14:30:00                 │
│  Report ID: SF-2026-08-06-001                   │
└─────────────────────────────────────────────────┘
```

## Report Content Fields

| Section | Field | Source | Bilingual |
|---------|-------|--------|-----------|
| Header | Product name | Config | Yes |
| Header | Report title | Language dict | Yes |
| Photo | Uploaded image | User upload | No |
| Details | Region | Form | No |
| Details | Township | Form | No |
| Details | Village | Form | No |
| Details | Crop type | Form | Yes |
| Details | Farm area | Form | No |
| Details | Flood days | Form | No |
| Details | Growth stage | Form | Yes |
| Assessment | Damage level | Model | Yes |
| Assessment | Confidence | Model | No |
| Assessment | Priority score | Calculator | No |
| Support | Recommended actions | Rule-based | Yes |
| Footer | Disclaimer | Language dict | Yes |
| Footer | Timestamp | System | No |
| Footer | Report ID | Generated | No |

## Bilingual PDF Generation

### Font Setup

```python
# utils/report.py

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

MYANMAR_FONT_PATH = os.path.join(
    os.path.dirname(__file__), 
    "fonts", 
    "NotoSansMyanmar.ttf"
)

def register_fonts():
    """Register Myanmar font for PDF generation."""
    try:
        pdfmetrics.registerFont(
            TTFont("NotoSansMyanmar", MYANMAR_FONT_PATH)
        )
        return True
    except Exception as e:
        print(f"Warning: Could not load Myanmar font: {e}")
        return False
```

### Language-Aware PDF Builder

```python
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.units import inch
from datetime import datetime

class ReportBuilder:
    def __init__(self, lang="en"):
        self.lang = lang
        self.styles = getSampleStyleSheet()
        self._setup_styles()
    
    def _setup_styles(self):
        """Configure styles with Myanmar font support."""
        font_name = "NotoSansMyanmar" if self.lang == "my" else "Helvetica"
        
        self.styles.add(ParagraphStyle(
            name="MyanmarTitle",
            fontName=font_name,
            fontSize=18,
            spaceAfter=12
        ))
        
        self.styles.add(ParagraphStyle(
            name="MyanmarBody",
            fontName=font_name,
            fontSize=10,
            spaceAfter=6
        ))
    
    def build_report(self, assessment_data, output_path):
        """Generate bilingual PDF report."""
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        story = []
        
        # Header
        story.append(Paragraph(
            self._get_string("report_title"),
            self.styles["MyanmarTitle"]
        ))
        story.append(Spacer(1, 12))
        
        # Photo
        if assessment_data.get("image_path"):
            img = Image(assessment_data["image_path"], 
                       width=4*inch, height=3*inch)
            story.append(img)
            story.append(Spacer(1, 12))
        
        # Assessment details
        story.append(Paragraph(
            self._get_string("assessment_details"),
            self.styles["Heading2"]
        ))
        
        fields = [
            ("region", assessment_data.get("region")),
            ("township", assessment_data.get("township")),
            ("village", assessment_data.get("village")),
            ("crop_type", assessment_data.get("crop_type")),
            ("farm_area", f"{assessment_data.get('farm_area')} acres"),
            ("flood_days", str(assessment_data.get("flood_days"))),
        ]
        
        for label, value in fields:
            story.append(Paragraph(
                f"<b>{self._get_string(label)}:</b> {value}",
                self.styles["MyanmarBody"]
            ))
        
        # Damage assessment
        story.append(Spacer(1, 12))
        story.append(Paragraph(
            self._get_string("damage_assessment"),
            self.styles["Heading2"]
        ))
        
        damage = assessment_data.get("damage_level", "unknown")
        confidence = assessment_data.get("confidence", 0)
        priority = assessment_data.get("priority_score", 0)
        
        story.append(Paragraph(
            f"<b>{self._get_string('damage_level')}:</b> {self._get_string(damage)}",
            self.styles["MyanmarBody"]
        ))
        story.append(Paragraph(
            f"<b>{self._get_string('confidence')}:</b> {confidence:.1%}",
            self.styles["MyanmarBody"]
        ))
        story.append(Paragraph(
            f"<b>{self._get_string('priority_score')}:</b> {priority}/100",
            self.styles["MyanmarBody"]
        ))
        
        # Recommended support
        story.append(Spacer(1, 12))
        story.append(Paragraph(
            self._get_string("recommended_support"),
            self.styles["Heading2"]
        ))
        
        recommendations = self._get_recommendations(damage, assessment_data)
        for rec in recommendations:
            story.append(Paragraph(
                f"• {rec}",
                self.styles["MyanmarBody"]
            ))
        
        # Disclaimer
        story.append(Spacer(1, 24))
        story.append(Paragraph(
            self._get_string("disclaimer"),
            self.styles["Disclaimer"]
        ))
        
        # Footer
        story.append(Spacer(1, 12))
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report_id = self._generate_report_id()
        
        story.append(Paragraph(
            f"Generated: {timestamp}",
            self.styles["Small"]
        ))
        story.append(Paragraph(
            f"Report ID: {report_id}",
            self.styles["Small"]
        ))
        
        doc.build(story)
        return output_path
    
    def _get_string(self, key):
        """Get bilingual string."""
        from lang.en import STRINGS as EN
        from lang.my import STRINGS as MY
        return MY.get(key, EN.get(key, key)) if self.lang == "my" else EN.get(key, key)
    
    def _get_recommendations(self, damage_level, data):
        """Generate support recommendations based on damage level."""
        recommendations = []
        
        if damage_level == "high":
            recommendations.append(self._get_string("rec_emergency_food"))
            recommendations.append(self._get_string("rec_insurance"))
            recommendations.append(self._get_string("rec_replanting"))
        elif damage_level == "medium":
            recommendations.append(self._get_string("rec_replanting"))
            recommendations.append(self._get_string("rec_monitoring"))
        elif damage_level == "low":
            recommendations.append(self._get_string("rec_monitoring"))
        else:
            recommendations.append(self._get_string("rec_verify"))
        
        if data.get("urgent_support"):
            recommendations.insert(0, self._get_string("rec_urgent"))
        
        return recommendations
    
    def _generate_report_id(self):
        """Generate unique report ID."""
        from datetime import datetime
        import random
        date_str = datetime.now().strftime("%Y-%m-%d")
        rand = random.randint(100, 999)
        return f"SF-{date_str}-{rand}"
```

## Recommended Support Rules

| Damage Level | Recommendations |
|--------------|-----------------|
| High | Emergency food assistance, Crop insurance claim, Replanting support |
| Medium | Replanting support, Field monitoring |
| Low | Continue monitoring |
| Unknown | Request further verification |

### Additional Rules

- If `urgent_support` checkbox is checked: Add "Prioritize urgent assistance" as first item
- If `flood_days > 14`: Add "Extended flood damage assessment recommended"
- If `growth_stage == "harvest"`: Add "Post-harvest loss assessment may apply"

## PDF Output Specifications

| Property | Value |
|----------|-------|
| Page size | A4 (210 × 297 mm) |
| Margins | 72pt (1 inch) all sides |
| Image width | 4 inches (max) |
| Image height | 3 inches (max) |
| Font size (title) | 18pt |
| Font size (body) | 10pt |
| Font size (disclaimer) | 8pt |
| Output format | PDF |

## Font Download

Myanmar font must be bundled:

```bash
# Download Noto Sans Myanmar
wget "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansMyanmar/NotoSansMyanmar-Regular.ttf"
mv NotoSansMyanmar-Regular.ttf safefarm/utils/fonts/NotoSansMyanmar.ttf
```

## Error Handling

| Error | Fallback |
|-------|----------|
| Myanmar font missing | Use Helvetica, warn user |
| Image too large for PDF | Resize to fit page |
| Report generation fails | Offer raw JSON download |
| Disk full | Show error message |
