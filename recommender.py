from data import CITIES, BUSINESSES, USERS, REVIEWS, TIPS, CHECKINS


import random
import json
from pandas.io.json import json_normalize
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def create_similarity_matrix_categories(matrix):
    """Create a  similarity matrix"""
    npu = matrix.values
    m1 = npu @ npu.T
    diag = np.diag(m1)
    m2 = m1 / diag
    m3 = np.minimum(m2, m2.T)
    return pd.DataFrame(m3, index = matrix.index, columns = matrix.index)

def extract_genres(businesses):
    """Create an unfolded genre dataframe. Unpacks genres seprated by a '|' into seperate rows.
    """
    cat_b = businesses.apply(lambda row: pd.Series([row['business_id']] + row['categories'].lower().split(",")), axis=1)
    stack_cat = cat_b.set_index(0).stack()
    df_stack_cat = stack_cat.to_frame()
    df_stack_cat['business_id'] = stack_cat.index.droplevel(1)
    df_stack_cat.columns = ['categories', 'business_id']
    return df_stack_cat.reset_index()[['business_id', 'categories']]

def pivot_ratings(df):
    return df.pivot_table(index = 'business_id', columns = 'categories', aggfunc = 'size', fill_value=0)

def predict_ratings(similarity, utility, to_predict, n):
    """Predicts the predicted rating for the input test data.
    
    Arguments:
    similarity -- a dataFrame that describes the similarity between items
    utility    -- a dataFrame that contains a rating for each user (columns) and each movie (rows). 
                  If a user did not rate an item the value np.nan is assumed. 
    to_predict -- A dataFrame containing at least the columns movieId and userId for which to do the predictions
    """
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
    # select only movies actually rated by user
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
    """Creates a utility matrix from a DataFrame (which contains at least the columns stars, user_id, and business_id)"""
    return df.pivot(values='stars', columns='user_id', index='business_id')

def recommend(user_id=None, business_id=None, city=None, n=10):
    """
    Returns n recommendations as a list of dicts.
    Optionally takes in a user_id, business_id and/or city.
    A recommendation is a dictionary in the form of:
        {
            business_id:str
            stars:str
            name:str
            city:str
            adress:str
        }
    """

    l=[]
    businessdict= {}
    for city in CITIES:
        for business in BUSINESSES[city]:
            businessdict[business["business_id"]] = business["categories"]
    df_categories = pd.DataFrame.from_dict(businessdict, orient= "index", columns=['categories'])
    df_categories['business_id'] = df_categories.index

    extracted_categories = extract_categories(df_categories)
    
    gepivoteerde_data = pivot_ratings(extracted_categories)

    sim = create_similarity_matrix_categories(gepivoteerde_data)

    for city in CITIES:
        reviews = REVIEWS[city]
        df_rev= pd.DataFrame.from_dict(json_normalize(reviews), orient='columns')
    
    df_review = df_rev.drop_duplicates(subset=["business_id", "user_id"], keep="last").reset_index()[["business_id", "stars", "user_id"]]
    
    ratings_utility = create_utility_matrix(df_review)

    predicted = predict_ratings(sim, ratings_utility, df_review, 0)

    return predicted.sort_values(by='predicted rating', ascending=False)[:10]

# def eat_place(user_id, n):
    
#     for city in CITIES:
#         for business in BUSINESSES[city]:
#             categ = pd.Series(data=[business["categories"]])
#             if categ.isin(["Food"]).any() or categ.isin(["Restaurants"]).any() or categ.isin(["Bars"]).any():
#                 return BUSINESSES[business]

