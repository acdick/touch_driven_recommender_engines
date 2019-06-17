class Recommender():
    
    def __init__(self, df):
        self.dataframe           = df
        self.product_similarity  = None
        self.recommender_history = []
        
    # appends the first recommendation not already in the recommender history
    def append_new_recommendation(self, recommendations):
        for recommendation in recommendations:
            if recommendation not in self.recommender_history:
                self.recommender_history.append(recommendation)
                break
        
        return self.recommender_history[-1]
    
    def clear_history(self):
        self.recommender_history = []
        
        return None