import pandas as pd

class Recommender():
    
    def __init__(self, df, rating_column, descriptor, two_feature_columns, two_group_columns):
        self.dataframe           = df
        self.rating_column       = rating_column
        self.descriptor          = descriptor
        self.two_feature_columns = two_feature_columns
        self.two_group_columns   = two_group_columns
        self.recommender_history = pd.DataFrame(columns=[self.rating_column,          self.descriptor,
                                                         self.two_feature_columns[0], self.two_feature_columns[1],
                                                         self.two_group_columns[0],   self.two_group_columns[1],
                                                         'Total Ratings',             'User Rating',
                                                         'Recommended By'])
        self.product_similarity  = None
        
    def load_content_similarity_matrix(self, file_path):
        self.product_similarity = pd.read_pickle(file_path)
        
        return self.product_similarity
        
    # appends the first recommendation not already in the recommender history
    def append_new_recommendation(self, recommendations, recommender):
        new_recommendation = None
        
        for recommendation in recommendations:
            if recommendation not in self.recommender_history[self.rating_column].unique():
                descriptor = self.dataframe.loc[
                    self.dataframe[self.rating_column] == recommendation].iloc[0][self.descriptor]
                feature_one = self.dataframe.loc[
                    self.dataframe[self.rating_column] == recommendation].iloc[0][self.two_feature_columns[0]]
                feature_two = self.dataframe.loc[
                    self.dataframe[self.rating_column] == recommendation].iloc[0][self.two_feature_columns[1]]
                column_one = self.dataframe.loc[
                    self.dataframe[self.rating_column] == recommendation].iloc[0][self.two_group_columns[0]]
                column_two = self.dataframe.loc[
                    self.dataframe[self.rating_column] == recommendation].iloc[0][self.two_group_columns[1]]
                    
                new_recommendation = {
                    self.rating_column:          recommendation,
                    self.descriptor:             descriptor,
                    self.two_group_columns[0]:   column_one,
                    self.two_group_columns[1]:   column_two,
                    self.two_feature_columns[0]: feature_one,
                    self.two_feature_columns[1]: feature_two,
                    'Total Ratings':             self.dataframe[self.rating_column].value_counts()[recommendation],
                    'User Rating':               -1,
                    'Recommended By':            recommender}
                
                self.recommender_history = self.recommender_history.append(new_recommendation, ignore_index=True)
                
                break
        
        return new_recommendation
    
    def update_user_rating(self, user_rating):
        self.recommender_history.iloc[-1, self.recommender_history.columns.get_loc('User Rating')] = user_rating
        
        return self.recommender_history.iloc[-1][self.rating_column]
    
    def user_favorites(self):
        favorites = self.recommender_history.sort_values(by = 'User Rating', ascending = False)[self.rating_column]
        
        return favorites
    
    def clear_history(self):
        self.recommender_history.drop(self.recommender_history.index, inplace=True)
        
        return None
    
    ################################################################################
    # UNPERSONALIZED RECOMMENDATIONS
    ################################################################################
    
    # returns the URL of the product with the most ratings
    def most_rated(self):
        recommendations    = self.dataframe[self.rating_column].value_counts().index
        new_recommendation = self.append_new_recommendation(recommendations, 'Most Rated')
        
        return new_recommendation
    
    # returns a tuple with the number of ratings for the combination of group levels
    def rating_by_group_levels(self, rating_column, group_levels):
        df = self.dataframe[[rating_column] + list(group_levels.keys())]
        
        for key in group_levels.keys():
            df = df.loc[df[key] == group_levels[key]]
            
        rating = list(group_levels.values()) + [df.shape[0]]
        
        return tuple(rating)
    
    # returns a sorted list of 9 tuples containing combinations of the top 3x3 most rated segments
    def best_nine(self):
        best_nine          = []
        top_3_first_group  = list(self.dataframe[self.two_group_columns[0]].value_counts().index[0:3])
        top_3_second_group = list(self.dataframe[self.two_group_columns[1]].value_counts().index[0:3])
        
        for first in top_3_first_group:
            for second in top_3_second_group:
                group_levels = {self.two_group_columns[0]: first, self.two_group_columns[1]: second}
                best_nine.append(self.rating_by_group_levels(self.rating_column, group_levels))
        
        best_nine.sort(key = lambda x: x[2], reverse = True)
        
        return best_nine
    
    # returns the URL of the product with the most ratings in the top nine groups
    def best_nine_breadth(self):
        new_recommendation = None
        recommendations    = []
        best_nine          = self.best_nine()
        
        i = 0
        while new_recommendation == None:
            for best_i in best_nine:
                df = self.dataframe[[self.rating_column] + self.two_group_columns]
                df = df.loc[df[self.two_group_columns[0]] == best_i[0]]
                df = df.loc[df[self.two_group_columns[1]] == best_i[1]]
                
                try:
                    recommendations.append(df[self.rating_column].value_counts().index[i])
                except:
                    pass
            
            new_recommendation = self.append_new_recommendation(recommendations, 'Best Nine Breadth')
            i += 1
        
        return new_recommendation
    
    def best_nine_depth(self):
        best_one = self.best_nine()[0]
        
        df              = self.dataframe[[self.rating_column] + self.two_group_columns]
        df              = df.loc[df[self.two_group_columns[0]] == best_one[0]]
        df              = df.loc[df[self.two_group_columns[1]] == best_one[1]]
        recommendations = df[self.rating_column].value_counts().index
        
        new_recommendation = self.append_new_recommendation(recommendations, 'Best Nine Depth')
        
        return new_recommendation
    
    ################################################################################
    # CONTENT-BASED
    ################################################################################
    
    # content-based similarity with Pearson correlation
    def content_based_similarity(self):
        
        top_favorite    = self.user_favorites().iloc[0]
        recommendations = self.product_similarity[top_favorite].sort_values(ascending = False)
        recommendations = recommendations.drop([top_favorite], axis=0).index
        
        new_recommendation = self.append_new_recommendation(recommendations, 'Content-Based Pearson Similarity')
        
        return new_recommendation
    
    ################################################################################
    # COLLABORATIVE FILTERING
    ################################################################################