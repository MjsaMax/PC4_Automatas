from tkinter import *
from tkinter import ttk, filedialog, messagebox
import nltk as nltk
from nltk.grammar import CFG
from nltk.parse.generate import generate
from nltk.tree import Tree

def leer_gramatica():
    s=2

def generar_cadena():
    
    texto = entrada.get()

def mostrar_arbol():
    cadena = entrada.get()
    

root = Tk()
root.title("Generador de Cadenas")

frm = ttk.Frame(root, padding=10)
root.geometry("500x100")
frm.grid()



# Campo de entrada con variable
entrada = StringVar()
ttk.Entry(frm, textvariable=entrada).grid(column=4, row=2)

# Botones con acciones personalizadas
ttk.Button(frm, text="  Leer Gramática   ", command=leer_gramatica).grid(column=0, row=1)
ttk.Button(frm, text="  Generar Cadena   ", command=generar_cadena).grid(column=0, row=2)
ttk.Button(frm, text="Árbol de Derivación", command=mostrar_arbol).grid(column=0, row=3)

root.mainloop()
