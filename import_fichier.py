from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from show_dataframe import *

root = Tk()
root.geometry("800x600")

#fonction permettant de gérer le lancement d'un fichier
def OpenFile():
    name = askopenfilename(filetypes =(("Text File", "*.csv"),("All Files","*.*")),title = "Choose a file.")
    print (name)
    # levée d'exception si le type est inconnu ou que le fichier est fermé
    try:

            df=pd.read_csv(name)
            table = Table(root, list(df))
            table.pack(padx=10,pady=10)


            table.set_data(df[:10].as_matrix())



            root.update()
            root.geometry("800x600")

            root.mainloop()


    except:
        print("fichier inexistant")


Title = root.title("Importer fichier")
btn = Button(root, text='import', command=OpenFile, padx=20)
btn.pack(pady = 20, padx = 20)

root.mainloop()
