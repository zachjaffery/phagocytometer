import tkinter as tk
from tkinter import filedialog



def batchOpen():

    global listfiles
    root = tk.Tk()
    root.withdraw()
    files = filedialog.askopenfilenames()
    listfiles = list(files)

    return listfiles
