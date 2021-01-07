import pytest
import xarray as xr

from roocs_utils.project_utils import get_project_base_dir
from roocs_utils.project_utils import get_project_name


def test_get_project_name():
    # dset = "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga"
    # project = get_project_name(dset)
    # assert project == "cmip5"
    #
    # dset = "/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/*.nc"
    # project = get_project_name(dset)
    # assert project == "cmip5"
    #
    # dset = (
    #     "tests/mini-esgf-data/test_data/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos"
    #     "/Amon/r1i1p1/latest/tas/*.nc"
    # )
    # project = get_project_name(dset)
    # assert project == "cmip5"
    #
    # dset = "CMIP6.CMIP.NCAR.CESM2.historical.r1i1p1f1.SImon.siconc.gn.latest"
    # project = get_project_name(dset)
    # assert project == "cmip6"
    #
    # ds = xr.open_mfdataset(
    #     "tests/mini-esgf-data/test_data/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical"
    #     "/mon/atmos/Amon/r1i1p1/latest/tas/*.nc",
    #     use_cftime=True,
    #     combine="by_coords",
    # )
    # project = get_project_name(ds)
    # assert project == "cmip5"

    # ds = xr.open_mfdataset(
    #     "tests/mini-esgf-data/test_data/badc/cmip6/data/CMIP6/CMIP/NCAR/CESM2/historical/r1i1p1f1"
    #     "/SImon/siconc/gn/latest/*.nc",
    #     use_cftime=True,
    #     combine="by_coords",
    # )
    # project = get_project_name(ds)
    # assert project == "cmip6"

    dset = "/badc/cmip6/data/CMIP6/CMIP/MIROC/MIROC6/historical/r1i1p1f1/SImon/siconc/gn/latest/*.nc"
    project = get_project_name(dset)
    assert project == "c3s-cmip6"


def test_get_project_base_dir():
    cmip5_base_dir = get_project_base_dir("cmip5")
    assert cmip5_base_dir == "/badc/cmip5/data/cmip5"

    c3s_cordex_base_dir = get_project_base_dir("c3s-cordex")
    assert c3s_cordex_base_dir == "/gws/nopw/j04/cp4cds1_vol1/data/c3s-cordex"

    with pytest.raises(Exception) as exc:
        get_project_base_dir("test")
        assert exc.value == "The project supplied is not known."
