def eliminar_inalcanzables(gram, inicial):
    alcanzables = set([inicial])
    cambio = True
    while cambio:
        cambio = False
        for A in list(alcanzables):
            if A in gram:
                for w in gram[A]:
                    for c in w:
                        if c in gram and c not in alcanzables:
                            alcanzables.add(c)
                            cambio = True
    # Filtrar reglas y no terminales
    
    nueva = {A: prods for A, prods in gram.items() if A in alcanzables}
    print(nueva)
    return nueva