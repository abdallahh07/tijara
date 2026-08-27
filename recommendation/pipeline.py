
from implicit.als import AlternatingLeastSquares
 
from data_manager import load_user_events
from features import (
    add_weights,
    build_interaction_scores,
    build_index_mappings,
    build_interaction_matrix,
)
from config import settings
 
 
class RecommendationPipeline:
    def __init__(self):
        self.model = None
        self.user_idx = None
        self.product_idx = None
        self.unique_users = None
        self.unique_products = None
        self.interaction_matrix = None
 
    def run(self):
        """Runs every step in order and stores the results on self,
        so they can be reused afterward (e.g. by predict.py)."""
 
        # 1. load data
        data = load_user_events()
 
        # 2. add weights
        data = add_weights(data)
 
        # 3. build interaction scores
        interaction_score = build_interaction_scores(data)
 
        # 4. build index mappings
        self.user_idx, self.product_idx, self.unique_users, self.unique_products = (
            build_index_mappings(interaction_score)
        )
 
        # 5. build the interaction matrix
        self.interaction_matrix = build_interaction_matrix(
            interaction_score,
            self.user_idx,
            self.product_idx,
            self.unique_users,
            self.unique_products,
        )
 
        # 6. train the model
        self.model = AlternatingLeastSquares(
            factors=settings["model"]["factors"],
            regularization=settings["model"]["regularization"],
            iterations=settings["model"]["iterations"],
        )
        self.model.fit(self.interaction_matrix)
 
        return self.model