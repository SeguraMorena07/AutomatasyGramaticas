import csv
import re
from datetime import timedelta

ARCHIVO = 'music.csv' #Cambiar por el archivo que se desea utilizar

def formato_duracion(ms):
    segundos = int(float(ms) // 1000)
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    seg = segundos % 60
    return f"{horas:02}:{minutos:02}:{seg:02}"

def duracion_a_ms(duracion):
    try:
        h, m, s = map(int, duracion.split(":"))  # Convierte HH:MM:SS a milisegundos
        return ((h * 3600 + m * 60 + s) * 1000)
    except ValueError:
        print(f"❌ Error en formato de duración: {duracion}")
        return None

def validar_numeros(likes, views):
    try:
        likes = int(likes)
        views = int(views)
        return likes <= views  # Los likes no deben ser mayores que las views
    except ValueError:
        return False

REGEX_URI = r"^spotify:track:[\w\d]+$"
REGEX_URL_SPOTIFY = r"^https?://open\.spotify\.com/(intl-[a-z]{2}/)?track/[\w\d]+(?:\?.*)?$"
REGEX_URL_YOUTUBE = r"^https?://(www\.)?youtube\.com/watch\?v=[\w\-]+(&[\w\-_=]+)*$"
REGEX_TEXTO = r"^[\w\s]+$"
REGEX_TIEMPO = r"^\d{2}:\d{2}:\d{2}$"


def validar_regex(campo, valor, pattern):
    if not re.fullmatch(pattern, valor):
        print(f"❌ {campo} inválido: {valor}")
        return False
    return True
"""
def validar_numeros(likes, views):
    try:
        l = int(likes)
        v = int(views)
        return l <= v
    except:
        return False"""

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

    with open(ARCHIVO, encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        next(lector)  # Omitimos encabezados

        for fila in lector:
            try:
                artista = fila[1]
                track = fila[3]
                duracion_ms = float(fila[17])
                reproducciones = float(fila[21])  # Revisa que el índice sea correcto

                if artista_input in artista.lower():
                    resultados.append({
                        'artista': artista,
                        'track': track,
                        'duracion_ms': duracion_ms,
                        'reproducciones': reproducciones
                    })
            except Exception as e:
                print(f"Error en la fila {fila}: {e}")

    if not resultados:
        print("❌ No se encontraron canciones de ese artista.")
        return

    resultados.sort(key=lambda x: x['reproducciones'], reverse=True)  # Orden descendente
    top_10 = resultados[:10]  # Seleccionar los 10 primeros

    print(f"\n{'Artista':30} | {'Canción':30} | {'Duración':10} | {'Reproducciones (M)'}")
    print("-" * 90)
    for r in top_10:
        duracion = str(timedelta(seconds=int(r['duracion_ms']) // 1000))
        print(f"{r['artista'][:30]:30} | {r['track'][:30]:30} | {duracion:10} | {round(r['reproducciones']/1_000_000, 2)} M")


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



def insertar_batch(nombre_archivo):
    nuevos_registros = []

    with open(nombre_archivo, encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        next(lector)  # Saltamos el encabezado

        for fila in lector:
            if len(fila) != 9:  # Validamos que la fila tenga exactamente 9 columnas
                print(f"❌ Registro inválido (cantidad incorrecta de columnas): {fila}")
                continue

            artista, track, album, uri, duracion, url_spotify, url_youtube, likes, views = map(str.strip, fila)

            if not validar_numeros(likes, views):
                print(f"❌ Registro inválido por valores incorrectos en likes/views: {fila}")
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




