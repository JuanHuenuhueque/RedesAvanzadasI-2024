import requests

def obtener_geolocalizacion(ciudad):
    # Llamada a la API para obtener la geolocalización de la ciudad
    url = f"https://graphhopper.com/api/1/geocode?q={ciudad}&key=53c6a8a1-47b6-40f5-82ee-c093f11e46ae"
    response = requests.get(url)
    data = response.json()

    if 'hits' in data and len(data['hits']) > 0:
        hit = data['hits'][0]  # Tomamos el primer resultado de la búsqueda
        latitud = hit['point']['lat']
        longitud = hit['point']['lng']
        ciudad = hit.get('city', '')
        region = hit.get('state', '')
        pais = hit.get('country', '')
        return latitud, longitud, ciudad, region, pais

    # Si no se encontró la ciudad en los resultados, devolver valores nulos
    return None, None, None, None, None

# Interacción con el usuario
while True:
    origen = input("Ingrese la ciudad de origen (o 'S' para salir): ")
    if origen.lower() == 's':
        print("¡Hasta luego!")
        break
    
    destino = input("Ingrese la ciudad de destino: ")
    
    lat_origen, lon_origen, ciudad_origen, region_origen, pais_origen = obtener_geolocalizacion(origen)
    lat_destino, lon_destino, ciudad_destino, region_destino, pais_destino = obtener_geolocalizacion(destino)
    
    print("\nInformación de la localización:")
    if lat_origen is not None and lon_origen is not None:
        print(f"Origen: {ciudad_origen}, {region_origen}, {pais_origen} - Latitud: {lat_origen}, Longitud: {lon_origen}")
    else:
        print("No se pudo obtener la geolocalización de la ciudad de origen.")

    if lat_destino is not None and lon_destino is not None:
        print(f"Destino: {ciudad_destino}, {region_destino}, {pais_destino} - Latitud: {lat_destino}, Longitud: {lon_destino}")
    else:
        print("No se pudo obtener la geolocalización de la ciudad de destino.")
