import pytest
import datetime

from roocs_utils.parameter.time_parameter import TimeParameter
from roocs_utils.exceptions import InvalidParameterValue


def test__str__():
    time = "2085-01-01T12:00:00Z/2120-12-30T12:00:00Z"
    parameter = TimeParameter(time)
    assert parameter.__str__ == "An object of the TimeParameter class"
    assert parameter.__repr__ == parameter.__str__
    assert parameter.__unicode__ == parameter.__str__


def test_raw():
    time = "2085-01-01T12:00:00Z/2120-12-30T12:00:00Z"
    parameter = TimeParameter(time)
    assert parameter.raw == time


def test_validate_error():
    time = datetime.datetime(2085, 1, 1)
    with pytest.raises(InvalidParameterValue) as exc:
        TimeParameter(time)
        assert exc.value == "The time period should be passed in as a string"


def test_tuple():
    time = "2085-01-01T12:00:00Z/2120-12-30T12:00:00Z"
    parameter = TimeParameter(time)
    assert parameter.tuple == ("2085-01-01T12:00:00Z", "2120-12-30T12:00:00Z")
