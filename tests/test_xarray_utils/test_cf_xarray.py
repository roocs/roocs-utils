import cf_xarray  # noqa: F401
import pytest
import xarray as xr


def test_get_standard_names(mini_esgf_data):
    with xr.open_mfdataset(
        mini_esgf_data["CMIP5_TAS"], use_cftime=True, combine="by_coords"
    ) as ds:
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
def test_get_latitude(mini_esgf_data):
    with xr.open_mfdataset(
        mini_esgf_data["CMIP5_TAS"], use_cftime=True, combine="by_coords"
    ) as ds:
        xr.testing.assert_identical(ds["lat"], ds.cf["lat"])
        xr.testing.assert_identical(ds["lat"], ds.cf["latitude"])
        xr.testing.assert_identical(ds["lat"], ds.cf["lats"])


def test_get_latitude_2(mini_esgf_data):
    with xr.open_mfdataset(
        mini_esgf_data["C3S_CMIP5_TAS"], use_cftime=True, combine="by_coords"
    ) as ds:
        xr.testing.assert_identical(ds["lat"], ds.cf["lat"])
        xr.testing.assert_identical(ds["lat"], ds.cf["latitude"])
        with pytest.raises(KeyError):
            xr.testing.assert_identical(ds["lat"], ds.cf["lats"])


def test_get_lat_lon_names_from_ds(mini_esgf_data):
    with xr.open_mfdataset(
        mini_esgf_data["CMIP5_TAS"], use_cftime=True, combine="by_coords"
    ) as ds:
        assert ds.cf["latitude"].name == "lat"
        assert ds.cf["longitude"].name == "lon"
        # not sure how it will deal with lats


@pytest.mark.xfail(reason="left has height coord")
def test_get_time(mini_esgf_data):
    with xr.open_mfdataset(
        mini_esgf_data["CMIP5_TAS"], use_cftime=True, combine="by_coords"
    ) as ds:
        xr.testing.assert_identical(ds["time"], ds.cf["time"])
