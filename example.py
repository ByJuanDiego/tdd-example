from geopy.distance import geodesic
import requests


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


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float):
    coordinates_point_1 = (lat1, lon1)
    coordinates_point_2 = (lat2, lon2)
    distance = geodesic(coordinates_point_1, coordinates_point_2).kilometers
    return distance


