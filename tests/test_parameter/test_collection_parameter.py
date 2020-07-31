import pytest

from roocs_utils.parameter.collection_parameter import CollectionParameter
from roocs_utils.exceptions import InvalidParameterValue


def test_validate():
    collection = [
        "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
        "cmip5.output1.MPI-M.MPI-ESM-LR.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
    ]
    parameter = CollectionParameter(collection)

    assert parameter.__str__ == "An object of the CollectionParameter class"
    assert parameter.__repr__ == parameter.__str__
    assert parameter.__unicode__ == parameter.__str__


def test_raw():
    collection = [
        "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
        "cmip5.output1.MPI-M.MPI-ESM-LR.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
    ]
    parameter = CollectionParameter(collection)
    assert parameter.raw == collection


def test_validate_error_id():
    collection = [
        "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
        2,
    ]

    with pytest.raises(InvalidParameterValue) as exc:
        CollectionParameter(collection)
        assert exc.value == "Each id must be a string"


def test_validate_error_lsit_or_tuple():
    collection = "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga, " \
                 "cmip5.output1.MPI-M.MPI-ESM-LR.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga"

    with pytest.raises(InvalidParameterValue) as exc:
        CollectionParameter(collection)
        assert exc.value == "Collections must be a list or tuple"
