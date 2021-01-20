import cf_xarray
import pytest
import xarray as xr

from tests.conftest import C3S_CMIP5_TAS
from tests.conftest import CMIP5_TAS


def test_get_standard_names(load_test_data):
    ds = xr.open_mfdataset(CMIP5_TAS, use_cftime=True, combine="by_coords")
    assert sorted(ds.cf.get_standard_names()) == sorted(
        [
            "air_temperature",
            "height",
            "latitude",
            "longitude",
            "time",
        ]
    )


@pytest.mark.xfail(reason="left has height coord")
def test_get_latitude(load_test_data):
    ds = xr.open_mfdataset(CMIP5_TAS, use_cftime=True, combine="by_coords")
    xr.testing.assert_identical(ds["lat"], ds.cf["lat"])
    xr.testing.assert_identical(ds["lat"], ds.cf["latitude"])
    xr.testing.assert_identical(ds["lat"], ds.cf["lats"])


def test_get_latitude_2(load_test_data):
    ds = xr.open_mfdataset(C3S_CMIP5_TAS, use_cftime=True, combine="by_coords")
    xr.testing.assert_identical(ds["lat"], ds.cf["lat"])
    xr.testing.assert_identical(ds["lat"], ds.cf["latitude"])
    with pytest.raises(KeyError):
        xr.testing.assert_identical(ds["lat"], ds.cf["lats"])


def test_get_lat_lon_names_from_ds(load_test_data):
    ds = xr.open_mfdataset(CMIP5_TAS, use_cftime=True, combine="by_coords")
    assert ds.cf["latitude"].name == "lat"
    assert ds.cf["longitude"].name == "lon"
    # not sure how it will deal with lats


@pytest.mark.xfail(reason="left has height coord")
def test_get_time(load_test_data):
    ds = xr.open_mfdataset(CMIP5_TAS, use_cftime=True, combine="by_coords")
    xr.testing.assert_identical(ds["time"], ds.cf["time"])
