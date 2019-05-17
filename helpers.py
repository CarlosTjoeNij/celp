from data import CITIES, BUSINESSES, USERS, REVIEWS, TIPS, CHECKINS

import data
import json
from pandas.io.json import json_normalize
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# creates similarity matrix based of categories
def create_similarity_matrix_categories(matrix):
    npu = matrix.values
    m1 = npu @ npu.T
    diag = np.diag(m1)
    m2 = m1 / diag
    m3 = np.minimum(m2, m2.T)
    return pd.DataFrame(m3, index = matrix.index, columns = matrix.index)

# extracts all categories
def extract_categories(businesses):
    cat_b = businesses.apply(lambda row: pd.Series([row['business_id']] + row['categories'].lower().split(",")), axis=1)
    stack_cat = cat_b.set_index(0).stack()
    df_stack_cat = stack_cat.to_frame()
    df_stack_cat['business_id'] = stack_cat.index.droplevel(1)
    df_stack_cat.columns = ['categories', 'business_id']
    return df_stack_cat.reset_index()[['business_id', 'categories']]

def pivot_ratings(df):
    return df.pivot_table(index = 'business_id', columns = 'categories', aggfunc = 'size', fill_value=0)

# predicts ratings based of similarity and given ratings
def predict_ratings(similarity, utility, to_predict, n):
    # copy input (don't overwrite)
    ratings_test_c = to_predict.copy()
    # apply prediction to each row
    ratings_test_c['predicted rating'] = to_predict.apply(lambda row: predict_ids(similarity, utility, row['user_id'], row['business_id'], n), axis=1)
    return ratings_test_c

def predict_ids(similarity, utility, userId, itemId, n):
    # select right series from matrices and compute
    if userId in utility.columns and itemId in similarity.index:
        return predict_vectors(utility.loc[:,userId], similarity[itemId], n)
    return np.nan

def predict_vectors(user_ratings, similarities, n):
    # select only businesses actually rated by user
    relevant_ratings = user_ratings.dropna()
    
    # select corresponding similairties
    similarities_s = similarities[relevant_ratings.index]
    
    # select neighborhood
    similarities_s = similarities_s[similarities_s > 0.0]
    relevant_ratings = relevant_ratings[similarities_s.index]
    
    # if there's nothing left return a prediction of 0
    norm = similarities_s.sum()
    if(norm == 0) or len(similarities_s) < n:
        return np.nan
    
    # compute a weighted average (i.e. neighborhood is all) 
    return np.dot(relevant_ratings, similarities_s)/norm

def create_utility_matrix(df):
    return df.pivot(values='stars', columns='user_id', index='business_id')