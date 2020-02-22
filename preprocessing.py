from timeit import timeit

# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 01:11:21 2020

@author: ufukprox
"""
import pandas as pd
#import sklearn as sk
import numpy as np

def AAAA():
	# importing
	np.concatenate((np.array([2,3]), np.array([3,4])))
	aa = pd.read_csv("C:/Users/canbora/Desktop/shortsales.csv", delimiter = ",")
	ab = pd.read_csv("C:/Users/canbora/Desktop/Data/product_hierarchy.csv", delimiter = "|")
	ac = pd.read_csv("C:/Users/canbora/Desktop/Data/store_cities.csv", delimiter = "|")

	# product_id ye gore siralama, muhtemelen tarih ile degistirilecek

	aa.sort_values("product_id", ascending = "True", inplace = True)
	aa = aa.reset_index(drop= True)

	# dummy variable uretme

	store_id = aa.iloc[:, 0].values

	product_id = aa.iloc[:, 1].values
	"""
	from sklearn import preprocessing as prep
	imputer = prep.Imputer(missing_values = "NaN",strategy = "mean", axis = 0)
	imputer.fit(store_id)
	store_id = imputer.fit_transform(store_id)

	store_id = np.array(ct.fit_transform(store_id), dtype="int8")
	store_id = labelencoder_X.fit_transform(store_id)
	store_id.reshape()
	onehotencoder = OneHotEncoder(categories = aa[store_id].values)
	store_id = onehotencoder.fit_transform(store_id).toarray()
	labelencoder_y = LabelEncoder()
	y = """

	# hierleri product id ile concateleme
	hier1, hier2 , hier3 = [], [], []
	for i in product_id:
	    hier1.append(ab.iloc[i-1,1])
	    hier2.append(ab.iloc[i-1,2])
	    hier3.append(ab.iloc[i-1,3])
	hier1 = np.array(hier1, dtype = "int8")
	hier2 = np.array(hier2, dtype = "int8")
	hier3 = np.array(hier3, dtype = "int8")

	productandhiers = np.concatenate(([product_id], [hier1], [hier2], [hier3]), axis = 0)

print(timeit(AAAA, number = 10))