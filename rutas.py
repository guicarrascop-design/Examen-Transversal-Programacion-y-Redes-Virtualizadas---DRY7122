import requests
import urllib.parse

API_KEY = "a419a296-6aba-49be-b71a-df4f4e9c274f" 
GEOCODE_URL = "https://graphhopper.com/api/1/geocode"
ROUTE_URL = "https://graphhopper.com/api/1/route"

def geocoding(origen, destino):
    origen_url = f"{GEOCODE_URL}?q={urllib.parse.quote(origen)}&key={API_KEY}"
    destino_url = f"{GEOCODE_URL}?q={urllib.parse.quote(destino)}&key={API_KEY}"
    
    ori_data = requests.get(origen_url).json()
    dest_data = requests.get(destino_url).json()
    
    if ori_data.get('hits') and dest_data.get('hits'):
        ori_lat = ori_data['hits'][0]['lat']
        ori_lng = ori_data['hits'][0]['lng']
        dest_lat = dest_data['hits'][0]['lat']
        dest_lng = dest_data['hits'][0]['lng']
        return (ori_lat, ori_lng), (dest_lat, dest_lng)
    return None, None

while True:
    print("\n--- Calculadora de Rutas (Chile - Perú) ---")
    origen = input("Ingrese Ciudad de Origen (o presione 's' para salir): ")
    if origen.lower() == 's':
        break
    destino = input("Ingrese Ciudad de Destino (o presione 's' para salir): ")
    if destino.lower() == 's':
        break
        
    print("Opciones de transporte: car (auto), bike (bicicleta), foot (caminando)")
    transporte = input("Elija el medio de transporte: ").lower()
    if transporte not in ['car', 'bike', 'foot']:
        transporte = 'car'
        
    coords_ori, coords_dest = geocoding(origen, destino)
    
    if coords_ori and coords_dest:
        url_ruta = (f"{ROUTE_URL}?point={coords_ori[0]},{coords_ori[1]}&point={coords_dest[0]},{coords_dest[1]}"
                    f"&vehicle={transporte}&locale=es&key={API_KEY}")
        
        res_ruta = requests.get(url_ruta).json()
        
        if 'paths' in res_ruta:
            camino = res_ruta['paths'][0]
            distancia_km = camino['distance'] / 1000
            distancia_mi = distancia_km * 0.621371
            tiempo_seg = camino['time'] / 1000
            horas = int(tiempo_seg // 3600)
            minutos = int((tiempo_seg % 3600) // 60)
            
            print("\n--- RESULTADOS ---")
            print(f"Distancia: {distancia_km:.2f} km ({distancia_mi:.2f} millas)")
            print(f"Duración: {horas} horas, {minutos} minutos")
            print("\n--- NARRATIVA DEL VIAJE ---")
            for instruction in camino['instructions']:
                print(f"- {instruction['text']} ({instruction['distance']/1000:.2f} km)")
        else:
            print("No se encontró una ruta posible.")
    else:
        print("Error: No se encontraron las coordenadas. Revisa la API Key.")
