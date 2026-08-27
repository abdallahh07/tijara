from config import settings
from scipy.sparse import csr_matrix

def add_weights(data):
    event_col = settings["columns"]["event_type"]
    weight_col = settings["columns"]["weight"]
    event_weights = settings["event_weights"]
    
    data[weight_col] = data[event_col].map(event_weights)
    return data
  
def build_interaction_scores(data):
    user_col = settings["columns"]["user_id"]
    product_col = settings["columns"]["product_id"]
    weight_col = settings["columns"]["weight"]
    
    interaction_score = data.groupby([user_col, product_col])[weight_col].sum().reset_index()
    return interaction_score

def build_index_mappings(interaction_score):
    user_col = settings["columns"]["user_id"]
    product_col = settings["columns"]["product_id"]

    unique_users = interaction_score[user_col].unique()
    unique_products = interaction_score[product_col].unique()

    user_idx = {user_id: i for i, user_id in enumerate(unique_users)}
    product_idx = {product_id: i for i, product_id in enumerate(unique_products)}

    return user_idx, product_idx, unique_users, unique_products
  

def build_interaction_matrix(interaction_score, user_idx, product_idx, unique_users, unique_products):
    weight_col = settings["columns"]["weight"]
    user_col = settings["columns"]["user_id"]
    product_col = settings["columns"]["product_id"]

    interaction_score["user_idx"] = interaction_score[user_col].map(user_idx)
    interaction_score["product_idx"] = interaction_score[product_col].map(product_idx)

    interaction_matrix = csr_matrix(
        (interaction_score[weight_col], (interaction_score["user_idx"], interaction_score["product_idx"])),
        shape=(len(unique_users), len(unique_products))
    )
    return interaction_matrix