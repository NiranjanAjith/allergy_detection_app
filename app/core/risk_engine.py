def calculate_score(ingredient, user_allergies):
    common_allergens = ["milk", "eggs", "fish", "shellfish", "tree nuts", "peanuts", "wheat", "soy"]
    if not user_allergies:
        if ingredient in common_allergens:
            return 0.5, ingredient
        return 0.0, None
    for allergy in user_allergies:
        if allergy.lower() in ingredient.lower():
            return 0.9, allergy
    return 0.0, None
