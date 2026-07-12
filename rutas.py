import requests
import urllib.parse

# Reemplaza esto con tu API Key real obtenida de GraphHopper
API_KEY = "a419a296-6aba-49be-b71a-df4f4e9c274f" 
GEOCODE_URL = "https://graphhopper.com/api/1/geocode"
ROUTE_URL = "https://graphhopper.com/api/1/route"

def geocoding(origen, destino):
    origen_url = f"{GEOCODE_URL}?q={urllib.parse.quote(origen)}&key={API_KEY}"
    destino_url = f"{GEOCODE_URL}?q={urllib.parse.quote(destino)}&key={API_KEY}"
    
    try:
        ori_data = requests.get(origen_url).json()
        dest_data = requests.get(destino_url).json()
        
        # Validar si la API devolvió un mensaje de error (ej: API Key inválida)
        if 'message' in ori_data:
            print(f"\n[ERROR DE API] GraphHopper indica: {ori_data['message']}")
            return None, None
            
        if ori_data.get('hits') and dest_data.get('hits'):
            # En la API actual de GraphHopper, lat y lng suelen venir dentro de 'point'
            if 'point' in ori_data['hits'][0] and 'point' in dest_data['hits'][0]:
                ori_lat = ori_data['hits'][0]['point']['lat']
                ori_lng = ori_data['hits'][0]['point']['lng']
                dest_lat = dest_data['hits'][0]['point']['lat']
                dest_lng = dest_data['hits'][0]['point']['lng']
                return (ori_lat, ori_lng), (dest_lat, dest_lng)
            # Por si acaso la versión de la API las devuelve en la raíz
            elif 'lat' in ori_data['hits'][0] and 'lat' in dest_data['hits'][0]:
                ori_lat = ori_data['hits'][0]['lat']
                ori_lng = ori_data['hits'][0]['lng']
                dest_lat = dest_data['hits'][0]['lat']
                dest_lng = dest_data['hits'][0]['lng']
                return (ori_lat, ori_lng), (dest_lat, dest_lng)
            else:
                print("\n[ERROR] La API no devolvió coordenadas válidas en la estructura esperada.")
                return None, None
        else:
            print("\n[ERROR] No se encontraron resultados para una o ambas ciudades.")
            return None, None
            
    except Exception as e:
        print(f"\n[ERROR DE CONEXIÓN] Falló la petición a la API de Geocoding: {e}")
        return None, None

while True:
    print("\n" + "="*50)
    print("--- Calculadora de Rutas (Chile - Perú) ---")
    print("="*50)
    
    origen = input("Ingrese Ciudad de Origen (o presione 's' para salir): ")
    if origen.lower() == 's':
        print("Saliendo del programa...")
        break
        
    destino = input("Ingrese Ciudad de Destino (o presione 's' para salir): ")
    if destino.lower() == 's':
        print("Saliendo del programa...")
        break
        
    print("\nOpciones de transporte: car (auto), bike (bicicleta), foot (caminando)")
    transporte = input("Elija el medio de transporte: ").lower()
    
    if transporte not in ['car', 'bike', 'foot']:
        print("Transporte no válido. Se usará 'car' por defecto.")
        transporte = 'car'
        
    print("\nObteniendo coordenadas geográficas...")
    coords_ori, coords_dest = geocoding(origen, destino)
    
    if coords_ori and coords_dest:
        print("Calculando la ruta óptima...")
        url_ruta = (f"{ROUTE_URL}?point={coords_ori[0]},{coords_ori[1]}&point={coords_dest[0]},{coords_dest[1]}"
                    f"&vehicle={transporte}&locale=es&key={API_KEY}")
        
        try:
            res_ruta = requests.get(url_ruta).json()
            
            # Validar si hubo error en la petición de ruta
            if 'message' in res_ruta:
                print(f"\n[ERROR DE API] GraphHopper indica en el cálculo de ruta: {res_ruta['message']}")
                continue
            
            if 'paths' in res_ruta:
                camino = res_ruta['paths'][0]
                distancia_km = camino['distance'] / 1000
                distancia_mi = distancia_km * 0.621371
                tiempo_seg = camino['time'] / 1000
                horas = int(tiempo_seg // 3600)
                minutos = int((tiempo_seg % 3600) // 60)
                
                print("\n" + "-"*50)
                print("                    RESULTADOS                  ")
                print("-" * 50)
                print(f"Ruta:        {origen.upper()} -> {destino.upper()}")
                print(f"Transporte:  {transporte.upper()}")
                print(f"Distancia:   {distancia_km:.2f} km ({distancia_mi:.2f} millas)")
                print(f"Duración:    {horas} horas, {minutos} minutos")
                
                print("\n" + "-"*50)
                print("               NARRATIVA DEL VIAJE            ")
                print("-" * 50)
                for instruction in camino['instructions']:
                    dist_tramo = instruction['distance'] / 1000
                    print(f"- {instruction['text']} ({dist_tramo:.2f} km)")
                print("="*50)
            else:
                print("\n[ERROR] No se encontró una ruta posible entre esas ciudades con el transporte seleccionado.")
                
        except Exception as e:
            print(f"\n[ERROR DE CONEXIÓN] Falló la petición a la API de Routing: {e}")
    else:
        print("\nEl cálculo de ruta fue cancelado debido a un error previo al obtener coordenadas.")
