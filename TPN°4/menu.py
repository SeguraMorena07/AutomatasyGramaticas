from tp4 import titulo, top_10_por_artista, insertar_manual, insertar_batch, mostrar_albumes_por_artista

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

