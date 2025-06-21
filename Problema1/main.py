from tkinter import *
from tkinter import ttk, filedialog, messagebox
import nltk
from nltk.grammar import CFG
from nltk.parse.generate import generate
from nltk.tree import Tree
from nltk.parse import ChartParser
import random
import json
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from io import BytesIO


# Variables globales
gramatica = None
parser = None
cadena_actual = ""
datos_gramatica = None

def convertir_reglas_nltk(reglas):
    """Convierte reglas del formato A->aA al formato NLTK"""
    reglas_nltk = []
    
    for regla in reglas:
        # Separar lado izquierdo y derecho y eliminar espacios
        izquierda, derecha = regla.split('->')
        izquierda = izquierda.strip()
        derecha = derecha.strip()
        
        # Procesar el lado derecho
        simbolos_derecha = []
        i = 0
        while i < len(derecha):
            if derecha[i].isupper():  # No terminal
                simbolos_derecha.append(derecha[i])
            elif derecha[i].islower() or derecha[i].isdigit():  # Terminal
                simbolos_derecha.append(f"'{derecha[i]}'")
            i += 1
        
        # Crear regla en formato NLTK
        regla_nltk = f"{izquierda} -> {' '.join(simbolos_derecha)}"
        reglas_nltk.append(regla_nltk)
    
    return reglas_nltk

def leer_gramatica():
    global gramatica, parser, datos_gramatica
    
    # Crear ventana para elegir método de entrada
    ventana_opcion = Toplevel(root)
    ventana_opcion.title("Cargar Gramática")
    ventana_opcion.geometry("300x150")
    ventana_opcion.transient(root)
    ventana_opcion.grab_set()
    
    ttk.Label(ventana_opcion, text="¿Cómo desea cargar la gramática?").pack(pady=10)
    
    def desde_archivo():
        global datos_gramatica, gramatica, parser  # ← Declarar las globales para que se asignen correctamente
        ventana_opcion.destroy()
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo JSON de gramática",
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")]
        )
        
        if archivo:
            try:
                # Leer JSON desde el archivo
                with open(archivo, 'r', encoding='utf-8') as f:
                    datos_gramatica = json.load(f)
                
                # Validar estructura mínima
                campos_requeridos = ["noterminales", "terminales", "simbolo_inicial", "reglas"]
                for campo in campos_requeridos:
                    if campo not in datos_gramatica:
                        raise ValueError(f"Campo requerido '{campo}' no encontrado en el JSON")
                
                # Convertir reglas al formato NLTK
                reglas_nltk = convertir_reglas_nltk(datos_gramatica["reglas"])
                gramatica_str = '\n'.join(reglas_nltk)
                
                # Crear la gramática y el parser
                gramatica = CFG.fromstring(gramatica_str)
                parser = ChartParser(gramatica)
                
                messagebox.showinfo(
                    "Éxito",
                    f"Gramática cargada correctamente desde archivo.\n"
                    f"Símbolo inicial: {datos_gramatica['simbolo_inicial']}\n"
                    f"No terminales: {', '.join(datos_gramatica['noterminales'])}\n"
                    f"Terminales: {', '.join(datos_gramatica['terminales'])}"
                )
            
            except json.JSONDecodeError:
                messagebox.showerror("Error", "El archivo no es un JSON válido.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar la gramática: {str(e)}")

    
    def escribir_manual():
        ventana_opcion.destroy()
        
        # Crear ventana para escribir gramática manualmente
        ventana_gramatica = Toplevel(root)
        ventana_gramatica.title("Escribir Gramática JSON")
        ventana_gramatica.geometry("600x500")
        ventana_gramatica.transient(root)
        ventana_gramatica.grab_set()
        
        ttk.Label(ventana_gramatica, text="Escriba la gramática en formato JSON:").pack(pady=5)
        
        texto_gramatica = Text(ventana_gramatica, height=20, width=70, font=('Courier', 10))
        texto_gramatica.pack(pady=10, padx=10, fill=BOTH, expand=True)
        
        # Ejemplo por defecto
        ejemplo = """{
                "noterminales": ["S", "A", "B"],
                "terminales": ["a", "b"],
                "simbolo_inicial": "S",
                "reglas": [
                    "S->A",
                    "S->B",
                    "A->a",
                    "A->aa",
                    "B->b",
                    "B->bb"
                ]
                }
                """
        texto_gramatica.insert('1.0', ejemplo)
        
        def cargar_gramatica_manual():
            global gramatica, parser, datos_gramatica
            try:
                contenido = texto_gramatica.get('1.0', END).strip()
                datos_gramatica = json.loads(contenido)
                
                # Validar estructura
                campos_requeridos = ["noterminales", "terminales", "simbolo_inicial", "reglas"]
                for campo in campos_requeridos:
                    if campo not in datos_gramatica:
                        raise ValueError(f"Campo requerido '{campo}' no encontrado")
                
                # Convertir reglas al formato NLTK
                reglas_nltk = convertir_reglas_nltk(datos_gramatica["reglas"])
                gramatica_str = '\n'.join(reglas_nltk)
                
                gramatica = CFG.fromstring(gramatica_str)
                parser = ChartParser(gramatica)
                ventana_gramatica.destroy()
                
                messagebox.showinfo("Éxito", f"Gramática cargada correctamente.\n"
                                           f"Símbolo inicial: {datos_gramatica['simbolo_inicial']}\n"
                                           f"No terminales: {', '.join(datos_gramatica['noterminales'])}\n"
                                           f"Terminales: {', '.join(datos_gramatica['terminales'])}")
                
            except json.JSONDecodeError as e:
                messagebox.showerror("Error", f"JSON inválido: {str(e)}")
            except Exception as e:
                messagebox.showerror("Error", f"Error en la gramática: {str(e)}")
        
        frame_botones = ttk.Frame(ventana_gramatica)
        frame_botones.pack(pady=10)
        
        ttk.Button(frame_botones, text="Cargar Gramática", 
                  command=cargar_gramatica_manual).pack(side=LEFT, padx=5)
        
        def validar_json():
            try:
                contenido = texto_gramatica.get('1.0', END).strip()
                json.loads(contenido)
                messagebox.showinfo("Validación", "JSON válido ✓")
            except json.JSONDecodeError as e:
                messagebox.showerror("Error de validación", f"JSON inválido: {str(e)}")
        
        ttk.Button(frame_botones, text="Validar JSON", 
                  command=validar_json).pack(side=LEFT, padx=5)
    
    ttk.Button(ventana_opcion, text="Desde Archivo JSON", command=desde_archivo).pack(pady=5)
    ttk.Button(ventana_opcion, text="Escribir Manualmente", command=escribir_manual).pack(pady=5)

def generar_cadena():
    global gramatica, cadena_actual
    
    if not gramatica:
        messagebox.showwarning("Advertencia", "Primero debe cargar una gramática.")
        return
    
    try:
        # Generar multiples cadenas y seleccionar una aleatoriamente
        cadenas = []
        contador = 0
        for sentence in generate(gramatica, n=20):
            cadenas.append(sentence)
            contador += 1
            if contador >= 15:  # Limitar para evitar bucles infinitos
                break
        
        if cadenas:
            cadena_seleccionada = random.choice(cadenas)
            # Unir sin espacios ya que los terminales son caracteres individuales
            cadena_actual = ''.join(cadena_seleccionada)
            entrada.set(cadena_actual)
        else:
            messagebox.showwarning("Advertencia", "No se pudieron generar cadenas con esta gramática.")
            
    except Exception as e:
        messagebox.showerror("Error", f"Error al generar cadena: {str(e)}")

def mostrar_arbol():
    global parser, cadena_actual, datos_gramatica
    
    if not parser:
        messagebox.showwarning("Advertencia", "Primero debe cargar una gramática.")
        return

    if not cadena_actual:
        messagebox.showwarning("Advertencia", "Primero debe generar una cadena.")
        return

    try:
        tokens = list(cadena_actual)
        arboles = list(parser.parse(tokens))

        if not arboles:
            messagebox.showerror("Error", "No se puede derivar la cadena con la gramática actual.")
            return

        arbol = arboles[0]

        # Crear la figura del árbol usando matplotlib
        fig = plt.figure(figsize=(6, 4))
        arbol.draw()  # Genera grafico en ventana externa
        buf = BytesIO()
        arbol.pretty_print(stream=buf)
        buf.seek(0)
        arbol_str = buf.read().decode()

        # Crear ventana para mostrar el árbol
        ventana_arbol = Toplevel(root)
        ventana_arbol.title(f"Árbol de Derivación: {cadena_actual}")
        ventana_arbol.geometry("800x600")

        frame_principal = ttk.Frame(ventana_arbol)
        frame_principal.pack(fill=BOTH, expand=True, padx=10, pady=10)

        info_frame = ttk.LabelFrame(frame_principal, text="Información de la Gramática")
        info_frame.pack(fill=X, pady=(0, 10))

        if datos_gramatica:
            ttk.Label(info_frame, text=f"Símbolo inicial: {datos_gramatica['simbolo_inicial']}").pack(anchor=W)
            ttk.Label(info_frame, text=f"Cadena derivada: {cadena_actual}").pack(anchor=W)

        arbol_frame = ttk.LabelFrame(frame_principal, text="Árbol de Derivación")
        arbol_frame.pack(fill=BOTH, expand=True)

        texto_arbol = Text(arbol_frame, font=('Courier', 10), wrap=NONE)
        texto_arbol.insert('1.0', arbol_str)
        texto_arbol.config(state=DISABLED)

        scrollbar_y = Scrollbar(arbol_frame, orient=VERTICAL, command=texto_arbol.yview)
        scrollbar_x = Scrollbar(arbol_frame, orient=HORIZONTAL, command=texto_arbol.xview)
        texto_arbol.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        texto_arbol.grid(row=0, column=0, sticky='nsew')
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        scrollbar_x.grid(row=1, column=0, sticky='ew')

        arbol_frame.grid_rowconfigure(0, weight=1)
        arbol_frame.grid_columnconfigure(0, weight=1)

        # Mostrar el arbol graficamente dentro de una etiqueta
        def mostrar_grafico_en_tk():
            try:
                fig = plt.figure(figsize=(8, 5))
                arbol.draw()
                buf_img = BytesIO()
                plt.savefig(buf_img, format='png')
                buf_img.seek(0)
                img = Image.open(buf_img)
                img_tk = ImageTk.PhotoImage(img)

                imagen_window = Toplevel(ventana_arbol)
                imagen_window.title("Árbol gráfico")
                label_img = Label(imagen_window, image=img_tk)
                label_img.image = img_tk
                label_img.pack(padx=10, pady=10)
                buf_img.close()
                plt.close(fig)

            except Exception as e:
                messagebox.showinfo("Info", f"No se pudo generar la imagen del árbol.\nError: {str(e)}")

        ttk.Button(frame_principal, text="Mostrar Gráfico", command=mostrar_grafico_en_tk).pack(pady=5)

    except Exception as e:
        messagebox.showerror("Error", f"Error al mostrar el árbol: {str(e)}")

def mostrar_gramatica_cargada():
    """Función adicional para mostrar la gramática actualmente cargada"""
    global datos_gramatica
    
    if not datos_gramatica:
        messagebox.showwarning("Advertencia", "No hay gramática cargada.")
        return
    
    ventana_info = Toplevel(root)
    ventana_info.title("Gramática Cargada")
    ventana_info.geometry("500x400")
    
    texto_info = Text(ventana_info, font=('Courier', 10))
    scrollbar = Scrollbar(ventana_info, orient=VERTICAL, command=texto_info.yview)
    texto_info.configure(yscrollcommand=scrollbar.set)
    
    # Mostrar información de la gramática
    info = f"""GRAMÁTICA CARGADA:

            Símbolo inicial: {datos_gramatica['simbolo_inicial']}

            No terminales: {', '.join(datos_gramatica['noterminales'])}

            Terminales: {', '.join(datos_gramatica['terminales'])}

            Reglas de producción:
            """
    
    for i, regla in enumerate(datos_gramatica['reglas'], 1):
        info += f"\t\t{i:2d}. {regla}\n"
    
    texto_info.insert('1.0', info)
    texto_info.config(state=DISABLED)
    
    texto_info.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

root = Tk()
root.title("Generador de Cadenas - Formato JSON")

frm = ttk.Frame(root, padding=10)
root.geometry("600x150")
frm.grid()

# Campo de entrada de texto
entrada = StringVar()
ttk.Label(frm, text="Cadena generada:").grid(column=3, row=2, padx=(10,5))
ttk.Entry(frm, textvariable=entrada, width=30).grid(column=4, row=2)

# Botones Principales
ttk.Button(frm, text="  Leer Gramática   ", command=leer_gramatica).grid(column=0, row=1, pady=2)
ttk.Button(frm, text="  Generar Cadena   ", command=generar_cadena).grid(column=0, row=2, pady=2)
ttk.Button(frm, text="Árbol de Derivación", command=mostrar_arbol).grid(column=0, row=3, pady=2)
ttk.Button(frm, text="Ver Gramática", command=mostrar_gramatica_cargada).grid(column=0, row=4, pady=2)

root.mainloop()
