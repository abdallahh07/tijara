from pydantic import BaseModel
from typing import List


class RecommendationItem(BaseModel):
    product_id: str
    score: float


class RecommendationResponse(BaseModel):
    user_id: str
    recommendations: List[RecommendationItem]