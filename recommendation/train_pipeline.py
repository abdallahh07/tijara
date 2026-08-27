from pipeline import RecommendationPipeline
from config import settings
import joblib

def train():
    pipeline = RecommendationPipeline()
    pipeline.run()

    joblib.dump(pipeline.model, settings["artifacts"]["model_path"])
    joblib.dump(pipeline.user_idx, settings["artifacts"]["user_index_path"])
    joblib.dump(pipeline.product_idx, settings["artifacts"]["product_index_path"])

    return pipeline.model

if __name__ == "__main__":
    train()