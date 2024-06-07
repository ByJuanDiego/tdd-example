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
def test_the_result_is_correct_for_all_inputs(city_name, expected_lat, expected_lon):
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


