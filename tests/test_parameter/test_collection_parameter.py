import pytest

from roocs_utils.exceptions import InvalidParameterValue
from roocs_utils.exceptions import MissingParameterValue
from roocs_utils.parameter.collection_parameter import CollectionParameter


def test__str__():
    collection = [
        "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
        "cmip5.output1.MPI-M.MPI-ESM-LR.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
    ]
    parameter = CollectionParameter(collection)

    assert (
        parameter.__str__() == "Datasets to analyse:"
        "\ncmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga"
        "\ncmip5.output1.MPI-M.MPI-ESM-LR.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga"
    )

    assert parameter.__repr__() == parameter.__str__()
    assert parameter.__unicode__() == parameter.__str__()


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
    assert (
        str(exc.value) == "Each id in a collection must be a string or "
        "an instance of <class 'roocs_utils.utils.file_utils.FileMapper'>"
    )


def test_string():
    collection = (
        "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga,"
        "cmip5.output1.MPI-M.MPI-ESM-LR.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga"
    )

    parameter = CollectionParameter(collection)
    assert parameter.tuple == (
        "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
        "cmip5.output1.MPI-M.MPI-ESM-LR.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
    )


def test_one_id():
    collection = "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga"
    parameter = CollectionParameter(collection)
    assert parameter.tuple == (
        "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
    )


def test_whitespace():
    collection = (
        "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga, "
        "cmip5.output1.MPI-M.MPI-ESM-LR.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga "
    )

    parameter = CollectionParameter(collection)
    assert parameter.tuple == (
        "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
        "cmip5.output1.MPI-M.MPI-ESM-LR.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
    )


def test_empty_string():
    collection = ""
    with pytest.raises(MissingParameterValue) as exc:
        CollectionParameter(collection)
    assert str(exc.value) == "CollectionParameter must be provided"


def test_none():
    collection = None

    with pytest.raises(MissingParameterValue) as exc:
        CollectionParameter(collection)
    assert str(exc.value) == "CollectionParameter must be provided"


def test_class_instance():
    collection = (
        "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga,"
        "cmip5.output1.MPI-M.MPI-ESM-LR.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga"
    )
    parameter = CollectionParameter(collection)
    new_parameter = CollectionParameter(parameter)
    assert new_parameter.tuple == (
        "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
        "cmip5.output1.MPI-M.MPI-ESM-LR.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
    )
