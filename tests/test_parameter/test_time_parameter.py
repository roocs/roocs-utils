import datetime

import pytest

from roocs_utils.exceptions import InvalidParameterValue
from roocs_utils.parameter.time_parameter import TimeParameter


def test__str__():
    time = "2085-01-01T12:00:00Z/2120-12-30T12:00:00Z"
    parameter = TimeParameter(time)
    assert (
        parameter.__str__() == "Time period to subset over"
        f"\n start time: 2085-01-01T12:00:00+00:00"
        f"\n end time: 2120-12-30T12:00:00+00:00"
    )
    assert parameter.__repr__() == parameter.__str__()
    assert parameter.__unicode__() == parameter.__str__()


def test_raw():
    time = "2085-01-01T12:00:00Z/2120-12-30T12:00:00Z"
    parameter = TimeParameter(time)
    assert parameter.raw == time


def test_validate_error_len_1_tuple():
    time = ("2085-01-01T12:00:00Z",)
    with pytest.raises(InvalidParameterValue) as exc:
        TimeParameter(time)
    assert (
        str(exc.value)
        == "TimeParameter should be a range. Expected 2 values, received 1"
    )


# should datetime objects be allowed?
def test_validate_error_datetime():
    time = datetime.datetime(2085, 1, 1)
    with pytest.raises(InvalidParameterValue) as exc:
        TimeParameter(time)
    assert str(exc.value) == "TimeParameter is not in an accepted format"


def test_datetime_tuple():
    time = (datetime.datetime(2085, 1, 1), datetime.datetime(2120, 12, 30))
    with pytest.raises(InvalidParameterValue) as exc:
        TimeParameter(time)
    assert str(exc.value) == "Unable to parse the time values entered"


def test_validate_error_no_slash():
    time = "2085-01-01T12:00:00Z 2120-12-30T12:00:00Z"
    with pytest.raises(InvalidParameterValue) as exc:
        TimeParameter(time)
    assert (
        str(exc.value) == "TimeParameter should be passed in as a range separated by /"
    )


def test_trailing_slash():
    time = "2085-01-01T12:00:00Z/"
    parameter = TimeParameter(time)
    assert parameter.tuple == ("2085-01-01T12:00:00+00:00", None)


def test_starting_slash():
    time = "/2120-12-30T12:00:00Z"
    parameter = TimeParameter(time)
    assert parameter.tuple == (None, "2120-12-30T12:00:00+00:00")


def test_tuple():
    time = "2085-01-01T12:00:00Z/2120-12-30T12:00:00Z"
    parameter = TimeParameter(time)
    assert parameter.tuple == ("2085-01-01T12:00:00+00:00", "2120-12-30T12:00:00+00:00")


def test_as_dict():
    time = "2085-01-01T12:00:00Z/2120-12-30T12:00:00Z"
    parameter = TimeParameter(time)
    assert parameter.asdict() == {
        "start_time": "2085-01-01T12:00:00+00:00",
        "end_time": "2120-12-30T12:00:00+00:00",
    }


def test_slash_none():
    time = "/"
    parameter = TimeParameter(time)
    assert parameter.tuple == (None, None)
    assert parameter.asdict() == {"start_time": None, "end_time": None}


def test_none():
    time = None
    parameter = TimeParameter(time)
    assert parameter.tuple == (None, None)


def test_empty_string():
    time = ""
    parameter = TimeParameter(time)
    assert parameter.tuple == (None, None)


def test_white_space():
    time = "2085-01-01T12:00:00Z / 2120-12-30T12:00:00Z "
    parameter = TimeParameter(time)
    assert parameter.tuple == ("2085-01-01T12:00:00+00:00", "2120-12-30T12:00:00+00:00")


def test_class_instance():
    time = "2085-01-01T12:00:00Z/2120-12-30T12:00:00Z"
    parameter = TimeParameter(time)
    new_parameter = TimeParameter(parameter)
    assert new_parameter.tuple == (
        "2085-01-01T12:00:00+00:00",
        "2120-12-30T12:00:00+00:00",
    )
