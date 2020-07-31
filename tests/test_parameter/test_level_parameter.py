import pytest

from roocs_utils.parameter.level_parameter import LevelParameter
from roocs_utils.exceptions import InvalidParameterValue


def test__str__():
    level = 1000
    parameter = LevelParameter(level)
    assert parameter.__str__ == "An object of the LevelParameter class"
    assert parameter.__repr__ == parameter.__str__
    assert parameter.__unicode__ == parameter.__str__


def test_raw():
    level = 1000
    parameter = LevelParameter(level)
    assert parameter.raw == level


def test_validate_error():
    level = '1000'
    with pytest.raises(InvalidParameterValue) as exc:
        LevelParameter(level)
        assert exc.value == "Levels should be passed in as integers"


def test_str():
    level = 1000
    parameter = LevelParameter(level)
    assert parameter.str == '1000'
