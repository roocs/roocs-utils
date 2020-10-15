import pytest

from roocs_utils.exceptions import InvalidParameterValue
from roocs_utils.parameter.area_parameter import AreaParameter


def test__str__():
    area = "0.,49.,10.,65"
    parameter = AreaParameter(area)
    assert parameter.__str__() == "Area to subset over:" f"\n (0.0, 49.0, 10.0, 65.0)"
    assert parameter.__repr__() == parameter.__str__()
    assert parameter.__unicode__() == parameter.__str__()


def test_raw():
    area = "0.,49.,10.,65"
    parameter = AreaParameter(area)
    assert parameter.raw == area


def test_tuple():
    area = "0.,49.,10.,65"
    parameter = AreaParameter(area)
    assert parameter.tuple == (0.0, 49.0, 10.0, 65)


def test_area_is_tuple_string():
    area = ("0", "-10", "120", "40")
    parameter = AreaParameter(area)
    assert parameter.tuple == (0.0, -10.0, 120.0, 40.0)


def test_input_list():
    area = [0, 49.5, 10, 65]
    parameter = AreaParameter(area)
    assert parameter.tuple == (0.0, 49.5, 10.0, 65)


def test_validate_error_number():
    area = 0
    with pytest.raises(InvalidParameterValue) as exc:
        AreaParameter(area)
    assert str(exc.value) == "AreaParameter is not in an accepted format"


def test_validate_error_words():
    area = ["test", "area", "error", "words"]
    with pytest.raises(InvalidParameterValue) as exc:
        AreaParameter(area)
    assert str(exc.value) == "Area values must be a number"


def test_validate_error_len_1_tuple():
    area = (0, 65)
    with pytest.raises(InvalidParameterValue) as exc:
        AreaParameter(area)
    assert str(exc.value) == "AreaParameter should be of length 4 but is of length 2"


def test_asdict():
    area = "0.,49.,10.,65"
    parameter = AreaParameter(area)
    assert parameter.asdict() == {"lon_bnds": (0, 10), "lat_bnds": (49, 65)}


def test_whitespace():
    area = "0., 49., 10., 65"
    parameter = AreaParameter(area)
    assert parameter.tuple == (0.0, 49.0, 10.0, 65)


def test_empty_string():
    area = ""
    assert AreaParameter(area).asdict() is None
    assert AreaParameter(area).tuple is None


def test_none():
    area = None
    assert AreaParameter(area).asdict() is None
    assert AreaParameter(area).tuple is None


def test_none_2():
    area = None
    assert AreaParameter(area).asdict() is None
    assert AreaParameter(area).tuple is None


def test_class_instance():
    area = "0.,49.,10.,65"
    parameter = AreaParameter(area)
    new_parameter = AreaParameter(parameter)
    assert new_parameter.tuple == (0.0, 49.0, 10.0, 65.0)
