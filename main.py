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
