import pytest
import example


def test_can_call_existing_endpoints_of_the_API():
    try:
        ret = example.get_coordinates("Lima,Peru")
        assert(ret is not None)
    except:
        assert False, "Exception while calling an existing function!"


def test_cannot_call_nonexisting_endpoints_of_the_API():
    try:
        ret = example.get_coordinates("blah blah")
        assert False, "Exception not raised"
    except:
        pass


def test_the_results_is_correct_for_simple_cases():
    try:
        ret = example.get_coordinates("Lima,Peru")
        expected = {'latitude': '-12.0621065', 'longitude': '-77.0365256'}
        assert ret == expected, "The result is not correct"
    except:
        assert False, "Exception while calling an existing function!"



@pytest.mark.parametrize("city_name, expected_lat, expected_lon", [
    ("London", '51.5074', '-0.1278'),
    ("New York", '40.7128', '-74.0060'),
    ("Paris", '48.8566', '2.3522'),
    ("Tokyo", '35.6895', '139.6917')
])
def test_the_result_is_correct_for_all_inputs(city_name, expected_lat, expected_lon):
    try:
        ret = example.get_coordinates(city_name)
        expected = {
            'longitude': expected_lon,
            'latitude': expected_lat
        }
        
        assert (abs(float(expected['longitude']) - float(ret['longitude'])) < 1)
        assert (abs(float(expected['latitude']) - float(ret['latitude'])) < 1)

    except:
        assert False, f"Get coordinates not working correctly for city: {city_name}"
