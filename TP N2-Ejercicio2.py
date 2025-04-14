def solve():
    operacion = input("Ingrese la operación matemática (solo números, '+' y '*'): ")
    try:
        # Validar que solo contenga números, '+' o '*'
        if not all(char.isdigit() or char in "+* " for char in operacion):
            return "Error: operación inválida. Usa solo números, '+' y '*'."
        resultado = eval(operacion)
        return int(resultado)
    except Exception:
        return "Error: ocurrió un problema al procesar la operación."

print(solve())