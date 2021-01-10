import os

import pytest
import xarray as xr

from roocs_utils.xarray_utils.xarray_utils import get_coord_type

f1 = "tests/mini-esgf-data/test_data/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/*.nc" #cmip5_tas
f2 = "tests/mini-esgf-data/test_data/group_workspaces/jasmin2/cp4cds1/vol1/data/c3s-cmip5/output1/ICHEC/EC-EARTH/historical/day/atmos/day/r1i1p1/tas/v20131231/*.nc" #c3s_cmip5_tas
f3 = "tests/mini-esgf-data/test_data/badc/cmip5/data/cmip5/output1/INM/inmcm4/rcp45/mon/ocean/Omon/r1i1p1/latest/zostoga/*.nc" #cmip5_zostoga
f4 = "tests/mini-esgf-data/test_data/badc/cmip6/data/CMIP6/CMIP/CCCma/CanESM5/historical/r1i1p1f1/SImon/siconc/gn/latest/*.nc" #cmip6_siconc
test_path = ( #cmip5_zostoga
    "tests/mini-esgf-data/test_data/badc/cmip5/data/cmip5"
    "/output1/INM/inmcm4/rcp45/mon/ocean/Omon/r1i1p1/latest/zostoga/*.nc"
)
text_coord_path = "/badc/cmip6/data/CMIP6/ScenarioMIP/IPSL/IPSL-CM6A-LR/ssp245/r1i1p1f1/Lmon/landCoverFrac/gr/v20190119/*.nc"


# test dataset with no known problems
def test_get_time(cmip5_tas):
    ds = xr.open_mfdataset(cmip5_tas, use_cftime=True, combine="by_coords")
    da = ds["tas"]
    coord = da.time
    assert get_coord_type(coord) == "time"


def test_get_latitude(cmip5_tas):
    ds = xr.open_mfdataset(cmip5_tas, use_cftime=True, combine="by_coords")
    da = ds["tas"]
    coord = da.lat
    assert get_coord_type(coord) == "latitude"


def test_get_longitude(cmip5_tas):
    ds = xr.open_mfdataset(cmip5_tas, use_cftime=True, combine="by_coords")
    da = ds["tas"]
    coord = da.lon
    assert get_coord_type(coord) == "longitude"


# test dataset with no standard name for time
def test_get_time_2(c3s_cmip5_tas):
    ds = xr.open_mfdataset(c3s_cmip5_tas, use_cftime=True, combine="by_coords")
    da = ds["tas"]
    coord = da.time
    assert get_coord_type(coord) == "time"


def test_get_latitude_2(c3s_cmip5_tas):
    ds = xr.open_mfdataset(c3s_cmip5_tas, use_cftime=True, combine="by_coords")
    da = ds["tas"]
    coord = da.lat
    assert get_coord_type(coord) == "latitude"


def test_get_longitude_2(c3s_cmip5_tas):
    ds = xr.open_mfdataset(c3s_cmip5_tas, use_cftime=True, combine="by_coords")
    da = ds["tas"]
    coord = da.lon
    assert get_coord_type(coord) == "longitude"


# test dataset with only time and another coordinate that isn't lat or lon
def test_get_time_3(cmip5_zostoga):
    ds = xr.open_mfdataset(cmip5_zostoga, use_cftime=True, combine="by_coords")
    da = ds["zostoga"]
    coord = da.time
    assert get_coord_type(coord) == "time"


def test_get_level(cmip5_zostoga):
    ds = xr.open_mfdataset(cmip5_zostoga, use_cftime=True, combine="by_coords")
    da = ds["zostoga"]
    coord = da.lev
    assert get_coord_type(coord) == "level"


def test_get_other(cmip6_siconc):
    ds = xr.open_mfdataset(cmip6_siconc, use_cftime=True, combine="by_coords")
    da = ds["siconc"]
    coord = da.type
    assert get_coord_type(coord) is None


def test_order_of_coords(cmip5_zostoga):
    ds = xr.open_mfdataset(cmip5_zostoga, use_cftime=True, combine="by_coords")
    da = ds["zostoga"]

    coords = [_ for _ in da.coords]
    assert coords == ["lev", "time"]

    coord_names_keys = [_ for _ in da.coords.keys()]
    assert coord_names_keys == ["lev", "time"]

    # this changes order each time
    # coord_names = [_ for _ in da.coords._names]
    # assert coord_names == ['time', 'lev']

    coord_names_keys = [_ for _ in da.coords]
    assert coord_names_keys == ["lev", "time"]

    coord_sizes = [da[f"{coord}"].size for coord in da.coords.keys()]
    shape = da.shape

    dims = da.dims
    assert dims == ("time", "lev")

    assert shape == (1140, 1)  # looks like shape comes from dims
    assert coord_sizes == [1, 1140]
    assert ds["lev"].shape == (1,)
    assert ds["time"].shape == (1140,)


@pytest.mark.skipif(os.path.isdir("/badc") is False, reason="data not available")
def test_text_coord_not_level():
    ds = xr.open_mfdataset(text_coord_path, use_cftime=True, combine="by_coords")
    coord_type = get_coord_type(ds.sector)
    assert coord_type is None
    assert coord_type != "level"
