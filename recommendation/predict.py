import joblib
from config import settings


def load_model():
    model = joblib.load(settings["artifacts"]["model_path"])
    user_idx = joblib.load(settings["artifacts"]["user_index_path"])
    product_idx = joblib.load(settings["artifacts"]["product_index_path"])
    return model, user_idx, product_idx


def get_recommendations(user_id, top_n=None):
    model, user_idx, product_idx = load_model()

    if top_n is None:
        top_n = settings["recommendation"]["top_n"]

    # reverse product_idx: integer index -> real product id
    index_to_product = {}
    for product_id, index in product_idx.items():
        index_to_product[index] = product_id

    # look up this user's integer index
    user_index = user_idx[user_id]

    # get recommendations from the trained model
    recommended_indices, recommended_scores = model.recommend(
        user_index, model.user_items[user_index], N=top_n
    )

    # translate indices back to real product ids
    recommended_product_ids = []
    for i in recommended_indices:
        product_id = index_to_product[i]
        recommended_product_ids.append(product_id)

    results = list(zip(recommended_product_ids, recommended_scores))
    return results


if __name__ == "__main__":
    # quick manual test — replace with a real userId from your data
    sample_user_id = list(load_model()[1].keys())[0]
    print(get_recommendations(sample_user_id))