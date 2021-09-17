import pytest

from roocs_utils.exceptions import InvalidParameterValue
from roocs_utils.parameter.time_components_parameter import (
    TimeComponentsParameter,
    time_components,
    string_to_dict,
)


type_error = (
    "Input type of <{}> not allowed. Must be one of: "
    "[<class 'dict'>, <class 'str'>, <class "
    "'roocs_utils.parameter.param_utils.TimeComponents'>, <class 'NoneType'>]"
)


tc_str = "year:1999,2000,2001|month:12,01,02|hour:00"
tc_dict = {"year": [1999, 2000, 2001], "month": [12, 1, 2], "hour": [0]}
tc_dict_month_long_names = {
    "year": [1999, 2000, 2001],
    "month": ["December", "January", "February"],
    "hour": [0],
}
tc_dict_short_names = {
    "year": [1999, 2000, 2001],
    "month": ["dec", "jan", "feb"],
    "hour": [0],
}


def test_TimeComponents_class():
    tc1 = time_components(**string_to_dict(tc_str))
    tc2 = time_components(**tc_dict)
    tc3 = time_components(**tc_dict_month_long_names)
    tc4 = time_components(**tc_dict_short_names)

    assert tc1.value == tc2.value
    assert tc2.value == tc3.value
    assert tc2.value == tc4.value


def test__str__():
    parameter = TimeComponentsParameter(tc_str)
    assert str(parameter).startswith("Time components to select:")
    assert "month => [12, 1, 2]" in str(parameter)


def test_raw():
    parameter = TimeComponentsParameter(tc_str)
    assert parameter.raw == tc_str


def test_validate_error_id():
    with pytest.raises(InvalidParameterValue) as exc:
        TimeComponentsParameter("I am rubbish")
    assert str(exc.value) == "Cannot create TimeComponentsParameter from: I am rubbish"


def test_bad_type_input():
    with pytest.raises(InvalidParameterValue) as exc:
        TimeComponentsParameter(34)
    assert str(exc.value) == type_error.format("class 'int'")


def test_dict():
    for input_dct in (tc_dict, tc_dict_short_names, tc_dict_month_long_names):
        parameter = TimeComponentsParameter(input_dct)
        assert parameter.value == tc_dict


def test_time_components_input():
    tc = time_components(**tc_dict)
    parameter = TimeComponentsParameter(tc)
    assert parameter.value == tc_dict


def test_time_components_with_args():
    tc = time_components(year=[200, 500], hour="06")
    assert tc.value["year"] == [200, 500]
    assert tc.value["hour"] == [6]


def test_whitespace():
    parameter = TimeComponentsParameter(tc_str + "   ")
    assert parameter.value == tc_dict


def test_empty_string():
    parameter = TimeComponentsParameter("")
    assert parameter.value is None


def test_none():
    parameter = TimeComponentsParameter(None)
    assert parameter.value is None


def test_class_instance():
    parameter = TimeComponentsParameter(tc_str)
    new_parameter = TimeComponentsParameter(parameter)
    assert new_parameter.value == tc_dict
