# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 14:09:53 2020

@author: ufukprox
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 01:11:21 2020

@author: ufukprox
"""
import pandas as pd
import sklearn as sk
import numpy as np


# importing
np.concatenate((np.array([2,3]), np.array([3,4])))
df = pd.read_csv("sales.csv", delimiter = "|")
basedf = pd.read_csv("product_hierarchy.csv", delimiter = "|")
citydf = pd.read_csv("store_cities.csv", delimiter = "|")

# product_id ye göre sıralama, muhtemelen tarih ile değiştirilecek

df.sort_values("product_id", ascending = "True", inplace = True)
df = df.reset_index(drop= True)

#hierarchyleri df'e ekleme

hierdict = {}
for i in range(1,15):
    for j in range(1,19):
        for k in range(1,19):
            if len(basedf[(basedf["hierarchy_id_1"]==i) & (basedf["hierarchy_id_2"]==j) & (basedf["hierarchy_id_3"]==k) ]) != 0:
                hierdict[(i,j,k)] = basedf[(basedf["hierarchy_id_1"]==i) & (basedf["hierarchy_id_2"]==j)& (basedf["hierarchy_id_3"]==k)]
df["hierarchy_id_1"] = np.asarray(basedf.iloc[df["product_id"]-1]["hierarchy_id_1"])
df["hierarchy_id_2"] = np.asarray(basedf.iloc[df["product_id"]-1]["hierarchy_id_2"])
df["hierarchy_id_3"] = np.asarray(basedf.iloc[df["product_id"]-1]["hierarchy_id_3"])

#dateleri sayılara çevirme
def dateToInt(datestr, monthvalue = {1:0, 2:31, 3:59, 4:90, 5:120, 6:151, 7:181, 8:212, 9:243, 10:273, 11:304, 12:334}):
	year, month, day = [int(i) for i in datestr.split("-")]
	return (year-2017)*365 + monthvalue[month] + day
df["date"]= df["date"].apply(dateToInt)

#city_id ekleme

df["city_id"] = ""
for i in citydf["store_id"]:
    df["city_id"][df["store_id"]==i] = citydf[citydf["store_id"]==i].iloc[0]["city_id"]
df["ULTIMATEHIER"].iloc[0] = 2
df.head(10)
for i,j,k in hierdict.keys():
    print(i,j,k,type(i))
for ind, tup in enumerate(hierdict.keys()):
    i,j,k = tup
    print(i,j,k)
    print(df["ULTIMATEHIER"].head(10))
    df["ULTIMATEHIER"][(df["hierarchy_id_1"]==i) & (df["hierarchy_id_2"]==j) & (df["hierarchy_id_1"]==k)] = ind
    print(df["ULTIMATEHIER"][(df["hierarchy_id_1"]==i) & (df["hierarchy_id_2"]==j) & (df["hierarchy_id_1"]==k)])

print(df["ULTIMATEHIER"].head(10))