#!/usr/bin/python

"""
Odpalanie: ./model_gen_forest.py
"""

################################################################

#import

import numpy as np
import pandas as pd
from sklearn import tree
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.externals import joblib

################################################################

#wczytywanie danych z plikow
data1415 = pd.read_csv('./1415.csv', sep = ',')
data16 = pd.read_csv('./16.csv', sep = ',')

#zbior uczacy - sezony 14 i 15
#walidacja - pierwsza polowa sezonu 16
#test - druga polowa sezonu 16
train = data1415
val = data16[0:2929]
test = data16[2929:]

#zbior uczacy
X = train[['T_d0', 'P_d0', 'Z_d0', 'W/W']]
Y = np.ravel(train[['Qrz']])

#parametry regresora
regr_1 = RandomForestRegressor(n_estimators=10, min_samples_leaf=5)

#uczenie
regr_1.fit(X, Y)

#in-sample error
Y_pred_in = regr_1.predict(X)
score_in = r2_score(Y, Y_pred_in)

print score_in

#TODO walidacja

#out-of-sample error
#zbior testowy - sprawdzam jakosc przewidywan
X_test = val[['T_d0', 'P_d0', 'Z_d0', 'W/W']]
Y_test = val[['Qrz']]
#przewidywanie wynikow dla danych testowych
Y_pred_out = regr_1.predict(X_test)
#porownanie z prawdziwymi danymi
score_out = r2_score(Y_test, Y_pred_out)

print score_out

#zapis nauczonego estymatora do pliku
joblib.dump(regr_1, 'forest_regr.pkl')

"""
Wczytywanie zapisanego estymatora w innym pliku:
regr_1 = joblib.load('forest_regr.pkl') 
"""

































