from pydantic import BaseModel
from typing import List, Optional

class IngredientInput(BaseModel):
    name: str
    processing: Optional[str] = "raw"

class AnalyzeRequest(BaseModel):
    ingredients: List[IngredientInput]
    user_allergies: Optional[List[str]] = None

class IngredientScore(BaseModel):
    ingredient: str
    score: float
    matched_allergen: Optional[str]

class AnalyzeResponse(BaseModel):
    risk_scores: List[IngredientScore]
    summary: str

class UserProfile(BaseModel):
    id: str
    name: Optional[str]
    allergies: List[str] = []

class UpdateProfileRequest(BaseModel):
    name: Optional[str]
    allergies: List[str]
