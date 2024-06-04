from geopy.distance import geodesic
import requests
import uvicorn
from fastapi import FastAPI


app = FastAPI()


@app.get("/getcoordinates/")
def get_coordinates(query = "Lima,Perú"):
    api_url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json"
    
    headers = {
        'User-Agent': 'Testing App'
    }
    response = requests.get(api_url, headers=headers)
    response_data = response.json()
    
    if not response_data:
        raise Exception(f"There is no coordinate available for the city: {query}")

    return {
        'latitude': response_data[0]['lat'],
        'longitude': response_data[0]['lon']
    }


@app.get("/getdistance/")
def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float):
    coordinates_point_1 = (lat1, lon1)
    coordinates_point_2 = (lat2, lon2)
    distance = geodesic(coordinates_point_1, coordinates_point_2).kilometers
    return distance


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")
