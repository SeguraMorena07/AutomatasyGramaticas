import re
from collections import Counter

def validaremail():
    """
    Valida y encuentra correos electrónicos en el archivo especificado.
    """
    try:
        with open('testTPN1.txt', encoding='utf-8') as file:
            contenido = file.read()
            patron = r'[a-zA-Z][\w.-]*@[a-zA-Z]+\.[a-zA-Z]{2,4}(?:\.[a-zA-Z]{2,4})?'
            matches = re.findall(patron, contenido)
            if matches:
                print('Mails encontrados:', matches)
            else:
                print('No se encontraron correos válidos en el archivo.')
    except FileNotFoundError:
        print('El archivo no se encontró. Por favor, verifica la ruta.')

def validar_url():
    """
    """
    try:
        with open('testTPN1.txt', encoding='utf-8') as file:
            contenido = file.read()
            patron = r'(https://)?(www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}(/[^\s]*)?(\?[^\s]*)?'
            matches = re.findall(patron, contenido)
            if matches:
                urls = [''.join(match) for match in matches]
                print('URLs encontradas:', urls)
            else:
                print('No se encontraron URLs válidas en el archivo.')
    except FileNotFoundError:
        print('El archivo no se encontró. Por favor, verifica la ruta.')

def validar_direccion_ipv4():
    """
    Valida y encuentra direcciones IPv4 en el archivo especificado.
    """
    try:
        with open('testTPN1.txt', encoding='utf-8') as file:
            contenido = file.read()
            patron = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
            matches = re.findall(patron, contenido)
            direccionesip = [
                ip for ip in matches
                if all(0 <= int(octeto) <= 255 for octeto in ip.split('.'))
            ]
            if direccionesip:
                print('Direcciones IP válidas:', direccionesip)
            else:
                print('No se encontraron direcciones IP válidas en el archivo.')
    except FileNotFoundError:
        print('El archivo no se encontró. Por favor, verifica la ruta.')

def analizar_texto():
    try:
        with open('testTPN1.txt', encoding='utf-8') as file:
            lineas = file.readlines()
            palabras = []
            for i, linea in enumerate(lineas, start=1):
                linea_palabras = linea.strip().split()
                palabras.extend(linea_palabras)
                print(f'Línea {i}: {linea_palabras}')
            contador = Counter(palabras)
            palabras_mas_frequentes, repeticiones = contador.most_common(1)[0]
            print(f'Palabra más frecuente: {palabras_mas_frequentes}')
            print(f'Repeticiones: {repeticiones}')
    except FileNotFoundError:
        print('El archivo no se encontró. Por favor, verifica la ruta.')

# Llamadas a las funciones
validar_url()
validar_direccion_ipv4()
validaremail()
analizar_texto()