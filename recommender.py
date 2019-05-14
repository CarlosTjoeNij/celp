from data import CITIES, BUSINESSES, USERS, REVIEWS, TIPS, CHECKINS

import random
import pandas as pd
import numpy as np
from pandas import Series, DataFrame

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

def eat_place(user_id=None, n=10):
    l = []
    for city in CITIES:
        for business in BUSINESSES[city]:
            for x in business["categories"] 
                if x == "Restaurants" or "Bars" or "Sports Bars":
                    l.append(business["business_id"])
    
    return l
