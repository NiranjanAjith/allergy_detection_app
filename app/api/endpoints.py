from fastapi import APIRouter, HTTPException, File, UploadFile
from app.api.schemas import *
from app.core.risk_engine import calculate_score
from app.core.llm_service import generate_summary
from app.models.memory_store import user_profiles

router = APIRouter()

@router.get("/")
def home():
    return {"message": "Allergy Detection API is running."}

@router.get("/profile/{user_id}", response_model=UserProfile)
def get_profile(user_id: str):
    if user_id not in user_profiles:
        raise HTTPException(status_code=404, detail="User not found")
    return user_profiles[user_id]

@router.post("/profile", response_model=UserProfile)
def create_profile(profile: UserProfile):
    if profile.id in user_profiles:
        raise HTTPException(status_code=400, detail="User already exists")
    user_profiles[profile.id] = profile
    return profile

@router.put("/profile/{user_id}", response_model=UserProfile)
def update_profile(user_id: str, update: UpdateProfileRequest):
    if user_id not in user_profiles:
        raise HTTPException(status_code=404, detail="User not found")
    existing = user_profiles[user_id]
    updated = existing.model_copy(update=update.model_dump(exclude_unset=True))
    user_profiles[user_id] = updated
    return updated

@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_product(data: AnalyzeRequest, image: Optional[UploadFile] = File(None)):
    """Analyze product ingredients and generate a summary."""
    allergies = data.user_allergies
    scores = []
    for ingredient in data.ingredients:
        score, matched = calculate_score(ingredient.name, allergies)
        scores.append(IngredientScore(
            ingredient=ingredient.name,
            score=score,
            matched_allergen=matched
        ))

    summary = generate_summary(data.ingredients, scores, allergies, image)
    return AnalyzeResponse(risk_scores=scores, summary=summary)
