"""SafeFarm Myanmar - Priority Score Calculator"""

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

GROWTH_STAGE_MAP = {
    "Seedling": "seedling",
    "Vegetative": "vegetative",
    "Flowering": "flowering",
    "Harvest": "harvest",
    "Post-harvest": "post_harvest",
    "အပင်ဖြူ": "seedling",
    "အရွက်ဖြူ": "vegetative",
    "ပွင့်ဖူး": "flowering",
    "ရိတ်သိမ်း": "harvest",
    "ရိတ်ပြီး": "post_harvest"
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
    s_damage = DAMAGE_SCORES.get(damage_level, 30)
    s_area = min(farm_area / 10, 1.0) * 100
    s_flood = min(flood_days / 30, 1.0) * 100

    stage_key = GROWTH_STAGE_MAP.get(growth_stage, "vegetative")
    s_growth = GROWTH_STAGE_SCORES.get(stage_key, 50)

    s_urgent = 50 if urgent_support else 0

    score = (
        WEIGHTS["damage"] * s_damage +
        WEIGHTS["area"] * s_area +
        WEIGHTS["flood_days"] * s_flood +
        WEIGHTS["growth_stage"] * s_growth +
        WEIGHTS["urgent"] * s_urgent
    )

    return max(0, min(100, round(score, 1)))


def get_priority_label(score):
    if score >= 70:
        return "high"
    elif score >= 40:
        return "medium"
    else:
        return "low"


def get_recommendations(damage_level, score, urgent_support):
    recommendations = []

    if damage_level == "high":
        recommendations.append("rec_emergency_food")
        recommendations.append("rec_insurance")
        recommendations.append("rec_replanting")
    elif damage_level == "medium":
        recommendations.append("rec_replanting")
        recommendations.append("rec_monitoring")
    elif damage_level == "low":
        recommendations.append("rec_monitoring")
    else:
        recommendations.append("rec_verify")

    if score >= 70:
        recommendations.insert(0, "rec_urgent")
    elif score >= 40:
        recommendations.insert(0, "rec_monitoring")

    if urgent_support:
        recommendations.insert(0, "rec_urgent")

    return recommendations
