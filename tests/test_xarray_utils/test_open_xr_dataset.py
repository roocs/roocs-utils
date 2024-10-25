import glob

import pytest
import xarray as xr

from roocs_utils.xarray_utils.xarray_utils import open_xr_dataset


def test_open_xr_dataset(mini_esgf_data):
    with open_xr_dataset(mini_esgf_data["C3S_CMIP5_TAS"]) as ds:
        assert isinstance(ds, xr.Dataset)


@pytest.mark.xfail(reason="cftime check fails on github workflow")
def test_open_xr_dataset_retains_time_encoding(mini_esgf_data):
    with open_xr_dataset(mini_esgf_data["CMIP5_TAS_EC_EARTH"]) as ds:
        assert isinstance(ds, xr.Dataset)
        assert hasattr(ds, "time")
        assert ds.time.encoding.get("units") == "days since 1850-01-01 00:00:00"

    # Now test without our clever opener - to prove time encoding is lost
    kwargs = {"use_cftime": True, "decode_timedelta": False, "combine": "by_coords"}
    with xr.open_mfdataset(
        glob.glob(mini_esgf_data["CMIP5_TAS_EC_EARTH"]), **kwargs
    ) as ds:
        assert ds.time.encoding == {}


def _common_test_open_xr_dataset_kerchunk(uri):
    with open_xr_dataset(uri) as ds:
        assert isinstance(ds, xr.Dataset)
        assert "tasmax" in ds

        # Also test time encoding is retained
        assert hasattr(ds, "time")
        assert ds.time.encoding.get("units") == "days since 1850-01-01"

        return ds


def test_open_xr_dataset_kerchunk_json(esgf_kerchunk_urls):
    _common_test_open_xr_dataset_kerchunk(esgf_kerchunk_urls["JSON"])


def test_open_xr_dataset_kerchunk_zst(esgf_kerchunk_urls):
    _common_test_open_xr_dataset_kerchunk(esgf_kerchunk_urls["ZST"])


def test_open_xr_dataset_kerchunk_compare_json_vs_zst(esgf_kerchunk_urls):
    with _common_test_open_xr_dataset_kerchunk(esgf_kerchunk_urls["JSON"]) as ds1:
        with _common_test_open_xr_dataset_kerchunk(esgf_kerchunk_urls["ZST"]) as ds2:
            diff = ds1.isel(time=slice(0, 2)) - ds2.isel(time=slice(0, 2))
            assert diff.max() == diff.min() == 0.0
