import os

import pytest
import xarray as xr

from roocs_utils.xarray_utils.xarray_utils import get_coord_type
from tests.conftest import C3S_CMIP5_TAS
from tests.conftest import CMIP5_TAS
from tests.conftest import CMIP5_ZOSTOGA
from tests.conftest import CMIP6_SICONC


text_coord_path = "/badc/cmip6/data/CMIP6/ScenarioMIP/IPSL/IPSL-CM6A-LR/ssp245/r1i1p1f1/Lmon/landCoverFrac/gr/v20190119/*.nc"


# test dataset with no known problems
def test_get_time(load_test_data):
    ds = xr.open_mfdataset(CMIP5_TAS, use_cftime=True, combine="by_coords")
    da = ds["tas"]
    coord = da.time
    assert get_coord_type(coord) == "time"


def test_get_latitude(load_test_data):
    ds = xr.open_mfdataset(CMIP5_TAS, use_cftime=True, combine="by_coords")
    da = ds["tas"]
    coord = da.lat
    assert get_coord_type(coord) == "latitude"


def test_get_longitude(load_test_data):
    ds = xr.open_mfdataset(CMIP5_TAS, use_cftime=True, combine="by_coords")
    da = ds["tas"]
    coord = da.lon
    assert get_coord_type(coord) == "longitude"


# test dataset with no standard name for time
def test_get_time_2(load_test_data):
    ds = xr.open_mfdataset(C3S_CMIP5_TAS, use_cftime=True, combine="by_coords")
    da = ds["tas"]
    coord = da.time
    assert get_coord_type(coord) == "time"


def test_get_latitude_2(load_test_data):
    ds = xr.open_mfdataset(C3S_CMIP5_TAS, use_cftime=True, combine="by_coords")
    da = ds["tas"]
    coord = da.lat
    assert get_coord_type(coord) == "latitude"


def test_get_longitude_2(load_test_data):
    ds = xr.open_mfdataset(C3S_CMIP5_TAS, use_cftime=True, combine="by_coords")
    da = ds["tas"]
    coord = da.lon
    assert get_coord_type(coord) == "longitude"


# test dataset with only time and another coordinate that isn't lat or lon
def test_get_time_3(load_test_data):
    ds = xr.open_mfdataset(CMIP5_ZOSTOGA, use_cftime=True, combine="by_coords")
    da = ds["zostoga"]
    coord = da.time
    assert get_coord_type(coord) == "time"


def test_get_level(load_test_data):
    ds = xr.open_mfdataset(CMIP5_ZOSTOGA, use_cftime=True, combine="by_coords")
    da = ds["zostoga"]
    coord = da.lev
    assert get_coord_type(coord) == "level"


def test_get_other(load_test_data):
    ds = xr.open_mfdataset(CMIP6_SICONC, use_cftime=True, combine="by_coords")
    da = ds["siconc"]
    coord = da.type
    assert get_coord_type(coord) is None


def test_order_of_coords(load_test_data):
    ds = xr.open_mfdataset(CMIP5_ZOSTOGA, use_cftime=True, combine="by_coords")
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
