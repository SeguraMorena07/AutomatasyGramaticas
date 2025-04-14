def solve():
    operacion = input("Ingrese la operación matemática (solo números, '+' y '*'): ")
    try:

        if not all(char.isdigit() or char in "+* " for char in operacion):
            return "Error: operación inválida. Usa solo números, '+' y '*'."
        

        operacion = operacion.replace(" ", "")

        sumandos = operacion.split('+')
        total = 0
        
        for sumando in sumandos:
            factores = sumando.split('*')
            producto = 1
            for factor in factores:
                if not factor.isdigit():
                    return "Error: operación inválida, formato incorrecto."
                
                producto *= int(factor)
            
            total += producto

        return total
    except Exception as e:
        return "Error: ocurrió un problema al procesar la operación."

print(solve())