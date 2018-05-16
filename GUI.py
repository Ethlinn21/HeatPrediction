#!/usr/bin/python

import Tkinter as tk
import numpy as np
import model
from tkFileDialog import *
import re
import os
import tkMessageBox

#spis nazw plikow regresorow wraz z nazwami regresorow i ich opisami (#TODO). Uzyte sa w liscie przyciskow z regresorami do wybrania w GUI:
regressors = [
	{'file': 'forest_regr.pkl', 'label': 'Random forests', 'description': 'Random forests are an ensemble learning method \nfor classification, regression and other tasks, \nthat operate by constructing a multitude \nof decision trees at training time \nand outputting the class that is the mode \nof the classes (classification) \nor mean prediction (regression) of the individual trees\nIN SAMPLE: ~0.827\nOUT OF SAMPLE:~0.844'},
	{'file': 'tree_regr.pkl', 'label': 'Decision tree', 'description': 'Decision tree learning uses a decision tree \n(as a predictive model) \nto go from observations about an item \n(represented in the branches) to conclusions \nabout the item\'s target value \n(represented in the leaves).\nIN SAMPLE: ~0.921\nOUT OF SAMPLE:~0.898'},
	{'file': 'svm_regr.pkl', 'label': 'SVM regression', 'description': 'SVMs are supervised learning models \nwith associated learning algorithms \nthat analyze data used for classification \nand regression analysis.\nIN SAMPLE: ~0.863\nOUT OF SAMPLE:~0.910'}
]

class GUI:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.picked_regressor = tk.StringVar()
        self.picked_regressor.set('forest_regr.pkl')
        self.picked_regressor_description = tk.StringVar()
        self.picked_regressor_description.set('Choose regressor to show its description, then Process')
        for r in regressors:
            tk.Radiobutton(self.frame, text=r['label'], variable=self.picked_regressor, value=r['file'], padx=20, font=(7), justify='left', anchor='w').grid(column=0, sticky="w")
	self.filename = tk.StringVar()
	self.filename.set(None)
        tk.Button(self.frame, text="Browse", command=self.askdirectory, font=(7), width=10).grid(column=0)
        tk.Button(self.frame, text="Process", command=self.save(), font=(7), anchor="n").grid(column=0)
        self.description = tk.Label(self.frame, textvariable=self.picked_regressor_description, font=(7), anchor="nw", justify='left').grid(column=1, row=3, sticky="nw")
        self.picked_regressor.trace('w', self.callback)

        self.frame.pack()

    def callback(self, *args):
        self.picked_regressor_description.set(next((r for r in regressors if r['file'] == self.picked_regressor.get()), regressors[0])['description'])

    def save(self):
        def predict(*args):
            try:
            	clients_data = model.read(self.filename.get())
            except:
            	tkMessageBox.showinfo("Error", "Select a weather forecast from the browser")
            regr = model.load_regressor(self.picked_regressor.get())
            try:
            	clients_Y = model.predict(clients_data, regr)
            	model.save_in_file(clients_Y)
            	model.show_plots(np.arange(24), clients_Y)
            except ValueError:
            	tkMessageBox.showinfo("Error", "Select a valid weather forecast")
        return predict

    def askdirectory(self):
	try:
            directory = askopenfilename(filetypes=([('CSV files', '*.csv')]))
            self.filename.set(directory)
            filename,file_extension = os.path.splitext(self.filename.get())
            if file_extension != '.csv':
            	tkMessageBox.showinfo("Error", "Wrong file format. Please choose .csv file")
	except:
            tkMessageBox.showinfo("Error", "There is no such file. Please choose existing file")

def main(): 
    root = tk.Tk()
    root.title("Heat Prediction")
    root.geometry("800x300")
    root.resizable(False, False)
    app = GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
