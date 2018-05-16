#!/usr/bin/python

################################################################

#include
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.externals import joblib

#nie wiem, czy do wczytania nauczonego regressora jest konieczny ponowny import bibliotek, czy wystarczy, ze to jest w skryptach

################################################################

#funkcje

def read(file_path):
    "wczytuje dane z pliku"
    data = pd.read_csv(file_path, sep = ',')
    return data

def load_regressor(file_path):
    "wczytywanie regressora z pliku pkl; mamy pliki forest_regr.pkl, svm_regr.pkl i tree_regr.pkl"
    regr = joblib.load(file_path)
    return regr 

def predict(data, regr):
    "tworzy predykcje dla danych"
    X = data[['T_d0', 'P_d0', 'Z_d0', 'W/W']]
    Y = regr.predict(X)
    return Y

def save_in_file(Y):
    np.savetxt('wyniki.csv', Y, fmt='%1.8f', delimiter=',')

def show_plots(X, Y):
    plt.figure()
    plt.scatter(X, Y, s=10, edgecolor="black", c="darkorange", label="training data")
    plt.xlabel("selected parameter")
    plt.ylabel("predicted Qrz")
    plt.title("Regression")
    plt.legend()
    plt.show()

################################################################

#przewidywanie dla danych z pliku

if __name__ == "__main__":
    clients_data = read('./do_przewidzenia.csv')
    regr = load_regressor('forest_regr.pkl')
    clients_Y = predict(clients_data, regr)
    save_in_file(clients_Y)
    show_plots(np.arange(24), clients_Y)

