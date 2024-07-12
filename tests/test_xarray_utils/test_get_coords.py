import os

import pytest
import xarray as xr

from roocs_utils.xarray_utils.xarray_utils import get_coord_by_type
from roocs_utils.xarray_utils.xarray_utils import get_coord_type

text_coord_path = "/badc/cmip6/data/CMIP6/ScenarioMIP/IPSL/IPSL-CM6A-LR/ssp245/r1i1p1f1/Lmon/landCoverFrac/gr/v20190119/*.nc"


# test dataset with no known problems
def test_get_time(load_test_data, cmip5_tas):
    ds = xr.open_mfdataset(cmip5_tas, use_cftime=True, combine="by_coords")
    da = ds["tas"]
    coord = da.time
    assert get_coord_type(coord) == "time"


def test_get_latitude(load_test_data, cmip5_tas):
    ds = xr.open_mfdataset(cmip5_tas, use_cftime=True, combine="by_coords")
    da = ds["tas"]
    coord = da.lat
    assert get_coord_type(coord) == "latitude"


def test_get_longitude(load_test_data, cmip5_tas):
    ds = xr.open_mfdataset(cmip5_tas, use_cftime=True, combine="by_coords")
    da = ds["tas"]
    coord = da.lon
    assert get_coord_type(coord) == "longitude"


# test dataset with no standard name for time
def test_get_time_2(load_test_data, c3s_cmip5_tas):
    ds = xr.open_mfdataset(c3s_cmip5_tas, use_cftime=True, combine="by_coords")
    da = ds["tas"]
    coord = da.time
    assert get_coord_type(coord) == "time"


def test_get_latitude_2(load_test_data, c3s_cmip5_tas):
    ds = xr.open_mfdataset(c3s_cmip5_tas, use_cftime=True, combine="by_coords")
    da = ds["tas"]
    coord = da.lat
    assert get_coord_type(coord) == "latitude"


def test_get_longitude_2(load_test_data, c3s_cmip5_tas):
    ds = xr.open_mfdataset(c3s_cmip5_tas, use_cftime=True, combine="by_coords")
    da = ds["tas"]
    coord = da.lon
    assert get_coord_type(coord) == "longitude"


# test dataset with only time and another coordinate that isn't lat or lon
def test_get_time_3(load_test_data, cmip5_zostoga):
    ds = xr.open_mfdataset(cmip5_zostoga, use_cftime=True, combine="by_coords")
    da = ds["zostoga"]
    coord = da.time
    assert get_coord_type(coord) == "time"


def test_get_level(load_test_data, cmip5_zostoga):
    ds = xr.open_mfdataset(cmip5_zostoga, use_cftime=True, combine="by_coords")
    da = ds["zostoga"]
    coord = da.lev
    assert get_coord_type(coord) == "level"


def test_get_other(load_test_data, cmip6_siconc):
    ds = xr.open_mfdataset(cmip6_siconc, use_cftime=True, combine="by_coords")
    da = ds["siconc"]
    coord = da.type
    assert get_coord_type(coord) is None


def test_order_of_coords(load_test_data, cmip5_zostoga):
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


def test_get_coords_by_type(c3s_cordex_afr_tas):
    ds = xr.open_mfdataset(c3s_cordex_afr_tas, use_cftime=True, combine="by_coords")

    # check lat, lon, time and level are found when they are coordinates
    lat = get_coord_by_type(ds, "latitude", ignore_aux_coords=False)
    lon = get_coord_by_type(ds, "longitude", ignore_aux_coords=False)
    time = get_coord_by_type(ds, "time", ignore_aux_coords=False)
    level = get_coord_by_type(ds, "level", ignore_aux_coords=False)

    assert lat.name == "lat"
    assert lon.name == "lon"
    assert time.name == "time"
    assert level.name == "height"

    # test that latitude and longitude are still found when they are data variables
    # reset coords sets lat and lon as data variables
    ds = ds.reset_coords(["lat", "lon"])

    # if ignore_Aux_coords=True then lat/lon should not be identified
    lat = get_coord_by_type(ds, "latitude", ignore_aux_coords=True)
    lon = get_coord_by_type(ds, "longitude", ignore_aux_coords=True)

    assert lat is None
    assert lon is None

    # if ignore_Aux_coords=False then lat/lon should be identified
    lat = get_coord_by_type(ds, "latitude", ignore_aux_coords=False)
    lon = get_coord_by_type(ds, "longitude", ignore_aux_coords=False)

    assert lat.name == "lat"
    assert lon.name == "lon"


def test_get_coords_by_type_with_no_time(c3s_cordex_afr_tas):
    ds = xr.open_mfdataset(c3s_cordex_afr_tas, use_cftime=True, combine="by_coords")
    # check time
    time = get_coord_by_type(ds, "time", ignore_aux_coords=False)
    assert time.name == "time"
    # drop time
    ds = ds.drop_dims("time")
    time = get_coord_by_type(ds, "time", ignore_aux_coords=False)
    assert time is None
