import cf_xarray
import pytest
import xarray as xr

f1 = "tests/mini-esgf-data/test_data/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp85/mon/atmos/Amon/r1i1p1/latest/tas/*.nc" #cmip5_tas
f2 = "tests/mini-esgf-data/test_data/group_workspaces/jasmin2/cp4cds1/vol1/data/c3s-cmip5/output1/ICHEC/EC-EARTH/historical/day/atmos/day/r1i1p1/tas/v20131231/*.nc" #c3s_cmip5_tas
f3 = "tests/mini-esgf-data/test_data/badc/cmip5/data/cmip5/output1/INM/inmcm4/rcp45/mon/ocean/Omon/r1i1p1/latest/zostoga/*.nc"
test_path = (
    "tests/mini-esgf-data/test_data/badc/cmip5/data/cmip5"
    "/output1/INM/inmcm4/rcp45/mon/ocean/Omon/r1i1p1/latest/zostoga/*.nc"
)


def test_get_standard_names(cmip5_tas):
    ds = xr.open_mfdataset(cmip5_tas, use_cftime=True, combine="by_coords")
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
def test_get_latitude(cmip5_tas):
    ds = xr.open_mfdataset(cmip5_tas, use_cftime=True, combine="by_coords")
    xr.testing.assert_identical(ds["lat"], ds.cf["lat"])
    xr.testing.assert_identical(ds["lat"], ds.cf["latitude"])
    xr.testing.assert_identical(ds["lat"], ds.cf["lats"])


def test_get_latitude_2(c3s_cmip5_tas):
    ds = xr.open_mfdataset(c3s_cmip5_tas, use_cftime=True, combine="by_coords")
    xr.testing.assert_identical(ds["lat"], ds.cf["lat"])
    xr.testing.assert_identical(ds["lat"], ds.cf["latitude"])
    with pytest.raises(KeyError):
        xr.testing.assert_identical(ds["lat"], ds.cf["lats"])


def test_get_lat_lon_names_from_ds(cmip5_tas):
    ds = xr.open_mfdataset(cmip5_tas, use_cftime=True, combine="by_coords")
    assert ds.cf["latitude"].name == "lat"
    assert ds.cf["longitude"].name == "lon"
    # not sure how it will deal with lats


@pytest.mark.xfail(reason="left has height coord")
def test_get_time(cmip5_tas):
    ds = xr.open_mfdataset(cmip5_tas, use_cftime=True, combine="by_coords")
    xr.testing.assert_identical(ds["time"], ds.cf["time"])
