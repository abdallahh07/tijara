from fastapi import FastAPI, HTTPException
from predict import get_recommendations
from schemas import RecommendationResponse, RecommendationItem

app = FastAPI(title="Tijara Recommendation Service")


@app.get("/")
def root():
    return {"status": "ok", "service": "recommendation"}


@app.get("/recommendations/{user_id}", response_model=RecommendationResponse)
def recommendations(user_id: str, top_n: int = 10):
    try:
        results = get_recommendations(user_id, top_n=top_n)
    except KeyError:
        raise HTTPException(status_code=404, detail="User not found")

    items = [
        RecommendationItem(product_id=pid, score=float(score))
        for pid, score in results
    ]
    return RecommendationResponse(user_id=user_id, recommendations=items)