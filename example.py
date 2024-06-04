from geopy.distance import geodesic
import requests
import uvicorn
from fastapi import FastAPI


app = FastAPI()


@app.get("/getcoordinates/")
def get_coordinates(city = "Lima,Perú"):
    """
    Este endpoint obtiene las coordenadas de una ciudad pasada como query.
    Internamente, se comunica con la API de openstreetmap para obtener las coordenadas.

    input: city (la ciudad de la cual queremos las coordenadas)
    output: dict({
                'latitude': float(x), 
                'longitude': float(y)
            })
    """

    api_url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json"
    
    headers = {
        'User-Agent': 'Testing App'
    }
    response = requests.get(api_url, headers=headers)
    response_data = response.json()
    
    if not response_data:
        raise Exception(f"There is no coordinate available for the city: {city}")

    return {
        'latitude': response_data[0]['lat'],
        'longitude': response_data[0]['lon']
    }


@app.get("/getdistance/")
def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float):
    """
    Este endpoint calcula la distancia geodésica entre 2 coordenadas

    inputs:
        float(lat1), float(lon1): La primera coordenada
        float(lat2), float(lon2): La segunda coordenada
    output:
        float(distance): La distancia geodésica entre las 2 coordenadas
    """
    coordinates_point_1 = (lat1, lon1)
    coordinates_point_2 = (lat2, lon2)
    distance = geodesic(coordinates_point_1, coordinates_point_2).kilometers
    return distance


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")
