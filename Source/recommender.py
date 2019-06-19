from   surprise                       import Reader, Dataset
from   surprise.model_selection       import GridSearchCV
from   surprise.prediction_algorithms import SVD
import pandas                         as     pd

class Recommender():
    
    def __init__(self, utility_matrix, reviews, rating_column, descriptor, five_feature_columns, two_group_columns):
        self.utility_matrix       = utility_matrix
        self.dataframe            = reviews
        self.rating_column        = rating_column
        self.descriptor           = descriptor
        self.five_feature_columns = five_feature_columns
        self.two_group_columns    = two_group_columns
        self.recommender_history  = pd.DataFrame(columns=[self.rating_column,           self.descriptor,
                                                          self.five_feature_columns[0], self.five_feature_columns[1],
                                                          self.five_feature_columns[2], self.five_feature_columns[3],
                                                          self.five_feature_columns[4],
                                                          self.two_group_columns[0],    self.two_group_columns[1],
                                                          'Total Ratings',              'User Rating',
                                                          'Recommended By'])
        self.product_similarity  = None
        self.current_user        = None
        
    def set_current_user(self, current_user):
        self.current_user = current_user
        
        return self.current_user
    
    def clear_current_user(self):
        self.current_user = None
        
        return self.current_user
    
    def load_content_similarity_matrix(self, file_path):
        self.product_similarity = pd.read_pickle(file_path)
        
        return self.product_similarity
        
    # appends the first recommendation not already in the recommender history
    def append_new_recommendation(self, recommendations, recommender):
        new_recommendation = None
        
        for recommendation in recommendations:
            if recommendation not in self.recommender_history[self.rating_column].unique():
                descriptor    = self.dataframe.loc[
                    self.dataframe[self.rating_column] == recommendation].iloc[0][self.descriptor]
                feature_one   = self.dataframe.loc[
                    self.dataframe[self.rating_column] == recommendation].iloc[0][self.five_feature_columns[0]]
                feature_two   = self.dataframe.loc[
                    self.dataframe[self.rating_column] == recommendation].iloc[0][self.five_feature_columns[1]]
                feature_three = self.dataframe.loc[
                    self.dataframe[self.rating_column] == recommendation].iloc[0][self.five_feature_columns[2]]
                feature_four  = self.dataframe.loc[
                    self.dataframe[self.rating_column] == recommendation].iloc[0][self.five_feature_columns[3]]
                feature_five  = self.dataframe.loc[
                    self.dataframe[self.rating_column] == recommendation].iloc[0][self.five_feature_columns[4]]
                column_one    = self.dataframe.loc[
                    self.dataframe[self.rating_column] == recommendation].iloc[0][self.two_group_columns[0]]
                column_two    = self.dataframe.loc[
                    self.dataframe[self.rating_column] == recommendation].iloc[0][self.two_group_columns[1]]
                    
                new_recommendation = {
                    self.rating_column:           recommendation,
                    self.descriptor:              descriptor,
                    self.two_group_columns[0]:    column_one,
                    self.two_group_columns[1]:    column_two,
                    self.five_feature_columns[0]: feature_one,
                    self.five_feature_columns[1]: feature_two,
                    self.five_feature_columns[2]: feature_three,
                    self.five_feature_columns[3]: feature_four,
                    self.five_feature_columns[4]: feature_five,
                    'Total Ratings':              self.dataframe[self.rating_column].value_counts()[recommendation],
                    'User Rating':                -1,
                    'Recommended By':             recommender}
                
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
        new_recommendation = self.append_new_recommendation(recommendations, 'Most Rated Products')
        
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
    
    def best_one_subcategory(self):
        best_one = self.best_nine()[0]
        
        df              = self.dataframe[[self.rating_column] + self.two_group_columns]
        df              = df.loc[df[self.two_group_columns[0]] == best_one[0]]
        df              = df.loc[df[self.two_group_columns[1]] == best_one[1]]
        recommendations = df[self.rating_column].value_counts().index
        
        new_recommendation = self.append_new_recommendation(recommendations, 'Best One Subcategory')
        
        return new_recommendation
    
    # returns the URL of the product with the most ratings in the top nine groups
    def best_nine_subcategories(self):
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
            
            new_recommendation = self.append_new_recommendation(recommendations, 'Best Nine Subcategories')
            i += 1
        
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
    
    # get utility matrix of current user in the recommender history
    def current_utility_matrix(self):
        
        # create local user utility matrix from recommender history
        current_utility_matrix           = pd.DataFrame(columns = ['User', 'URL', 'Rating'])
        current_utility_matrix['URL']    = self.recommender_history['URL']
        current_utility_matrix['Rating'] = self.recommender_history['User Rating']
        current_utility_matrix['User']   = self.current_user
        
        # combine local user utility matrix with global utility matrix
        current_utility_matrix = current_utility_matrix.append(
            self.utility_matrix[['User', 'URL', 'Rating']], ignore_index = True)
        
        return current_utility_matrix
    
    # grid search for matrix factorization with singular value decomposition
    def grid_search_singular_value_decomposition(self, params):
        
        # build and fit full grid search with the SVD training set
        current_utility_matrix = self.current_utility_matrix()
        reader                 = Reader(rating_scale = (1, 5))
        data                   = Dataset.load_from_df(current_utility_matrix[['User', 'URL', 'Rating']], reader)
        gs                     = GridSearchCV(SVD,
                                              param_grid = params,
                                              measures   = ['rmse', 'mae'],
                                              cv         = 5)
        gs.fit(data)
        
        return (gs.best_score['rmse'], gs.best_params['rmse'])
    
    # matrix factorization with singular value decomposition for last user in Mongo database
    def singular_value_decomposition(self, n_factors, reg_all):
        
        # build and fit full SVD training set
        current_utility_matrix = self.current_utility_matrix()
        reader                 = Reader(rating_scale = (1, 5))
        data                   = Dataset.load_from_df(current_utility_matrix[['User', 'URL', 'Rating']], reader)
        dataset                = data.build_full_trainset()
        algo                   = SVD(n_factors = n_factors, reg_all = reg_all)
        algo.fit(dataset)
        
        # calculate SVD predictions for local user
        recommendations        = current_utility_matrix.drop(['User', 'Rating'], axis=1).drop_duplicates()
        recommendations['SVD'] = recommendations['URL'].apply(lambda x: algo.predict(self.current_user, x)[3])
        recommendations        = recommendations.sort_values(by = 'SVD', ascending = False)['URL']
        
        new_recommendation = self.append_new_recommendation(recommendations, 'Singular Value Decomposition')
        
        return new_recommendation