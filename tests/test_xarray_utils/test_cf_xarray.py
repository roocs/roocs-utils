import cf_xarray  # noqa: F401
import pytest
import xarray as xr


def test_get_standard_names(load_test_data, cmip5_tas):
    ds = xr.open_mfdataset(cmip5_tas, use_cftime=True, combine="by_coords")
    assert sorted(ds.cf.standard_names) == sorted(
        [
            "air_temperature",
            "height",
            "latitude",
            "longitude",
            "time",
        ]
    )


@pytest.mark.xfail(reason="left has height coord")
def test_get_latitude(load_test_data, cmip5_tas):
    ds = xr.open_mfdataset(cmip5_tas, use_cftime=True, combine="by_coords")
    xr.testing.assert_identical(ds["lat"], ds.cf["lat"])
    xr.testing.assert_identical(ds["lat"], ds.cf["latitude"])
    xr.testing.assert_identical(ds["lat"], ds.cf["lats"])


def test_get_latitude_2(load_test_data, c3s_cmip5_tas):
    ds = xr.open_mfdataset(c3s_cmip5_tas, use_cftime=True, combine="by_coords")
    xr.testing.assert_identical(ds["lat"], ds.cf["lat"])
    xr.testing.assert_identical(ds["lat"], ds.cf["latitude"])
    with pytest.raises(KeyError):
        xr.testing.assert_identical(ds["lat"], ds.cf["lats"])


def test_get_lat_lon_names_from_ds(load_test_data, cmip5_tas):
    ds = xr.open_mfdataset(cmip5_tas, use_cftime=True, combine="by_coords")
    assert ds.cf["latitude"].name == "lat"
    assert ds.cf["longitude"].name == "lon"
    # not sure how it will deal with lats


@pytest.mark.xfail(reason="left has height coord")
def test_get_time(load_test_data, cmip5_tas):
    ds = xr.open_mfdataset(cmip5_tas, use_cftime=True, combine="by_coords")
    xr.testing.assert_identical(ds["time"], ds.cf["time"])
