# 2025-I  TALC  
FC-UNI  
PRÁCTICA CALIFICADA 4  
TEORÍA DE AUTÓMATAS, LENGUAJES Y COMPUTACIÓN  
CC321-A  
## [DIAPOSITIVAS](https://www.canva.com/design/DAGq1-iiHrI/tfSx2NmPWS6hvsDVjAVPIw/edit?utm_content=DAGq1-iiHrI&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton) \ [INFORME](https://1drv.ms/w/c/fdb226ef3c2e079a/EfAj7rCOgvlIgpKbS4MuHZkBILMieBOzxBniI3HjcieO5w?e=hb3wWP)
## 1. Desarrolle una Interfaz Gráfica de Usuario similar a la Figura 1.

Para el diseño de la aplicación puede utilizar el módulo tkinter. A continuación proceda a incorporar tres componentes botones, un entry para una sola línea o un Text para multilínea.

Asimismo para el desarrollo de este Proyecto puede importar el conjunto de librerías NLTK (Natural Language Toolkit).

![Imagen](image.png)

### Leer Gramática:

Este botón permitirá abrir un archivo de texto para leer una Gramática Libre de Contexto. Opcionalmente puede abrir una ventana que le permita escribir las reglas de la gramática en un componente Text y cargarlas a la memoria.

### Generar Cadena:

Cada vez que se presione este botón permitirá obtener una nueva cadena a partir de la selección de algunas reglas de la gramática.

### Árbol de Derivación:

Este botón permitirá visualizar el Árbol de Derivación que corresponde a la cadena obtenida al presionar el botón anterior.

---

## 2. Diseñar una aplicación en Python 
... que utilice una interfaz gráfica a través de la cual sea posible leer desde fichero una gramática libre de contexto y realizar la eliminación de variables inútiles según los algoritmos desarrollados en clase. ([Sesión 19 - Equivalencia Gramatical](https://univirtual.uni.pe/mod/resource/view.php?id=435849) - Parte 1, 9Junio2025)

El programa deberá ser capaz de:

### 1. Leer y mostrar la cuádrupla de la gramática de entrada. Puede usar diccionarios.

Ejemplo:

```json
{
    "noterminales": ["A", "B"],
    "terminales": ["a", "b"],
    "simbolo_inicial": "A",
    "reglas": [
        "A->aA",
        "A->aB",
        "B->bB",
        "B->b"
    ]
}
```
### 2. Eliminar símbolos no generativos y las reglas que la contienen y luego mostrar la gramática resultante

[(Páginas 7 y 8, Equivalencia Gramatical - Parte 1)](https://univirtual.uni.pe/mod/resource/view.php?id=435849)

### 3. Eliminar símbolos no alcanzables y las reglas que la contienen y luego mostrar la gramática resultante

[(Páginas 14 y 15, Equivalencia Gramatical - Parte 1)](https://univirtual.uni.pe/mod/resource/view.php?id=435849)

Los resultados de cada proceso son la entrada del siguiente.

### Importante

- Adjuntar la guía con la solución para la(s) gramática(s) de prueba.
- Archivos de texto con las gramáticas utilizadas. Screenshots con la ejecución de su aplicación.
- La aplicación deberá ser resuelta de manera modular (Importante modelar la solución con orientación a objetos).
- Realizar el diagrama de clases correspondiente a la solución de cada caso.
- Se evaluará la usabilidad de la aplicación.
- Mostrar el funcionamiento del programa, este ya deberá de contar con la documentación necesaria.
- Autodocumentado. Documentación de clases, atributos, métodos y algoritmos.

