from data import CITIES, BUSINESSES, USERS, REVIEWS, TIPS, CHECKINS

import random
import json
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

def extract_categories(businesses):
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
    
    pivoted_data = pivot_ratings(extracted_categories)

    sim = create_similarity_matrix_categories(pivoted_data)

# def eat_place(user_id, n):
    
#     for city in CITIES:
#         for business in BUSINESSES[city]:
#             categ = pd.Series(data=[business["categories"]])
#             if categ.isin(["Food"]).any() or categ.isin(["Restaurants"]).any() or categ.isin(["Bars"]).any():
#                 return BUSINESSES[business]

