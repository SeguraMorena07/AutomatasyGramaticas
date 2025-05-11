import csv

ARCHIVO = 'movies.csv'
PLATAFORMAS = ['Netflix', 'Hulu', 'Prime Video', 'Disney+']
CATEGORIAS_VALIDAS = ['7+', '13+', '16+', '18+']

def cargar_peliculas():
    with open(ARCHIVO, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def detectar_plataforma(fila):
    for plataforma in PLATAFORMAS:
        if fila[plataforma] == '1':
            return plataforma
    return "Desconocida"