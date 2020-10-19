import datetime

import pytest

from roocs_utils.exceptions import InvalidParameterValue
from roocs_utils.parameter.level_parameter import LevelParameter


def test__str__():
    level = "1000/2000"
    parameter = LevelParameter(level)
    assert (
        parameter.__str__() == "Level range to subset over"
        f"\n first_level: 1000.0"
        f"\n last_level: 2000.0"
    )
    assert parameter.__repr__() == parameter.__str__()
    assert parameter.__unicode__() == parameter.__str__()


def test_raw():
    level = "1000/2000"
    parameter = LevelParameter(level)
    assert parameter.raw == level


def test_validate_error_format():
    level = 1000
    with pytest.raises(InvalidParameterValue) as exc:
        LevelParameter(level)
    assert str(exc.value) == "LevelParameter is not in an accepted format"


def test_validate_error_len_1_tuple():
    level = (1000,)
    with pytest.raises(InvalidParameterValue) as exc:
        LevelParameter(level)
    assert (
        str(exc.value)
        == "LevelParameter should be a range. Expected 2 values, received 1"
    )


def test_not_numbers():
    level = (datetime.datetime(2085, 1, 1), datetime.datetime(2120, 12, 30))
    with pytest.raises(InvalidParameterValue) as exc:
        LevelParameter(level)
    assert str(exc.value) == "Level values must be a number"


def test_word_string():
    level = "level/range"
    with pytest.raises(InvalidParameterValue) as exc:
        LevelParameter(level)
    assert str(exc.value) == "Level values must be a number"


def test_validate_error_no_slash():
    level = "1000 2000"
    with pytest.raises(InvalidParameterValue) as exc:
        LevelParameter(level)
    assert (
        str(exc.value) == "LevelParameter should be passed in as a range separated by /"
    )


def test_tuple():
    level = "1000/2000"
    parameter = LevelParameter(level)
    assert parameter.tuple == (1000, 2000)


def test_float_string():
    level = "1000.50/2000.60"
    parameter = LevelParameter(level)
    assert parameter.tuple == (1000.5, 2000.6)


def test_float_tuple():
    level = (1000.50, 2000.60)
    parameter = LevelParameter(level)
    assert parameter.tuple == (1000.5, 2000.6)


def test_string_tuple():
    level = ("1000.50", "2000.60")
    parameter = LevelParameter(level)
    assert parameter.tuple == (1000.5, 2000.6)


def test_int_tuple():
    level = (1000, 2000)
    parameter = LevelParameter(level)
    assert parameter.tuple == (1000, 2000)


def test_starting_slash():
    level = "1000/"
    parameter = LevelParameter(level)
    assert parameter.tuple == (1000, None)


def test_trailing_slash():
    level = "/2000"
    parameter = LevelParameter(level)
    assert parameter.tuple == (None, 2000)


def test_as_dict():
    level = "1000/2000"
    parameter = LevelParameter(level)
    assert parameter.asdict() == {"first_level": 1000, "last_level": 2000}


def test_slash_none():
    level = "/"
    parameter = LevelParameter(level)
    assert parameter.tuple == (None, None)
    assert parameter.asdict() == {"first_level": None, "last_level": None}


def test_none():
    level = None
    parameter = LevelParameter(level)
    assert parameter.tuple == (None, None)


def test_empty_string():
    level = ""
    parameter = LevelParameter(level)
    assert parameter.tuple == (None, None)


def test_white_space():
    level = " 1000 /2000"
    parameter = LevelParameter(level)
    assert parameter.tuple == (1000, 2000)


def test_class_instance():
    level = "1000/2000"
    parameter = LevelParameter(level)
    new_parameter = LevelParameter(parameter)
    assert new_parameter.tuple == (1000, 2000)
