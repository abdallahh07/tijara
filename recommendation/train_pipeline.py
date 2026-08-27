from data_manager import load_user_events
from features import add_weights, build_interaction_scores, build_index_mappings, build_interaction_matrix
from implicit.als import AlternatingLeastSquares
from config import settings
import joblib

def train():
    data = load_user_events()

    data = add_weights(data)

    interaction_score = build_interaction_scores(data)

    user_idx, product_idx, unique_users, unique_products = build_index_mappings(interaction_score)

    interaction_matrix = build_interaction_matrix(
        interaction_score, user_idx, product_idx, unique_users, unique_products
    )

    model = AlternatingLeastSquares(
        factors=settings["model"]["factors"],
        regularization=settings["model"]["regularization"],
        iterations=settings["model"]["iterations"]
    )
    model.fit(interaction_matrix)

    joblib.dump(model, settings["artifacts"]["model_path"])
    joblib.dump(user_idx, settings["artifacts"]["user_index_path"])
    joblib.dump(product_idx, settings["artifacts"]["product_index_path"])

    return model

if __name__ == "__main__":
    train()