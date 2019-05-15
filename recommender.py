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

def utilityMatrix(USERS, BUSINESSES, REVIEWS, CITIES):
    business_id = [business["business_id"] for city in CITIES for business in BUSINESSES[city]]
    user_id = [user["user_id"] for city in CITIES for user in USERS[city]]

    matrix= pd.DataFrame(np.nan, columns= user_id, index= business_id, dtype= float)

    for user in user_id:
        for business in business_id:
            matrix.loc[business][user]= get_rating(REVIEWS, user, business)
    return matrix

def cosine_similarity(matrix=utility, business1, business2):
    selected_features= matrix.loc[business1].notna() & matrix.loc[business2].notna()

    if business1== business2:
        return 1

    if not selected_features.any():
        return 0

    features1= matrix.loc[business1][selected_features]
    features2= matrix.loc[business2][selected_features]
    
    if (features1==0.0).all() or (features2==0.0).all():
        return 0

    num= (features1 * features2).sum()
    den= np.sqrt((features1**2).sum()) * np.sqrt((features2**2).sum())

    if num == 0 or den == 0:
        return 0
    else:
        return num/den
    
def simMatrix(matrix=utility):
    similiarityMatrix= pd.DataFrame(0, index=matrix.index, columns=matrix.index, dtype=float)

    for business1 in BUSINESSES:
        for business2 in BUSINESSES:
            for user in USERS:
                similiarityMatrix.xs(business1)[business2]= cosine_similarity(matrix, business1, business2)

    return similiarityMatrix

def meanCenteredSim(matrix= utility):
    return matrix.sub(matrix.mean())
