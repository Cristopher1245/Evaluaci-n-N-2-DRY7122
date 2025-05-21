import requests

def obtener_coordenadas(ciudad):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={ciudad}&count=1"
    respuesta = requests.get(url)
    datos = respuesta.json()
    if 'results' in datos and datos['results']:
        latitud = datos['results'][0]['latitude']
        longitud = datos['results'][0]['longitude']
        return latitud, longitud
    else:
        print(f"No se encontraron coordenadas para {ciudad}.")
        return None, None

def obtener_clima(latitud, longitud):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitud}&longitude={longitud}&current_weather=true"
    respuesta = requests.get(url)
    datos = respuesta.json()
    clima = datos['current_weather']
    temperatura = clima['temperature']
    viento = clima['windspeed']
    codigo_clima = clima['weathercode']
    estado_cielo = interpretar_clima(codigo_clima)
    return temperatura, viento, estado_cielo

def interpretar_clima(codigo):
    condiciones = {
        0: "despejado",
        1: "principalmente despejado",
        2: "parcialmente nublado",
        3: "nublado",
        45: "niebla",
        48: "niebla con escarcha",
        51: "llovizna ligera",
        61: "lluvia ligera",
        71: "nieve ligera",
        80: "lluvia débil",
        95: "tormentas"
    }
    return condiciones.get(codigo, "condición desconocida")

def main():
    while True:
        origen = input("Ingresa Ciudad de Origen (o 'q' para salir): ")
        if origen.lower() == 'q':
            break

        destino = input("Ingresa Ciudad de Destino (o 'q' para salir): ")
        if destino.lower() == 'q':
            break

        lat_o, lon_o = obtener_coordenadas(origen)
        lat_d, lon_d = obtener_coordenadas(destino)

        if None in (lat_o, lon_o, lat_d, lon_d):
            print("No se pudo obtener información para alguna de las ciudades.")
            continue

        temp_o, viento_o, cielo_o = obtener_clima(lat_o, lon_o)
        temp_d, viento_d, cielo_d = obtener_clima(lat_d, lon_d)

        print("\n--- Comparación Climática ---")
        print(f"{origen}: {temp_o:.2f}°C, Viento: {viento_o:.2f} km/h, Cielo: {cielo_o}")
        print(f"{destino}: {temp_d:.2f}°C, Viento: {viento_d:.2f} km/h, Cielo: {cielo_d}")

        print(f"\nNarrativa: En {origen} actualmente hay {temp_o:.2f} °C con cielos {cielo_o}, "
              f"mientras que en {destino} hay {temp_d:.2f} °C y está {cielo_d}.\n")

if __name__ == "__main__":
    main()