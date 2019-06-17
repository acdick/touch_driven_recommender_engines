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
    
    ################################################################################
    # UNPERSONALIZED RECOMMENDATIONS
    ################################################################################
    
    # returns the URL of the product with the most ratings
    def most_rated(self, rating_column):
        recommendations = self.dataframe[rating_column].value_counts().index
        self.append_new_recommendation(recommendations)
        ratings = self.dataframe[rating_column].value_counts()[self.recommender_history[-1]]
        
        return (self.recommender_history[-1], ratings)
    
    # returns a tuple with the number of ratings for the combination of group levels
    def rating_by_group_levels(self, rating_column, group_levels):
        df = self.dataframe[[rating_column] + list(group_levels.keys())]
        
        for key in group_levels.keys():
            df = df.loc[df[key] == group_levels[key]]
            
        rating = list(group_levels.values()) + [df.shape[0]]
        
        return tuple(rating)
    
    # returns a sorted list of 9 tuples containing combinations of the top 3x3 most rated segments
    def best_nine(self, rating_column, two_group_columns):
        best_nine          = []
        top_3_first_group  = list(self.dataframe[two_group_columns[0]].value_counts().index[0:3])
        top_3_second_group = list(self.dataframe[two_group_columns[1]].value_counts().index[0:3])
        
        for first in top_3_first_group:
            for second in top_3_second_group:
                group_levels = {two_group_columns[0]: first, two_group_columns[1]: second}
                best_nine.append(self.rating_by_group_levels(rating_column, group_levels))
        
        best_nine.sort(key = lambda x: x[2], reverse = True)
        
        return best_nine
    
    # returns the URL of the product with the most ratings in the top nine groups
    def best_nine_breadth(self, rating_column, two_group_columns):
        recommendations = []
        best_nine       = self.best_nine(rating_column, two_group_columns)
        
        for best_i in best_nine:
            df = self.dataframe[[rating_column] + two_group_columns]
            df = df.loc[df[two_group_columns[0]] == best_i[0]]
            df = df.loc[df[two_group_columns[1]] == best_i[1]]
            recommendations.append(df[rating_column].value_counts().index[0])
            
        self.append_new_recommendation(recommendations)
        ratings = self.dataframe[rating_column].value_counts()[self.recommender_history[-1]]
        
        return (self.recommender_history[-1], ratings)
    
    def best_nine_depth(self, rating_column, two_group_columns):
        best_one = self.best_nine(rating_column, two_group_columns)[0]
        
        df              = self.dataframe[[rating_column] + two_group_columns]
        df              = df.loc[df[two_group_columns[0]] == best_one[0]]
        df              = df.loc[df[two_group_columns[1]] == best_one[1]]
        recommendations = df[rating_column].value_counts().index
        
        self.append_new_recommendation(recommendations)
        ratings = self.dataframe[rating_column].value_counts()[self.recommender_history[-1]]
        
        return (self.recommender_history[-1], ratings)
    
    ################################################################################
    # CONTENT-BASED
    ################################################################################
    
    # content-based similarity with Pearson correlation
    def content_based_similarity(self, rating_column):
        
        return self.recommender_history[-1]
    
    ################################################################################
    # COLLABORATIVE FILTERING
    ################################################################################