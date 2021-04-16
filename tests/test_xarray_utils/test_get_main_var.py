import os

import pytest
import xarray as xr

from roocs_utils.xarray_utils.xarray_utils import get_main_variable
from tests.conftest import CMIP5_TAS


@pytest.mark.skipif(os.path.isdir("/gws") is False, reason="data not available")
def test_get_main_var():
    data = (
        "/gws/nopw/j04/cp4cds1_vol1/data"
        "/c3s-cmip5/output1/ICHEC/EC-EARTH/historical/day"
        "/atmos/day/r1i1p1/tas/latest/*.nc"
    )

    ds = xr.open_mfdataset(data, use_cftime=True, combine="by_coords")
    result = get_main_variable(ds)
    assert result == "tas"


@pytest.mark.skipif(os.path.isdir("/badc") is False, reason="data not available")
def test_get_main_var_2():
    data = "/badc/cmip5/data/cmip5/output1/INM/inmcm4/rcp45/mon/ocean/Omon/r1i1p1/latest/zostoga/*.nc"

    ds = xr.open_mfdataset(data, use_cftime=True, combine="by_coords")
    result = get_main_variable(ds)
    assert result == "zostoga"


@pytest.mark.skipif(os.path.isdir("/badc") is False, reason="data not available")
def test_get_main_var_3():
    data = "/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/*.nc"

    ds = xr.open_mfdataset(data, use_cftime=True, combine="by_coords")
    result = get_main_variable(ds)
    assert result == "tas"


@pytest.mark.skipif(os.path.isdir("/badc") is False, reason="data not available")
def test_get_main_var_4():
    data = "/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/land/Lmon/r1i1p1/latest/rh/*.nc"

    ds = xr.open_mfdataset(data, use_cftime=True, combine="by_coords")
    result = get_main_variable(ds)
    assert result == "rh"


def test_get_main_var_test_data(load_test_data):
    ds = xr.open_mfdataset(CMIP5_TAS, use_cftime=True, combine="by_coords")
    var_id = get_main_variable(ds)
    assert var_id == "tas"


def test_get_main_var_include_common_coords(load_test_data):
    ds = xr.open_mfdataset(CMIP5_TAS, use_cftime=True, combine="by_coords")
    var_id = get_main_variable(ds, exclude_common_coords=False)

    # incorrectly identified main variable and common_coords included in search
    assert var_id == "lat_bnds"
