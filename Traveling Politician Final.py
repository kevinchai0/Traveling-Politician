#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import math
from sympy.combinatorics import Permutation
from itertools import permutations 


# Function to calculate distances between longitudes and latitudes.
# 
# Credits to: https://gist.github.com/rochacbruno/2883505

# In[2]:


def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1))         * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d


# In[3]:


def long_lat(abbreviation):
    table = capitals.loc[capitals["abbreviation"] == abbreviation]
    long = table["longitude"].values[0]
    lat = table["latitude"].values[0]
    return [long,lat]


# In[15]:


capitals = pd.read_csv("us-state-capitals.csv")
state_abbreviations = list(capitals["abbreviation"])


# In[18]:


start = long_lat("IA")
end = [-77.0369, 38.8951] #longitude and latitude for the white house(ending point)
distance(start,end)


# In[64]:


def total_distance(start, middle_states, end):
    total_dist = 0
    path = []
    ret = {}
    for i in range(len(middle_states)):
        total_dist += distance(start, (long_lat(middle_states[i])))
        path.append(middle_states[i])
        start = long_lat(middle_states[i])    
        
#adding path to DC
    total_dist += distance(long_lat(middle_states[-1]), end)
    path.append("D.C")
    ret[total_dist] = path
    return ret


# In[103]:


def shortest_path(middle_states):
    all_distances = []
    final = []
    perms = list(permutations(middle_states))
    start = long_lat("IA")
    end = [-77.0369, 38.8951] #longitude and latitude for the white house(ending point)
    for perm in perms:
        x = total_distance(start, perm, end)
        final.append(x)
        all_distances.append(list(x.keys())[0])
    min_dist = min(all_distances)
    for dict in final:
        if min_dist in dict.keys():
            final_path = dict.get(min_dist)
    return (final_path,min_dist)


# In[109]:


def run():
    middle_states = []
    input_nums = int(input("How many states do you want to visit? "))
    while input_nums > 0:
        input_state = input("Enter the capitalized state abbreviation of a state you want to visit: ")
        if input_state not in state_abbreviations:
            print ("Invalid state")
        else:
            middle_states.append(input_state)
            input_nums -= 1
    return shortest_path(middle_states)


# In[ ]:


run()

