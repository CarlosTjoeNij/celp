from data import CITIES, BUSINESSES, USERS, REVIEWS, TIPS, CHECKINS
import sklearn.metrics.pairwise as pw
import random
import pandas as pd
import numpy as np
from pandas import Series, DataFrame

# create DataFrame with business name as index, categories as value
businessdict= {}
for city in CITIES:
    for business in BUSINESSES[city]:
        businessdict[business["name"]] = business["categories"]
pd.DataFrame.from_dict(businessdict, orient= "index")

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
    if not city:
        city = random.choice(CITIES)
    return random.sample(BUSINESSES[city], n)

# def eat_place(user_id, n):
    
#     for city in CITIES:
#         for business in BUSINESSES[city]:
#             categ = pd.Series(data=[business["categories"]])
#             if categ.isin(["Food"]).any() or categ.isin(["Restaurants"]).any() or categ.isin(["Bars"]).any():
#                 return BUSINESSES[business]
