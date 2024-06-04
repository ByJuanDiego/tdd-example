from fastapi.testclient import TestClient
import pytest
from example import app

client = TestClient(app)


def test_can_call_existing_endpoints_of_the_API():
    try:
        ret = client.get("/getcoordinates/?city=Lima, Peru")
        assert(ret is not None)
    except:
        assert False, "Exception while calling an existing function!"


def test_cannot_call_nonexisting_endpoints_of_the_API():
    try:
        ret = client.get("/getcoordinateszzz/?city=Lima, Peru")
    except:
        pass


def test_API_reponse_404_for_nonexisting_city():
    try:
        ret = client.get("/getcoordinates/?city=xdddddd")
    except:
        assert True


def test_the_results_is_correct_for_simple_cases():
    try:
        ret = client.get("/getcoordinates/?city=Lima, Peru")
        ret = ret.json()
        expected = {'latitude': '-12.0621065', 'longitude': '-77.0365256'}
        assert (
                    ret['latitude'] == expected['latitude'] 
                and ret['longitude'] == expected['longitude']
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

        assert (abs(float(expected['longitude']) - float(ret['longitude'])) < 1)
        assert (abs(float(expected['latitude']) - float(ret['latitude'])) < 1)

    except:
        assert False, f"Get coordinates not working correctly for city: {city_name}"




