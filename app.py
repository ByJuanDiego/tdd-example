from geopy.distance import geodesic
import requests
import uvicorn
from fastapi import FastAPI


app = FastAPI()


@app.get("/getcoordinates/")
def get_coordinates(city: str):
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
        return {
            'response': 404,
            'message': 'City not found'
        }

    return {
        'response': 200,
        'message': 'Success',
        'latitude': response_data[0]['lat'],
        'longitude': response_data[0]['lon']
    }


@app.get("/getdistance/")
def get_distance(lat1: float, lon1: float, lat2: float, lon2: float):
    coordinates1 = (lat1, lon1)
    coordinates2 = (lat2, lon2)

    distance_km = geodesic(coordinates1, coordinates2).kilometers
    return {
        'response': 200,
        'message': 'Success',
        'distance': distance_km
    }
