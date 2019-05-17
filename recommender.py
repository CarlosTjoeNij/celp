from data import CITIES, BUSINESSES, USERS, REVIEWS, TIPS, CHECKINS
from helpers import *

import random
import data

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

    # create dataframe containing business id and all categories
    businessdict= {}
    for city in CITIES:
        for business in BUSINESSES[city]:
            businessdict[business["business_id"]] = business["categories"]
    df_categories = pd.DataFrame.from_dict(businessdict, orient= "index", columns=['categories'])
    df_categories['business_id'] = df_categories.index

    # extract categories and compute similarity based of categories
    extracted_categories = extract_categories(df_categories)
    pivoted_data = pivot_ratings(extracted_categories)
    sim = create_similarity_matrix_categories(pivoted_data)

    # create dataframe containing reviews
    for city in CITIES:
        reviews = REVIEWS[city]
        df_rev= pd.DataFrame.from_dict(json_normalize(reviews), orient='columns')
    # delete duplicates, and keep most recent ones
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

