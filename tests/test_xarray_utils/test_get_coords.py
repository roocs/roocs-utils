import os

import pytest
import xarray as xr

from roocs_utils.xarray_utils.xarray_utils import get_coord_by_type
from roocs_utils.xarray_utils.xarray_utils import get_coord_type


# test dataset with no known problems
def test_get_time(mini_esgf_data):
    with xr.open_mfdataset(
        mini_esgf_data["CMIP5_TAS"], use_cftime=True, combine="by_coords"
    ) as ds:
        da = ds["tas"]
        coord = da.time
        assert get_coord_type(coord) == "time"


def test_get_latitude(mini_esgf_data):
    with xr.open_mfdataset(
        mini_esgf_data["CMIP5_TAS"], use_cftime=True, combine="by_coords"
    ) as ds:
        da = ds["tas"]
        coord = da.lat
        assert get_coord_type(coord) == "latitude"


def test_get_longitude(mini_esgf_data):
    with xr.open_mfdataset(
        mini_esgf_data["CMIP5_TAS"], use_cftime=True, combine="by_coords"
    ) as ds:
        da = ds["tas"]
        coord = da.lon
        assert get_coord_type(coord) == "longitude"


# test dataset with no standard name for time
def test_get_time_2(mini_esgf_data):
    with xr.open_mfdataset(
        mini_esgf_data["C3S_CMIP5_TAS"], use_cftime=True, combine="by_coords"
    ) as ds:
        da = ds["tas"]
        coord = da.time
        assert get_coord_type(coord) == "time"


def test_get_latitude_2(mini_esgf_data):
    with xr.open_mfdataset(
        mini_esgf_data["C3S_CMIP5_TAS"], use_cftime=True, combine="by_coords"
    ) as ds:
        da = ds["tas"]
        coord = da.lat
        assert get_coord_type(coord) == "latitude"


def test_get_longitude_2(mini_esgf_data):
    with xr.open_mfdataset(
        mini_esgf_data["C3S_CMIP5_TAS"], use_cftime=True, combine="by_coords"
    ) as ds:
        da = ds["tas"]
        coord = da.lon
        assert get_coord_type(coord) == "longitude"


# test dataset with only time and another coordinate that isn't lat or lon
def test_get_time_3(mini_esgf_data):
    with xr.open_mfdataset(
        mini_esgf_data["CMIP5_ZOSTOGA"], use_cftime=True, combine="by_coords"
    ) as ds:
        da = ds["zostoga"]
        coord = da.time
        assert get_coord_type(coord) == "time"


def test_get_level(mini_esgf_data):
    with xr.open_mfdataset(
        mini_esgf_data["CMIP5_ZOSTOGA"], use_cftime=True, combine="by_coords"
    ) as ds:
        da = ds["zostoga"]
        coord = da.lev
        assert get_coord_type(coord) == "level"


def test_get_other(mini_esgf_data):
    with xr.open_mfdataset(
        mini_esgf_data["CMIP6_SICONC"], use_cftime=True, combine="by_coords"
    ) as ds:
        da = ds["siconc"]
        coord = da.type
        assert get_coord_type(coord) is None


def test_order_of_coords(mini_esgf_data):
    with xr.open_mfdataset(
        mini_esgf_data["CMIP5_ZOSTOGA"], use_cftime=True, combine="by_coords"
    ) as ds:
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
    text_coord_path = "/badc/cmip6/data/CMIP6/ScenarioMIP/IPSL/IPSL-CM6A-LR/ssp245/r1i1p1f1/Lmon/landCoverFrac/gr/v20190119/*.nc"

    with xr.open_mfdataset(text_coord_path, use_cftime=True, combine="by_coords") as ds:
        coord_type = get_coord_type(ds.sector)
        assert coord_type is None
        assert coord_type != "level"


def test_get_coords_by_type(mini_esgf_data):
    with xr.open_mfdataset(
        mini_esgf_data["C3S_CORDEX_AFR_TAS"], use_cftime=True, combine="by_coords"
    ) as ds:

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


def test_get_coords_by_type_with_no_time(mini_esgf_data):
    with xr.open_mfdataset(
        mini_esgf_data["C3S_CORDEX_AFR_TAS"], use_cftime=True, combine="by_coords"
    ) as ds:
        # check time
        time = get_coord_by_type(ds, "time", ignore_aux_coords=False)
        assert time.name == "time"
        # drop time
        ds = ds.drop_dims("time")
        time = get_coord_by_type(ds, "time", ignore_aux_coords=False)
        assert time is None
