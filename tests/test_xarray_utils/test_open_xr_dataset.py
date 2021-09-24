import os
import glob
import xarray as xr

from roocs_utils.xarray_utils.xarray_utils import open_xr_dataset
from tests.conftest import C3S_CMIP5_TAS, CMIP5_TAS_EC_EARTH


def test_open_xr_dataset(load_test_data):
    dset = C3S_CMIP5_TAS
    ds = open_xr_dataset(dset)
    assert isinstance(ds, xr.Dataset)


def test_open_xr_dataset_retains_time_encoding(load_test_data):
    dset = CMIP5_TAS_EC_EARTH
    ds = open_xr_dataset(dset)
    assert isinstance(ds, xr.Dataset)
    assert hasattr(ds, "time")
    assert ds.time.encoding.get("units") == "days since 1850-01-01 00:00:00"

    # Now test without our clever opener - to prove time encoding is lost
    kwargs = {"use_cftime": True, "decode_timedelta": False, "combine": "by_coords"}
    ds = xr.open_mfdataset(glob.glob(dset), **kwargs)
    assert ds.time.encoding == {} 

