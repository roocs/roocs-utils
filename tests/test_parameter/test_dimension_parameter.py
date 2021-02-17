import pytest

from roocs_utils.exceptions import InvalidParameterValue
from roocs_utils.parameter.dimension_parameter import DimensionParameter


def test__str__():
    dims = "time,latitude"
    parameter = DimensionParameter(dims)
    assert (
        parameter.__str__() == "Dimensions to average over:" f"\n ('time', 'latitude')"
    )
    assert parameter.__repr__() == parameter.__str__()
    assert parameter.__unicode__() == parameter.__str__()


def test_raw():
    dims = "time,latitude"
    parameter = DimensionParameter(dims)
    assert parameter.raw == dims


def test_str():
    dims = "time,latitude"
    parameter = DimensionParameter(dims)
    assert parameter.tuple == ("time", "latitude")


def test_tuple():
    dims = ("time", "latitude")
    parameter = DimensionParameter(dims)
    assert parameter.tuple == ("time", "latitude")


def test_input_list():
    dims = ["time", "latitude"]
    parameter = DimensionParameter(dims)
    assert parameter.tuple == ("time", "latitude")


def test_validate_error_dimension():
    dims = "wrong"
    with pytest.raises(InvalidParameterValue) as exc:
        DimensionParameter(dims)
    assert (
        str(exc.value)
        == "Dimensions for averaging must be one of ['time', 'level', 'latitude', 'longitude']"
    )


def test_asdict():
    dims = ["time", "latitude"]
    parameter = DimensionParameter(dims)
    assert parameter.asdict() == {"dims": ("time", "latitude")}


def test_whitespace():
    dims = "time, latitude"
    parameter = DimensionParameter(dims)
    assert parameter.tuple == ("time", "latitude")


def test_empty_string():
    dims = ""
    assert DimensionParameter(dims).asdict() is None
    assert DimensionParameter(dims).tuple is None


def test_none():
    dims = None
    assert DimensionParameter(dims).asdict() is None
    assert DimensionParameter(dims).tuple is None


def test_class_instance():
    dims = "time"
    parameter = DimensionParameter(dims)
    new_parameter = DimensionParameter(parameter)
    assert new_parameter.tuple == ("time",)


def test_not_a_string():
    dims = (0, "latitude")
    with pytest.raises(InvalidParameterValue) as exc:
        DimensionParameter(dims)
    assert str(exc.value) == "Each dimension must be a string."
