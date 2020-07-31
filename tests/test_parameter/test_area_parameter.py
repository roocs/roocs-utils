import pytest

from roocs_utils.parameter.area_parameter import AreaParameter
from roocs_utils.exceptions import InvalidParameterValue


def test__str__():
    area = '0.,49.,10.,65'
    parameter = AreaParameter(area)
    assert parameter.__str__ == "An object of the AreaParameter class"
    assert parameter.__repr__ == parameter.__str__
    assert parameter.__unicode__ == parameter.__str__


def test_raw():
    area = '0.,49.,10.,65'
    parameter = AreaParameter(area)
    assert parameter.raw == area


def test_validate_error():
    area = (0., 49., 10., 65)
    with pytest.raises(InvalidParameterValue) as exc:
        AreaParameter(area)
        assert exc.value == "Area parameter must be passed as a string"


def test_tuple():
    area = '0.,49.,10.,65'
    parameter = AreaParameter(area)
    assert parameter.tuple == (0., 49., 10., 65)