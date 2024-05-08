import requests


def obtener_geolocalizacion(ciudad):
    url = f"https://graphhopper.com/api/1/geocode?q={ciudad}&key=53c6a8a1-47b6-40f5-82ee-c093f11e46ae"
    response = requests.get(url)
    data = response.json()

    if 'hits' in data and len(data['hits']) > 0:
        latitud = data['hits'][0]['point']['lat']
        longitud = data['hits'][0]['point']['lng']
        ciudad = data['hits'][0].get('city', '')
        region = data['hits'][0].get('state', '')
        pais = data['hits'][0].get('country', '')
    else:
        latitud = None
        longitud = None
        ciudad = ''
        region = ''
        pais = ''

    return latitud, longitud, ciudad, region, pais

def calcular_distancia_tiempo(origen, destino, medio_transporte):
    url = f"https://graphhopper.com/api/1/route?point={origen}&point={destino}&vehicle={medio_transporte}&key=53c6a8a1-47b6-40f5-82ee-c093f11e46ae&locale=es"
    response = requests.get(url)
    data = response.json()

    if 'paths' in data and len(data['paths']) > 0:
        distancia_km = round(data['paths'][0]['distance'] / 1000, 1)
        distancia_millas = round(distancia_km / 1.60934, 1)
        duracion_segundos = data['paths'][0]['time']
        
        duracion_horas = duracion_segundos // 1000 // 60 // 60 
        duracion_minutos = (duracion_segundos % 3600) // 60
        duracion_segundos = duracion_segundos % 60
    else:
        distancia_km = None
        distancia_millas = None
        duracion_horas = None
        duracion_minutos = None
        duracion_segundos = None

    return distancia_km, distancia_millas, duracion_horas, duracion_minutos, duracion_segundos

def calcular_instrucciones(origen, destino, medio_transporte):
    url = f"https://graphhopper.com/api/1/route?point={origen}&point={destino}&vehicle={medio_transporte}&key=53c6a8a1-47b6-40f5-82ee-c093f11e46ae&type=json&instructions=true&locale=es"
    response = requests.get(url)
    data = response.json()

    if 'paths' in data and len(data['paths']) > 0:
        instrucciones = []
        for instruccion in data['paths'][0]['instructions']:
            instrucciones.append((instruccion['text'], round(instruccion['distance'] / 1000, 1)))
        return instrucciones
    else:
        return None

while True:
    origen = input("Ingrese la ciudad de origen (o 'S' para salir): ")
    if origen.lower() == 's' or origen.lower() == 'salir':
        print("¡Hasta luego!")
        break

    destino = input("Ingrese la ciudad de destino: ")
    medio_transporte = input("Elija el medio de transporte (auto, bicicleta, a pie): ")

    # Mapear los medios de transporte a los valores esperados por la API
    if medio_transporte.lower() == "auto":
        medio_transporte_api = "car"
    elif medio_transporte.lower() == "bicicleta":
        medio_transporte_api = "bike"
    elif medio_transporte.lower() == "a pie":
        medio_transporte_api = "foot"
    else:
        print("¡Medio de transporte no válido!")
        continue

    lat_origen, lon_origen, ciudad_origen, region_origen, pais_origen = obtener_geolocalizacion(origen)
    lat_destino, lon_destino, ciudad_destino, region_destino, pais_destino = obtener_geolocalizacion(destino)

    distancia_km, distancia_millas, duracion_horas, duracion_minutos, duracion_segundos = calcular_distancia_tiempo(f"{lat_origen},{lon_origen}", f"{lat_destino},{lon_destino}", medio_transporte_api)

    if distancia_km is not None and duracion_horas is not None:
        print("\nInformación de la ruta:")
        print(f"Origen: {ciudad_origen}, {region_origen}, {pais_origen}")
        print(f"Destino: {ciudad_destino}, {region_destino}, {pais_destino}")
        print(f"Distancia: {distancia_km} km ({distancia_millas} millas)")
        print(f"Duración del viaje: {duracion_horas} horas, {duracion_minutos} minutos, {duracion_segundos} segundos")
    else:
        print("No se pudo calcular la distancia y duración del viaje.")

    instrucciones = calcular_instrucciones(f"{lat_origen},{lon_origen}", f"{lat_destino},{lon_destino}", medio_transporte_api)
    if instrucciones is not None:
        print("\nInstrucciones de la ruta:")
        for instruccion, distancia in instrucciones:
            print(f"- {instruccion} ({distancia} km)")
    else:
        print("No se pudo obtener la descripción detallada de la ruta.")