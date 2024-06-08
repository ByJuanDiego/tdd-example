from fastapi.testclient import TestClient
import pytest
from app import app
from dataclasses import dataclass


@dataclass
class City:
    name: str
    lat: float
    lon: float
    
    def __init__(self, name: str, lat: float = 0, lon: float = 0):
        self.name = name
        self.lat = lat
        self.lon = lon


client = TestClient(app)

#######################################################################################
#                                  Constants
#######################################################################################

test_city = City(name="Lima, Peru", lat=-12.0621065, lon=-77.0365256)
epsilon = 10e-2

# Point 1
lat1: float = 51.5074
lon1 : float = -0.1278

# Point 2
lat2: float = 40.7128
lon2: float = -74.0060


#######################################################################################
#                            Tests for get city coordinates
#######################################################################################

def test_can_call_existing_endpoints_of_the_API():
    try:
        ret = client.get(f"/getcoordinates/?city={test_city.name}")
        assert(ret is not None)
    except:
        assert False, "Exception while calling an existing function!"


def test_cannot_call_nonexisting_endpoints_of_the_API():
    try:
        ret = client.get(f"/getcoordinateszzz/?city={test_city.name}")
    except:
        pass


def test_API_reponse_404_for_nonexisting_city():
    try:
        nonexisting_city = City(name="xdddddd")
        ret = client.get(f"/getcoordinates/?city={nonexisting_city.name}")
    except:
        assert True


def test_the_results_is_correct_for_simple_cases():
    try:
        ret = client.get(f"/getcoordinates/?city={test_city.name}")
        ret = ret.json()
        assert (
                    (abs(test_city.lat - float(ret['latitude'])) < epsilon)
                and (abs(test_city.lon - float(ret['longitude'])) < epsilon)
            ), "The result is not correct"
    except:
        assert False, "Exception while calling an existing function!"


@pytest.mark.parametrize("city_name, expected_lat, expected_lon", [
    ("London", '51.5074', '-0.1278'),
    ("New York", '40.7128', '-74.0060'),
    ("Paris", '48.8566', '2.3522'),
    ("Tokyo", '35.6895', '139.6917'),
    ('Lima', '-12.0621065', '-77.0365256'),
    ('Miami', '25.7741728', '-80.19362')
])
def test_the_result_is_correct_for_all_inputs_get_coordinates(city_name, expected_lat, expected_lon):
    try:
        ret = client.get(f"/getcoordinates/?city={city_name}")
        ret = ret.json()

        expected = {
            'longitude': expected_lon,
            'latitude': expected_lat
        }

        assert (abs(float(expected['longitude']) - float(ret['longitude'])) < epsilon)
        assert (abs(float(expected['latitude']) - float(ret['latitude'])) < epsilon)

    except:
        assert False, f"Get coordinates not working correctly for city: {city_name}"



#######################################################################################
#                            Tests for compute distance
#######################################################################################

def test_get_distance_is_correct_for_1_case():
    try:
        ret = client.get(f"/getdistance/?lat1={lat1}&lon1={lon1}&lat2={lat2}&lon2={lon2}")
        ret = ret.json()

        expected_distance = 5585.23357
        assert abs(ret['distance'] - expected_distance) < epsilon, "The computed distance is not correct"

    except:
        assert False, "Error while calling getdistance endpoint!"


def test_get_distance_fails_when_calling_endpoint_with_incomplete_parameters():
    try:
        ret = client.get(f"/getdistance/?lat1={lat1}")
    except:
        assert True


@pytest.mark.parametrize("lat1, lon1, lat2, lon2, expected_distance", [
    (51.5074, -0.1278, 40.7128, -74.006, 5585.2335789313),
    (51.5074, -0.1278, 48.8566, 2.3522, 343.92312009098924),
    (51.5074, -0.1278, 35.6895, 139.6917, 9582.309507921495),
    (51.5074, -0.1278, -12.0621065, -77.0365256, 10161.675614833683),
    (51.5074, -0.1278, 25.7741728, -80.19362, 7138.311331337135),
    (40.7128, -74.006, 48.8566, 2.3522, 5852.935291766765),
    (40.7128, -74.006, 35.6895, 139.6917, 10872.799519316866),
    (40.7128, -74.006, -12.0621065, -77.0365256, 5850.985550108614),
    (40.7128, -74.006, 25.7741728, -80.19362, 1753.084215688838),
    (48.8566, 2.3522, 35.6895, 139.6917, 9735.661095604704),
    (48.8566, 2.3522, -12.0621065, -77.0365256, 10247.234015886044),
    (48.8566, 2.3522, 25.7741728, -80.19362, 7368.963955834835),
    (35.6895, 139.6917, -12.0621065, -77.0365256, 15500.497129820867),
    (35.6895, 139.6917, 25.7741728, -80.19362, 12019.954199762427),
    (-12.0621065, -77.0365256, 25.7741728, -80.19362, 4199.739527412813)
])
def test_the_result_is_correct_for_all_inputs_get_distance(lat1, lon1, lat2, lon2, expected_distance):
    ret = client.get(f"/getdistance/?lat1={lat1}&lon1={lon1}&lat2={lat2}&lon2={lon2}")
    ret = ret.json()

    assert abs(ret['distance'] - expected_distance) < epsilon, "The computed distance is not correct"
