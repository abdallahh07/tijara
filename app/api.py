from fastapi import FastAPI
from api import router

app = FastAPI(title="Tijara Recommendation Service")


@app.get("/")
def root():
    return {"status": "ok", "service": "recommendation"}


app.include_router(router)