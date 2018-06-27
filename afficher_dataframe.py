from tkinter import *
import csv
import pandas as pd

class WINDOW(Frame):
    def __init__(self, fenetre, df, height, width):
        Frame.__init__(self, fenetre)
        self.df=df
        self.numberLines = height
        self.numberColumns = width
        self.pack(fill=BOTH)
        self.data = list()

        #affichage du contenu de la dataframme df dans notre fentre sous forme de Grid
        for i in range(self.numberLines):
            line = list()
            for j in range(self.numberColumns):
                cell = Entry(self)
                cell.insert(0,self.df.iloc[i-1,j-1])
                cell.configure(state='readonly')
                line.append(cell)
                cell.grid(row = i, column = j)
            self.data.append(line)

        self.results = list()


#test

df=pd.read_csv("/home/thierno/WorldCupMatches.csv")

fenetre = Tk()
fenetre.title("test affichage d'un fichier CSV")
interface = WINDOW(fenetre, df, 10, 10)
interface.mainloop()
