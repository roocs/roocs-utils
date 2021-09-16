import datetime

import pytest

from roocs_utils.exceptions import InvalidParameterValue
from roocs_utils.parameter.level_parameter import LevelParameter
from roocs_utils.parameter.param_utils import level_interval, level_series

type_err = ("Input type of <{}> not allowed. Must be one of: [<class "
            "'roocs_utils.parameter.param_utils.Interval'>, "
            "<class 'roocs_utils.parameter.param_utils.Series'>, <class 'NoneType'>]")


def test__str__():
    level = level_interval("1000/2000")
    parameter = LevelParameter(level)
    assert (
        parameter.__str__() == "Level range to subset over"
        f"\n first_level: 1000.0"
        f"\n last_level: 2000.0"
    )
    assert parameter.__repr__() == parameter.__str__()
    assert parameter.__unicode__() == parameter.__str__()


def test_raw():
    level = level_interval("1000/2000")
    parameter = LevelParameter(level)
    assert parameter.raw == level


def test_validate_error_format():
    level = 1000
    with pytest.raises(InvalidParameterValue) as exc:
        LevelParameter(level)
    assert str(exc.value) == type_err.format("class 'int'")


def test_validate_error_len_1_tuple():
    with pytest.raises(InvalidParameterValue) as exc:
        level_interval((1000,))
    assert (
        str(exc.value)
        == "Interval should be a range. Expected 2 values, received 1"
    )


def test_not_numbers():
    level = level_interval(datetime.datetime(2085, 1, 1), datetime.datetime(2120, 12, 30))
    with pytest.raises(InvalidParameterValue) as exc:
        LevelParameter(level)
    assert str(exc.value) == "Values must be valid numbers"


def test_word_string():
    level = level_interval("level/range")
    with pytest.raises(InvalidParameterValue) as exc:
        LevelParameter(level)
    assert str(exc.value) == "Values must be valid numbers"


def test_validate_error_no_slash():
    with pytest.raises(InvalidParameterValue) as exc:
        level_interval("1000 2000")
    assert (
        str(exc.value) == "Interval should be passed in as a range separated by /"
    )


def test_start_slash_end():
    level = level_interval("1000/2000")
    parameter = LevelParameter(level)
    assert parameter.value == (1000, 2000)


def test_float_string():
    level = level_interval("1000.50/2000.60")
    parameter = LevelParameter(level)
    assert parameter.value == (1000.5, 2000.6)


def test_float_tuple():
    level = level_interval(1000.50, 2000.60)
    parameter = LevelParameter(level)
    assert parameter.value == (1000.5, 2000.6)


def test_string_tuple():
    level = level_interval("1000.50", "2000.60")
    parameter = LevelParameter(level)
    assert parameter.value == (1000.5, 2000.6)


def test_int_tuple():
    level = level_interval(1000, 2000)
    parameter = LevelParameter(level)
    assert parameter.value == (1000, 2000)


def test_starting_slash():
    level = level_interval("1000/")
    parameter = LevelParameter(level)
    assert parameter.value == (1000, None)


def test_trailing_slash():
    level = level_interval("/2000")
    parameter = LevelParameter(level)
    assert parameter.value == (None, 2000)


def test_as_dict():
    level = level_interval("1000/2000")
    parameter = LevelParameter(level)
    assert parameter.asdict() == {"first_level": 1000, "last_level": 2000}


def test_slash_none():
    level = level_interval("/")
    parameter = LevelParameter(level)
    assert parameter.value == None
    assert parameter.asdict() == {"first_level": None, "last_level": None}


def test_none():
    level = None
    parameter = LevelParameter(level)
    assert parameter.value == None


def test_empty_string():
    level = level_interval("")
    parameter = LevelParameter(level)
    assert parameter.value == None

    with pytest.raises(InvalidParameterValue) as exc:
        LevelParameter("")
    assert str(exc.value) == type_err.format("class 'str'")


def test_white_space():
    level = level_interval(" 1000 /2000")
    parameter = LevelParameter(level)
    assert parameter.value == (1000, 2000)


def test_class_instance():
    level = level_interval("1000/2000")
    parameter = LevelParameter(level)
    new_parameter = LevelParameter(parameter)
    assert new_parameter.value == (1000, 2000)
