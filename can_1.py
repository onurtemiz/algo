import pandas as pd
import numpy as np

def read_csv(filename, delimiter, **kwargs):
	if "dtype" in kwargs and "chunksize" in kwargs:
		return pd.concat(pd.read_csv(filename, delimiter = delimiter, chunksize = kwargs["chunksize"], dtype = kwargs["dtype"]))
	elif "dtype" in kwargs:
		return pd.read_csv(filename, delimiter = delimiter, dtype = kwargs["dtype"])
	elif "chunksize" in kwargs:
		return pd.concat(pd.read_csv(filename, delimiter = delimiter, chunksize = kwargs["chunksize"]))
	else:
		return pd.read_csv(filename, delimiter = delimiter)

def dateToInt(datestr, monthvalue = {1:0, 2:31, 3:59, 4:90, 5:120, 6:151, 7:181, 8:212, 9:243, 10:273, 11:304, 12:334}):
	year, month, day = [int(i) for i in datestr.split("-")]
	return (year-2017)*365 + monthvalue[month] + day

def storeToCity(store_id):
	return citydf[citydf["store_id"] == store_id].iloc[0]["city_id"]

basedf = read_csv("shortsales.csv", ",", chunksize = 100000)
basedf.sort_values("date", ascending = "True", inplace = True)
basedf.sort_values("product_id", ascending = "True", inplace = True)
basedf.sort_values("store_id", ascending = "True", inplace = True)
basedf.reset_index(drop= True, inplace = True)

hierdf = read_csv("C:/Users/canbora/Desktop/Data/product_hierarchy.csv", "|", dtype = "int8")
citydf = read_csv("C:/Users/canbora/Desktop/Data/store_cities.csv", "|")

promodf = read_csv("C:/Users/canbora/Desktop/Data/test.csv", "|")
promodf.sort_values("product_id", ascending = "True", inplace = True)
promodf.sort_values("product_id", ascending = "True", inplace = True)
promodf.sort_values("product_id", ascending = "True", inplace = True)
promodf.reset_index(drop= True, inplace = True)

basedf["hierarchy_id_1"] = np.asarray(hierdf.iloc[basedf["product_id"]-1]["hierarchy_id_1"])
basedf["hierarchy_id_2"] = np.asarray(hierdf.iloc[basedf["product_id"]-1]["hierarchy_id_2"])
basedf["hierarchy_id_3"] = np.asarray(hierdf.iloc[basedf["product_id"]-1]["hierarchy_id_3"])
basedf["city_id"] = basedf["store_id"].apply(storeToCity)
basedf["date"] = basedf["date"].apply(dateToInt)

