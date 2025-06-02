import csv
import re
from datetime import timedelta

ARCHIVO = 'Proyecto_final/spotify_and_youtube.csv'

def formato_duracion(ms):
    segundos = int(float(ms) // 1000)
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    seg = segundos % 60
    return f"{horas:02}:{minutos:02}:{seg:02}"

def duracion_a_ms(duracion):
    h, m, s = map(int, duracion.split(":"))
    return ((h * 3600 + m * 60 + s) * 1000)

REGEX_URI = r"^spotify:track:[\w\d]+$"
REGEX_URL_SPOTIFY = r"^https?://open\.spotify\.com/track/[\w\d]+(?:\?.*)?$"
REGEX_URL_YOUTUBE = r"^https?://(www\.)?youtube\.com/watch\?v=[\w\-]+$"
REGEX_TEXTO = r"^[\w\s]+$"
REGEX_TIEMPO = r"^\d{2}:\d{2}:\d{2}$"

def validar_regex(campo, valor, pattern):
    if not re.fullmatch(pattern, valor):
        print(f"❌ {campo} inválido: {valor}")
        return False
    return True

def validar_numeros(likes, views):
    try:
        l = int(likes)
        v = int(views)
        return l <= v
    except:
        return False

def titulo():
    busqueda = input("Ingrese el título o artista que desea buscar: ")
    patron = re.compile(re.escape(busqueda), re.IGNORECASE)

    encontrados = []
    with open(ARCHIVO, encoding='utf-8') as music:
        lector = csv.reader(music)
        next(lector)

        for fila in lector:
            if patron.search(fila[19]) or patron.search(fila[1]):
                encontrados.append(fila)

    encontrados.sort(key=lambda x: float(x[21]), reverse=True)

    if encontrados:
        print(f"{'Artista':30} | {'Canción':30} | {'Duración'}")
        print("-" * 70)
        for r in encontrados:
            duracion = formato_duracion(r[17])
            print(f"{r[1][:30]:30} | {r[19][:30]:30} | {duracion}")
    else:
        print("No se encontró el patrón buscado.")

def top_10_por_artista():
    artista_input = input("Ingrese el nombre del artista: ").strip().lower()
    resultados = []

    with open(ARCHIVO, encoding='utf-8') as music:
        lector = csv.reader(music)
        next(lector)  # Saltar encabezado

        for fila in lector:
            try:
                artista = fila[1].strip().lower()
                track = fila[3].strip()
                duracion_ms = float(fila[17])
                views = float(fila[21])

                if artista_input in artista:
                    duracion_hms = str(timedelta(milliseconds=duracion_ms))
                    resultados.append((fila[1], track, duracion_hms, views))
            except (IndexError, ValueError):
                continue

    resultados.sort(key=lambda x: x[3], reverse=True)

    if resultados:
        print("\n🎶 Top 10 temas más reproducidos:")
        print(f"{'Artista':25} | {'Tema':30} | {'Duración':9} | {'Reproducciones (M)'}")
        print("-" * 80)
        for artista, titulo, duracion, views in resultados[:10]:
            print(f"{artista[:25]:25} | {titulo[:30]:30} | {duracion:9} | {views / 1_000_000:.2f}M")
    else:
        print("❌ No se encontraron canciones para ese artista.")
 

def insertar_manual(): 
    print("== Inserción manual ==")
    artista = input("Artista: ").strip()
    track = input("Track: ").strip()
    album = input("Álbum: ").strip()
    uri = input("URI Spotify: ").strip()
    duracion = input("Duración (HH:MM:SS): ").strip()
    url_spotify = input("URL Spotify: ").strip()
    url_youtube = input("URL YouTube: ").strip()
    likes = input("Likes: ").strip()
    views = input("Views: ").strip()

    if not all([
        validar_regex("Artista", artista, REGEX_TEXTO),
        validar_regex("Track", track, REGEX_TEXTO),
        validar_regex("Álbum", album, REGEX_TEXTO),
        validar_regex("URI", uri, REGEX_URI),
        validar_regex("Duración", duracion, REGEX_TIEMPO),
        validar_regex("URL Spotify", url_spotify, REGEX_URL_SPOTIFY),
        validar_regex("URL YouTube", url_youtube, REGEX_URL_YOUTUBE),
        validar_numeros(likes, views)
    ]):
        print("❌ Registro inválido.")
        return

    duracion_ms = duracion_a_ms(duracion)

    with open(ARCHIVO, mode='a', newline='', encoding='utf-8') as archivo:
        writer = csv.writer(archivo)
        writer.writerow([
            "", artista, "", track, album,
            *["" for _ in range(12)],
            duracion_ms,
            *["" for _ in range(8)],
            views, likes,
            *["" for _ in range(10)],
            uri, url_spotify, url_youtube
        ])

    print("✅ Registro insertado correctamente.")

'''def insertar_batch(nombre_archivo):
    nuevos_registros = []
    with open(nombre_archivo, encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        next(lector)  # Saltar encabezado

        for fila in lector:
            try:
                artista = fila[1].strip()
                url_spotify = fila[2].strip()
                track = fila[3].strip()
                album = fila[4].strip()
                uri = fila[6].strip()
                duracion_ms = float(fila[17])
                url_youtube = fila[18].strip()
                likes = fila[23].strip()
                views = fila[22].strip()

                # Validaciones
                if not all([
                    validar_regex("Artista", artista, REGEX_TEXTO),
                    validar_regex("Track", track, REGEX_TEXTO),
                    validar_regex("Álbum", album, REGEX_TEXTO),
                    validar_regex("URI Spotify", uri, REGEX_URI),
                    validar_regex("URL Spotify", url_spotify, REGEX_URL_SPOTIFY),
                    validar_regex("URL YouTube", url_youtube, REGEX_URL_YOUTUBE),
                    validar_numeros(likes, views)
                ]):
                    print(f"❌ Registro inválido: {fila}")
                    continue

                nuevos_registros.append([
                    "", artista, "", track, album,
                    *["" for _ in range(12)],
                    duracion_ms,
                    *["" for _ in range(8)],
                    views, likes,
                    *["" for _ in range(10)],
                    uri, url_spotify, url_youtube
                ])
            except (IndexError, ValueError):
                print(f"❌ Error al procesar registro: {fila}")
                continue

    with open(ARCHIVO, mode='a', newline='', encoding='utf-8') as archivo:
        writer = csv.writer(archivo)
        writer.writerows(nuevos_registros)

    print(f"✅ {len(nuevos_registros)} registros insertados.")'''

def insertar_batch(nombre_archivo):
    nuevos_registros = []

    with open(nombre_archivo, encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        next(lector)  # Saltamos el encabezado

        for fila in lector:
            if len(fila) != 9:  # Validamos que la fila tenga exactamente 9 columnas
                print(f"✅ Registro válido : {fila}")
                continue

            artista, track, album, uri, duracion, url_spotify, url_youtube, likes, views = map(str.strip, fila)

            if not validar_numeros(likes, views):
                print(f"✅ Registro válido por valores incorrectos en likes/views: {fila}")
            if not all([
                validar_regex("Artista", artista, REGEX_TEXTO),
                validar_regex("Track", track, REGEX_TEXTO),
                validar_regex("Álbum", album, REGEX_TEXTO),
                validar_regex("URI Spotify", uri, REGEX_URI),
                validar_regex("Duración", duracion, REGEX_TIEMPO),
                validar_regex("URL Spotify", url_spotify, REGEX_URL_SPOTIFY),
                validar_regex("URL YouTube", url_youtube, REGEX_URL_YOUTUBE),
                validar_numeros(likes, views)
            ]):
                #print(f"❌ Registro inválido: {fila}")
                continue

            duracion_ms = duracion_a_ms(duracion)
            if duracion_ms is None:
                continue  # Si hubo un error en la conversión de duración, ignoramos la fila

            nuevos_registros.append([
                "", artista, "", track, album,  # Índices opcionales vacíos
                *["" for _ in range(12)],  # Relleno para coincidir con el formato completo
                duracion_ms,
                *["" for _ in range(8)],  # Más espacios vacíos para las columnas faltantes
                views, likes,
                *["" for _ in range(10)],  # Más columnas vacías
                uri, url_spotify, url_youtube
            ])

    with open(ARCHIVO, mode='a', newline='', encoding='utf-8') as archivo:
        writer = csv.writer(archivo)
        writer.writerows(nuevos_registros)
        print(f"✅ {len(nuevos_registros)} registros insertados correctamente.")


def mostrar_albumes_por_artista():
    artista_input = input("Ingrese el nombre del artista: ").strip().lower()
    albumes = {}

    with open(ARCHIVO, encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        next(lector)
        for fila in lector:
            try:
                artista = fila[1]
                album = fila[4]
                duracion_ms = float(fila[17])

                if artista_input in artista.lower():
                    if album not in albumes:
                        albumes[album] = {'canciones': 0, 'duracion_total': 0}
                    albumes[album]['canciones'] += 1
                    albumes[album]['duracion_total'] += duracion_ms
            except:
                continue

    if not albumes:
        print("❌ No se encontraron álbumes.")
        return

    print(f"\n🎵 Álbumes de '{artista_input.title()}': {len(albumes)} encontrados")
    print(f"{'Álbum':40} | {'Canciones':9} | {'Duración total'}")
    print("-" * 70)
    for album, datos in albumes.items():
        duracion_seg = int(datos['duracion_total']) // 1000
        duracion_hms = str(timedelta(seconds=duracion_seg))
        print(f"{album[:40]:40} | {datos['canciones']:9} | {duracion_hms}")

def menu():
    while True:
        print("\n===== MENÚ PRINCIPAL =====")
        print("1. Buscar por título o artista")
        print("2. Mostrar top 10 por artista")
        print("3. Insertar registro manual")
        print("4. Insertar registros desde archivo CSV")
        print("5. Mostrar álbumes por artista")
        print("0. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == '1':
            titulo()
        elif opcion == '2':
            top_10_por_artista()
        elif opcion == '3':
            insertar_manual()
        elif opcion == '4':
            nombre = input("Nombre del archivo CSV: ").strip()
            insertar_batch(nombre)
        elif opcion == '5':
            mostrar_albumes_por_artista()
        elif opcion == '0':
            print("Saliendo del programa...")
            break
        else:
            print("❌ Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    menu()
