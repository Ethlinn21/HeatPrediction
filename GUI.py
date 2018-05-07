#!/usr/bin/python

import tkinter as tk
import numpy as np
import model

#spis nazw plikow regresorow wraz z nazwami regresorow i ich opisami (#TODO). Uzyte sa w liscie przyciskow z regresorami do wybrania w GUI:
regressors = [
	{'file': 'forest_regr.pkl', 'label': 'Metoda lasow losowych', 'description': 'Tutaj opis regresji'},
	{'file': 'tree_regr.pkl', 'label': 'Drzewa decyzyjne', 'description': 'Inny opis regresji'},
	{'file': 'svm_regr.pkl', 'label': 'Inna regresja', 'description': 'Jeszcze cos innego'}
]

'''
picked_regressor - zmienna przechowujaca nazwe pliku aktualnego regresora
picked_regressor_description - jak wyzej, z tym ze aktualny opis. W linii 31 nasluchuje ona, czy aktualny plik przy kliknieciu innego regresora sie zmienil i jesli tak, w funkcji callback zmienia opis do aktualnie wybranego regresora
petla for tworzy radiobuttony dla wszystkich regresorow
przycisk wypluwa wynik na podstawie regresora
'''
class GUI:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.picked_regressor = tk.StringVar()
        self.picked_regressor.set('forest_regr.pkl')
        self.picked_regressor_description = tk.StringVar()
        self.picked_regressor_description.set('Wybierz regresor aby wyswietlic opis')
        for r in regressors:
            tk.Radiobutton(self.frame, text=r['label'], variable=self.picked_regressor, value=r['file'], font=(8), justify='left', anchor='w').grid(column=0)
        self.description = tk.Label(self.frame, textvariable=self.picked_regressor_description, font=(8), anchor="w", justify='right').grid(column=1)
        self.picked_regressor.trace('w', self.callback)

        tk.Button(self.frame, text="Przetwórz", command=self.save(), font=(8), anchor="n").grid(column=0)

        self.frame.pack()

    def callback(self, *args):
        self.picked_regressor_description.set(next((r for r in regressors if r['file'] == self.picked_regressor.get()), regressors[0])['description'])

    def save(self):
        def predict(*args):
            clients_data = model.read('./do_przewidzenia.csv')
            regr = model.load_regressor(self.picked_regressor.get())
            clients_Y = model.predict(clients_data, regr)
            model.show_plots(np.arange(24), clients_Y)
        return predict

def main(): 
    root = tk.Tk()
    root.title("Predykcja zapotrzebowania na cieplo")
    root.geometry("600x150")
    app = GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
