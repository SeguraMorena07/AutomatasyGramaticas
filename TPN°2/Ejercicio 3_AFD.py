def automata_finito_subconjuntos(cadena):
    # Función de transición entre subconjuntos
    def transicion(estado, simbolo):
        if estado == "A":
            if simbolo == "a":
                return "B"
            elif simbolo == "b":
                return "C"
        elif estado == "B":
            if simbolo == "a":
                return "B"
            elif simbolo == "b":
                return "C"
        elif estado == "C":
            if simbolo == "a":
                return "B"
            elif simbolo == "b":
                return "C"
        else:
            return None

    # Estado inicial
    estado_actual = "A"

    # Conjuntos de estados de aceptación (según el diagrama y descripción)
    estados_aceptacion = {"A", "B", "C"}

    # Procesar cada símbolo en la cadena
    for simbolo in cadena:
        estado_siguiente = transicion(estado_actual, simbolo)
        print(f"[{estado_actual}]-- ({simbolo})--> [{estado_siguiente}]")

        # Mover al siguiente estado
        estado_actual = estado_siguiente

        # Si el estado es None, la cadena no es válida
        if estado_actual is None:
            print("La cadena NO es aceptada")
            return

    # Verificar si terminamos en un estado de aceptación
    if estado_actual in estados_aceptacion:
        print("La cadena es aceptada")
    else:
        print("La cadena NO es aceptada")


# Ingreso y ejecución
cadena = input("Ingrese una cadena: ")
cadena_minus = cadena.lower()  # Convertir a minúsculas por uniformidad
automata_finito_subconjuntos(cadena_minus)