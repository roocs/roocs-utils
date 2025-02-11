import glob

import pytest
import xarray as xr

from roocs_utils.xarray_utils.xarray_utils import open_xr_dataset


def test_open_xr_dataset(load_test_data, c3s_cmip5_tas):
    ds = open_xr_dataset(c3s_cmip5_tas)
    assert isinstance(ds, xr.Dataset)


@pytest.mark.xfail(reason="cftime check fails on github workflow")
def test_open_xr_dataset_retains_time_encoding(load_test_data, cmip5_tas_ec_earth):
    ds = open_xr_dataset(cmip5_tas_ec_earth)
    assert isinstance(ds, xr.Dataset)
    assert hasattr(ds, "time")
    assert ds.time.encoding.get("units") == "days since 1850-01-01 00:00:00"

    # Now test without our clever opener - to prove time encoding is lost
    kwargs = {"use_cftime": True, "decode_timedelta": False, "combine": "by_coords"}
    ds = xr.open_mfdataset(glob.glob(cmip5_tas_ec_earth), **kwargs)
    assert ds.time.encoding == {}


def _common_test_open_xr_dataset_kerchunk(uri):
    ds = open_xr_dataset(uri)
    assert isinstance(ds, xr.Dataset)
    assert "tasmax" in ds

    # Also test time encoding is retained
    assert hasattr(ds, "time")
    assert ds.time.encoding.get("units") == "days since 1850-01-01"

    return ds


# def test_open_xr_dataset_kerchunk_json(load_test_data, cmip6_kerchunk_https_open_json):
#     _common_test_open_xr_dataset_kerchunk(cmip6_kerchunk_https_open_json)

# def test_open_xr_dataset_kerchunk_zst(load_test_data, cmip6_kerchunk_https_open_zst):
#     _common_test_open_xr_dataset_kerchunk(cmip6_kerchunk_https_open_zst)


# def test_open_xr_dataset_kerchunk_compare_json_vs_zst(
#     load_test_data, cmip6_kerchunk_https_open_json, cmip6_kerchunk_https_open_zst
# ):
#     ds1 = _common_test_open_xr_dataset_kerchunk(cmip6_kerchunk_https_open_json)
#     ds2 = _common_test_open_xr_dataset_kerchunk(cmip6_kerchunk_https_open_zst)
#
#     diff = ds1.isel(time=slice(0, 2)) - ds2.isel(time=slice(0, 2))
#     assert diff.max() == diff.min() == 0.0
