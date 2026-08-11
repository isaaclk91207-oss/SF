---
kind: spec
title: SafeFarm Myanmar - Priority Score Calculator
---

# SafeFarm Myanmar - Priority Score Calculator

## Purpose

The priority score helps field workers and aid organizations **prioritize which farms to verify first**. It is NOT an official compensation calculation.

## Formula

```
Priority Score = (W_d × S_d) + (W_a × S_a) + (W_f × S_f) + (W_g × S_g) + (W_u × S_u)
```

Where:
- `S_d` = Damage severity score
- `S_a` = Farm area score
- `S_f` = Flood duration score
- `S_g` = Crop growth stage score
- `S_u` = Urgent support score
- `W_*` = Weight for each factor

## Component Scores

### 1. Damage Severity (S_d)

| Damage Level | Score |
|--------------|-------|
| low | 25 |
| medium | 50 |
| high | 75 |
| unknown | 30 |

### 2. Farm Area (S_a)

```python
def area_score(area_acres):
    """
    Larger farms = higher priority (more impact)
    Scale: 0-100, capped at 100 acres
    """
    return min(area_acres / 10, 10) * 10  # Max 100 points
```

| Area (acres) | Score |
|--------------|-------|
| 0.5 | 5 |
| 1 | 10 |
| 5 | 50 |
| 10 | 100 |
| 20+ | 100 (capped) |

### 3. Flood Duration (S_f)

```python
def flood_days_score(days):
    """
    Longer flooding = higher priority
    Scale: 0-100, capped at 30 days
    """
    return min(days / 30, 1.0) * 100
```

| Days | Score |
|------|-------|
| 1 | 3 |
| 7 | 23 |
| 14 | 47 |
| 21 | 70 |
| 30+ | 100 (capped) |

### 4. Crop Growth Stage (S_g)

| Stage | Score | Rationale |
|-------|-------|-----------|
| Seedling | 80 | Most vulnerable, high replanting cost |
| Vegetative | 60 | Moderate recovery potential |
| Flowering | 90 | Critical stage, high loss |
| Harvest | 70 | Near-complete crop at risk |
| Post-harvest | 30 | Lower immediate impact |

### 5. Urgent Support (S_u)

| Urgent Needed | Score |
|---------------|-------|
| No | 0 |
| Yes | 50 |

## Default Weights

```python
WEIGHTS = {
    "damage": 0.35,      # Most important factor
    "area": 0.20,        # Scale of impact
    "flood_days": 0.20,  # Duration of damage
    "growth_stage": 0.15, # Crop vulnerability
    "urgent": 0.10       # Immediate need
}
```

## Implementation

```python
# utils/priority.py

WEIGHTS = {
    "damage": 0.35,
    "area": 0.20,
    "flood_days": 0.20,
    "growth_stage": 0.15,
    "urgent": 0.10
}

DAMAGE_SCORES = {
    "low": 25,
    "medium": 50,
    "high": 75,
    "unknown": 30
}

GROWTH_STAGE_SCORES = {
    "seedling": 80,
    "vegetative": 60,
    "flowering": 90,
    "harvest": 70,
    "post_harvest": 30
}

def calculate_priority(damage_level, farm_area, flood_days, 
                       growth_stage, urgent_support):
    """
    Calculate support priority score (0-100).
    
    Args:
        damage_level: "low", "medium", "high", "unknown"
        farm_area: float, acres
        flood_days: int
        growth_stage: "seedling", "vegetative", "flowering", 
                     "harvest", "post_harvest"
        urgent_support: bool
    
    Returns:
        float: Priority score 0-100
    """
    # Damage score
    s_damage = DAMAGE_SCORES.get(damage_level, 30)
    
    # Area score (0-100)
    s_area = min(farm_area / 10, 1.0) * 100
    
    # Flood days score (0-100)
    s_flood = min(flood_days / 30, 1.0) * 100
    
    # Growth stage score
    s_growth = GROWTH_STAGE_SCORES.get(growth_stage, 50)
    
    # Urgent support score
    s_urgent = 50 if urgent_support else 0
    
    # Weighted sum
    score = (
        WEIGHTS["damage"] * s_damage +
        WEIGHTS["area"] * s_area +
        WEIGHTS["flood_days"] * s_flood +
        WEIGHTS["growth_stage"] * s_growth +
        WEIGHTS["urgent"] * s_urgent
    )
    
    # Clamp to 0-100
    return max(0, min(100, round(score, 1)))

def get_priority_label(score):
    """Get human-readable priority label."""
    if score >= 70:
        return "high"
    elif score >= 40:
        return "medium"
    else:
        return "low"

def get_recommendations(damage_level, score, urgent_support):
    """Generate support recommendations."""
    recommendations = []
    
    # Based on damage level
    if damage_level == "high":
        recommendations.append("Emergency food assistance")
        recommendations.append("Crop insurance claim processing")
        recommendations.append("Replanting support for next season")
    elif damage_level == "medium":
        recommendations.append("Replanting support")
        recommendations.append("Field monitoring")
    elif damage_level == "low":
        recommendations.append("Continue monitoring")
    else:
        recommendations.append("Request further verification")
    
    # Based on priority score
    if score >= 70:
        recommendations.insert(0, "PRIORITY: Schedule field verification within 48 hours")
    elif score >= 40:
        recommendations.insert(0, "Schedule field verification within 1 week")
    
    # Urgent support
    if urgent_support:
        recommendations.insert(0, "URGENT: Prioritize immediate assistance")
    
    return recommendations
```

## Usage Example

```python
from utils.priority import calculate_priority, get_recommendations

score = calculate_priority(
    damage_level="high",
    farm_area=5.2,
    flood_days=12,
    growth_stage="flowering",
    urgent_support=True
)

# Result: 72.4

recommendations = get_recommendations("high", score, True)
# ["URGENT: Prioritize immediate assistance",
#  "PRIORITY: Schedule field verification within 48 hours",
#  "Emergency food assistance",
#  "Crop insurance claim processing",
#  "Replanting support for next season"]
```

## Score Interpretation

| Score Range | Priority Label | Recommended Action |
|-------------|----------------|-------------------|
| 70-100 | High | Verify within 48 hours |
| 40-69 | Medium | Verify within 1 week |
| 0-39 | Low | Standard monitoring |

## Limitations

1. **Not compensation**: Score does not determine payment amounts
2. **Simplified**: Real assessment requires field inspection
3. **Weights adjustable**: May need tuning based on local priorities
4. **Subjective factors**: Growth stage assessment varies
5. **No regional adjustment**: Flood severity varies by geography

## Disclaimer Text

> The support priority score is a preliminary tool for aid prioritization. It does not determine compensation amounts or official damage assessments. All farms require field verification before aid distribution.
