#!/usr/bin/python

from Tkinter import *
import tkFileDialog

class Application(Frame):
    def browse(self):
        file = tkFileDialog.askopenfile(parent=root,mode='rb',title='Choose a file')
	if file != None:
    		data = file.read()
    		file.close()
    		print "I got %d bytes from this file." % len(data)

    def createWidgets(self):
        self.hi_there = Button(self)
        self.hi_there["text"] = "Browse",
        self.hi_there["command"] = self.browse

        self.hi_there.pack({"side": "left"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()


