def generate_summary(ingredients, scores, user_allergies):
    flagged = [s for s in scores if s.score > 0]
    if not user_allergies:
        common = [s.ingredient for s in flagged]
        return f"This product contains {', '.join(common)}, which are common allergens. Since your profile is incomplete, please review carefully."
    else:
        high_risk = [f"{s.ingredient} (score: {s.score})" for s in flagged]
        if high_risk:
            return f"This product contains {', '.join(high_risk)}, which may pose a risk based on your allergy profile. It is advised to avoid this item."
        return "No high-risk ingredients found for your profile."
