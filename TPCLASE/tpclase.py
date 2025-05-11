import csv

ARCHIVO = 'TPCLASE/movies.csv'
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

def convertir_rating(rating_str):
    try:
        return float(rating_str.split('/')[0])
    except:
        return 0.0

def buscar_por_titulo(titulo, peliculas):
    titulo = titulo.lower()
    resultados = [p for p in peliculas if titulo in p['Title'].lower()]
    if resultados:
        for p in resultados:
            plataforma = detectar_plataforma(p)
            print(f"{p['Title']} ({plataforma} - {p['Age']} - Rating: {p['Rating']})")
    else:
        print("No se encontraron coincidencias")

def buscar_por_plataforma_y_categoria(plataforma, categoria, peliculas):
    resultados = [
        p for p in peliculas
        if p.get(plataforma) == '1' and p.get('Age') == categoria
    ]
    resultados_ordenados = sorted(
        resultados,
        key=lambda x: convertir_rating(x['Rating']),
        reverse=True
    )
    for p in resultados_ordenados[:10]:
        print(f"{p['Title']} ({plataforma} - {p['Age']} - Rating: {p['Rating']})")
    if not resultados_ordenados:
        print("No se encontraron coincidencias.")

def insertar_pelicula():
    titulo = input("Título: ").strip()
    year = input("Año: ").strip()
    edad = input("Categoría de edad (7+, 13+, 16+, 18+): ").strip()
    rating = input("Rating (ej: 85/100): ").strip()
    plataforma = input("Plataforma (Netflix, Hulu, Prime Video, Disney+): ").strip()

    if plataforma not in PLATAFORMAS:
        print("Error: Plataforma no válida")
        return
    if edad not in CATEGORIAS_VALIDAS:
        print("Error: Categoría no válida")
        return
    try:
        rating_val = float(rating.split('/')[0])
        if not (0 <= rating_val <= 100):
            print("Error: Rating fuera de rango")
            return
    except:
        print("Error: Rating inválido")
        return

    fila = {
        'Title': titulo,
        'Year': year,
        'Age': edad,
        'Rating': rating,
        'Netflix': '1' if plataforma == 'Netflix' else '0',
        'Hulu': '1' if plataforma == 'Hulu' else '0',
        'Prime Video': '1' if plataforma == 'Prime Video' else '0',
        'Disney+': '1' if plataforma == 'Disney+' else '0'
    }

    with open(ARCHIVO, 'a', newline='', encoding='utf-8') as f:
        escritor = csv.DictWriter(f, fieldnames=fila.keys())
        escritor.writerow(fila)

    print("Película agregada con éxito")

def menu():
    while True:
        print("\n--- Menú ---")
        print("1 - Buscar por título")
        print("2 - Buscar por plataforma y categoría")
        print("3 - Agregar una nueva película")
        print("4 - Salir")
        opcion = input("Seleccione una opción: ")

        peliculas = cargar_peliculas()

        if opcion == '1':
            titulo = input("Ingrese el título de la película: ")
            buscar_por_titulo(titulo, peliculas)
        elif opcion == '2':
            plataforma = input("Plataforma (Netflix, Hulu, Prime Video, Disney+): ").strip()
            categoria = input("Categoría (7+, 13+, 16+, 18+): ").strip()
            buscar_por_plataforma_y_categoria(plataforma, categoria, peliculas)
        elif opcion == '3':
            insertar_pelicula()
        elif opcion == '4':
            print("Mejor, ponete a ver un partido de fútbol!")
            break
        else:
            print("Opción no válida. Intente nuevamente")

if __name__ == '__main__':
    menu()