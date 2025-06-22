import json
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from NoAlcanzables import eliminar_inalcanzables
from NoGenerativos import eliminar_no_generativos
import threading
# Parsear gramática desde texto a dict {A: [producciones]}
def parsear_gramatica_texto(texto):
    gramatica = {}
    for linea in texto.strip().split('\n'):
        if '->' in linea:
            izquierda, derecha = linea.split('->')
            A = izquierda.strip()
            # cada producción es una lista de símbolos (caracteres)
            prods = [list(p.strip()) for p in derecha.split('|')]
            gramatica[A] = prods
    return gramatica

# Construir cuádrupla (diccionario)
def construir_cuadrupla(gramatica):
    no_terminales = list(gramatica.keys())
    simbolo_inicial = no_terminales[0] if no_terminales else ''
    terminales = set()
    # Recorrer RHS para identificar terminales
    for prods in gramatica.values():
        for w in prods:
            for c in w:
                if c not in gramatica:
                    terminales.add(c)
    reglas_list = [f"{A}->" + ''.join(w) for A, prods in gramatica.items() for w in prods]
    return {
        "noterminales": no_terminales,
        "terminales": sorted(list(terminales)),
        "simbolo_inicial": simbolo_inicial,
        "reglas": reglas_list
    }

class Simplificador:
    def __init__(self, root):
        self.root = root
        root.title("Gestión de Gramáticas")
        root.geometry("800x600")

        self.gramatica = {}      # gramática original dict
        self.gram_actual = {}    # gramática modificada dict

        frame = ttk.Frame(root, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Gramática (una producción por línea):").pack(anchor=tk.W)
        self.entrada = tk.Text(frame, height=10)
        self.entrada.pack(fill=tk.BOTH, expand=False)

        boton_frame = ttk.Frame(frame)
        boton_frame.pack(fill=tk.X, pady=5)

        ttk.Button(boton_frame, text="Cargar Gramática", command=self.cargar_gramatica).pack(side=tk.LEFT, padx=5)
        ttk.Button(boton_frame, text="1. Mostrar Cuádrupla", command=self.mostrar_cuadrupla).pack(side=tk.LEFT, padx=5)
        ttk.Button(boton_frame, text="2. Eliminar No Generativos", command=self.proceso_no_generativos).pack(side=tk.LEFT, padx=5)
        ttk.Button(boton_frame, text="3. Eliminar Inalcanzables", command=self.proceso_inalcanzables).pack(side=tk.LEFT, padx=5)
        ttk.Button(boton_frame, text="4. Árbol de Derivación", command=self.mostrar_arbol).pack(side=tk.LEFT, padx=5)

        ttk.Label(frame, text="Resultado (cuádrupla o derivación):").pack(anchor=tk.W)
        self.salida = tk.Text(frame, height=15, bg="#f0f0f0")
        self.salida.pack(fill=tk.BOTH, expand=True)

    def mostrar_cuadrupla(self):
        texto = self.entrada.get('1.0', tk.END)
        self.gramatica = parsear_gramatica_texto(texto)
        self.gram_actual = self.gramatica.copy()
        cuad = construir_cuadrupla(self.gram_actual)
        self.salida.delete('1.0', tk.END)
        self.salida.insert(tk.END, json.dumps(cuad, indent=2, ensure_ascii=False))

    def proceso_no_generativos(self):
        if not self.gram_actual:
            messagebox.showwarning("Aviso", "Debe mostrar primero la cuádrupla.")
            return
        self.gram_actual = eliminar_no_generativos(self.gram_actual)
        cuad = construir_cuadrupla(self.gram_actual)
        self.salida.delete('1.0', tk.END)
        self.salida.insert(tk.END, json.dumps(cuad, indent=2, ensure_ascii=False))

    def proceso_inalcanzables(self):
        if not self.gram_actual:
            messagebox.showwarning("Aviso", "Debe mostrar primero la cuádrupla.")
            return
        inicial = construir_cuadrupla(self.gramatica)['simbolo_inicial']
        self.gram_actual = eliminar_inalcanzables(self.gram_actual, inicial)
        cuad = construir_cuadrupla(self.gram_actual)
        self.salida.delete('1.0', tk.END)
        self.salida.insert(tk.END, json.dumps(cuad, indent=2, ensure_ascii=False))
    
    
    def mostrar_arbol(self):
        self.gramatica = parsear_gramatica_texto(self.entrada.get('1.0', tk.END))
        cadena = simpledialog.askstring("Derivación", "Ingrese la cadena objetivo:")
        if not cadena:
            return
        objetivo = list(cadena.strip())
        cuad = construir_cuadrupla(self.gramatica)
        inicial = cuad['simbolo_inicial']

        resultados = []

        def derivar(pila, derivacion):
            if len(resultados) > 0:
                return
            if pila == objetivo:
                resultados.append(derivacion[:])
                return
            if len(pila) > len(objetivo):
                return
            for i, simbolo in enumerate(pila):
                if simbolo in self.gramatica:
                    for produccion in self.gramatica[simbolo]:
                        nueva = pila[:i] + produccion + pila[i+1:]
                        derivar(nueva, derivacion + [''.join(nueva)])
                    break

        derivar([inicial], [inicial])

        self.salida.delete('1.0', tk.END)
        if resultados:
            self.salida.insert(tk.END, "Derivación encontrada:\n")
            for i, paso in enumerate(resultados[0]):
                self.salida.insert(tk.END, f"Paso {i}: {paso}\n")
        else:
            self.salida.insert(tk.END, "No se pudo derivar completamente la cadena.")

    def cargar_gramatica(self):
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if not path:
            return
        try:
            data = json.load(open(path, encoding='utf-8'))
            self.gramatica = { }
            for regla in data.get('reglas', []):
                A, d = regla.split('->')
                self.gramatica.setdefault(A.strip(), []).append(list(d.strip()))
            self.entrada.delete('1.0', tk.END)
            for A, prods in self.gramatica.items():
                linea = f"{A} -> {' | '.join(''.join(p) for p in prods)}\n"
                self.entrada.insert(tk.END, linea)
            self.salida.delete('1.0', tk.END)
            self.salida.insert(tk.END, "Gramática cargada. Use '1. Mostrar Cuádrupla'.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar JSON:\n{e}")

if __name__ == '__main__':
    root = tk.Tk()
    app = Simplificador(root)
    root.mainloop()
