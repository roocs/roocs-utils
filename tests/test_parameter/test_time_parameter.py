import datetime

import pytest

from roocs_utils.exceptions import InvalidParameterValue
from roocs_utils.parameter.time_parameter import TimeParameter
from roocs_utils.parameter.param_utils import (
    time_interval,
    time_series,
    time_components,
)


type_err = (
    "Input type of <{}> not allowed. Must be one of: [<class "
    "'roocs_utils.parameter.param_utils.Interval'>, "
    "<class 'roocs_utils.parameter.param_utils.Series'>, <class 'NoneType'>]"
)


def test__str__():
    time = time_interval("2085-01-01T12:00:00Z/2120-12-30T12:00:00Z")
    parameter = TimeParameter(time)
    assert (
        parameter.__str__() == "Time period to subset over"
        f"\n start time: 2085-01-01T12:00:00+00:00"
        f"\n end time: 2120-12-30T12:00:00+00:00"
    )
    assert parameter.__repr__() == parameter.__str__()
    assert parameter.__unicode__() == parameter.__str__()


def test_raw():
    time = time_interval("2085-01-01T12:00:00Z/2120-12-30T12:00:00Z")
    parameter = TimeParameter(time)
    assert parameter.raw == time


def test_validate_error_len_1_tuple():
    with pytest.raises(InvalidParameterValue) as exc:
        time_interval(("2085-01-01T12:00:00Z",))
    assert str(exc.value) == "Interval should be a range. Expected 2 values, received 1"


# should datetime objects be allowed?
def test_validate_error_datetime():
    time = datetime.datetime(2085, 1, 1)
    with pytest.raises(InvalidParameterValue) as exc:
        TimeParameter(time)
    assert str(exc.value) == type_err.format("class 'datetime.datetime'")


def test_datetime_tuple():
    time = time_interval(datetime.datetime(2085, 1, 1), datetime.datetime(2120, 12, 30))
    with pytest.raises(InvalidParameterValue) as exc:
        TimeParameter(time)
    assert str(exc.value) == "Unable to parse the time values entered"


def test_validate_error_no_slash():
    with pytest.raises(InvalidParameterValue) as exc:
        time_interval("2085-01-01T12:00:00Z 2120-12-30T12:00:00Z")
    assert str(exc.value) == ("Interval should be passed in as a range separated by /")


def test_trailing_slash():
    time = time_interval("2085-01-01T12:00:00Z/")
    parameter = TimeParameter(time)
    assert parameter.value == ("2085-01-01T12:00:00+00:00", None)


def test_starting_slash():
    time = time_interval("/2120-12-30T12:00:00Z")
    parameter = TimeParameter(time)
    assert parameter.value == (None, "2120-12-30T12:00:00+00:00")


def test_start_slash_end():
    time = time_interval("2085-01-01T12:00:00Z/2120-12-30T12:00:00Z")
    parameter = TimeParameter(time)
    assert parameter.value == ("2085-01-01T12:00:00+00:00", "2120-12-30T12:00:00+00:00")


def test_as_dict():
    time = time_interval("2085-01-01T12:00:00Z/2120-12-30T12:00:00Z")
    parameter = TimeParameter(time)
    assert parameter.asdict() == {
        "start_time": "2085-01-01T12:00:00+00:00",
        "end_time": "2120-12-30T12:00:00+00:00",
    }


def test_slash_none():
    time = time_interval("/")
    parameter = TimeParameter(time)
    assert parameter.value is None
    assert parameter.asdict() == {"start_time": None, "end_time": None}


def test_none():
    time = None
    parameter = TimeParameter(time)
    assert parameter.value is None


def test_empty_string():
    time = time_interval("")
    parameter = TimeParameter(time)
    assert parameter.value is None

    with pytest.raises(InvalidParameterValue) as exc:
        TimeParameter("")
    assert str(exc.value) == type_err.format("class 'str'")


def test_white_space():
    time = time_interval("2085-01-01T12:00:00Z / 2120-12-30T12:00:00Z ")
    parameter = TimeParameter(time)
    assert parameter.value == ("2085-01-01T12:00:00+00:00", "2120-12-30T12:00:00+00:00")


def test_class_instance():
    time = time_interval("2085-01-01T12:00:00Z/2120-12-30T12:00:00Z")
    parameter = TimeParameter(time)
    new_parameter = TimeParameter(parameter)
    assert new_parameter.value == (
        "2085-01-01T12:00:00+00:00",
        "2120-12-30T12:00:00+00:00",
    )


def test_time_series_input():
    value = ["2085-01-01T12:00:00Z", "2095-03-03T03:03:03", "2120-12-30T12:00:00Z"]
    expected_value = [i.replace("Z", "+00:00") for i in value]
    vstring = ",".join([str(i) for i in value])

    for tm in (vstring, value, tuple(value)):

        times = time_series(tm)
        parameter = TimeParameter(times)
        assert parameter.type == "series"
        assert parameter.value == expected_value
        assert parameter.asdict() == {"time_values": expected_value}
