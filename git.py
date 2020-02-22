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
import numpy as np
from sklearn.preprocessing import OneHotEncoder


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

##def dateToYear(datestr, monthvalue = {1:0, 2:31, 3:59, 4:90, 5:120, 6:151, 7:181, 8:212, 9:243, 10:273, 11:304, 12:334}):
##    year, month, day = [int(i) for i in datestr.split("-")]
##    return year-2017
## 
##def dateToDay(datestr, monthvalue = {1:0, 2:31, 3:59, 4:90, 5:120, 6:151, 7:181, 8:212, 9:243, 10:273, 11:304, 12:334}):
##    year, month, day = [int(i) for i in datestr.split("-")]
##    return monthvalue[month] + day
## 
##df["day"] = df["date"].apply(dateToDay)
##df["year"] = df["date"].apply(dateToYear)

#city_id ekleme

df["city_id"] = ""
for i in citydf["store_id"]:
    df["city_id"][df["store_id"]==i] = citydf[citydf["store_id"]==i].iloc[0]["city_id"]

#ultimatehier ekleme
    
df["ULTIMATEHIER"]= 1
df.head(10)
l = 0
for i,j,k in hierdict.keys():
    l+=1
    df["ULTIMATEHIER"][(df["hierarchy_id_1"]==i) & (df["hierarchy_id_2"]==j) & (df["hierarchy_id_3"]==k)] = l
#product_id,store_id,hierleri çıkarma
print("f823", df.shape)
df = df.drop("store_id", axis = 1)
df = df.drop("product_id", axis = 1)
df = df.drop("hierarchy_id_1", axis = 1)
df = df.drop("hierarchy_id_2", axis = 1)
df = df.drop("hierarchy_id_3", axis = 1)
onehotencoder= OneHotEncoder(sparse = False)
a = onehotencoder.fit_transform(df[["city_id"]])
a = pd.DataFrame({'a0': a[:, 0], 'a1': a[:, 1], 'a2': a[:, 2],'a3': a[:, 3],'a4': a[:, 4],'a5': a[:, 5],'a6': a[:, 6],'a7': a[:, 7],'a8': a[:, 8],'a9': a[:, 9],'a10': a[:, 10],'a11': a[:, 11],'a12': a[:, 12]})
a = a.astype("int8")
print("f93v", df.shape)
df = pd.concat((df,a),axis = 1)
del a
print("c9dh", df.shape)
df["date"].astype("int16")
df = df.drop("city_id",axis = 1)
df = df.drop("a0", axis = 1)
b = onehotencoder.fit_transform(df[["ULTIMATEHIER"]])
b = pd.DataFrame({f"b{i}": b[:, i] for i in range(20)})
b =b.astype("int8")
df = pd.concat((df,b),axis = 1)