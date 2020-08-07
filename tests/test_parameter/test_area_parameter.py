import pytest

from roocs_utils.parameter.area_parameter import AreaParameter
from roocs_utils.exceptions import InvalidParameterValue


def test__str__():
    area = "0.,49.,10.,65"
    parameter = AreaParameter(area)
    assert parameter.__str__() == 'Area to subset over:' \
                                  f'\n (0.0, 49.0, 10.0, 65.0)'
    assert parameter.__repr__() == parameter.__str__()
    assert parameter.__unicode__() == parameter.__str__()


def test_raw():
    area = "0.,49.,10.,65"
    parameter = AreaParameter(area)
    assert parameter.raw == area


def test_tuple():
    area = "0.,49.,10.,65"
    parameter = AreaParameter(area)
    assert parameter.tuple == (0., 49., 10., 65)


def test_input_list():
    area = [0, 49.5, 10, 65]
    parameter = AreaParameter(area)
    assert parameter.tuple == (0., 49.5, 10., 65)


def test_validate_error_number():
    area = 0
    with pytest.raises(InvalidParameterValue) as exc:
        AreaParameter(area)
    assert str(exc.value) == "The parameter is not in an accepted format"


def test_validate_error_words():
    area = ['test', 'area', 'error', 'words']
    with pytest.raises(InvalidParameterValue) as exc:
        AreaParameter(area)
    assert str(exc.value) == "Area values must be a number"


def test_validate_error_len_1_tuple():
    area = (0, 65)
    with pytest.raises(InvalidParameterValue) as exc:
        AreaParameter(area)
    assert str(exc.value) == "The parameter should be of length 4 but is of length 2"


def test_asdict():
    area = "0.,49.,10.,65"
    parameter = AreaParameter(area)
    assert parameter.asdict() == {"lon_bnds": [0, 10],
                                  "lat_bnds": [49, 65]}


def test_whitespace():
    area = "0., 49., 10., 65"
    parameter = AreaParameter(area)
    assert parameter.tuple == (0., 49., 10., 65)


def test_empty_string():
    area = ""
    with pytest.raises(InvalidParameterValue) as exc:
        AreaParameter(area)
    assert str(exc.value) == "This parameter must be provided"


def test_none():
    area = None
    with pytest.raises(InvalidParameterValue) as exc:
        AreaParameter(area)
    assert str(exc.value) == "This parameter must be provided"
    

def test_class_instance():
    area = "0.,49.,10.,65"
    parameter = AreaParameter(area)
    new_parameter = AreaParameter(parameter)
    assert new_parameter.tuple == (0., 49., 10., 65.)

