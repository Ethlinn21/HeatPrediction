#!/usr/bin/python

"""
Odpalanie: ./model_generator.py

jesli graphviz nie jest zainstalowany:
sudo easy_install graphviz
"""

################################################################

#import

import numpy as np
import pandas as pd
import graphviz
from sklearn import tree
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt

################################################################

#skrypt

#wczytywanie danych z plikow
data1415 = pd.read_csv('./1415.csv', sep = ',')
data16 = pd.read_csv('./16.csv', sep = ',')

#print data1415.info()
#print data16.info()

#zbior uczacy - sezony 14 i 15
#walidacja - pierwsza polowa sezonu 16
#test - druga polowa sezonu 16
train = data1415
val = data16[0:2929]
test = data16[2929:]

#zbior uczacy
X = train[['T_d0', 'P_d0', 'Z_d0', 'W/W']]
Y = train[['Qrz']]

#parametry regresora - ograniczenie glebokosci drzewa i minimalnej ilosci probek w lisciu
regr_1 = DecisionTreeRegressor(max_depth=4, min_samples_leaf=5)

#rng = np.random.RandomState(1)
#regr_1 = AdaBoostRegressor(DecisionTreeRegressor(max_depth=4), n_estimators=300, random_state=rng)

#uczenie
regr_1.fit(X, Y)

#in-sample error
Y_pred_in = regr_1.predict(X)
score_in = r2_score(Y, Y_pred_in)

print score_in

#out-of-sample error
#zbior testowy - sprawdzam jakosc przewidywan
X_test = test[['T_d0', 'P_d0', 'Z_d0', 'W/W']]
Y_test = test[['Qrz']]
#przewidywanie wynikow dla danych testowych
Y_pred_out = regr_1.predict(X_test)
#porownanie z prawdziwymi danymi
score_out = r2_score(Y_test, Y_pred_out)

print score_out


################################################################

#wykresy
'''
plt.figure()
plt.scatter(X_test[['T_d0']], Y_test, s=10, edgecolor="black", c="darkorange", label="test data")
plt.scatter(X_test[['T_d0']], Y_pred_out,  s=10, edgecolor="black", c="cornflowerblue", label="predicted data")
plt.xlabel("T_d0")
plt.ylabel("Qrz")
plt.title("Y_test & Y_pred_out comparison")
plt.legend()
plt.show()
'''

#eksport drzewa do pdf
'''
dot_data = tree.export_graphviz(regr_1, out_file=None, feature_names=['T_d0', 'P_d0', 'Z_d0', 'W/W']) 
graph = graphviz.Source(dot_data) 
graph.render("weather")
'''

# wyswietlanie zaleznosci
'''
plt.figure()
plt.scatter(X[['T_d0']], Y, s=10, edgecolor="black", c="darkorange", label="training data")
plt.plot(X_test[['T_d0']], Y_pred_out, color="cornflowerblue", label="predicted test", linewidth=0.5)
plt.xlabel("T_d0")
plt.ylabel("Qrz")
plt.title("Decision Tree Regression")
plt.legend()
plt.show()

plt.figure()
plt.scatter(X[['P_d0']], Y, s=10, edgecolor="black", c="darkorange", label="training data")
plt.plot(X_test[['P_d0']], Y_pred_out, color="cornflowerblue", label="predicted test", linewidth=0.5)
plt.xlabel("P_d0")
plt.ylabel("Qrz")
plt.title("Decision Tree Regression")
plt.legend()
plt.show()

plt.figure()
plt.scatter(X[['Z_d0']], Y, s=10, edgecolor="black", c="darkorange", label="training data")
plt.plot(X_test[['Z_d0']], Y_pred_out, color="cornflowerblue", label="predicted test", linewidth=0.5)
plt.xlabel("Z_d0")
plt.ylabel("Qrz")
plt.title("Decision Tree Regression")
plt.legend()
plt.show()
'''
################################################################

#funkcje

def read(file_path):
    "wczytuje dane z pliku"
    data = pd.read_csv(file_path, sep = ',')
    return data

def predict(data):
    "tworzy predykcje dla danych"
    X = data[['T_d0', 'P_d0', 'Z_d0', 'W/W']]
    Y = regr_1.predict(X)
    return Y

def save_in_file(Y):
    np.savetxt('wyniki.csv', Y, fmt='%1.8f', delimiter=',')

def show_plots(X, Y):
    plt.figure()
    plt.scatter(X, Y, s=10, edgecolor="black", c="darkorange", label="training data")
    plt.xlabel("selected parameter")
    plt.ylabel("predicted Qrz")
    plt.title("Decision Tree Regression")
    plt.legend()
    plt.show()



################################################################

#przewidywanie dla danych z pliku
'''
clients_data = read('./do_przewidzenia.csv')
clients_Y = predict(clients_data)
save_in_file(clients_Y)

show_plots(np.arange(24), clients_Y)
'''
################################################################































