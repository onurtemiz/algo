import keras

import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense


    # importing
df = pd.read_csv(r"C:\Users\ufukprox\Downloads\algorun20-data(1)\data\sales.csv", delimiter = "|")
basedf = pd.read_csv(r"C:\Users\ufukprox\Downloads\algorun20-data(1)\data\product_hierarchy.csv", delimiter = "|")
citydf = pd.read_csv(r"C:\Users\ufukprox\Downloads\algorun20-data(1)\data\store_cities.csv", delimiter = "|")


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


def dateToYear(datestr, monthvalue = {1:0, 2:31, 3:59, 4:90, 5:120, 6:151, 7:181, 8:212, 9:243, 10:273, 11:304, 12:334}):
    year, month, day = [int(i) for i in datestr.split("-")]
    return year-2017
     
def dateToDay(datestr, monthvalue = {1:0, 2:31, 3:59, 4:90, 5:120, 6:151, 7:181, 8:212, 9:243, 10:273, 11:304, 12:334}):
    year, month, day = [int(i) for i in datestr.split("-")]
    return monthvalue[month] + day
     
df["day"] = df["date"].apply(dateToDay)
df["year"] = df["date"].apply(dateToYear)

    #city_id ekleme

df["city_id"] = ""
for i in citydf["store_id"]:
    df["city_id"][df["store_id"]==i] = citydf[citydf["store_id"]==i].iloc[0]["city_id"]

    #ultimatehier ekleme
        
df["ULTIMATEHIER"]= 1
l = 0
for i,j,k in hierdict.keys():
    l+=1
    df["ULTIMATEHIER"][(df["hierarchy_id_1"]==i) & (df["hierarchy_id_2"]==j) & (df["hierarchy_id_3"]==k)] = l
    
#product_id,store_id,hierleri çıkarma

df = df.drop("date", axis = 1)
df = df.drop("store_id", axis = 1)
df = df.drop("product_id", axis = 1)
df = df.drop("hierarchy_id_1", axis = 1)
df = df.drop("hierarchy_id_2", axis = 1)
df = df.drop("hierarchy_id_3", axis = 1)

#creating dummy variable

onehotencoder= OneHotEncoder(sparse = False)
a = onehotencoder.fit_transform(df[["city_id"]])
a = pd.DataFrame({'a0': a[:, 0], 'a1': a[:, 1], 'a2': a[:, 2],'a3': a[:, 3],'a4': a[:, 4],'a5': a[:, 5],'a6': a[:, 6],'a7': a[:, 7],'a8': a[:, 8],'a9': a[:, 9],'a10': a[:, 10],'a11': a[:, 11],'a12': a[:, 12]})
a = a.astype("int8")


df = pd.concat((df,a),axis = 1)
del a

df = df.drop("city_id",axis = 1)
df = df.drop("a0", axis = 1)

b = onehotencoder.fit_transform(df[["ULTIMATEHIER"]])
b = pd.DataFrame({f"b{i}": b[:, i] for i in range(len(hierdict)-2)})
b = b.astype("int8")
df = pd.concat((df,b),axis = 1)
del b

#standard scaling

sc = StandardScaler()

# ann model

classifier = Sequential()
classifier.add(Dense(units = 6, kernel_initializer = 'uniform', activation = 'relu', input_dim = 36))
classifier.add(Dense(units = 6, kernel_initializer = 'uniform', activation = 'relu'))
classifier.add(Dense(units = 1, kernel_initializer = 'uniform', activation = 'relu'))
classifier.add(Dense(units = 1, kernel_initializer = 'uniform', activation = 'relu'))

# ordering columns of df

df = df.reindex(sorted(df.columns), axis=1)
print(df.columns)

# starting the loop

oooo = 0

for iiii in range(0, 100000, 5000):
    dd = df.iloc[iiii:iiii+5000]

    while len(dd.columns) < 37:
        dd["extra" + str(len(dd.columns))] = 0
    X = (dd.drop("sales_quantity", axis = 1)).iloc[:,:].values
    y = dd["sales_quantity"].values
    

    del dd
    # Splitting the dataset into the Training set and Test set

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
    
    # Feature Scaling
    
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
    classifier.fit(X_train, y_train, batch_size = 25, epochs = 1)
    
    oooo += 1
    print(oooo, "out of 500")
    if oooo == 20:
        break
    # Predicting the Test set results
    
y_pred = classifier.predict(X_test)

print(df.columns)
del df

    # za
realtestdf = pd.read_csv(r"C:\Users\ufukprox\Downloads\algorun20-data(1)\data\test.csv", delimiter = "|")
testdf = pd.read_csv(r"C:\Users\ufukprox\Downloads\algorun20-data(1)\data\sample_submission.csv", delimiter = "|")
obtainpromo1 = pd.read_csv(r"C:\Users\ufukprox\Downloads\algorun20-data(1)\data\test.csv", delimiter = "|")
testdf["is_promo"] = obtainpromo1["is_promo"].values
testdf["hierarchy_id_1"] = np.asarray(basedf.iloc[testdf["product_id"]-1]["hierarchy_id_1"])
testdf["hierarchy_id_2"] = np.asarray(basedf.iloc[testdf["product_id"]-1]["hierarchy_id_2"])
testdf["hierarchy_id_3"] = np.asarray(basedf.iloc[testdf["product_id"]-1]["hierarchy_id_3"])
testdf["day"] = testdf["date"].apply(dateToDay)
testdf["year"] = testdf["date"].apply(dateToYear)

testdf["city_id"] = ""

for i in citydf["store_id"]:
    testdf["city_id"][testdf["store_id"]==i] = citydf[citydf["store_id"]==i].iloc[0]["city_id"]

testdf["ULTIMATEHIER"]= 1
l = 0
for i,j,k in hierdict.keys():
    l+=1
    testdf["ULTIMATEHIER"][(testdf["hierarchy_id_1"]==i) & (testdf["hierarchy_id_2"]==j) & (testdf["hierarchy_id_3"]==k)] = l

#product_id,store_id,hierleri çıkarma
    
testdf = testdf.drop("date", axis = 1)
testdf = testdf.drop("store_id", axis = 1)
testdf = testdf.drop("product_id", axis = 1)
testdf = testdf.drop("hierarchy_id_1", axis = 1)
testdf = testdf.drop("hierarchy_id_2", axis = 1)
testdf = testdf.drop("hierarchy_id_3", axis = 1)

a = onehotencoder.fit_transform(testdf[["city_id"]])
a = pd.DataFrame({'a0': a[:, 0], 'a1': a[:, 1], 'a2': a[:, 2],'a3': a[:, 3],'a4': a[:, 4],'a5': a[:, 5],'a6': a[:, 6],'a7': a[:, 7],'a8': a[:, 8],'a9': a[:, 9],'a10': a[:, 10],'a11': a[:, 11],'a12': a[:, 12]})
a = a.astype("int8")

testdf = pd.concat((testdf,a),axis = 1)
del a
testdf = testdf.drop("city_id",axis = 1)
testdf = testdf.drop("a0", axis = 1)
b = onehotencoder.fit_transform(testdf[["ULTIMATEHIER"]])
b = pd.DataFrame({f"b{i}": b[:, i] for i in range(len(hierdict)-2)})
b = b.astype("int8")
testdf = pd.concat((testdf,b),axis = 1)
del b
testdf["order_quantity"] = 0
K = (testdf.drop("prediction", axis = 1)).iloc[:,:]
K = K.values
##testdf = testdf.drop("order_quantity", axis = 1)
#testdf["prediction"] = 0
#m = testdf.values
#print(testdf.columns)
#from sklearn.preprocessing import Imputer
#imputer = Imputer()
#K_test = imputer.fit()
#K_train, K_test, m_train, m_test = train_test_split(K, m, test_size = 1, random_state = 0)

K = sc.fit_transform(K)

#K_test = sc.transform(K_test)
m_pred = classifier.predict(K)
print(testdf)
print(m_pred)
testdf["prediction"] = m_pred
print(testdf.head(10))
Kcsv = testdf.to_csv("transport.csv")

    # Making the Confusion Matrix

