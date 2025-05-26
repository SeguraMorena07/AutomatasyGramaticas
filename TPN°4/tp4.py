import csv
import re

ARCHIVO = 'TPN°4/music.csv'

# Buscar por título o artista
def titulo():
    busqueda = input("Ingrese el título o artista que desea buscar: ")
    patron = re.compile(re.escape(busqueda), re.IGNORECASE)  # búsqueda insensible a mayúsculas

    with open(ARCHIVO, encoding='utf-8') as music:
        lector = csv.reader(music)
        encabezado = next(lector)  # Saltar encabezado si existe

        encontrados = []
        for fila in lector:
            # Suponemos que el título está en la columna 0 y el artista en la columna 1
            if patron.search(fila[0]) or patron.search(fila[1]):
                encontrados.append(fila)

        if encontrados:
            print('Búsqueda exitosa:')
            for resultado in encontrados:
                print(f"Título: {resultado[5]} | Artista: {resultado[1]}")
        else:
            print("No se encontró el patrón buscado.")

# Llamar a la función
titulo()