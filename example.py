from geopy.distance import geodesic
import requests
import uvicorn
from fastapi import FastAPI


app = FastAPI()


@app.get("/getcoordinates/")
def get_coordinates(city):
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

# run command: uvicorn example:app
