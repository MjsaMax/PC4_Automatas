def eliminar_no_generativos(gram):
    generativos = set()
    nts = set(gram.keys())
    def es_terminal(c): return c not in nts
    # Paso 1: producciones solo con terminales
    for A, prods in gram.items():
        for w in prods:
            if all(es_terminal(c) for c in w):
                generativos.add(A)
                break
    # Paso iterativo
    cambio = True
    while cambio:
        cambio = False
        for A, prods in gram.items():
            if A not in generativos:
                for w in prods:
                    if all((c in generativos) or es_terminal(c) for c in w):
                        generativos.add(A)
                        cambio = True
                        break
    # Filtrar reglas y no terminales
    nueva = {}
    for A, prods in gram.items():
        if A in generativos:
            filtradas = [w for w in prods if all((c in generativos) or es_terminal(c) for c in w)]
            if filtradas:
                nueva[A] = filtradas
    return nueva
