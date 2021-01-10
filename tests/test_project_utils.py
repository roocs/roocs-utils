import pytest
import xarray as xr

from roocs_utils.project_utils import get_project_base_dir
from roocs_utils.project_utils import get_project_name


def test_get_project_name(cmip5_tas, cmip6_siconc):
    dset = "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga"
    project = get_project_name(dset)
    assert project == "cmip5""

    dset = cmip5_tas
    project = get_project_name(dset)
    assert project == "cmip5"

    dset = "CMIP6.CMIP.NCAR.CESM2.historical.r1i1p1f1.SImon.siconc.gn.latest"
    project = get_project_name(dset)
    assert project == "cmip6"

    ds = xr.open_mfdataset(
        cmip5_tas,
        use_cftime=True,
        combine="by_coords",
    )
    project = get_project_name(ds)
    assert project == "cmip5"

    ds = xr.open_mfdataset(
        cmip6_siconc,
        use_cftime=True,
        combine="by_coords",
    )
    project = get_project_name(ds)
    assert project == "cmip6"


def test_get_project_name_badc():
    dset = "/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/*.nc"
    project = get_project_name(dset)
    assert project == "cmip5


def test_get_project_base_dir():
    cmip5_base_dir = get_project_base_dir("cmip5")
    assert cmip5_base_dir == "/badc/cmip5/data"

    c3s_cordex_base_dir = get_project_base_dir("c3s-cordex")
    assert c3s_cordex_base_dir == "/group_workspaces/jasmin2/cp4cds1/vol1/data"

    with pytest.raises(Exception) as exc:
        get_project_base_dir("test")
        assert exc.value == "The project supplied is not known."
